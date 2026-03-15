import os
import sys
from types import SimpleNamespace

import dash_mantine_components as dmc


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import dash_popup_window


class DummyAttributeValue:
    def __init__(
        self,
        value=10.0,
        rank=1,
        number_of_countries_ranked=10,
        additional_information_name="",
        additional_information="",
        additional_information_link="",
    ):
        self.value = value
        self.rank = rank
        self.number_of_countries_ranked = number_of_countries_ranked
        self.additional_information_name = additional_information_name
        self.additional_information = additional_information
        self.additional_information_link = additional_information_link


class DummyCountry:
    def __init__(self, name, country_code, attribute_name, attribute_value):
        self.name = name
        self._country_code = country_code
        self.dict_of_attributes = {attribute_name: attribute_value}

    def get_two_country_code(self):
        return self._country_code


class DummyAttribute:
    def __init__(self, name="test_attribute.csv", is_active=False):
        self.name = name
        self.is_active = is_active


class DummyBackendGame:
    def __init__(self, current_attribute, country_a, country_b):
        self.current_attribute = current_attribute
        self.chosen_country_1 = country_a
        self.chosen_country_2 = country_b
        self.ignore_next_map_click = False
        self.active_player = SimpleNamespace(name="Player 2")
        self.which_round_counter = 1
        self.number_of_rounds = 10
        self.next_turn_calls = []

    def go_to_next_turn_and_check_if_game_should_end(self, same_player_again=False):
        self.next_turn_calls.append(same_player_again)
        return False

    def get_replaced_A_and_B_category_string_for_current_attribute(self):
        return "Population of CountryA vs CountryB"


def _build_backend(is_active=False, include_extra_info=True):
    attribute = DummyAttribute(is_active=is_active)

    first_info = DummyAttributeValue(
        value=123.0,
        rank=2,
        number_of_countries_ranked=20,
        additional_information_name="Alpha City" if include_extra_info else "",
        additional_information="Alpha summary" if include_extra_info else "",
        additional_information_link="https://example.com/alpha" if include_extra_info else "",
    )
    second_info = DummyAttributeValue(
        value=456.0,
        rank=3,
        number_of_countries_ranked=20,
        additional_information_name="Beta City" if include_extra_info else "",
        additional_information="Beta summary" if include_extra_info else "",
        additional_information_link="https://example.com/beta" if include_extra_info else "",
    )

    country_a = DummyCountry("Germany", "de", attribute.name, first_info)
    country_b = DummyCountry("France", "fr", attribute.name, second_info)
    return DummyBackendGame(attribute, country_a, country_b)


def test_get_flag_asset_path_uses_expected_dash_asset_url():
    country = DummyCountry("Germany", "de", "attr.csv", DummyAttributeValue())

    assert dash_popup_window._get_flag_asset_path(country) == "/assets/pictures/flag_pictures/w320/de.png"


def test_build_country_info_contains_resized_flag_and_country_name():
    attribute = DummyAttribute()
    country = DummyCountry("Germany", "de", attribute.name, DummyAttributeValue(value=1234.0, rank=5, number_of_countries_ranked=50))

    info = dash_popup_window._build_country_info(country, attribute, "#e74c3c")

    assert info.children[0].children == "Germany"
    image = info.children[1].children
    assert isinstance(image, dmc.Image)
    assert image.src == "/assets/pictures/flag_pictures/w320/de.png"
    assert image.h == 72
    assert image.w == 116


def test_populate_popup_content_returns_blank_content_when_closed():
    footer_buttons = ["existing-button"]

    content = dash_popup_window.populate_popup_content(False, footer_buttons)

    assert content == ("", "", "", "", "", footer_buttons)


def test_populate_popup_content_builds_country_panels_and_extra_info(monkeypatch):
    backend_game = _build_backend(is_active=False, include_extra_info=True)
    monkeypatch.setattr(dash_popup_window, "get_backend_game", lambda: backend_game)

    fake_cards = ["left-card", "right-card"]
    monkeypatch.setattr(
        dash_popup_window,
        "get_two_popup_extra_information_window_cards",
        lambda *args: fake_cards,
    )

    footer_buttons = ["continue-button"]
    country_a_info, country_b_info, attribute_info, card_a, card_b, returned_footer = dash_popup_window.populate_popup_content(
        True,
        footer_buttons,
    )

    assert country_a_info.children[0].children == "Germany"
    assert country_b_info.children[0].children == "France"
    assert attribute_info == "test_attribute"
    assert card_a == "left-card"
    assert card_b == "right-card"
    assert returned_footer == footer_buttons


def test_populate_popup_content_centers_guessed_correct_button_for_active_attribute(monkeypatch):
    backend_game = _build_backend(is_active=True, include_extra_info=False)
    monkeypatch.setattr(dash_popup_window, "get_backend_game", lambda: backend_game)
    monkeypatch.setattr(
        dash_popup_window,
        "get_two_popup_extra_information_window_cards",
        lambda *args: ["ignored-left", "ignored-right"],
    )

    _, _, _, card_a, card_b, footer_buttons = dash_popup_window.populate_popup_content(True, ["continue-button"])

    assert card_a == ""
    assert card_b == ""
    assert len(footer_buttons) == 1
    button = footer_buttons[0]
    assert isinstance(button, dmc.Button)
    assert button.children == "Guessed Correct"
    assert button.justify == "center"


def test_close_popup_advances_turn_and_suppresses_next_map_click(monkeypatch):
    backend_game = _build_backend(is_active=True, include_extra_info=True)
    monkeypatch.setattr(dash_popup_window, "get_backend_game", lambda: backend_game)
    monkeypatch.setattr(
        dash_popup_window,
        "callback_context",
        SimpleNamespace(
            triggered=[
                {
                    "value": 1,
                    "prop_id": '{"type":"close-button","is_guessed_correct_or_not":"guessed_correct"}.n_clicks',
                }
            ]
        ),
    )

    segmented_control_data = ["Round: 1 / 10", "Player 1", "Player 2"]
    hideout = {"selected": ["Germany", "France"]}

    is_open, returned_hideout, active_player_name, updated_segmented_control_data, header_text = dash_popup_window.close_popup(
        [1],
        segmented_control_data,
        True,
        hideout,
    )

    assert is_open is False
    assert returned_hideout["selected"] == []
    assert active_player_name == "Player 2"
    assert updated_segmented_control_data[0] == "Round: 2 / 10"
    assert header_text == "Population of CountryA vs CountryB"
    assert backend_game.ignore_next_map_click is True
    assert backend_game.next_turn_calls == [True]
