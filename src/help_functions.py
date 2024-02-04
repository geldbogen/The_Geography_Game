from PIL import ImageDraw
import pickle
import tkinter as tk

from global_definitions import all_players, category_to_displayed_name_dict, category_to_displayed_extra_information_category, all_countries_available, reverse_countries_alternative_names
from player import mr_nobody
from image import green_image_2, greencountrydict
from country import Country, Unknown_country
from category import Category


def coloring(xcoordinate, ycoordinate, color, image):
    xyn = (xcoordinate, ycoordinate)
    ImageDraw.floodfill(image=image, xy=xyn, value=color, thresh=200)


def save_properties():
    global preallCountries
    propertydict = dict()
    for country in all_countries_available:
        propertydict[country.name] = country.dict_of_attributes
    with open("backenddata/propertydict_new", "wb") as f:
        pickle.dump(propertydict, f)
    print("\n\n\n !properties saved! \n\n\n")


def call_country_by_name(name):
    for country in all_countries_available:
        if country.name == name:
            return country


def call_player_by_name(name):
    for playername in all_players.keys():
        if playername == name:
            return all_players[playername]
    return mr_nobody


def get_country_by_position(xcoordinate, ycoordinate):
    # if bild.getpixel((xcoordinate,ycoordinate))==oceanblue:
    #     return Unknown_country
    x = xcoordinate
    y = ycoordinate

    color = green_image_2[x, y]
    try:
        result = call_country_by_name(greencountrydict[color])
    except KeyError:
        result = Unknown_country
    return result


def Countriesareconnected(countrya: Country, countryb: Country) -> bool:
    if countrya.name in countryb.neighboring_countries or countryb.name in countrya.neighboring_countries:
        return True
    else:
        return False


def replace_A_and_B_in_category_name(tk_label: tk.Label,
                                     category: Category,
                                     first_country: Country = None,
                                     second_country: Country = None) -> str:

    categoryname = category.name.rstrip(".csv")
    try:
        displaystring = category_to_displayed_name_dict[categoryname]
        if (displaystring in ["", "TODO"]):
            displaystring = categoryname + " (TODO)"
    except KeyError:
        displaystring = categoryname + " (ERROR)"

    if (second_country == None):
        displaystring = displaystring.replace("CountryB", " (...) ")
    else:
        displaystring = displaystring.replace("CountryB", second_country.name)

    if (first_country == None):
        displaystring = displaystring.replace("CountryA", " (...) ")
    else:
        displaystring = displaystring.replace("CountryA", first_country.name)

    extra_information_displayed = ""

    try:
        if (category_to_displayed_extra_information_category[categoryname] ==
                "person"):
            extra_information_displayed = "\n (citizenship or birthplace in the current territory of the country)"
        if (category_to_displayed_extra_information_category[categoryname] ==
                "historical event"):
            extra_information_displayed = "\n (took place in the current territory of the country)"
    except KeyError:
        pass

    displaystring += extra_information_displayed

    # TODO: append guessing hint

    # guessing_hint = ""
    # try:
    #     guessing_hint = " \n (guess the "+ +")"
    # except KeyError:
    #     pass

    # displaystring+= guessing_hint

    tk_label.configure(text=displaystring)

    return tk_label

def normalize_country_name(countryname: str) -> str:
    try:
        return reverse_countries_alternative_names[countryname]
    except KeyError:
        return countryname
