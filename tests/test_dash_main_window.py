import os
import sys
from types import SimpleNamespace

import dash


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import dash_main_window


class DummyAttributeValue:
    def __init__(self, rank=1):
        self.rank = rank


class DummyAttribute:
    def __init__(self, name="test_attribute.csv"):
        self.name = name

    def replace_A_and_B_in_category_name(self, first_country, second_country):
        first_name = first_country.name if first_country else "CountryA"
        second_name = second_country.name if second_country else "CountryB"
        return f"Compare {first_name} vs {second_name}"


class DummyCountry:
    def __init__(self, name, owner, attribute_name, rank=1):
        self.name = name
        self.owner = owner
        self.dict_of_attributes = {attribute_name: DummyAttributeValue(rank=rank)}
        self.connected_names = set()

    def is_connected_with(self, other_country):
        return other_country is not None and other_country.name in self.connected_names


class DummyBackendGame:
    def __init__(self, active_player, current_attribute, peacemode=False):
        self.active_player = active_player
        self.current_attribute = current_attribute
        self.peacemode = peacemode
        self.chosen_country_1 = None
        self.chosen_country_2 = None
        self.hideout_dict_for_dash = {"selected": [], "country_owner_dict": {}, "player_color_dict": {}}
        self.ignore_next_map_click = False

    def get_replaced_A_and_B_category_string_for_current_attribute(self):
        return self.current_attribute.replace_A_and_B_in_category_name(
            self.chosen_country_1,
            self.chosen_country_2,
        )


def _make_feature(country_name):
    return {"properties": {"sovereignt": country_name}}


def _notification_message(notifications):
    return notifications[0]["message"]


def test_click_on_map_selects_owned_country_as_attacker(monkeypatch):
    player = SimpleNamespace(name="Player 1")
    attribute = DummyAttribute()
    attacker = DummyCountry("Attackerland", player, attribute.name, rank=5)
    backend_game = DummyBackendGame(player, attribute)

    monkeypatch.setattr(dash_main_window, "get_backend_game", lambda: backend_game)
    monkeypatch.setattr(dash_main_window, "call_country_by_name", lambda _: attacker)

    header, hideout, popup_open, _, notifications = dash_main_window.click_on_map(
        1,
        _make_feature(attacker.name),
        backend_game.hideout_dict_for_dash.copy(),
        False,
    )

    assert header == "Compare Attackerland vs CountryB"
    assert backend_game.chosen_country_1 == attacker
    assert backend_game.chosen_country_2 is None
    assert hideout["selected"] == ["Attackerland"]
    assert popup_open is False
    assert notifications == []


def test_click_on_map_rejects_enemy_country_in_peace_mode(monkeypatch):
    player = SimpleNamespace(name="Player 1")
    opponent = SimpleNamespace(name="Player 2")
    attribute = DummyAttribute()
    attacker = DummyCountry("Attackerland", player, attribute.name, rank=5)
    defender = DummyCountry("Defenderland", opponent, attribute.name, rank=4)
    defender.connected_names.add(attacker.name)

    backend_game = DummyBackendGame(player, attribute, peacemode=True)
    backend_game.chosen_country_1 = attacker

    monkeypatch.setattr(dash_main_window, "get_backend_game", lambda: backend_game)
    monkeypatch.setattr(dash_main_window, "call_country_by_name", lambda _: defender)

    header, hideout, popup_open, title, notifications = dash_main_window.click_on_map(
        1,
        _make_feature(defender.name),
        backend_game.hideout_dict_for_dash.copy(),
        False,
    )

    assert header == "Compare CountryA vs CountryB"
    assert backend_game.chosen_country_1 is None
    assert backend_game.chosen_country_2 is None
    assert hideout["selected"] == []
    assert popup_open is dash.no_update
    assert title is dash.no_update
    assert "peace mode" in _notification_message(notifications)


