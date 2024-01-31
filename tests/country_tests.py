import pytest

from Player import Player
import Country
from Country import Country, Nigeria, Niger, Chad

class TestPlayer():

    def setup_method(self, method):
        self.player1 = Player()


    def teardown_method(self, method):
        pass


class TestCountry():

    def setup_method(self, method):
        self.country1 = Chad
        self.country2 = Niger

    def test_connected(self):
        assert Niger.continent == 'Africa'