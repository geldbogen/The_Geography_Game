import pytest

from player import Player, mr_nobody

import start

from country import *
from setup_game import setup_the_game
from global_definitions import red, yellow, reverse_countries_alternative_names
from category import dictionary_attribute_name_to_attribute
from backend_game import BackendGame

player_a = Player(color=yellow, name='PlayerA')
player_b = Player(color=red, name='PlayerB')

setup_the_game(continent_list=['Africa'], list_of_players=[player_a, player_b])
my_backend_game = BackendGame(list_of_players=[player_a, player_b], wormhole_mode='', starting_countries_preferences='random', number_of_rounds=3,
                              winning_condition='number of countries',
                              number_of_wormholes=3,
                              pred_attribute='Price of 1kg of rice in US$ (lower is better).csv',
                              peacemode=True,
                              reversed_end_attribute=1)


def test_countries_are_neighbors():
    # assert 0
    for country1 in all_countries_available:
        for country2 in all_countries_available:
            assert (country1.name in country2.neighboring_countries) == (
                country2.name in country1.neighboring_countries)

    for country in all_countries_available:
        assert country.is_connected_with(country) == False

def test_categories():

    price_rice_category: category.Category = dictionary_attribute_name_to_attribute[
        'Price of 1kg of rice in US$ (lower is better).csv'][0]

    assert player_a.check_if_attack_is_succesful(
        price_rice_category, Mauritania, Libya) == 'no data'
    assert price_rice_category.is_end_only == False
    assert price_rice_category.is_active == False
    assert price_rice_category.treat_missing_data_as_bad == False
    assert price_rice_category.number_of_chosen_already == 0

    # export_import_category : category.Category = dictionary_attribute_name_to_attribute['Export to import ratio (higher is better).csv']
    assert United_States.dict_of_attributes['Export to import ratio (higher is better).csv'].value == 0.77

    # assert reverse_countries_alternative_names == 0
    # assert dictionary_attribute_name_to_attribute == 0


def test_setup_category():
    top_2_happiness = my_backend_game.find_top_n_countries(2,'World Happiness Index (higher is better).csv')
    assert top_2_happiness == [call_country_by_name('Mauritius'),call_country_by_name('Libya')]
    # all_countries_in_game = all_countries_available
    # top_2_happiness = my_backend_game.find_top_n_countries(3,'World Happiness Index (higher is better).csv')
    # assert top_2_happiness == [call_country_by_name('Finland'),call_country_by_name('Denmark'),call_country_by_name('Iceland')]
    
def test_get_good_category():
    my_backend_game.claim_country_backend(loose_player=mr_nobody,win_player=player_a,country= call_country_by_name('Chad'))
    assert player_a.list_of_possessed_countries == [call_country_by_name('Chad')]
    my_dict = Chad.win_analysis(dictionary_attribute_name_to_attribute['Number of physicians by 10,000 population (higher is better).csv'][0])
    assert my_dict == {'win': 1, 'no data': 0, 'draw': 1, 'loose': 4}
    my_dict2 = United_States.win_analysis(dictionary_attribute_name_to_attribute['Export to import ratio (higher is better).csv'][0])
    assert my_dict2['no data'] == 0
    assert player_a.check_if_attack_is_succesful(dictionary_attribute_name_to_attribute['Number of wiki-languages of most famous desert of that country (higher is better).csv'][0], Switzerland, Germany) == 'loose'
    
    category_name_list = [player_a.get_good_attribute().name for _ in range(100)]
    assert len(category_name_list) == 100
    # assert 0

def test_that_all_countries_have_good_attributes():
    country_dict = {}
    for country in all_countries_available:
        new_owner = Player(yellow,country.name)
        assert len(new_owner.list_of_possessed_countries) == 0
        my_backend_game.claim_country_backend(mr_nobody,new_owner,country)
        category_name_list = [player_a.get_good_attribute().name for _ in range(200)]
        assert len(set(category_name_list)) > 100
        country_dict[country.name] = len(set(category_name_list))
    # assert 0