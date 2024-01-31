import pytest
from src.IntroWindow import IntroWindow


@pytest.fixture
def my_intro_window():
    print('!')
    intro_window = IntroWindow()
    intro_window.gogo()
    return intro_window