from global_definitions import (all_countries_available, all_countries_in_game,
                                country_name_list, neighboring_countries,
                                my_property_dict, all_players)
from country import Unknown_country
from main_window import MainWindow
from player import Player

from image import im


def setup_the_game(continent_list: list[str] = [],
         list_of_players: list[Player] = [],
         number_of_rounds: int = -1,
         number_of_rerolls: int = 0,
         starting_countries_preferences : str = '',
         winning_condition : str = '',
         end_attribute_path : str = '',
         peacemode : bool = False,
         wormhole_mode : str = '',
         reversed_end_attribute : int = 0,
         start_the_game : bool = False
         ):

    for country in all_countries_available:
        if country.continent in continent_list:
            all_countries_in_game.append(country)
    
    all_countries_in_game.append(Unknown_country)

    for country in all_countries_in_game:
        country_name_list.append(country.name)

    # TODO: this is quite ugly
    for country_1 in all_countries_in_game:
        if country_1 == Unknown_country:
            continue
        data = neighboring_countries[neighboring_countries[0] ==
                                        country_1.name]
        for country_2 in all_countries_in_game:
            if country_2 == Unknown_country:
                continue
            if not data.empty:
                if country_2.name in str(data.iat[0, 5]):
                    country_2.neighboring_countries.append(country_1.name)

    # assigns the countries all the local attributes
    for country in all_countries_in_game:
        country.dict_of_attributes = my_property_dict[country.name]

    if list_of_players == []:
        return None

    for player in all_players.values():
        player.rerolls_left = number_of_rerolls

    if start_the_game:
        my_main_window = MainWindow(bild=im,
                    list_of_players=list_of_players,
                    starting_countries_preferences=starting_countries_preferences,
                    number_of_rounds=number_of_rounds,
                    winning_condition=winning_condition,
                    pred_attribute=end_attribute_path,
                    wormhole_mode=wormhole_mode,
                    peacemode=peacemode,
                    reversed_end_attribute=reversed_end_attribute)
        my_main_window.start()