from inspect import trace
from multiprocessing.dummy import active_children
from sre_parse import State
from textwrap import fill, wrap
from tkinter import Variable, font
import time
from tkinter.constants import ANCHOR
import traceback
from tracemalloc import start
from turtle import circle, color
from PIL import Image, ImageDraw, ImageTk
import os
import tkinter as tk
from tkinter import StringVar,ttk,colorchooser,messagebox,ALL,EventType
import pandas as pd
from pandas.io.pickle import read_pickle
import numpy as np
import random
import pickle
from requests.api import options
import wikipedia
import webbrowser
import sv_ttk

Image.MAX_IMAGE_PIXELS = 1000000000                                                                                              


# filename=os.path.realpath(__file__).replace("\\","/")
# filename=filename.rstrip("/Backup/try_1.py")
# print(filename)
# os.chdir(filename)
pd.options.display.max_rows = None
pd.options.display.max_columns = None


main=tk.Tk()
myframe=tk.Frame(main)
c=tk.Canvas(myframe,bg="white",width=1000,height=600)
bild=im=Image.open("new worldmap.png").convert("RGB")
bild= bild.resize((3500,1737), Image.ANTIALIAS)
ph=ImageTk.PhotoImage(image=bild,master=c)
c.background=ph
image_on_canvas=c.create_image(0,0,image=c.background,anchor="nw")
myframe.pack(side="top",fill="both",expand=True)
c.pack(side="top",fill="both",expand=True)

main.mainloop()