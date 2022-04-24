from helper import get_link, get_games_info, get_promotional


def get_free_games() -> dict:
    games_dict = get_games_info()

    output = []

    for game in games_dict:
        game_name = game.get('title')
        game_description = game.get('description')
        game_price = game.get('price').get('totalPrice').get('originalPrice')
        game_current_price = f'{str(game_price)[:-2]} руб.'

        link = get_link(game)

        try:
            game_promotions = game.get('promotions').get('promotionalOffers')
            upcoming_promotions = game.get('promotions').get('upcomingPromotionalOffers')

            if not game_promotions and upcoming_promotions:
                promotion_data = upcoming_promotions[0]['promotionalOffers'][0]
                start_date, end_date = get_promotional(promotion_data)

                output.append(
                    {
                        'name': game_name,
                        'price': game_current_price,
                        'description': game_description,
                        'link': link,
                        'start_date': start_date,
                        'end_date': end_date
                    }
                )
            else:
                promotion_data = game_promotions[0].get('promotionalOffers')[0]
                end_date = get_promotional(promotion_data)[1]

                output.append(
                    {
                        'name': game_name,
                        'price': game_current_price,
                        'description': game_description,
                        'link': link,
                        'end_date': end_date
                    }
                )

            output_dict = {'items': output}

        except Exception:
            pass

    return output_dict
