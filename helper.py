import requests
from datetime import datetime
from typing import Tuple


def get_games_info() -> dict:

    api_url = (
        'https://store-site-backend-static.ak.epicgames.com/'
        'freeGamesPromotions?locale=ru_RU&country=RU&allowCountries=RU'
    )
    response = requests.get(api_url).json()
    games_dict = response['data']['Catalog']['searchStore']['elements']

    return games_dict


def get_link(game: dict) -> str:

    raw_link = game.get('catalogNs').get('mappings')
    raw_link_slug = game.get('productSlug')

    final_link = raw_link[0].get('pageSlug') if raw_link != [] else raw_link_slug
    link = f'https://store.epicgames.com/ru/p/{final_link}'

    return link


def get_promotional(promotion_data: dict) -> Tuple[datetime, datetime]:

    start_date_iso, end_date_iso = (
        promotion_data['startDate'][:-1],
        promotion_data['endDate'][:-1]
    )

    start_date = datetime.fromisoformat(start_date_iso)
    end_date = datetime.fromisoformat(end_date_iso)

    return start_date, end_date
