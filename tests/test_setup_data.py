import sys
import os
import pytest
import pandas as pd

# Add src to the path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from setup_data import extract_data_from_record, setup_data
from local_attribute import LocalAttribute
from country import Country
import global_definitions

@pytest.fixture
def isolated_global_state():
    """Fixture to provide a clean global state and restore it after the test."""
    # 1. Backup original state
    original_countries = global_definitions.all_countries_available.copy()
    original_categories = global_definitions.all_categories.copy()
    
    # 2. Setup clean state for testing
    country1 = Country("Country1")
    country2 = Country("Country2")
    country1.dict_of_attributes = {}
    country2.dict_of_attributes = {}
    
    global_definitions.all_countries_available = [country1, country2]
    global_definitions.all_categories = []
    
    # Yield the controlled objects to the test
    yield {"Country1": country1, "Country2": country2}
    
    # 3. Teardown / Restore original state
    global_definitions.all_countries_available = original_countries
    global_definitions.all_categories = original_categories

def test_extract_data_from_record_basic(isolated_global_state):
    # Setup
    countries = isolated_global_state
    test_country = countries["Country1"]
    
    record = {
        'name': 'Country1',
        'value': 10.5,
        'ranking': 1
    }
    
    # Execute
    extract_data_from_record(record, 'TestAttr', 100, False)
    
    # Assert
    assert 'TestAttr' in test_country.dict_of_attributes
    attr = test_country.dict_of_attributes['TestAttr']
    assert isinstance(attr, LocalAttribute)
    assert attr.value == 10.5
    assert attr.rank == 1
    assert attr.number_of_countries_ranked == 100

def test_extract_data_from_record_not_in_game(isolated_global_state):
    # Setup
    record = {'name': 'ExternalCountry'}
    
    # Execute
    result = extract_data_from_record(record, 'TestAttr', 100, False)
    
    # Assert
    assert result is None
    # Ensure no existing countries were modified
    for country in isolated_global_state.values():
        assert 'TestAttr' not in country.dict_of_attributes

def test_setup_data_basic(isolated_global_state):
    countries = isolated_global_state
    
    # Execute the real function against the real CSV
    setup_data('for_testing_only/test.csv', column_index=1, namecolumn_index=0, ascending=True)
    
    # Assert the global state was altered correctly
    attr_name = 'test' 
    
    # Check Country 2
    assert attr_name in countries['Country2'].dict_of_attributes
    assert countries['Country2'].dict_of_attributes[attr_name].value == 10.0
    assert countries['Country2'].dict_of_attributes[attr_name].rank == 1
    
    # Check Country 1
    assert attr_name in countries['Country1'].dict_of_attributes
    assert countries['Country1'].dict_of_attributes[attr_name].value == 20.0
    assert countries['Country1'].dict_of_attributes[attr_name].rank == 2
    
    # Check Category creation
    assert len(global_definitions.all_categories) == 1
    assert global_definitions.all_categories[0].name == 'test'
