from PIL import ImageDraw
import pickle
import tkinter as tk

from globalDefinitions import allPlayers, category_to_displayed_name_dict, category_to_displayed_extra_information_category, preAllCountries
from Player import mrNobody
from Image import greenImage2, greencountrydict
from Country import Country, Unknown_country
from Category import Category


def coloring(xcoordinate, ycoordinate, color, image):
    xyn = (xcoordinate, ycoordinate)
    ImageDraw.floodfill(image=image, xy=xyn, value=color, thresh=200)


def save_properties():
    global preallCountries
    propertydict = dict()
    for country in preallCountries:
        propertydict[country.name] = country.dictofattributes
    with open("backenddata/propertydict_new", "wb") as f:
        pickle.dump(propertydict, f)
    print("\n\n\n !properties saved! \n\n\n")


def callcountrybyname(name):
    for country in preAllCountries:
        if country.name == name:
            return country


def callplayerbyname(name):
    for playername in allPlayers.keys():
        if playername == name:
            return allPlayers[playername]
    return mrNobody


def get_country_by_position(xcoordinate, ycoordinate):
    # if bild.getpixel((xcoordinate,ycoordinate))==oceanblue:
    #     return Unknown_country
    x = xcoordinate
    y = ycoordinate

    color = greenImage2[x, y]
    try:
        result = callcountrybyname(greencountrydict[color])
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