def test_click_on_map_rejects_non_neighbor_and_clears_attacker(monkeypatch):
    player = SimpleNamespace(name="Player 1")
    neutral_owner = SimpleNamespace(name="Nobody")
    attribute = DummyAttribute()
    attacker = DummyCountry("Attackerland", player, attribute.name, rank=5)
    defender = DummyCountry("Far Away", neutral_owner, attribute.name, rank=4)

    backend_game = DummyBackendGame(player, attribute)
    backend_game.chosen_country_1 = attacker

    monkeypatch.setattr(dash_main_window, "get_backend_game", lambda: backend_game)
    monkeypatch.setattr(dash_main_window, "call_country_by_name", lambda _: defender)

    header, hideout, popup_open, title, notifications = dash_main_window.click_on_map(
        1,
        _make_feature(defender.name),
        backend_game.hideout_dict_for_dash.copy(),
        False,
    )

    assert header == "Compare CountryA vs CountryB"
    assert backend_game.chosen_country_1 is None
    assert hideout["selected"] == []
    assert popup_open is dash.no_update
    assert title is dash.no_update
    assert "don't share a border" in _notification_message(notifications)


def test_click_on_map_rejects_owned_defender_but_keeps_attacker(monkeypatch):
    player = SimpleNamespace(name="Player 1")
    attribute = DummyAttribute()
    attacker = DummyCountry("Attackerland", player, attribute.name, rank=5)
    friendly_target = DummyCountry("Friendlyland", player, attribute.name, rank=4)
    friendly_target.connected_names.add(attacker.name)

    backend_game = DummyBackendGame(player, attribute)
    backend_game.chosen_country_1 = attacker

    monkeypatch.setattr(dash_main_window, "get_backend_game", lambda: backend_game)
    monkeypatch.setattr(dash_main_window, "call_country_by_name", lambda _: friendly_target)

    header, hideout, popup_open, title, notifications = dash_main_window.click_on_map(
        1,
        _make_feature(friendly_target.name),
        backend_game.hideout_dict_for_dash.copy(),
        False,
    )

    assert header == "Compare Attackerland vs CountryB"
    assert backend_game.chosen_country_1 == attacker
    assert backend_game.chosen_country_2 is None
    assert hideout["selected"] == ["Attackerland"]
    assert popup_open is dash.no_update
    assert title is dash.no_update
    assert "already own this country" in _notification_message(notifications).lower()


def test_click_on_map_rejects_missing_data_but_keeps_attacker(monkeypatch):
    player = SimpleNamespace(name="Player 1")
    neutral_owner = SimpleNamespace(name="Nobody")
    attribute = DummyAttribute()
    attacker = DummyCountry("Attackerland", player, attribute.name, rank=5)
    no_data_target = DummyCountry("Mysteryland", neutral_owner, attribute.name, rank=0)
    no_data_target.connected_names.add(attacker.name)

    backend_game = DummyBackendGame(player, attribute)
    backend_game.chosen_country_1 = attacker

    monkeypatch.setattr(dash_main_window, "get_backend_game", lambda: backend_game)
    monkeypatch.setattr(dash_main_window, "call_country_by_name", lambda _: no_data_target)

    header, hideout, popup_open, title, notifications = dash_main_window.click_on_map(
        1,
        _make_feature(no_data_target.name),
        backend_game.hideout_dict_for_dash.copy(),
        False,
    )

    assert header == "Compare Attackerland vs CountryB"
    assert backend_game.chosen_country_1 == attacker
    assert backend_game.chosen_country_2 is None
    assert hideout["selected"] == ["Attackerland"]
    assert popup_open is dash.no_update
    assert title is dash.no_update
    assert "no data" in _notification_message(notifications).lower()


def test_click_on_map_accepts_valid_defender_selection(monkeypatch):
    player = SimpleNamespace(name="Player 1")
    neutral_owner = SimpleNamespace(name="Nobody")
    attribute = DummyAttribute()
    attacker = DummyCountry("Attackerland", player, attribute.name, rank=5)
    defender = DummyCountry("Defenderland", neutral_owner, attribute.name, rank=4)
    defender.connected_names.add(attacker.name)

    backend_game = DummyBackendGame(player, attribute)
    backend_game.chosen_country_1 = attacker

    monkeypatch.setattr(dash_main_window, "get_backend_game", lambda: backend_game)
    monkeypatch.setattr(dash_main_window, "call_country_by_name", lambda _: defender)

    header, hideout, popup_open, _, notifications = dash_main_window.click_on_map(
        1,
        _make_feature(defender.name),
        backend_game.hideout_dict_for_dash.copy(),
        False,
    )

    assert header == "Compare Attackerland vs Defenderland"
    assert backend_game.chosen_country_1 == attacker
    assert backend_game.chosen_country_2 == defender
    assert hideout["selected"] == ["Attackerland", "Defenderland"]
    assert popup_open is False
    assert notifications == []
