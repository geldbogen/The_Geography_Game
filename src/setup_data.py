import pandas as pd

import additional_explanations

from category import Category
from country import all_countries_available, call_country_by_name
from help_functions import normalize_country_name
from local_attribute import LocalAttribute

def extract_data_from_series(series: pd.DataFrame, nameofattribute,
                             numberofranked, additional_information,
                             additional_information_column_list):

    countryname = series.iloc[0]

    # if the country is not in the game, we don't need to proceed
    if not call_country_by_name(countryname) in all_countries_available:
        return None

    # the value of the attribute
    value = series.iloc[1]

    my_local_attribute = LocalAttribute()

    try:
        my_local_attribute.value = float(value)
    except ValueError:
        print(nameofattribute)
        print(value)

    my_local_attribute.rank = series.loc["ranking"] + 1

    my_local_attribute.how_many_ranked = numberofranked

    # extract the additional information
    if additional_information:

        for index, column_index in enumerate(
                additional_information_column_list):
            value = series.iloc[column_index]

            if index == 0:
                my_local_attribute.additional_information_name = value

            if index == 1:
                my_local_attribute.additional_information = value

            if index == 2:
                my_local_attribute.wikipedia_link = value

    call_country_by_name(
        countryname).dict_of_attributes[nameofattribute] = my_local_attribute


def setup_data(name,
               column=1,
               namecolumn=0,
               ascending=False,
               treat_missing_data_as_bad=False,
               apply_frac=False,
               dif=0,
               additional_information=False,
               additional_information_column_list=[2],
               cluster=None,
               is_end_only: bool = False):

    # just for convenience
    if "lower is better" in name:
        ascending = True

    # load the data
    data = pd.read_csv("data/" + name, index_col=None)

    # normalize the country names
    data.iloc[:, namecolumn] = data.iloc[:, namecolumn].apply(
        lambda x: normalize_country_name(x))

    # get the relative ranking of each country in the countrylist
    # TODO rank only the countries, which are in the game
    data.sort_values(by=data.columns[column],
                     ascending=ascending,
                     inplace=True)
    data = data.reset_index(drop=True)
    ranking_list = list(range(len(data.index)))
    data["ranking"] = ranking_list

    # get the data from the rows
    data.apply(lambda x: extract_data_from_series(
        x,
        nameofattribute=name,
        numberofranked=len(ranking_list),
        additional_information=additional_information,
        additional_information_column_list=additional_information_column_list),
               axis=1)

    # get additional explanations, if it is provided
    try:
        explanation = additional_explanations.additional_explanations[name]
    except KeyError:
        explanation = ""

    # create Category with information provided
    Category(name,
             is_active=additional_information,
             treat_missing_data_as_bad=treat_missing_data_as_bad,
             difficulty=dif,
             explanation=explanation,
             is_end_only=is_end_only)
    
    for country in all_countries_available:
        try:
            country.dict_of_attributes[name]
        except KeyError:
            country.dict_of_attributes[name] = LocalAttribute()
