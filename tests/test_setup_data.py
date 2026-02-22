import sys
import os
import pytest
from unittest.mock import MagicMock, patch
import pandas as pd

# Add src to the path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from setup_data import extract_data_from_record, setup_data
from local_attribute import LocalAttribute

@patch('setup_data.call_country_by_name')
@patch('setup_data.all_countries_available')
def test_extract_data_from_record_basic(mock_all_countries, mock_call_country):
    # Setup
    mock_country = MagicMock()
    mock_country.dict_of_attributes = {}
    mock_call_country.return_value = mock_country
    mock_all_countries.__contains__.return_value = True
    
    record = {
        'name': 'TestCountry',
        'value': 10.5,
        'ranking': 1
    }
    
    # Execute
    extract_data_from_record(record, 'TestAttr', 100, False)
    
    # Assert
    assert 'TestAttr' in mock_country.dict_of_attributes
    attr = mock_country.dict_of_attributes['TestAttr']
    assert isinstance(attr, LocalAttribute)
    assert attr.value == 10.5
    assert attr.rank == 1
    assert attr.number_of_countries_ranked == 100

@patch('setup_data.call_country_by_name')
@patch('setup_data.all_countries_available')
def test_extract_data_from_record_not_in_game(mock_all_countries, mock_call_country):
    # Setup
    mock_country = MagicMock()
    mock_call_country.return_value = mock_country
    mock_all_countries.__contains__.return_value = False
    
    record = {'name': 'ExternalCountry'}
    
    # Execute
    result = extract_data_from_record(record, 'TestAttr', 100, False)
    
    # Assert
    assert result is None
    assert not hasattr(mock_country, 'dict_of_attributes') or 'TestAttr' not in mock_country.dict_of_attributes

@patch('setup_data.pd.read_csv')
@patch('setup_data.normalize_country_name')
@patch('setup_data.extract_data_from_record')
@patch('category.Category')
@patch('setup_data.all_countries_available')
def test_setup_data_basic(mock_all_countries, mock_category, mock_extract, mock_normalize, mock_read_csv):
    # Setup
    df = pd.DataFrame({
        'Country': ['Country1', 'Country2'],
        'Value': [20, 10]
    })
    mock_read_csv.return_value = df
    mock_normalize.side_effect = lambda x: x
    mock_all_countries = [] # Empty list for the cleanup loop at the end of setup_data
    
    # Execute
    setup_data('test.csv', column_index=1, namecolumn_index=0, ascending=True)
    
    # Assert
    # Check if sorting worked (ascending=True means 10 then 20)
    # The record passed to extract_data_from_record should have ranking 1 for Country2 and 2 for Country1
    
    # Sorting (ascending=True) -> [10, 20] -> [Country2, Country1]
    # rankings -> [1, 2]
    
    assert mock_extract.call_count == 2
    
    # Check one of the calls
    first_call_record = mock_extract.call_args_list[0][0][0]
    assert first_call_record['name'] == 'Country2'
    assert first_call_record['value'] == 10
    assert first_call_record['ranking'] == 1
    
    # Check Category creation
    mock_category.assert_called_once()
    args, kwargs = mock_category.call_args
    assert args[0] == 'test.csv'
