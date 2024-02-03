import pytest

from player import Player

from country import Niger, Chad
from setup_game import setup_the_game
from global_definitions import red, yellow

# @pytest.fixture
# def my_intro_window():
#     print('!')
#     intro_window = IntroWindow()
#     intro_window.go()
#     return intro_window

@pytest.fixture
def player1():
    my_player = Player(color=red,name='Player1')
    return my_player
@pytest.fixture
def player2():
    my_player = Player(color=yellow,name='Player2')
    return my_player

def test_countries_are_neighbors():
    # assert 0
    setup_the_game(continent_list=['Africa'], list_of_players= [player1, player2])
    print(Niger.neighboring_countries)
    assert ('Chad' in Niger.neighboring_countries) == True