import pytest

import start

from player import Player

from country import *
from setup_game import setup_the_game
from global_definitions import red, yellow
from category import dictionary_attribute_name_to_attribute

# @pytest.fixture
# def my_intro_window():
#     print('!')
#     intro_window = IntroWindow()
#     intro_window.go()
#     return intro_window


@pytest.fixture
def player1():
    my_player = Player(color=red, name='Player1')
    return my_player


@pytest.fixture
def player2():
    my_player = Player(color=yellow, name='Player2')
    return my_player


def test_countries_are_neighbors():
    # assert 0
    setup_the_game(continent_list=['Africa'],
                   list_of_players=[player1, player2])
    print(Niger.neighboring_countries)
    assert Chad.is_connected_with(Niger) == True
    assert Chad.is_connected_with(Germany) == False

def test_categories():

    player_a = Player(color=yellow, name='PlayerA')
    player_b = Player(color=yellow, name='PlayerB')
    setup_the_game(continent_list=['Africa'],
                   list_of_players=[player_a,player_b])
    price_rice_category : category.Category = dictionary_attribute_name_to_attribute['Price of 1kg of rice in US$ (lower is better).csv'][0]

    assert player_a.check_if_attack_is_succesful(price_rice_category,Mauritania,Libya) == 'no data'
    assert price_rice_category.is_end_only == False
    assert price_rice_category.is_active == False
    assert price_rice_category.treat_missing_data_as_bad == False
    assert price_rice_category.number_of_chosen_already == 0
    