from PIL import Image
import pickle

im = Image.open("map/new_worldmap.png").convert("RGB")
im = im.resize((3500, 1737), Image.LANCZOS)
pngImage = Image.open("map/new_worldmap.png").convert("RGB")
pngImage = pngImage.resize((3500, 1737), Image.LANCZOS)

greenImage = Image.open("new_greenimage.png").convert("RGB")
greenImage = greenImage.resize((3500, 1737), Image.LANCZOS)

greenImage2 = greenImage.load()

finalimage = pngImage

with open("data/important/whichcountrydict_new","rb") as f:
    greencountrydict=pickle.load(f)
