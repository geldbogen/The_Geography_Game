import pytest

from player import Player

from country import Niger, Chad
from intro_window import IntroWindow

@pytest.fixture
def my_intro_window():
    print('!')
    intro_window = IntroWindow()
    intro_window.gogo()
    return intro_window



def test_countries_are_neighbors():
    intro_window = IntroWindow()
    intro_window.gogo()
    print(Niger.neighboring_countries)
    assert (Chad in Niger.neighboring_countries) == True