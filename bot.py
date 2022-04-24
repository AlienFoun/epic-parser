from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from config import BOT_TOKEN
from sql_funcs import sql_check_user, sql_add_user, sql_remove_user, sql_get_users
from keyboards import startMenu
from get_free_games import get_free_games

import asyncio

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)
logger.add("epicgames.log", format="{time} {level} {message}", level="DEBUG",
           rotation='100 KB', compression='zip')


@dp.message_handler(commands='start')
async def say_hello(event: types.Message):
    user_id = event['from']['id']
    if not sql_check_user(user_id):
        await event.answer(
            f"Добрый день, {event.from_user.get_mention(as_html=True)}, Вы обратились к боту для уведомления о "
            f"наличии бесплатных игры в Epic Games Store. Хотите подписаться на рассылку?",
            parse_mode=types.ParseMode.HTML, reply_markup=startMenu
        )
    else:
        await event.answer(
            f"Хэй, {event.from_user.get_mention(as_html=True)}! Вы уже подписаны на рассылку! "
            f"Чтобы отписаться, введите /stop!",
            parse_mode=types.ParseMode.HTML
        )


@dp.callback_query_handler(Text(startswith="data_"))
async def callbacks_num(call: types.CallbackQuery):
    action = call.data.split('_')[1]
    user_id = call['from']['id']
    if action == 'yes':
        sql_add_user(user_id)

        await call.message.edit_text(
            f"Прекрасно, {call.from_user.get_mention(as_html=True)}, я буду уведомлять вас каждый день в 20:00! "
            f"Чтобы отписаться от рассылки, введи команду /stop!",
            parse_mode=types.ParseMode.HTML
        )

    else:
        await call.message.edit_text(
            f"Очень жаль, {call.from_user.get_mention(as_html=True)}, буду ждать вас снова! "
            f"Я всегда доступен по команде /start!",
            parse_mode=types.ParseMode.HTML
        )
    await call.answer()


@dp.message_handler(commands='stop')
async def say_hello(event: types.Message):
    user_id = event['from']['id']
    if sql_check_user(user_id):
        sql_remove_user(user_id)
        await event.answer(
            f"Очень жаль, {event.from_user.get_mention(as_html=True)}, буду ждать вас снова! "
            f"Я всегда доступен по команде /start!",
            parse_mode=types.ParseMode.HTML
        )
    else:
        await event.answer(
            f"К сожалению, {event.from_user.get_mention(as_html=True)}, вы и так не подписаны на рассылку:с "
            f"подписаться на нее вы можете при помощи команды /start!",
            parse_mode=types.ParseMode.HTML
        )


async def collect_data():
    data = get_free_games().get('items')
    message_list = []
    for game in data:
        game_name = game.get('name')
        game_price = game.get('price')
        game_description = game.get('description')
        link = game.get('link')
        start_date = game.get('start_date')
        end_date = game.get('end_date').strftime(f"%d.%m.%Y %H:%M")

        availability = 'Игра раздается бесплатно ПРЯМО СЕЙЧАС' if start_date is None \
            else f'Игра будет бесплатной с {start_date.strftime("%d.%m.%Y %H:%M")} по {end_date}'

        message_list.append(f'Название: {game_name}\nОбычная цена: {game_price}\nСюжет: {game_description}\n'
                            f'Ссылка: {link}\n{availability}')

    user_data = sql_get_users()
    message = '\n\n'.join(message_list)
    for user in user_data:
        await bot.send_message(chat_id=user, text=f'На данный момент доступны игры:\n\n{message}',
                               disable_web_page_preview=True)
        logger.info(f'Сообщение успешно отправлено пользователю {user}')


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(collect_data, 'cron', hour=20, minute=0, timezone='Europe/Moscow')
    try:
        scheduler.start()
        logger.info('Бот был успешно запущен')
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit) as err:
        logger.exception(f"Бот был отключен {err}!")
