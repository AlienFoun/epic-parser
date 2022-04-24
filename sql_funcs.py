import psycopg2
from config import host, user, password, db_name
from loguru import logger
from typing import List


def sql_check_user(user_id: int) -> bool:
    cursor.execute(f"SELECT user_id FROM user_base WHERE user_id = '{user_id}'")
    rows = cursor.fetchall()
    for row in rows:
        if user_id in row:
            return True
    return False


def sql_add_user(user_id: int):
    cursor.execute(f"INSERT INTO user_base (user_id) VALUES ('{user_id}')")
    logger.info(f"Новый пользователь {user_id} добавлен в базу данных")


def sql_remove_user(user_id: int):
    cursor.execute(f"DELETE FROM user_base WHERE user_id = '{user_id}'")
    logger.info(f"Пользователь {user_id} удален из базы данных")


def sql_get_users() -> List[int]:
    user_data = []
    cursor.execute(f"SELECT user_id FROM user_base")
    rows = cursor.fetchall()
    for row in rows:
        user_data.append(row[0])
    return user_data


def sql_close():
    connection.close()


connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)

connection.autocommit = True

cursor = connection.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS user_base "
    "(id SERIAL NOT NULL PRIMARY KEY,"
    "user_id BIGINT NOT NULL)"
)
