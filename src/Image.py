from PIL import Image
import pickle

im = Image.open("map/new_worldmap.png").convert("RGB")
im = im.resize((3500, 1737), Image.LANCZOS)
png_image = Image.open("map/new_worldmap.png").convert("RGB")
png_image = png_image.resize((3500, 1737), Image.LANCZOS)

green_image = Image.open("map/new_greenimage.png").convert("RGB")
green_image = green_image.resize((3500, 1737), Image.LANCZOS)

green_image_2 = green_image.load()

finalimage = png_image

with open("data/important/whichcountrydict_new","rb") as f:
    greencountrydict=pickle.load(f)
