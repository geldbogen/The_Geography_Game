import pandas as pd
import pickle

import alternative_names
import categoryname_to_displayed_name

resize_ratio = [3500 / 14063, 1737 / 6981]

oceanblue = (44, 130, 201)
yellow = (255, 255, 0)
grey = (128, 128, 128)
purple = (128, 0, 128)
orange = (255, 128, 0)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
realgrey = (105, 105, 105)
gold = (255, 215, 0)

country_name_list = []
flagframedict = dict()
all_countries_available = []
clusterdict = dict()
clusternamelist = []
all_players = dict()

all_countries_in_game = []
all_categories = []
all_categories_names_and_clusters = []

mycounter = 0
whichcountrydict = dict()

p = pd.read_csv("data/important/countrylist.csv",
                index_col=False,
                keep_default_na=False)
countries_for_language_en = p.values.tolist()

neighboring_countries = pd.read_csv("data/Really New Country Borders.csv")
neighboring_countries.columns = range(len(neighboring_countries.columns))

reverse_countries_alternative_names = dict()

category_to_displayed_name_dict = categoryname_to_displayed_name.category_to_displayed_name_dict
category_to_displayed_guess_hint = categoryname_to_displayed_name.category_to_displayed_guess_hint
category_to_displayed_extra_information_category = categoryname_to_displayed_name.category_to_displayed_extra_information_category

countries_alternative_names = alternative_names.countries_alternative_names

for item in countries_alternative_names.keys():
    countries_alternative_names[item].append(item)

for mlist in countries_alternative_names.values():
    for key in countries_alternative_names.keys():
        if countries_alternative_names[key] == mlist:
            for item in mlist:
                reverse_countries_alternative_names[item.lower()] = key

for item in countries_for_language_en:
    reverse_countries_alternative_names[item[1].lower()] = item[1]

for item in countries_for_language_en:
    reverse_countries_alternative_names[item[1]] = item[1]


with open("backenddata/propertydict_new", "rb") as handle:
    my_property_dict = pickle.load(handle)


# a dictionary which takes a string and if it is a clustername
# returns the list of categories associated to it. If it is just a normal
# categoryname it returns a list with only the asked category in it.
dictionary_attribute_name_to_attribute = {}
