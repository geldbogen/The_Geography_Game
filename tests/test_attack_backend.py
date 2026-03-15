import os
import sys

import pytest


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import global_definitions
from backend_game import BackendGame
from country import Country
from player import Player


@pytest.fixture
def restore_player_registry():
    original_players = global_definitions.all_players.copy()
    yield
    global_definitions.all_players.clear()
    global_definitions.all_players.update(original_players)


def test_attack_backend_claims_country_on_hard_defeat(restore_player_registry):
    attacker = Player(color=(1, 2, 3), name="Attacker")
    defender = Player(color=(4, 5, 6), name="Defender")

    attacking_country = Country([], [], "Attacking Country", is_in_game=False)
    defending_country = Country([], [], "Defending Country", is_in_game=False)

    attacking_country.owner = attacker
    defending_country.owner = defender
    attacker.list_of_possessed_countries = [attacking_country]
    defender.list_of_possessed_countries = [defending_country]

    backend = BackendGame.__new__(BackendGame)
    backend.active_player = attacker
    backend.chosen_country_1 = attacking_country
    backend.chosen_country_2 = defending_country
    backend.current_attribute = object()
    backend.hideout_dict_for_dash = {"country_owner_dict": {}}
    backend.winning_condition = "number of countries"

    attacker.check_if_attack_is_succesful = lambda category, country_a, country_b: "hard defeat"

    result = backend.attack_backend()

    assert result == "hard defeat"
    assert defending_country.owner == attacker
    assert defending_country in attacker.list_of_possessed_countries
    assert defending_country not in defender.list_of_possessed_countries
