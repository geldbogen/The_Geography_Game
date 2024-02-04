from PIL import ImageDraw
import pickle

from global_definitions import all_countries_available, reverse_countries_alternative_names

def coloring(xcoordinate, ycoordinate, color, image):
    xyn = (xcoordinate, ycoordinate)
    ImageDraw.floodfill(image=image, xy=xyn, value=color, thresh=200)

def save_properties():
    propertydict = dict()
    for country in all_countries_available:
        propertydict[country.name] = country.dict_of_attributes
    with open("backenddata/propertydict_new", "wb") as f:
        pickle.dump(propertydict, f)
    print("\n\n\n !properties saved! \n\n\n")

def normalize_country_name(countryname: str) -> str:
    try:
        return reverse_countries_alternative_names[countryname]
    except KeyError:
        return countryname