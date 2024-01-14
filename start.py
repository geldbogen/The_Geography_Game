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

#local files
import alternative_names
import additional_explanations
import categoryname_to_displayed_name


filename=os.path.realpath(__file__).replace("\\","/")
filename=filename.rstrip("/Backup/start.py")
print(filename)
os.chdir(filename)
pd.options.display.max_rows = None
pd.options.display.max_columns = None

im=Image.open("map/new_worldmap.png").convert("RGB")
im=im.resize((3500,1737), Image.LANCZOS)
pngim=Image.open("map/new_worldmap.png").convert("RGB")
pngim=pngim.resize((3500,1737), Image.LANCZOS)

greenimage=Image.open("new_greenimage.png").convert("RGB")
greenimage=greenimage.resize((3500,1737), Image.LANCZOS)

resize_ratio=[3500/14063,1737/6981]

greenimage2=greenimage.load()

# for item in countries_for_language("en"):
#     print(item)
with open("data/important/whichcountrydict_new","rb") as f:
    greencountrydict=pickle.load(f)

# for key in greencountrydict.keys():
#     greencountrydict[key]=greencountrydict[key].replace("Argentinia","Argentina")
  
# with open("data/important/whichcountrydict","wb") as f:
#     pickle.dump(greencountrydict,f)
# quit()



with open("backenddata/propertydict_new","rb") as handle:
    mypropertydict=pickle.load(handle)







p=pd.read_csv("data/important/countrylist.csv",index_col=False,keep_default_na=False)
countries_for_language_en=p.values.tolist()










category_to_displayed_name_dict=categoryname_to_displayed_name.category_to_displayed_name_dict
category_to_displayed_guess_hint=categoryname_to_displayed_name.category_to_displayed_guess_hint
category_to_displayed_extra_information_category=categoryname_to_displayed_name.category_to_displayed_extra_information_category



countries_alternative_names=alternative_names.countries_alternative_names




reverse_countries_alternative_names=dict()
for item in countries_alternative_names.keys():
    countries_alternative_names[item].append(item)

for mlist in countries_alternative_names.values():
    for key in countries_alternative_names.keys():
        if countries_alternative_names[key]==mlist:
            for item in mlist:
                reverse_countries_alternative_names[item.lower()]=key


for item in countries_for_language_en:
    reverse_countries_alternative_names[item[1].lower()]=item[1]




neighboring_countries=pd.read_csv("data/Really New Country Borders.csv")
neighboring_countries.columns=range(len(neighboring_countries.columns))


oceanblue=(44,130,201)
yellow=(255,255,0)
grey=(128,128,128)
purple=(128,0,128)
orange=(255,128,0)
red=(255,0,0)
green=(0,255,0)
white=(255,255,255)
realgrey=(105,105,105)
gold=(255,215,0)

all_countries=[]
all_categories=[]
all_categories_names_and_clusters=[]



# a dictionary which takes a string and if it is a clustername
# returns the list of categories associated to it. If it is just a normal 
# categoryname it returns a list with only the asked category in it.
dictionary_attribute_name_to_attribute={}


countrynamelist=[]
flagframedict=dict()
preallCountries=[]
clusterdict=dict()
clusternamelist=list()

allPlayers=dict()
class Player:
    def __init__(self,color,name,reroll_number=3):
        # name of the player
        self.name=name

        # color of the player (on the map)
        self.color=color
        
        # a collection of the flags of the countries that player possesses
        self.labeldict=dict()

        # a list of all countries the player currently controls
        self.list_of_possessed_countries=[]

        # a list of all countries with gold, which the player currently controls
        self.list_of_possessed_countries_gold=[]
        
        # a dictionary needed to translate between 
        # the name of the player and the corresponding class        
        allPlayers[self.name]=self

        # the number of rerolls the player has left
        self.rerolls_left=reroll_number

class Category:
    def __init__(self,name:str,isActive:bool,treatMissingDataAsBad:bool,difficulty:int,explanation:str="",cluster:str="",is_end_only:bool=False):
        pass
        
        # the name of the category
        self.name=name
        
        # whether a category is active, i.e. whether the player 
        # can "guess" before taking a move in order to get a freee turn
        self.isActive=isActive

        # In order to prevent that the same category is chosen too often, 
        # a counter which tracks how often a category has already been chosen 
        self.numberOfChosenAlready=0
        
        # whether the category is a "treat missing data as a loss" - category
        self.treatMissingDataAsBad=treatMissingDataAsBad
        
        # the difficulty on the category on a scale of 1 (easiest) to 5 (hardest)
        self.difficulty=difficulty

        # if provided, an explanation, which gives some details on the category (what it exactly means, the source etc.)
        self.explanation=explanation

        # whether a category is only used as a target attribute 
        # for the end of game and can not appear in the normal flow of the game
        # (usually because it is too easy)
        self.is_end_only=is_end_only
        
        # append the global list of all categories with this instance.
        all_categories.append(self)
        

        # if there is a real cluster
        if not cluster=="":
            # append the name of cluster in the namelist. 
            # One can specify the probabily of choosing this cluster by appending it multiple times.
            if not cluster in all_categories_names_and_clusters:
                # here one can tune the probability of choosing the specific cluster
                # set it as 5/number of attribute
                for i in range(5):
                    all_categories_names_and_clusters.append(cluster)
            
            
            try:
                # map clustername to the list of categories it refers to 
                dictionary_attribute_name_to_attribute[cluster].append(self)
                
                # map categoryname to single item list of corresponding class
                dictionary_attribute_name_to_attribute[self.name]=[self]

            except KeyError:
                # map clustername to the list of categories it refers to 
                dictionary_attribute_name_to_attribute[cluster]=[self]


                # map categoryname to single item list of corresponding class
                dictionary_attribute_name_to_attribute[self.name]=[self]

        else:
            # add category name to list of category names
            all_categories_names_and_clusters.append(self.name)

            # map categoryname to single item list of corresponding class             
            dictionary_attribute_name_to_attribute[self.name]=[self]


def coloring(xcoordinate,ycoordinate,color,image):
    xyn= (xcoordinate, ycoordinate)
    ImageDraw.floodfill(image=image,xy=xyn,value=color,thresh=200)


class Country:
    def __init__(self,xcoordinate,ycoordinate,name,continent=None):
        self.coordinatelist=[]
        for i in range (len(xcoordinate)):
            self.coordinatelist.append((xcoordinate[i],ycoordinate[i]))
        self.xcoordinate=xcoordinate
        self.neighboringcountries=[]
        self.ycoordinate=ycoordinate
        self.dictofattributes=dict()
        self.name=name
        self.owner="Nobody"
        self.continent=continent
        preallCountries.append(self)
        self.savelocation="data/npdata/" + self.name + "-nparray.npy"
        self.wormholecoordinates=[resize_ratio[0]* xcoordinate[0],resize_ratio[1]*ycoordinate[0]]

    def getcolor(self,image):
        output=[]
        for coordinates in self.coordinatelist:
            output.append(image.getpixel(coordinates))
        return output
    def gettwocountrycode(self) -> str:
        if self.name=="Ivory Coast":
            return "ci"
        if self.name=="Myanmar":
            return "mm"
        if self.name=="Democratic Republic of the Congo":
            return "cd"
        if self.name=="Bosnia and Herzegovina":
            return "ba"
        if self.name=="Czech Republic":
            return "cz"
        if self.name=="Republic of the Congo":
            return "cg"
        for item in countries_for_language_en:
            if item[1]==self.name:
                return item[0]
        return "noflag"
    def setpixels(self,image):
        if self.name=="Unknown Country":
            return None
        print(self.name)
        savearray=np.zeros(shape=(1,2))
        for coordinate in self.coordinatelist:
            image2=image
            seed=(coordinate[0],coordinate[1])
            ImageDraw.floodfill(image2,seed,(0,255,0),thresh=200)
            npimage=np.array(image2)
            print(npimage.shape)
            green=np.array([0,255,0],dtype=np.uint8)
            greens=list(zip(*np.where(np.all((npimage==green),axis=-1))))
            sarray=np.array([*greens])
            savearray=np.append(savearray,sarray,axis=0)
            print(sarray)
            print(sarray.shape)
            print(savearray.shape)
        with open(self.savelocation,"wb") as f:
            np.save(f,savearray)
    def getresizedflag(self,height):
        countryurl="pictures/flag_pictures/w1280/" + self.gettwocountrycode().lower() + ".png"
        flagimage=(Image.open(countryurl))
        w=float(flagimage.width)
        h=float(flagimage.height)
        return ImageTk.PhotoImage(flagimage.resize((int(height*w/h),int(height)),Image.LANCZOS))
    def loadpixels(self):
        global all_countries
        global countrynamelist
        if self.name=="Unknown Country":
            self.set_of_pixels=set()
            all_countries.append(self)
            countrynamelist.append(self.name)
            return None
        try:
            print(self.name)
            marray=np.load(self.savelocation,allow_pickle=True)
            marray=marray.T
            self.set_of_pixels=set(zip(marray[0],marray[1]))
        except Exception as e:
            print(str(e))
            self.setpixels(pngim)  
        all_countries.append(self)
        countrynamelist.append(self.name)



def save_properties():
    global preallCountries
    propertydict=dict()
    for country in preallCountries:
        propertydict[country.name]=country.dictofattributes
    with open("backenddata/propertydict_new","wb") as f:
        pickle.dump(propertydict,f)
    print("\n\n\n !properties saved! \n\n\n")




def setupdata(data,column,namecolumn,nameofattribute,ascending,treatmissingdataasbad=False,applyfrac=False,additional_information=False,additional_information_column=2):
    
    def append_dataframe(series,nameofattribute,numberofranked):
        additional_informations=[]
        try:
            countryname=reverse_countries_alternative_names[series.iloc[0].lower()]
        except KeyError:
            return None  
        except AttributeError:
            return None  
        if not callcountrybyname(countryname) in preallCountries:
            return None
        value=series.iloc[1]
        if additional_information:
            additional_informations=list()
            for item in additional_information_column:
                additional_informations.append(series.iloc[item])
        mylist=list()
        mylist.append(value)
        mylist.append((series.loc["ranking"]+1))
        mylist.append(numberofranked+1)
        mylist+=additional_informations
        callcountrybyname(countryname).dictofattributes[nameofattribute]=mylist
        pass

    
    if not treatmissingdataasbad:
        data=data[data["1"]!=float(-1)]
    else:
        if not ascending:
            data["1"]=data["1"].apply(lambda x: float(0) if x==float(-1) else x)
        else:
            data["1"]=data["1"].apply(lambda x: float(9999999999) if x==float(-1) else x)
    data.sort_values(by=str(column),ascending=ascending,inplace=True)
    data=data.reset_index(drop=True)
    dlist=data.iloc[:,0].tolist()
    pass
    for index,item in enumerate(dlist):
        try:
            dlist[index]=reverse_countries_alternative_names[item]
        except KeyError:
            pass        
    data.iloc[:,0]=dlist
    if treatmissingdataasbad:
        for countryclass in preallCountries:
            if countryclass.name not in dlist:
                if not ascending:
                    myseries={"0":countryclass.name,"1":float(0)}
                else:
                    myseries={"0":countryclass.name,"1":float(9999999999)}
                myseries = pd.DataFrame(myseries)
                data = pd.concat([data,myseries],ignore_index=True)
    rankinglist=list(range(len(data.index)))
    data["ranking"]=rankinglist
    data.apply(lambda x: append_dataframe(x,nameofattribute=nameofattribute,numberofranked=len(rankinglist)),axis=1)




def bettersetupdata(name,column=1,namecolumn=0,ascending=False,treatmissingdataasbad=False,applyfrac=False,dif=0,additional_information=False,additional_information_column=[2],cluster=None,is_end_only:bool=False):

    if "lower is better" in name:
        ascending=True
    data=pd.read_csv("data/" + name,index_col=False)
    setupdata(data,column,namecolumn,name,ascending=ascending,treatmissingdataasbad=treatmissingdataasbad,applyfrac=applyfrac,additional_information=additional_information,additional_information_column=additional_information_column)
    
    # get additional explanations, if it is provided
    try:
        explanation=additional_explanations.additional_explanations[name]
    except KeyError:
        explanation=""
    
    # create Category with information provided
    Category(name,isActive=additional_information,treatMissingDataAsBad=treatmissingdataasbad,difficulty=dif,explanation=explanation,is_end_only=is_end_only)


def callcountrybyname(name):
    for country in preallCountries:
        if country.name==name:
            return country

def callplayerbyname(name):
    for playername in allPlayers.keys():
        if playername==name:
            return allPlayers[playername]
    return Mr_Nobody

def getcountrybyposition(xcoordinate,ycoordinate):
    # if bild.getpixel((xcoordinate,ycoordinate))==oceanblue:
    #     return Unknown_country
    x=xcoordinate
    y=ycoordinate

    color=greenimage2[x,y]
    try:
        result= callcountrybyname(greencountrydict[color]) 
    except KeyError:
        result=Unknown_country 
    return result


def Countriesareconnected(countrya:Country,countryb:Country) -> bool:
    if countrya.name in countryb.neighboringcountries or countryb.name in countrya.neighboringcountries:
        return True
    else:
        return False



def replace_A_and_B_in_category_name(tk_label:tk.Label,category:Category, first_country:Country = None, second_country:Country = None) -> str:
    
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
        if (category_to_displayed_extra_information_category[categoryname] == "person"):
            extra_information_displayed = "\n (citizenship or birthplace in the current territory of the country)"
        if (category_to_displayed_extra_information_category[categoryname] == "historical event"):
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



Mr_Nobody=Player(color="white",name="Nobody")
No_Data_Body=Player(color=realgrey,name="Nobody")

class MainWindow():
    def __init__(self,bild,listofplayers,wormholemode,startingcountries="random",numberofrounds=99999999999,winningcondition="number of countries",numberofwormholes=3,pred_attribute="random",peacemode=0,reversed_end_attribute=0):
        
        self.rerolls=3
        self.numberoftargets=2
        self.pred_attribute_name=pred_attribute
        self.winningcondition=winningcondition
        self.flagframedict=dict()
        self.numberofrounds=numberofrounds
        self.index=0
        self.goldlist=list()
        self.choosingindex=-1
        self.startingcountries=startingcountries
        self.reversed_end_attribute=reversed_end_attribute
        main=tk.Tk()
        sv_ttk.set_theme("dark")  # Set light theme

        self.list_of_players=listofplayers
        print(self.list_of_players)
        print(len(listofplayers))
        self.activeplayercounter=0
        self.active_player=self.list_of_players[self.activeplayercounter]
        self.numberofplayers=len(self.list_of_players)
        self.endattribute=None
        self.wormholemode=wormholemode
        self.wormholed_countries=list()
        self.numberofwormholes=numberofwormholes
        print(self.winningcondition)

        self.peacemode=peacemode

        self.currentattribute=all_categories[0]

        self.main=main

        self.chosencountrya=None
        self.turncounter=0

        self.frame1=tk.Frame(main,width=300,height=300) 
        self.frame1.pack(side="bottom", fill="both",expand=True)
        
        #frame1=frame2+areyousurebuttons

        self.frame2=tk.Frame(self.frame1)
        # frame2= frame3 + flags    

        self.frame3=tk.Frame(self.frame2)
        self.buttonframe=tk.Frame(self.frame1)
        self.buttonframe2=tk.Frame(self.frame1)
        self.bild=bild
        self.c=tk.Canvas(self.frame3,bg="white",width=1000,height=600)
        
        ph=ImageTk.PhotoImage(image=bild,master=self.c)
        self.c.background=ph
        self.image_on_canvas=self.c.create_image(0,0,image=self.c.background,anchor="nw")
        
        #scrollbar
        my_scrollbar1=tk.Scrollbar(self.frame3,orient="vertical",command=self.c.yview)
        my_scrollbar1.pack(side="right",fill="y")
        my_scrollbar1.config(command=self.c.yview)
        my_scrollbar2=tk.Scrollbar(self.frame3,orient="horizontal",command=self.c.xview)
        my_scrollbar2.pack(side="bottom",fill="x")
        my_scrollbar2.config(command=self.c.xview)
        self.c.config(yscrollcommand=my_scrollbar1.set,xscrollcommand=my_scrollbar2.set)
        self.c.config(scrollregion = self.c.bbox("all"))

        for player in self.list_of_players:
            self.flagframedict[player.name]=tk.Frame(self.frame2)
            self.flagframedict[player.name].current_flagdict=dict()
        
        


        self.c.bind("<ButtonPress-1>",self.click)
        
        
        self.c.bind("<ButtonPress-3>", self.scroll_start)
        self.c.bind("<B3-Motion>", self.scroll_move)


       
        #unpacking
        self.frame3.pack(side="bottom",expand=True,fill="both")
        self.frame2.pack(side="top",expand=True,fill="both")
        self.frame1.pack(side="top",expand=True,fill="both")
        self.frame4=tk.Frame(self.frame3)
        self.frame5=tk.Frame(self.frame3)


        self.reroll_button=tk.Button(self.frame5,text="rerolls left:\n " +str(self.active_player.rerolls_left) ,font="Helvetica 25",anchor="sw",command=lambda: self.reroll(player=self.active_player))
        self.reroll_button.pack(side="left",fill="y")

        self.showing_country_label=tk.Label(self.frame5,text="It is the turn of " +self.active_player.name +"\n You have not chosen any country yet",font="Helvetica 25")
        self.showing_country_label.pack(side="bottom",expand=True,fill="both")

        self.turn_counter_label=tk.Label(self.frame4,text=str(self.turncounter),font="Helvetica 50")
        self.turn_counter_label.pack(side="right")
        
        self.showing_current_attribute_text_label=tk.Label(self.frame4,text="Welcome!",font="Helvetica 25")
        self.showing_current_attribute_text_label.pack(anchor="nw",expand=True,fill="both")

        self.frame4.pack(side="top",fill="x")
        self.frame5.pack(side="bottom",fill="x")
        
        self.c.pack(side="top",fill="both",expand=True)
        



        self.button_sure=tk.Button(self.buttonframe,text="Attack!",font="Helvetica 20")
        self.button_not_sure=tk.Button(self.buttonframe,text="No go back",font="Helvetica 20")
        self.button_sure.pack(side="left")
        self.button_not_sure.pack(side="right")
        self.button_claim=tk.Button(self.buttonframe2,text="Yes Please!",font="Helvetica 20")
        
        self.d=""
        self.randompeoplestart=random.sample(range(0,len(self.list_of_players)),len(self.list_of_players))


        #usher choosing countries procedure if that mode was chosen
        if self.startingcountries=="choose":
            self.choosingindex=0
            self.active_player=self.list_of_players[self.randompeoplestart[self.choosingindex]]
            self.showing_current_attribute_text_label["text"]="Choose a starting country of your choice"
            self.showing_country_label["text"]=self.active_player.name + "\n Please choose a starting country"
        
        #roll starting countries for the players
        #TODO take care of ending attribute
        if self.startingcountries=="random":
            self.choosingindex=len(self.list_of_players)
            self.setupgame()
            while True:
                j=0
                self.randomstart=random.sample(range(0,len(all_countries)),len(self.list_of_players))
                for rng in self.randomstart:
                    if len(all_countries[rng].neighboringcountries)<3:
                        j=1
                    for rng2 in self.randomstart:
                        if Countriesareconnected(all_countries[rng2],all_countries[rng]):
                            j=1
                    if self.winningcondition=="attribute":
                        try:
                            all_countries[rng].dictofattributes[self.endattribute.name][0]
                        except:
                            j=1
                if j==0:
                    break
            for i in range (len(self.list_of_players)):
                self.claimcountry(self.list_of_players[i],all_countries[self.randomstart[i]])
                print(all_countries[self.randomstart[i]].name)

        #roll first attribute
        self.getgoodattribute(self.active_player)
        replace_A_and_B_in_category_name(self.showing_current_attribute_text_label,self.currentattribute)
        
        main.mainloop()

    def updateimage(self,newimage):
        newimage=ImageTk.PhotoImage(newimage)
        self.c.background=newimage
        self.c.itemconfig(self.image_on_canvas,image=newimage)
    def click(self,event):
        
        if self.d=="disabled":
            return None
        if self.choosingindex<len(self.list_of_players):
            clickedcountry=getcountrybyposition(self.c.canvasx(event.x),self.c.canvasy(event.y))
            self.showing_country_label["text"]=self.active_player.name + " do you want to start with \n" + clickedcountry.name + " ?"
            self.button_claim["command"]=lambda: self.claimstartingcountry(self.active_player,clickedcountry)
            self.button_claim.pack(side="bottom")
            self.buttonframe2.pack(side="bottom")
            return None
        clickedcountry=getcountrybyposition(self.c.canvasx(event.x),self.c.canvasy(event.y))
        if self.chosencountrya==None:
            self.showing_country_label["text"]="It is the turn of " + self.active_player.name + "\n You have chosen " + clickedcountry.name + " currently controlled by " + clickedcountry.owner
            if clickedcountry.owner==self.active_player.name:
                self.chosencountrya=clickedcountry
                replace_A_and_B_in_category_name(self.showing_current_attribute_text_label,self.currentattribute,self.chosencountrya)

                self.showing_country_label["text"]=self.showing_country_label["text"] + "\n You can attack with this country"
        else:
            if self.peacemode==1 and clickedcountry.owner!="Nobody" and callplayerbyname(clickedcountry.owner)!=self.active_player:
                self.chosencountrya=None
                self.showing_country_label["text"]="You can not attack anoter player's countries in peace mode! \n Choose another country!"
                # time.sleep(5)
                # self.showingcountrylabel["text"]=""
                return None
            if Countriesareconnected(clickedcountry,self.chosencountrya):
                if self.active_player!=callplayerbyname(clickedcountry.owner):
                    replace_A_and_B_in_category_name(self.showing_current_attribute_text_label,self.currentattribute,self.chosencountrya,clickedcountry)

                    self.showing_country_label["text"]="Does the above sentence looks correct to you?"
                    self.button_sure["command"]= lambda: self.attack(self.chosencountrya,clickedcountry)
                    self.button_not_sure["command"]=self.fuckgoback
                    self.buttonframe.pack(side="bottom")
                    self.d="disabled"
                else:
                    self.showing_country_label["text"]="You already own this country"
            else:
                self.chosencountrya=None
                self.showing_country_label["text"]="These countries do not share a common land border.\n Please choose another pair!"

    def find_distance(self,countrya:Country,countryb:Country):
        mydict=dict()
        myset=set(countrya.name)
        q=[[countrya.name,0]]
        print(q)
        for country in all_countries:
            mydict[country.name]=country.neighboringcountries
        while countryb.name not in myset:
            temp=q[0]
            q.pop(0)
            for countryname in mydict[temp[0]]:
                if countryname in myset:
                    pass
                else:
                    myset.add(countryname)
                    q.append([countryname, temp[1]+1])
                    if countryname==countryb.name:
                        return temp[1]+1
            pass
        return None

    def attack(self,countrya,countryb):
        
        self.buttonframe.pack_forget()
        self.d=""
        self.showing_country_label["text"]=""
        self.chosencountrya=None
        result=self.attackwithattribute(self.currentattribute.name,countrya,countryb)
        if result=="no data":
            self.popupwinorloose(countrya,countryb,self.currentattribute,wl="no data")
            self.getgoodattribute(self.active_player)
            replace_A_and_B_in_category_name(self.showing_current_attribute_text_label,self.currentattribute)
            return None
        if result=="draw!":
            self.popupwinorloose(countrya,countryb,self.currentattribute,wl="draw!")
            self.getgoodattribute(self.active_player)
            replace_A_and_B_in_category_name(self.showing_current_attribute_text_label,self.currentattribute)
            return None
        if result=="hard defeat!":
            self.claimcountry(self.active_player,countryb)
            self.popupwinorloose(countrya,countryb,self.currentattribute,wl="hard defeat!")
            return None
        if result=="True":
            self.claimcountry(self.active_player,countryb)
            self.popupwinorloose(countrya,countryb,self.currentattribute,wl="you win!")
            
            
        else:
            self.popupwinorloose(countrya,countryb,self.currentattribute,wl="you loose!")
            if countryb.owner!="Nobody":
                self.claimcountry(callplayerbyname(countryb.owner),countrya)

        
        
                

    def transition(self,sameplayeragain=False):

        if not sameplayeragain:
            if self.checkifgameshouldend():
                return None
            self.activeplayercounter=self.activeplayercounter+1
        self.index=self.activeplayercounter%len(self.list_of_players)
        
        if not sameplayeragain:
            if self.index==0:
                self.turncounter+=1

        #update the interface
        self.turn_counter_label["text"]=str(self.turncounter)
        self.flagframedict[self.active_player.name].pack_forget()
        self.active_player=self.list_of_players[self.index]
        self.showing_country_label["text"]="It is the turn of " +self.active_player.name +"\n You have not chosen any country yet"
        
        #roll a new attribute
        self.getgoodattribute(self.active_player)
        replace_A_and_B_in_category_name(self.showing_current_attribute_text_label,self.currentattribute)
        self.flagframedict[self.active_player.name].pack(side="top")
        if self.wormholemode=="every round changing wormholes":
            if self.index==0:
                try:
                    self.destroy_all_wormholes()    
                except:
                    traceback.print_exc()
                self.activate_wormholes(3)    
        if self.wormholemode=="every round changing wormholes from your countries":
            try:
                self.destroy_all_wormholes()
            except:
                traceback.print_exc()
            if len(self.active_player.list_of_possessed_countries)>=3:
                print("wormholes werden aktiviert")
                self.activate_wormholes(1,player=self.active_player)
        self.reroll_button["text"]="rerolls left:\n " +str(self.active_player.rerolls_left)

    def reroll(self,player:Player):
        if player.rerolls_left==0:
            return None
        player.rerolls_left-=1
        
        self.getgoodattribute(self.active_player)
        replace_A_and_B_in_category_name(self.showing_current_attribute_text_label,self.currentattribute)
        self.reroll_button["text"]="rerolls left:\n " +str(self.active_player.rerolls_left)


    def getgoodattribute(self,player,counter=0,i=0) -> None:
        i=0
        counter=0
        atleast_one=False
        self.currentattribute=self.getrandomattribute_with_cluster()


        # if the attribute is end only it should not be a valid attribute
        if self.currentattribute.is_end_only:
            self.getgoodattribute(player)


        for country in player.list_of_possessed_countries:
            #TODO:make it better if just some continents are chosen
            #simulate attacks in order to get an attribute, with which one can actually do something (to no frustrate players)
            for neighboringcountrystring in list(set(country.neighboringcountries)):
                i+=1
                if self.attackwithattribute(self.currentattribute.name,country,callcountrybyname(neighboringcountrystring))=="no data":
                    counter = counter+1
                    print(neighboringcountrystring +" \n" + country.name)
                if self.attackwithattribute(self.currentattribute.name,country,callcountrybyname(neighboringcountrystring)) in ["draw","True"]:
                    if not callcountrybyname(neighboringcountrystring) in player.list_of_possessed_countries:
                        atleast_one=True
        
        print(float(counter)/float(i))
        if float(counter)/float(i)>0.25 or not atleast_one:
            print(self.currentattribute.name)
            print("doesn't work because of the missing above we get a new attribute!")
            self.getgoodattribute(player)
        else:
            if self.currentattribute.numberOfChosenAlready==1:
                self.currentattribute.numberOfChosenAlready=0
                self.getgoodattribute(player)
            else:
                self.currentattribute.numberOfChosenAlready+=1


    def getrandomattribute_with_cluster(self) -> Category:

        # get a random attribute name (including the name of a cluster)
        
        self.currentattributename_with_cluster=random.choice(all_categories_names_and_clusters)

        # if a cluster is chosen choose a random attribute from that cluster
        if len(dictionary_attribute_name_to_attribute[self.currentattributename_with_cluster])>1:
            return random.choice(dictionary_attribute_name_to_attribute[self.currentattributename_with_cluster])
        # if it is not a cluster, just return the attribute
        else: 
            return dictionary_attribute_name_to_attribute[self.currentattributename_with_cluster][0]
        


    def fuckgoback(self):
        # self.buttonsure.pack_forget()
        # self.buttonnotsure.pack_forget()
        self.buttonframe.pack_forget()
        self.chosencountrya=None
        self.showing_country_label["text"]=""
        self.d=""
    def attackwithattribute(self,attributename,countrya,countryb):
        try:
            if isinstance(countrya.dictofattributes[attributename][1],int) and isinstance(countryb.dictofattributes[attributename][1],int):
                if countrya.dictofattributes[attributename][0]==countryb.dictofattributes[attributename][0]:
                    return "draw!"
                if countrya.dictofattributes[attributename][1]< countryb.dictofattributes[attributename][1]:
                    if countrya.dictofattributes[attributename][1]+99< countryb.dictofattributes[attributename][1]:
                        return "hard defeat!"
                    return "True"
                else:
                    return "False"
            else:
                return "no data"
        except:
            return "no data"
        
    def claimcountry(self,player,country):

        def changethingswhencountryclicked(country):
            clickedcountry=country
            if self.chosencountrya==None:
                self.showing_country_label["text"]="It is the turn of " + self.active_player.name + "\n You have chosen " + clickedcountry.name + " currently controlled by " + clickedcountry.owner
                if clickedcountry.owner==self.active_player.name:
                    self.chosencountrya=clickedcountry
                    self.showing_country_label["text"]=self.showing_country_label["text"] + "\n You can attack with this country"
            else:
                if Countriesareconnected(clickedcountry,self.chosencountrya):
                    if self.active_player!=callplayerbyname(clickedcountry.owner):
                        self.showing_country_label["text"]="You want to attack  " + clickedcountry.name + " currently controlled by " + clickedcountry.owner +" with " + self.chosencountrya.name + " are you sure?"
                        self.button_sure["command"]= lambda: self.attack(self.chosencountrya,clickedcountry)
                        self.button_not_sure["command"]=self.fuckgoback
                        self.buttonframe.pack(side="bottom")
                        self.d="disabled"
                    else:
                        self.showing_country_label["text"]="You already own this country"
                else:
                    self.chosencountrya=None
                    self.showing_country_label["text"]="Those countries do not share a common land border. Please choose another pair"
                    time.wait(5)
                    self.showing_country_label["text"]=""
                


        player.list_of_possessed_countries.append(country)
        oldowner=country.owner
        country.owner=player.name
    

        inv_map = {v: k for k, v in greencountrydict.items()}
        color=inv_map[country.name]
        npimage=np.array(greenimage)
        green=np.array(color,dtype=np.uint8)
        greens=list(zip(*np.where(np.all((npimage==green),axis=-1))))
    
        for tuplen in greens:
            self.bild.putpixel((tuplen[1],tuplen[0]),player.color)
        
        if player.name!="Nobody":
            if self.winningcondition!="get gold" or country in self.goldlist:
                frame=self.flagframedict[player.name]
                myimage=country.getresizedflag(50)
                newlabel=tk.Label(frame,image=myimage)
                newlabel.grid(row=0,column=len(player.list_of_possessed_countries)+1)
                newlabel.bind("<Button-1>",lambda x: self.popupcountrystats(country))
                player.labeldict[country]=newlabel
                frame.current_flagdict[country]=myimage
                
        
        
        if oldowner!="Nobody" and not self.winningcondition in ["get gold"]:
            callplayerbyname(oldowner).list_of_possessed_countries.remove(country)
            callplayerbyname(oldowner).labeldict[country].destroy()
        


        self.updateimage(self.bild)

        if self.winningcondition=="get gold":
            if player.name!="Nobody":
                if country in self.goldlist:
                    player.gold=player.gold+1
                    self.goldlist.remove(country)
                    player.list_of_possessed_countries_gold.append(country)
        


    def claimstartingcountry(self,player,country):
        self.buttonframe2.pack_forget()
        self.claimcountry(player,country)
        self.choosingindex=self.choosingindex+1
        if self.choosingindex==len(self.list_of_players):
            self.active_player=self.list_of_players[self.index]
            self.showing_country_label["text"]="It is the turn of " +self.active_player.name +"\n You have not chosen any country yet"
            replace_A_and_B_in_category_name(self.showing_current_attribute_text_label,self.currentattribute)
            self.setupgame()
        else:
            self.active_player=self.list_of_players[self.randompeoplestart[self.choosingindex]]
            self.showing_current_attribute_text_label["text"]="Choose a starting country of your choice"
            self.showing_country_label["text"]=self.active_player.name + " Please choose a starting country"

    def callback(self,url):
        webbrowser.open_new(url)

    def popupcountrystats(self,country):
        def _on_mousewheel(event):
            canvas21.yview_scroll(int(-1*(float(event.delta)/120)), "units")
        
        win2=tk.Toplevel()

        frame21=tk.Frame(win2)
        frame21.pack(fill="both",expand=True)
        canvas21=tk.Canvas(frame21)
        canvas21.pack(side="left",expand=True,fill="both")

        my_scrollbar12=tk.Scrollbar(frame21,orient="vertical",command=canvas21.yview)
        my_scrollbar12.pack(side="right",fill="y")
        my_scrollbar12.config(command=canvas21.yview)


        frame22=tk.Frame(canvas21)
        canvas21.create_window((0,0),window=frame22,anchor="nw")
        win2.geometry("1650x825")
        frame22.bind(
            "<Configure>",
            lambda e: canvas21.configure(
                scrollregion=canvas21.bbox("all")
            )
        )
        canvas21.bind_all("<MouseWheel>",_on_mousewheel)

        img=country.getresizedflag(800)
        self.img221=img
        panel=tk.Label(frame22,image=img)
        panel.grid(column=0,row=0,columnspan=4,sticky="N")
        namelabel=tk.Label(frame22,text=country.name,font="Helvetica 100")
        namelabel.grid(row=1,column=0,columnspan=4)


        mylist=list(country.dictofattributes.keys())
        mylist.sort(key=lambda x: x.lower())
        for index,item in enumerate(mylist):
            mylabel=tk.Label(frame22,text=item.replace(".csv",""),font="Helvetica 15")
            mylabel.grid(row=index+2,column=0,pady=10)
            mylabel2=tk.Label(frame22,text=country.dictofattributes[item][0],font="Helvetica 15")
            try:
                mylabel3=tk.Label(frame22,text=country.dictofattributes[item][3],font="Helvetica 15")
            except IndexError:
                mylabel3=tk.Label(frame22,text="--",font="Helvetica 15")
            mylabel2.grid(row=index+2,column=1,pady=10)
            mylabel3.grid(row=index+2,column=2,pady=10)
            mylabel4=tk.Label(frame22,text=str(country.dictofattributes[item][1]) + "/"+ str(country.dictofattributes[item][2]),font="Helvetica 15")
            mylabel4.grid(row=index+2,column=3,pady=10)
        ddlist=[[propertyname,value[1]/value[2]] for propertyname,value in country.dictofattributes.items()]
        ddlist.sort(key=lambda x: x[1])
        print(ddlist)
        goodlist=ddlist[:5]
        ddlist=[[pname,value] for [pname,value] in ddlist if country.dictofattributes[pname][0] not in [-1,-1.0,-9999.0,-9999]]
        badlist=ddlist[-5:]
        badlist.reverse()
        goodLabel=tk.Label(frame22,text=country.name + " is good in:",font="Helvetica 15")
        badLabel=tk.Label(frame22,text=country.name + " is bad in:",font="Helvetica 15")

        goodLabel.grid(row=len(mylist)+3,column=0,columnspan=4,pady=20)
        for index,ditem in enumerate(goodlist):
            item=ditem[0]
            mylabel=tk.Label(frame22,text=item.replace(".csv",""),font="Helvetica 15")
            mylabel.grid(row=len(mylist) + index+4,column=0,pady=10)
            mylabel2=tk.Label(frame22,text=country.dictofattributes[item][0],font="Helvetica 15")
            try:
                mylabel3=tk.Label(frame22,text=country.dictofattributes[item][3],font="Helvetica 15")
            except IndexError:
                mylabel3=tk.Label(frame22,text="--",font="Helvetica 15")
            mylabel2.grid(row=index+4+len(mylist),column=1,pady=10)
            mylabel3.grid(row=index+4+len(mylist),column=2,pady=10)
            mylabel4=tk.Label(frame22,text=str(country.dictofattributes[item][1]) + "/"+ str(country.dictofattributes[item][2]),font="Helvetica 15")
            mylabel4.grid(row=index+4+len(mylist),column=3,pady=10)

        badLabel.grid(row=len(mylist)+9,column=0,columnspan=4,pady=20)
        for index,ditem in enumerate(badlist):
            item=ditem[0]
            mylabel=tk.Label(frame22,text=item.replace(".csv",""),font="Helvetica 15")
            mylabel.grid(row=len(mylist) + index+10,column=0,pady=10)
            mylabel2=tk.Label(frame22,text=country.dictofattributes[item][0],font="Helvetica 15")
            try:
                mylabel3=tk.Label(frame22,text=country.dictofattributes[item][3],font="Helvetica 15")
            except IndexError:
                mylabel3=tk.Label(frame22,text="--",font="Helvetica 15")
            mylabel2.grid(row=index+10+len(mylist),column=1,pady=10)
            mylabel3.grid(row=index+10+len(mylist),column=2,pady=10)
            mylabel4=tk.Label(frame22,text=str(country.dictofattributes[item][1]) + "/"+ str(country.dictofattributes[item][2]),font="Helvetica 15")
            mylabel4.grid(row=index+10+len(mylist),column=3,pady=10)

    def activate_wormholes(self,numberofwormholes,player=None):    
        self.colorarray=["cyan", "dark slate grey", "dark green", "dark violet", "dark goldenrod", "medium violet red", "brown2", "medium spring green", "grey2"]
        def makeline_not_hidden(line):
            self.c.itemconfig(line,state=tk.NORMAL)
        def makeline_hidden(line):
            self.c.itemconfig(line,state=tk.HIDDEN)
        def create_good_line(country1: Country,country2:Country):
            ml=self.c.create_line(country1.wormholecoordinates[0], country1.wormholecoordinates[1], country2.wormholecoordinates[0], country2.wormholecoordinates[1],width=5,fill="black",dash=[5,2],state=tk.HIDDEN)
            self.linelist.append(ml)
            color=self.colorarray[random.randrange(0,len(self.colorarray))]
            self.colorarray.remove(color)
            startpoint=self.c.create_rectangle(country1.wormholecoordinates[0]+15,country1.wormholecoordinates[1]+15,country1.wormholecoordinates[0]-15,country1.wormholecoordinates[1]-15,fill="gray",stipple="@my_stripple.xbm",outline=color,width=5)
            endpoint=self.c.create_rectangle(country2.wormholecoordinates[0]+15,country2.wormholecoordinates[1]+15,country2.wormholecoordinates[0]-15,country2.wormholecoordinates[1]-15,fill="gray",stipple="@my_stripple.xbm",outline=color,width=5)
            self.pointlist.append(startpoint)
            self.pointlist.append(endpoint)
            self.c.tag_bind(startpoint,"<Enter>",lambda x: makeline_not_hidden(ml))
            self.c.tag_bind(endpoint,"<Enter>",lambda x: makeline_not_hidden(ml))
            self.c.tag_bind(startpoint,"<Leave>",lambda x: makeline_hidden(ml))
            self.c.tag_bind(endpoint,"<Leave>",lambda x: makeline_hidden(ml))
        self.linelist=list()
        self.pointlist=list()
        country1=Germany
        country2=France
        if player!=None:
            while (country2.name in country1.neighboringcountries or country1.name in country2.neighboringcountries or country1.continent==country2.continent or country2 in player.list_of_possessed_countries or country1==Unknown_country or country2==Unknown_country or (self.peacemode==1 and (country1.owner!="Nobody" and country2.owner!="Nobody"))):
                country1=player.list_of_possessed_countries[random.randrange(1,len(player.list_of_possessed_countries))]
                country2=all_countries[random.randrange(1,len(all_countries))]
            country1.neighboringcountries.append(country2.name)
            self.wormholed_countries.append([country1,country2])
            create_good_line(country1,country2)
            print(self.linelist)
            return None
        
        for i in range(numberofwormholes):
            
            while (country2.name in country1.neighboringcountries or country1.name in country2.neighboringcountries or country1.continent==country2.continent):
                country1=all_countries[random.randrange(1,len(all_countries))]
                country2=all_countries[random.randrange(1,len(all_countries))]
            country1.neighboringcountries.append(country2.name)
            self.wormholed_countries.append([country1,country2])
            create_good_line(country1,country2)
            print(self.linelist)

    def destroy_all_wormholes(self):
        self.colorarray=["indian red", "dark slate grey", "dark green", "dark violet", "dark goldenrod", "tomato3", "medium violet red", "brown2", "PaleGreen4"]
        for item in self.wormholed_countries:
            item[0].neighboringcountries.remove(item[1].name)
        self.wormholed_countries=list()
        print("delete")
        print(self.linelist)
        for item in self.linelist:
            self.c.delete(item)
        for item in self.linelist:
            self.linelist.remove(item)

        for item in self.pointlist:
            self.c.delete(item)
        for item in self.pointlist:
            self.pointlist.remove(item)
    
    def popupwinorloose(self,countrya,countryb,property:Category,wl):
        def kill_guessed_correct():
            self.transition(sameplayeragain=True)
            win.destroy()
        def kill_button():
            if wl=="no data" or wl=="draw!":
                self.transition(sameplayeragain=True)
            else:
                self.transition(sameplayeragain=False)
            win.destroy()
        def _on_mousewheel(event):
            canvas11.yview_scroll(int(-1*(float(event.delta)/120)), "units")
        
        additional_information=property.isActive
        win=tk.Toplevel()
        win.geometry("1400x825")
        frame11=tk.Frame(win)
        frame11.pack(fill="both",expand=True)
        canvas11=tk.Canvas(frame11)
        canvas11.pack(side="left",expand=True,fill="both")
        


        my_scrollbar11=tk.Scrollbar(frame11,orient="vertical",command=canvas11.yview)
        my_scrollbar11.pack(side="right",fill="y")
        my_scrollbar11.config(command=canvas11.yview)
        

        frame12=tk.Frame(canvas11)
        canvas11.create_window((0,0),window=frame12,anchor="nw")

        frame12.bind(
            "<Configure>",
            lambda e: canvas11.configure(
                scrollregion=canvas11.bbox("all")
            )
        )


        canvas11.bind_all("<MouseWheel>",_on_mousewheel)
        

        url1="pictures/flag_pictures/w320/" + countrya.gettwocountrycode().lower() + ".png"
        print(countryb.gettwocountrycode())
        print("das war der Code")
        url2="pictures/flag_pictures/w320/" + countryb.gettwocountrycode().lower() + ".png"
        img1=ImageTk.PhotoImage(Image.open(url1))
        img2=ImageTk.PhotoImage(Image.open(url2))
        frame12.img1=img1
        frame12.img2=img2
        panel1=tk.Label(frame12,image=img1)
        panel2=tk.Label(frame12,image=img2)

        url3="pictures/success3.png"
        url4="pictures/fail2.png"
        url5="pictures/vs.png"
        url6="pictures/no_data.png"
        url7="pictures/draw.png"
        url8="pictures/top5.png"
        url9="pictures/worst5.png"
        url10="pictures/great_success.png"

        img3=ImageTk.PhotoImage(Image.open(url3))
        img4=ImageTk.PhotoImage(Image.open(url4))
        img5=ImageTk.PhotoImage(Image.open(url5))
        img6=ImageTk.PhotoImage(Image.open(url6))
        img7=ImageTk.PhotoImage(Image.open(url7))
        img8=ImageTk.PhotoImage(Image.open(url8))
        img9=ImageTk.PhotoImage(Image.open(url9))
        img10=ImageTk.PhotoImage(Image.open(url10))
        


        frame12.img3=img3
        frame12.img4=img4
        frame12.img5=img5
        frame12.img6=img6
        frame12.img7=img7
        frame12.img8=img8
        frame12.img9=img9
        frame12.img10=img10

        panel3=tk.Label(frame12,image=img3)
        panel4=tk.Label(frame12,image=img4)
        panel5=tk.Label(frame12,image=img5)
        panel6=tk.Label(frame12,image=img6)
        panel7=tk.Label(frame12,image=img7)
        panel8_1=tk.Label(frame12,image=img8)
        panel8_2=tk.Label(frame12,image=img8)

        panel9_1=tk.Label(frame12,image=img9)
        panel9_2=tk.Label(frame12,image=img9)


        
        try:
            l1=tk.Label(frame12,text=countrya.name + "\n" + property.name.replace(".csv","") +"\n" +\
                format((countrya.dictofattributes[property.name][0]),",") + "\n" +"worldrank:"+str(countrya.dictofattributes[property.name][1])+ "\n (of " + str(countrya.dictofattributes[property.name][2])+ " countries ranked)",font="Helvetica 25",wraplength=500 )
        except:
            l1=tk.Label(frame12,text=countrya.name + "\n" + property.name.replace(".csv","") +"\n" + "sorry no data",font="Helvetica 25" )
        
        try:
            l2=tk.Label(frame12,text=countryb.name + "\n" + property.name.replace(".csv","") +"\n" + format((countryb.dictofattributes[property.name][0]),",") + "\n" +"worldrank:"+str(countryb.dictofattributes[property.name][1])+ "\n (of " + str(countryb.dictofattributes[property.name][2])+ " countries ranked)",font="Helvetica 25",wraplength=500)
        except:
            traceback.print_exc()
            l2=tk.Label(frame12,text=countryb.name + "\n" + property.name.replace(".csv","") +"\n" + "sorry no data",font="Helvetica 25")
        
        killbutton=tk.Button(frame12,image=img7,command=kill_button,width=400,height=200)

        l1.grid(row=1,column=0)
        l2.grid(row=1,column=2)

        panel1.grid(row=0,column=0)
        panel2.grid(row=0,column=2)
        panel5.grid(row=0,column=1)
        killbutton.grid(row=2,column=1)


        if wl=="you win!":
            killbutton["image"]=img3
            killbutton["width"]=300
            killbutton["height"]=300
            #panel3.grid(row=2,column=1)
            
        if wl=="you loose!":
            killbutton["image"]=img4
            killbutton["width"]=300
            killbutton["height"]=300

        if wl=="no data":
            killbutton["image"]=img6
            killbutton["width"]=300
            killbutton["height"]=300
            

        if wl=="draw!":
            killbutton["image"]=img7
            killbutton["width"]=300
            killbutton["height"]=300
        
        if wl=="hard defeat!":
            killbutton["image"]=img10
            killbutton["width"]=300
            killbutton["height"]=300
            killbutton.configure(command=kill_guessed_correct)

        
        
        if additional_information:
            guessed_correct_button=tk.Button(frame12,text="guessed correct",font="Helvetica 30",command=kill_guessed_correct)
            guessed_correct_button.grid(row=3,column=1)
            try:
                wiki_summary_A_extra=countrya.dictofattributes[property.name][4]
                wiki_summary_B_extra=countryb.dictofattributes[property.name][4]
                wikiurl_A=countrya.dictofattributes[property.name][5]
                wikiurl_B=countryb.dictofattributes[property.name][5]
            except:
                traceback.print_exc()
                wiki_summary_A_extra=""
                wiki_summary_B_extra=""
                wikiurl_A=""
                wikiurl_B=""
            height=320
            try:
                
                urlA="pictures/attribute_pictures/" + property.name.replace(".csv","") + "/"+ countrya.dictofattributes[property.name][3] + ".jpg"
                try:
                    imgA=Image.open(urlA)
                except FileNotFoundError:
                    imgA=Image.open("pictures/no_image_available.png")
                w=float(imgA.width)
                h=float(imgA.height)
                imgA=ImageTk.PhotoImage(imgA.resize((int(height*w/h),int(height)),Image.LANCZOS))
                frame12.imgA=imgA
                panelA=tk.Label(frame12,image=imgA)
                panelA.grid(row=2,column=0)
                panelA_extra=tk.Label(frame12,text=countrya.dictofattributes[property.name][3],font="Helvetica 20",wraplength=500)
                panelA_extra.grid(row=3,column=0)
            except:
                traceback.print_exc()
            try:

                urlB="pictures/attribute_pictures/" + property.name.replace(".csv","") +"/" + countryb.dictofattributes[property.name][3] + ".jpg"
                try:
                    imgB=Image.open(urlB)
                except FileNotFoundError:
                    imgB=Image.open("pictures/no_image_available.png")
                w=float(imgB.width)
                h=float(imgB.height)
                imgB=ImageTk.PhotoImage(imgB.resize((int(height*w/h),int(height)),Image.LANCZOS))
                frame12.imgB=imgB
                
                
                
                panelB=tk.Label(frame12,image=imgB)
                
                panelB.grid(row=2,column=2)

                
                panelB_extra=tk.Label(frame12,text=countryb.dictofattributes[property.name][3],font="Helvetica 20",wraplength=500)
                
                panelB_extra.grid(row=3,column=2)
            except:
                traceback.print_exc()
            try:
                if countrya.dictofattributes[property.name][3]!=countrya.name:
                    if wikiurl_A=="":
                        self.search_string=countrya.dictofattributes[property.name][3]
                        self.search_string=wikipedia.search(self.search_string)[0]
                        print(self.search_string)
                        print(wikipedia.search(self.search_string)[0])
                        print(self.search_string)
                        wiki_url_A=wikipedia.page(self.search_string).url
                        print("hier kommt url")
                        print(type(wiki_url_A))
                        print(wiki_url_A)
                        wiki_summary_A=wikipedia.summary(self.search_string,sentences=2)
                    else:
                        wiki_url_A=wikiurl_A
                        wiki_summary_A=wiki_summary_A_extra
                
                    wiki_url_A_Label=tk.Label(frame12,text=wiki_url_A,fg="blue",cursor="hand2",font="Helvetica 15")
                    wiki_url_A_Label.bind("<Button-1>",lambda x: self.callback(wiki_url_A))

                    wiki_summary_A_Label=tk.Label(frame12,text=wiki_summary_A,wraplength=500,font="Helvetica 15")
                    wiki_summary_A_Label.grid(row=4,column=0)
                    wiki_url_A_Label.grid(row=5,column=0)
            except:
                traceback.print_exc()
            try:
                if countryb.dictofattributes[property.name][3]!=countryb.name:
                    if wikiurl_B=="":
                        self.search_string=countryb.dictofattributes[property.name][3]
                        self.search_string=wikipedia.search(self.search_string)[0]
                        print(self.search_string)
                        print(wikipedia.search(self.search_string)[0])
                        print(self.search_string)
                        wiki_url_B=wikipedia.page(self.search_string).url
                        print("hier kommt url")
                        print(type(wiki_url_B))
                        print(wiki_url_B)
                        wiki_summary_B=wikipedia.summary(self.search_string,sentences=2)
                        
                    else:
                        wiki_url_B=wikiurl_B
                        wiki_summary_B=wiki_summary_B_extra

                    wiki_url_B_Label=tk.Label(frame12,text=wiki_url_B,fg="blue",cursor="hand2",font="Helvetica 15",wraplength=500)
                    wiki_url_B_Label.bind("<Button-1>",lambda x: self.callback(wiki_url_B))
                    
                    wiki_summary_B_Label=tk.Label(frame12,text=wiki_summary_B,wraplength=500,font="Helvetica 15")
                    wiki_summary_B_Label.grid(row=4,column=2)
                    wiki_url_B_Label.grid(row=5,column=2)
            except:
                traceback.print_exc()



        try:
            countrya_top5=countrya.dictofattributes[property.name][1]<6
        except: countrya_top5=False

        try:
            countryb_top5=countryb.dictofattributes[property.name][1]<6
        except: countryb_top5=False

        try:
            countrya_worst5=countrya.dictofattributes[property.name][2]-countrya.dictofattributes[property.name][1] <6
        except:
            countrya_worst5=False
            
        try:
            countryb_worst5=countryb.dictofattributes[property.name][2]-countryb.dictofattributes[property.name][1] <6
        except:
            countryb_worst5=False  

        if countrya_top5:
            panel8_1.grid(row=6,column=0)

        if countryb_top5:
            panel8_2.grid(row=6,column=2)

        if countrya_worst5:
            panel9_1.grid(row=6,column=0)

        if countryb_worst5:
            panel9_2.grid(row=6,column=2)

        

    def endscreen(self,cause="numberofrounds",winner=None,gotcha_country=None):
        def _on_mousewheel(event):
            canvas21.yview_scroll(int(-1*(float(event.delta)/120)), "units")

        win2=tk.Toplevel()

        frame21=tk.Frame(win2)
        frame21.pack(fill="both",expand=True)
        canvas21=tk.Canvas(frame21)

        my_scrollbar12=tk.Scrollbar(frame21,orient="vertical",command=canvas21.yview)
        my_scrollbar12.pack(side="right",fill="y")
        my_scrollbar12.config(command=canvas21.yview)

        my_scrollbar13=tk.Scrollbar(frame21,orient="horizontal",command=canvas21.xview)
        my_scrollbar13.pack(side="bottom",fill="x")
        my_scrollbar13.config(command=canvas21.xview)
        canvas21.pack(side="left",expand=True,fill="both")

        win=tk.Frame(canvas21)
        canvas21.create_window((0,0),window=win,anchor="nw")
        win2.geometry("1650x825")
        win.bind(
            "<Configure>",
            lambda e: canvas21.configure(
                scrollregion=canvas21.bbox("all")
            )
        )
        canvas21.bind_all("<MouseWheel>",_on_mousewheel)


        if self.winningcondition=="get gold":
                a=sorted(self.list_of_players,key=lambda x: self.score(x.list_of_possessed_countries),reverse=True)
                self.shitdict=dict()
                for i in range (len(a)):
                    self.shitdict[i]=dict()
                    text=str(i+1) + ". place : " + a[i].name  + " with " +str(a[i].gold) +  " gold \n"
                    newframe=tk.Frame(win)
                    label1=tk.Label(newframe,text=text)
                    label1.config(font=("Helvetica", 20))
                    flagframe=tk.Frame(newframe)
                    for j in range(len(a[i].list_of_possessed_countries_gold)):
                        self.doubleframe=tk.Frame(flagframe)
                        flag=a[i].list_of_possessed_countries_gold[j].getresizedflag(100)
                        self.newlabel=tk.Label(self.doubleframe,image=flag)
                        countrylabel=tk.Label(self.doubleframe,text=a[i].list_of_possessed_countries_gold[j].name)
                        self.newlabel.pack(side="top")
                        countrylabel.pack(side="bottom")
                        self.shitdict[i][j]=flag
                        self.doubleframe.grid(row=0,column=j)
                    label1.grid(row=0,column=0)
                    flagframe.grid(row=1,column=0)
                    newframe.grid(row=i,column=0)
                self.d="disabled"
                self.showing_country_label["text"]="Congratulations, " + a[0].name
                self.showing_current_attribute_text_label["text"]="Congratulations, " + a[0].name 
                return None
        
        if self.winningcondition=="attribute":
            a=sorted(self.list_of_players,key=lambda x: sum(self.score(x.list_of_possessed_countries)),reverse=True)
            self.shitdict=dict()
            #sorting
            def bla(x):
                try:
                    return x.dictofattributes[self.endattribute.name][0]
                except: 
                    return -9999999.0
            for i in range (len(a)):
                if "higher is better" in self.endattribute.name:
                    a[i].list_of_possessed_countries=sorted(a[i].list_of_possessed_countries,key=lambda x: bla(x),reverse=True)
                else:
                    a[i].list_of_possessed_countries=sorted(a[i].list_of_possessed_countries,key=lambda x: bla(x))
            for i in range (len(a)):
                scorelist=self.score(a[i].list_of_possessed_countries)
                self.shitdict[i]=dict()
                text=str(i+1) + ". place : " + a[i].name  + " with " +str(round(sum(scorelist),2)) +  " points \n"
                newframe=tk.Frame(win)
                label1=tk.Label(newframe,text=text)
                label1.config(font=("Helvetica", 44))
                flagframe=tk.Frame(newframe,highlightbackground="green",highlightthickness=2)
                flagframe.grid_columnconfigure(0,weight=1)
                flagframe.grid_rowconfigure(0,weight=1)
                for j in range(len(a[i].list_of_possessed_countries)):
                        
                    self.doubleframe=tk.Frame(flagframe,highlightbackground="white",highlightthickness=2)
                    self.name_value_rank_frame=tk.Frame(self.doubleframe)
                    

                    flag=a[i].list_of_possessed_countries[j].getresizedflag(100)
                    
                    countryscorelabel=tk.Label(self.doubleframe,text=scorelist[j],font="Helvetica 30")
                    self.newlabel=tk.Label(self.doubleframe,image=flag)
                    country=a[i].list_of_possessed_countries[j]
                    if self.reversed_end_attribute==1:
                        country.dictofattributes[self.endattribute.name][1]=country.dictofattributes[self.endattribute.name][2]-country.dictofattributes[self.endattribute.name][1]


                    countrylabel=tk.Label(self.doubleframe,text=country.name,font="Helvetica 20")
                    self.newlabel.grid(row=0)
                    countryscorelabel.grid(row=1)
                    countrylabel.grid(row=2)
                    if self.endattribute.isActive:
                        try:
                            label_of_thing=tk.Label(self.name_value_rank_frame,text=str(country.dictofattributes[self.endattribute.name][3]),font="Helvetica 20")
                        except:
                            label_of_thing=tk.Label(self.name_value_rank_frame,text="--",font="Helvetica 20")
                        try:
                            width=200                            
                            urlA="pictures/attribute_pictures/" + self.endattribute.name.replace(".csv","") + "/"+ country.dictofattributes[self.endattribute.name][3] + ".jpg"
                            try:
                                imgA=Image.open(urlA)
                            except FileNotFoundError:
                                imgA=Image.open("pictures/no_image_available.png")
                            w=float(imgA.width)
                            h=float(imgA.height)
                            imgA=ImageTk.PhotoImage(imgA.resize((int(width),int(width*h/w)),Image.LANCZOS))
                            panelA=tk.Label(self.doubleframe,image=imgA)
                            panelA.imgA=imgA
                            panelA.grid(row=3)
                        except:
                            traceback.print_exc()
                        label_of_thing.grid(row=0)
                        label_of_value=tk.Label(self.name_value_rank_frame,text=format((country.dictofattributes[self.endattribute.name][0]),","),font="Helvetica 20")
                        label_of_value.grid(row=1)
                        label_of_worldrank=tk.Label(self.name_value_rank_frame,text="worldrank:" + str(country.dictofattributes[self.endattribute.name][1]),font="Helvetica 20")
                        label_of_worldrank.grid(row=2)
                        self.doubleframe.grid_rowconfigure(4,weight=1)
                        self.name_value_rank_frame.grid(row=4,sticky="s")
                    else:
                        label_of_value=tk.Label(self.doubleframe,text=format((country.dictofattributes[self.endattribute.name][0]),","),font="Helvetica 20")
                        label_of_value.grid(row=5,sticky="s")
                        label_of_worldrank=tk.Label(self.doubleframe,text="worldrank:" + str(country.dictofattributes[self.endattribute.name][1]),font="Helvetica 20")
                        label_of_worldrank.grid(row=6,sticky="s")


                    self.shitdict[i][j]=flag
                    self.doubleframe.grid(row=0,column=j,sticky="NS")
                label1.grid(row=0,column=0)
                flagframe.grid(row=1,column=0)
                newframe.grid(row=i,column=0)
            self.d="disabled"
            self.showing_country_label["text"]="Congratulations, " + a[0].name
            self.showing_current_attribute_text_label["text"]="Congratulations, " + a[0].name 
        
        if self.winningcondition=="number of countries":
            a=sorted(self.list_of_players,key=lambda x: float((len(x.list_of_possessed_countries)) +random.random()),reverse=True)
            self.shitdict=dict()
            for i in range (len(a)):
                self.shitdict[i]=dict()
                text=str(i+1) + ". place : " + a[i].name  + " with " +str(len(a[i].list_of_possessed_countries)) +  " countries \n"
                newframe=tk.Frame(win)
                label1=tk.Label(newframe,text=text)
                label1.config(font=("Helvetica", 44))
                flagframe=tk.Frame(newframe)
                for j in range(len(a[i].list_of_possessed_countries)):
                    self.doubleframe=tk.Frame(flagframe)
                    flag=a[i].list_of_possessed_countries[j].getresizedflag(100)
                    self.newlabel=tk.Label(self.doubleframe,image=flag)
                    countrylabel=tk.Label(self.doubleframe,text=a[i].list_of_possessed_countries[j].name)
                    self.newlabel.pack(side="top")
                    countrylabel.pack(side="bottom")
                    self.shitdict[i][j]=flag
                    self.doubleframe.grid(row=0,column=j)
                label1.grid(row=0,column=0)
                flagframe.grid(row=1,column=0)
                newframe.grid(row=i,column=0)
            self.d="disabled"
            self.showing_country_label["text"]="Congratulations, " + a[0].name
            self.showing_current_attribute_text_label["text"]="Congratulations, " + a[0].name 
        if cause=="twocountriesclaimed":
            text=""
            winner=self.targetcountry1.owner
            messagebox.showinfo(self.root,message="Congratulations " + winner + " you claimed both countries and therefore you are the winner")
            self.d="disabled"
            self.showing_country_label["text"]="Congratulations, " + winner
            self.showing_current_attribute_text_label["text"]="Congratulations, " + winner
        if self.winningcondition=="secret targets":
            a=sorted(self.list_of_players,key=lambda x: float((len(set(x.list_of_possessed_countries).intersection(set(self.dict_of_targets[x])))) +random.random()),reverse=True)
            self.shitdict=dict()
            for i in range (len(a)):
                self.shitdict[i]=dict()
                text=str(i+1) + ". place : " + a[i].name
                newframe=tk.Frame(win)
                label1=tk.Label(newframe,text=text)
                label1.config(font=("Helvetica", 44))
                flagframe=tk.Frame(newframe)
                for j in range(len(a[i].list_of_possessed_countries)):
                    if a[i].list_of_possessed_countries[j] in self.dict_of_targets[a[i]]:
                        self.doubleframe=tk.Frame(flagframe)
                        flag=a[i].list_of_possessed_countries[j].getresizedflag(100)
                        self.newlabel=tk.Label(self.doubleframe,image=flag)
                        countrylabel=tk.Label(self.doubleframe,text=a[i].list_of_possessed_countries[j].name)
                        self.newlabel.pack(side="top")
                        countrylabel.pack(side="bottom")
                        self.shitdict[i][j]=flag
                        self.doubleframe.grid(row=0,column=j)
                label1.grid(row=0,column=0)
                flagframe.grid(row=1,column=0)
                newframe.grid(row=i,column=0)
            self.d="disabled"
            self.showing_country_label["text"]="Congratulations, " + a[0].name
            self.showing_current_attribute_text_label["text"]="Congratulations, " + a[0].name
        if self.winningcondition=="secret attribute":
            text=""
            self.d="disabled"
            self.showing_country_label["text"]="Congratulations, " + winner.name
            self.showing_current_attribute_text_label["text"]="Congratulations, " + winner.name
            showing_winner_label=tk.Label(win,text="Congratulations, " + winner.name + "\nbecause " + gotcha_country.name + " is worldrank\n" + str(self.dict_of_targets[winner].index(gotcha_country)+1) + "\nin\n" + self.dict_of_target_attribute_name[winner] + "\nyou win the game!!!",font="Helvetivca 30")
            showing_winner_label.grid(row=0,column=0)

        
    def setupclaim2countries(self):
        Target=Player(realgrey,"Nobody")
        if self.choosingindex==len(self.list_of_players):
            self.targetcountry1=all_countries[random.randrange(1,len(all_countries))]
            self.targetcountry2=all_countries[random.randrange(1,len(all_countries))]
            if self.targetcountry1.name ==self.targetcountry2.name:
                self.targetcountry2=all_countries[random.randrange(1,len(all_countries))]
            self.claimcountry(Target,self.targetcountry1)
            print(self.targetcountry1.name)
            self.claimcountry(Target,self.targetcountry2)
    def setupgold(self):
        def get_good_ids(numberofgold):
            self.goldids=random.sample(range(len(all_countries)),numberofgold)
            for i in self.goldids:
                if all_countries[i].owner!="Nobody" or all_countries[i].name=="Unknown Country":
                    get_good_ids(numberofgold)
            return None
        for player in self.list_of_players:
            player.gold=0
        Target=Player(gold,"Nobody")
        self.numberofgold=len(all_countries)//20
        print(self.numberofgold)
        get_good_ids(self.numberofgold)
        for i in self.goldids:
            self.claimcountry(Target,all_countries[i])
            self.goldlist.append(all_countries[i])
            
    def getstartingattribute(self) -> Category:
        if self.pred_attribute_name!="Random":
            print(self.pred_attribute_name)
            attribute= dictionary_attribute_name_to_attribute[self.pred_attribute_name][0]
            
        else:
            numberofnodata=999999
            while numberofnodata >5:
                attribute=self.getrandomattribute_with_cluster()
                numberofnodata=0
                for country in all_countries:
                    try:
                        if isinstance(country.dictofattributes[attribute],list):
                            try:
                                i=country.dictofattributes[attribute][1]
                            except IndexError:
                                numberofnodata=numberofnodata+1
                        else:
                            numberofnodata=numberofnodata+1
                    except KeyError:
                        numberofnodata+=1
            if random.random()<0.5:

                text="The target attribute is " + attribute
                v=messagebox.showinfo(self.main,message=text)
                self.reversed_end_attribute=0
                
            else:
                self.reversed_end_attribute=1
                text="The target attribute is " + attribute + "\n REVERSED!!!"
                v=messagebox.showinfo(self.main,message=text)
        return attribute



    def setuppredattribute(self):
        self.endattribute=self.getstartingattribute()
        if True:
            self.grey_no_data()
    
    def grey_no_data(self):
        for country in all_countries:
            if country==Unknown_country:
                continue
            try:
                country.dictofattributes[self.endattribute.name][0]
            except:
                print(country.name)
                traceback.print_exc()
                self.claimcountry(No_Data_Body,country)

    
    def setup_secret_target_countries(self,numberoftargets:int):
        self.really_unknown=Unknown_country
        def checkcountrylist(list1):
            for country in list1:
                if country.owner!="Nobody" or country==self.really_unknown:
                    return False
            return True
        def roll_random_country(oldcountry):
            return all_countries[random.randrange(1,len(all_countries))]

        def show_targets(player:Player):
            self.no_targets_yetlist.remove(player)
            self.target_countries_frame=tk.Toplevel()
            targetlist=[Unknown_country]*numberoftargets
            while (not checkcountrylist(targetlist)):
                targetlist=[roll_random_country(item) for item in targetlist]

            welcomelabel=tk.Label(self.target_countries_frame,text="Welcome " + player.name + " those are your countries\n if you don't know where these are feel free to look at the map.",font="Helvetica 25")
            welcomelabel.grid(row=0,column=0,columnspan=len(targetlist))
            self.myimage=[0]*numberoftargets
            self.created_circles=list()
            for index,country in enumerate(targetlist):
                item=self.c.create_oval(country.wormholecoordinates[0]+20,country.wormholecoordinates[1]+20,country.wormholecoordinates[0]-20,country.wormholecoordinates[1]-20,width=3,outline="red")
                self.created_circles.append(item)
                newcountrylabel=tk.Label(self.target_countries_frame, text=country.name,font="Helvetica 25")
                newcountrylabel.grid(row=1,column=index)
                self.myimage[index]=country.getresizedflag(400)
                newlabel=tk.Label(self.target_countries_frame,image=self.myimage[index],pady=40)
                newlabel.grid(row=2,column=index)
                pass
            self.dict_of_targets[player]=targetlist
            self.got_targets_Button=tk.Button(self.target_countries_frame,text="got it",command=open_next_frame,font="Helvetica 25")
            self.got_targets_Button.grid(row=3,column=0,columnspan=len(targetlist)+2)

        def open_next_frame():
            for item in self.created_circles:
                self.c.delete(item)
            self.created_circles=[]
            self.target_countries_frame.destroy()
            if len(self.no_targets_yetlist)==0:
                return None
            show_targets(self.no_targets_yetlist[0])
        self.dict_of_targets=dict()
        self.no_targets_yetlist=self.list_of_players.copy()
        show_targets(self.active_player)


    def setup_secret_attribute(self,n):
        def find_top_n_countries(n,attribute):
            returnlist=list()
            for country in all_countries:
                try:
                    if country.dictofattributes[attribute][1]<=n:
                        returnlist.append(country)
                except KeyError:
                    continue
            returnlist.sort(key=lambda x: x.dictofattributes[attribute][1])
            return returnlist



        def open_next_frame():
            self.target_countries_frame.destroy()
            if len(self.no_targets_yetlist)==0:
                return None
            show_targets(self.no_targets_yetlist[0])
        
        def show_targets(player:Player):
            self.no_targets_yetlist.remove(player)
            self.target_countries_frame=tk.Toplevel()
            self.target_attribute=self.getrandomattribute_with_cluster()
            self.dict_of_target_attribute_name[player]=self.target_attribute
            welcomelabel=tk.Label(self.target_countries_frame,text="Welcome " + player.name + "your attribute is the following: \n\n" + self.target_attribute.rstrip(".csv") + "\n\nclaim one of the top " +str(n) + " countries in order to win the game" ,font="Helvetica 25")
            welcomelabel.grid(row=0,column=0)
            self.dict_of_targets[player]=find_top_n_countries(n,self.target_attribute)
            self.got_targets_Button=tk.Button(self.target_countries_frame,text="got it",command=open_next_frame,font="Helvetica 25")
            self.got_targets_Button.grid(row=3,column=0) 
       
        self.dict_of_target_attribute_name=dict()
        self.dict_of_targets=dict()
        self.no_targets_yetlist=self.list_of_players.copy()
        show_targets(self.active_player)



    def score(self,countrylist):
        def helphelp(number,list1):
            if self.higherorlower=="higher":
                return  sum([item<=number for item in list1])
            if self.higherorlower=="lower":
                return sum([item>=number for item in list1])
        
        higherorlower=""
        propertylist=list()
        mcountrylist=list()
        dlist=list()
        if self.reversed_end_attribute==0:
            if "higher is better" in self.endattribute.name:
                self.higherorlower="higher"
            else:
                self.higherorlower="lower"
        else:
            if "higher is better" in self.endattribute.name:
                self.higherorlower="lower"
            else:
                self.higherorlower="higher"

        for country in all_countries:
            try:
                if (country.dictofattributes[self.endattribute.name][0])!=float(-1):
                    propertylist.append((country.dictofattributes[self.endattribute.name][0]))            
                    mcountrylist.append(country)
                else: 
                    dlist.append(country)
            except KeyError:
                dlist.append(country)
        print(propertylist)
        returnlist=list()
        for country in countrylist:
            if country in dlist:
                returnlist.append(30.0)
            else:
                returnlist.append(helphelp(country.dictofattributes[self.endattribute.name][0],propertylist))
        returnlist=[float(item)/float(5) for item in returnlist]
        return returnlist        


    def checkifgameshouldend(self):
        if self.activeplayercounter==len(self.list_of_players)*self.numberofrounds-1:
            self.endscreen()
            return True
        if self.winningcondition=="claim 2 countries":
            if self.targetcountry1.owner!="Nobody" and self.targetcountry1.owner==self.targetcountry2.owner:
                self.endscreen(cause="twocountriesclaimed")
                return True
        if self.winningcondition=="get gold":
            if len(self.goldlist)==0:
                self.endscreen(cause="all gold left")
                return True
        if self.winningcondition=="secret targets":
            if set(self.dict_of_targets[self.active_player]).issubset(set(self.active_player.list_of_possessed_countries)):
                self.endscreen(cause="co")
                return True
        if self.winningcondition=="secret attribute":
            if len(set(self.dict_of_targets[self.active_player]).intersection(set(self.active_player.list_of_possessed_countries)))>=1:
                for country in self.active_player.list_of_possessed_countries:
                    if country in self.dict_of_targets[self.active_player]:
                        self.endscreen(cause="co",winner=self.active_player,gotcha_country=country)
                        break
                return True
        return False

    def setupgame(self):
        
        if self.wormholemode=="fixed starting wormholes":
            self.activate_wormholes(5)
        if self.wormholemode=="every round changing wormholes":
            self.activate_wormholes(3)

        if self.winningcondition=="claim 2 countries":
            self.setupclaim2countries()
        if self.winningcondition=="get gold":
            self.setupgold()
        if self.winningcondition=="attribute":
            self.setuppredattribute()
        if self.winningcondition=="secret targets":
            self.setup_secret_target_countries(self
            .numberoftargets)
        if self.winningcondition=="secret attribute":
            self.setup_secret_attribute(5)

    def scroll_start(self, event):
        self.c.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.c.scan_dragto(event.x, event.y, gain=1)

    def do_zoom(self,event):
        x = self.c.canvasx(event.x)
        y = self.c.canvasy(event.y)
        factor = 1.001 ** event.delta
        self.c.scale(ALL, x, y, factor, factor)





class IntroWindow :
    

    global im
    def __init__(self):

        
        
        self.i=0
        self.root=tk.Tk()
        self.startcountry=tk.StringVar()
        self.winningcondition=tk.StringVar()
        self.wormholeoption=tk.StringVar()
        self.listofplayers=list()
        pred_choose_var=tk.StringVar(self.root)
        pred_choose_var.set("Random")
        self.current_var=tk.StringVar()
        self.current_var.set("Random")

        self.showinglabel=tk.Label(self.root,text="Welcome to the Geo-Game,\n please choose your names and colors")
        self.showinglabel.grid(row=0,column=0)



        #middle side
        self.nameentry=tk.Entry(self.root,text="Your name")
        self.nameentry.grid(row=1,column=0)

        choosecolorbutton=tk.Button(self.root,text="Choose your color",command=self.choose_color)
        choosecolorbutton.grid(row=2,column=0)

        gogobutton=tk.Button(self.root,text="Let's go",command=self.gogo)
        gogobutton.grid(row=9,column=0)

        self.currentplayerslistbox=tk.Listbox(self.root,height=4)
        self.currentplayerslistbox.grid(row=4,column=0)

        self.label2=tk.Label(self.root,text="How many rounds do you want to play")
        self.label2.grid(row=5,column=0)

        self.label3=tk.Label(self.root,text="Current participating players:")
        self.label3.grid(row=3,column=0)

        self.numberofroundsentry=tk.Entry(self.root)
        self.numberofroundsentry.grid(row=6,column=0,)




        # right side
        self.label4=tk.Label(self.root,text="Some (advanced) options")
        self.label4.grid(row=0,column=1)

        self.label5=tk.Label(self.root,text="Starting countries")
        self.label5.grid(row=1,column=1)

        self.startcountryoptions1=tk.Radiobutton(self.root,text="Random",variable=self.startcountry,value="random")
        self.startcountryoptions1.grid(row=2,column=1)

        self.startcountryoptions2=tk.Radiobutton(self.root,text="Choose",variable=self.startcountry,value="choose")
        self.startcountryoptions2.grid(row=3,column=1)

        self.startcountry.set("random")
        
        self.winconditionframe=tk.Frame(self.root)


        self.label6=tk.Label(self.winconditionframe,text="Winning condition")
        self.label6.grid(row=0,column=0)

        self.winningconditionoption1=tk.Radiobutton(self.winconditionframe,text="Number of countries",variable=self.winningcondition,value="number of countries")
        self.winningconditionoption1.grid(row=1,column=0,sticky="w",padx=60)

        self.winningconditionoption2=tk.Radiobutton(self.winconditionframe,text="Hold 2 countries to win",variable=self.winningcondition,value="claim 2 countries")
        self.winningconditionoption2.grid(row=2,column=0,sticky="w",padx=60)

        self.winningconditionoption3=tk.Radiobutton(self.winconditionframe,text="Claim at first the golden countries",variable=self.winningcondition,value="get gold")
        self.winningconditionoption3.grid(row=3,column=0,sticky="w",padx=60)

        self.winningconditionoption4=tk.Radiobutton(self.winconditionframe,text="Claim countries according to a predeterminded attribute",variable=self.winningcondition,value="attribute",command=self.show_option_for_pred_attribute)
        self.winningconditionoption4.grid(row=4,column=0,sticky="w",padx=60)

        self.winningconditionoption5=tk.Radiobutton(self.winconditionframe,text="Secret targets",variable=self.winningcondition,value="secret targets")
        self.winningconditionoption5.grid(row=7,column=0,sticky="w",padx=60)

        self.winningconditionoption6=tk.Radiobutton(self.winconditionframe,text="Secret attribute",variable=self.winningcondition,value="secret attribute")
        self.winningconditionoption6.grid(row=8,column=0,sticky="w",padx=60)


        self.winningcondition.set("number of countries")


        self.winconditionframe.grid(row=4,column=1,padx=60)


        #far right side
        self.africavar=tk.IntVar()
        self.north_americavar=tk.IntVar()
        self.middle_americavar=tk.IntVar()
        self.south_americavar=tk.IntVar()
        self.asiavar=tk.IntVar()
        self.europevar=tk.IntVar()
        self.oceaniavar=tk.IntVar()



        self.farrightframe=tk.Frame(self.root)

        self.label7=tk.Label(self.farrightframe,text="Which continents would you like to play?")
        self.label7.grid(row=0,column=0,)

        self.africa_check=tk.Checkbutton(self.farrightframe,text="Africa",variable=self.africavar)
        self.africa_check.grid(row=1,column=0,sticky="W")
        self.africa_check.select()

        self.north_america_check=tk.Checkbutton(self.farrightframe,text="North America",variable=self.north_americavar)
        self.north_america_check.grid(row=2,column=0,sticky="W")
        self.north_america_check.select()

        self.middle_america_check=tk.Checkbutton(self.farrightframe,text="Middle America",variable=self.middle_americavar)
        self.middle_america_check.grid(row=3,column=0,sticky="W")
        self.middle_america_check.select()

        self.south_america_check=tk.Checkbutton(self.farrightframe,text="South America",variable=self.south_americavar)
        self.south_america_check.grid(row=4,column=0,sticky="W")
        self.south_america_check.select()

        self.asia_check=tk.Checkbutton(self.farrightframe,text="Asia",variable=self.asiavar)
        self.asia_check.grid(row=5,column=0,sticky="W")
        self.asia_check.select()

        self.europe_check=tk.Checkbutton(self.farrightframe,text="Europe",variable=self.europevar)
        self.europe_check.grid(row=6,column=0,sticky="W")
        self.europe_check.select()

        self.oceania_check=tk.Checkbutton(self.farrightframe,text="Oceania",variable=self.oceaniavar)
        self.oceania_check.grid(row=7,column=0,sticky="W")
        self.oceania_check.select()
        self.farrightframe.grid(row=0,column=2,rowspan=8)
        
        self.wormhole_optionsframe=tk.Frame(self.root)

        self.wormhole_optionslabel=tk.Label(self.wormhole_optionsframe,text="Wormhole options")
        self.no_wormholes=tk.Radiobutton(self.wormhole_optionsframe,text="No wormholes at all",variable=self.wormholeoption,value="no wormholes at all")
        self.fixed_wormholes=tk.Radiobutton(self.wormhole_optionsframe,text="Fixed starting wormholes",variable=self.wormholeoption,value="fixed starting wormholes")
        self.every_round_changing_wormholes=tk.Radiobutton(self.wormhole_optionsframe,text="Every round changing wormholes",variable=self.wormholeoption,value="every round changing wormholes")
        self.from_your_side_changing_wormholes=tk.Radiobutton(self.wormhole_optionsframe,variable=self.wormholeoption,text="Every round changing wormholes from your countries",value="every round changing wormholes from your countries")

        self.wormholeoption.set("no wormholes at all")

        self.wormhole_optionslabel.grid(row=0,column=0)
        self.no_wormholes.grid(row=1,column=0,sticky="w")
        self.fixed_wormholes.grid(row=2,column=0,sticky="w")
        self.every_round_changing_wormholes.grid(row=3,column=0,sticky="w")
        self.from_your_side_changing_wormholes.grid(row=4,column=0,sticky="w")

        self.wormhole_optionsframe.grid(row=0,column=3,rowspan=5)


        self.peacemode_var=tk.IntVar()
        self.peacemode_check=tk.Checkbutton(self.root,text="Peace Mode",variable=self.peacemode_var)
        self.peacemode_check.grid(row=5,column=3)
        
        #variable for setting whether the final attribute will be reversed, if we play the random attribute mode
        self.reverse_yes_or_novar=tk.IntVar()
        self.reverse_yes_or_novar.set(0)


        self.root.mainloop()



    def choose_color(self):
        if self.nameentry.get()=="":
            return None
        playercolor=colorchooser.askcolor(title="choose your color")
        name=self.nameentry.get()
        self.nameentry.delete(0,"end")
        self.listofplayers.append(Player(color=playercolor[0],name=name))
        self.currentplayerslistbox.insert(self.i,name)
        self.i=self.i+1

    

    def show_option_for_pred_attribute(self):
        def roll_attribute():
            rng=random.randrange(1,len(self.displayed_list))
            print(rng)
            self.choose_pred_attribute.current(rng)
            if random.random() <=0.5:
                self.reverse_yes_or_no.select()
                self.reverse_yes_or_novar.set(1)
            else:
                self.reverse_yes_or_novar.set(0)
                self.reverse_yes_or_no.deselect()



        pred_choose_var=tk.StringVar(self.winconditionframe)
        pred_choose_var.set("Random")
        self.displayed_list=[c.name for c in all_categories]
        self.displayed_list.sort()
        self.displayed_list=["Surprise Me!"] + self.displayed_list
        self.displayed_list=[m.rstrip(".csv") for m in self.displayed_list]
        self.current_var=tk.StringVar()
        self.choose_pred_attribute=ttk.Combobox(self.winconditionframe,values=self.displayed_list,width=100,state="readonly",textvariable=self.current_var)
        self.choose_pred_attribute.current(0)
        self.choose_pred_attribute.grid(row=5,column=0,)

        

        self.reverse_yes_or_no=tk.Checkbutton(self.winconditionframe,text="Reverse?",variable=self.reverse_yes_or_novar)
        self.reverse_yes_or_no.grid(row=6,column=0,padx=60)

        self.roll_button=tk.Button(self.winconditionframe,text="Randomize!",command=roll_attribute)
        self.roll_button.grid(row=5,column=1,sticky="w")
    def gogo(self):
        global all_countries
        global preallCountries
        self.activecontinents=list()
        if self.africavar.get()==1:
            self.activecontinents.append("Africa")
        if self.asiavar.get()==1:
            self.activecontinents.append("Asia")
        if self.europevar.get()==1:
            self.activecontinents.append("Europe")
        if self.north_americavar.get()==1:
            self.activecontinents.append("North America")
        if self.middle_americavar.get()==1:
            self.activecontinents.append("Middle America")
        if self.south_americavar.get()==1:
            self.activecontinents.append("South America")
        if self.oceaniavar.get()==1:
            self.activecontinents.append("Oceania")


        for country in preallCountries:
            if country.continent in self.activecontinents:
                all_countries.append(country)
        all_countries.append(Unknown_country)
        self.numberofrounds=self.numberofroundsentry.get()

        for country in all_countries:
            name=country.name
            countrynamelist.append(name)

        for acountry in all_countries:
            try:
                if acountry==Unknown_country:
                    continue
                data=neighboring_countries[neighboring_countries[0]==acountry.name]
                for bcountry in all_countries:
                    if bcountry==Unknown_country:
                        continue
                    if bcountry.name in data.iat[0,5]:
                        bcountry.neighboringcountries.append(acountry.name)
            except: 
                continue

        for country in all_countries:
            try:
                country.dictofattributes=mypropertydict[country.name]
            except:
                pass

        if len(self.listofplayers)==0:
            return None

        for player in allPlayers.values():
            try:
                player.rerolls_left=int(self.numberofroundsentry.get())//3
            except ValueError:
                player.rerolls_left=3


        self.root.destroy()
        if self.numberofrounds=="":
            MainWindow(bild=im,listofplayers=self.listofplayers,startingcountries=self.startcountry.get(),winningcondition=self.winningcondition.get(),pred_attribute=self.current_var.get() +".csv",wormholemode=self.wormholeoption.get(),peacemode=self.peacemode_var.get(),reversed_end_attribute=self.reverse_yes_or_novar.get())
        else:
            MainWindow(bild=im,listofplayers=self.listofplayers,startingcountries=self.startcountry.get(),numberofrounds=int(self.numberofrounds),winningcondition=self.winningcondition.get(),pred_attribute=self.current_var.get()+".csv",wormholemode=self.wormholeoption.get(),peacemode=self.peacemode_var.get(),reversed_end_attribute=self.reverse_yes_or_novar.get())









# #Europe
# Iceland=Country(xcoordinate=[1455],ycoordinate=[433],name="Iceland",continent="Europe")
# United_Kingdom=Country(xcoordinate=[1627],ycoordinate=[568],name="United Kingdom",continent="Europe")
# Ireland=Country(xcoordinate=[1570],ycoordinate=[560],name="Ireland",continent="Europe")
# Norway=Country(xcoordinate=[1735,1877,1818,1775,1828],ycoordinate=[475,379,275,273,384],name="Norway",continent="Europe")
# Sweden=Country(xcoordinate=[1790],ycoordinate=[470],name="Sweden",continent="Europe")
# Finland=Country(xcoordinate=[1900],ycoordinate=[450],name="Finland",continent="Europe")
# Spain=Country(xcoordinate=[1600],ycoordinate=[700],name="Spain",continent="Europe")
# Portugal=Country(xcoordinate=[1560],ycoordinate=[715],name="Portugal",continent="Europe")
# France=Country(xcoordinate=[1667],ycoordinate=[622],name="France",continent="Europe")
# Switzerland=Country(xcoordinate=[1715],ycoordinate=[632],name="Switzerland",continent="Europe")
# Belgium=Country(xcoordinate=[1690],ycoordinate=[590],name="Belgium",continent="Europe")
# Netherlands=Country(xcoordinate=[1692],ycoordinate=[574],name="Netherlands",continent="Europe")
# Germany=Country(xcoordinate=[1738],ycoordinate=[583],name="Germany",continent="Europe")    
# Denmark=Country(xcoordinate=[1730,1300],ycoordinate=[530,300],name="Denmark",continent="Europe")
# Austria=Country(xcoordinate=[1780],ycoordinate=[620],name="Austria",continent="Europe")
# Czech_Republic=Country(xcoordinate=[1780],ycoordinate=[600],name="Czech Republic",continent="Europe")
# Poland=Country(xcoordinate=[1830],ycoordinate=[570],name="Poland",continent="Europe")
# Slovakia=Country(xcoordinate=[1825],ycoordinate=[610] ,name="Slovakia",continent="Europe")
# Hungary=Country(xcoordinate=[1825],ycoordinate=[630],name="Hungary",continent="Europe")
# Slovenia=Country(xcoordinate=[1785],ycoordinate=[640],name="Slovenia",continent="Europe")
# Croatia=Country(xcoordinate=[1800],ycoordinate=[640],name="Croatia",continent="Europe")
# Serbia=Country(xcoordinate=[1845],ycoordinate=[660],name="Serbia",continent="Europe")
# Bosnia_and_Herzegovina=Country(xcoordinate=[1815],ycoordinate=[669],name="Bosnia and Herzegovina",continent="Europe")
# Albania=Country(xcoordinate=[1838],ycoordinate=[700],name="Albania")
# North_Macedonia=Country(xcoordinate=[1850],ycoordinate=[690],name="North Macedonia",continent="Europe")
# Bulgaria=Country(xcoordinate=[1885],ycoordinate=[680],name="Bulgaria",continent="Europe")
# Romania=Country(xcoordinate=[1880],ycoordinate=[640],name="Romania",continent="Europe")
# Moldova=Country(xcoordinate=[1920],ycoordinate=[625],name="Moldova",continent="Europe")
# Ukraine=Country(xcoordinate=[1920,1929],ycoordinate=[600,643],name="Ukraine",continent="Europe")
# Belarus=Country(xcoordinate=[1910],ycoordinate=[560],name="Belarus",continent="Europe")
# Greece=Country(xcoordinate=[1855,1858],ycoordinate=[715,737],name="Greece",continent="Europe")
# Lithuania=Country(xcoordinate=[1875],ycoordinate=[535],name="Lithuania",continent="Europe")
# Latvia=Country(xcoordinate=[1890],ycoordinate=[520],name="Latvia",continent="Europe")
# Estonia=Country(xcoordinate=[1900],ycoordinate=[500],name="Estonia",continent="Europe")
# Italy=Country(xcoordinate=[1751,1728,1782],ycoordinate=[663,708,735],name="Italy",continent="Europe")
# Luxembourg=Country(xcoordinate=[1700],ycoordinate=[600],name="Luxembourg",continent="Europe")
# Cyprus=Country(xcoordinate=[1964],ycoordinate=[764],name="Cyprus",continent="Europe")
# Montenegro=Country(xcoordinate=[1827],ycoordinate=[677],name="Montenegro",continent="Europe")



# #Asia and Middle East
# Turkey=Country(xcoordinate=[2000,1909],ycoordinate=[715,692],name="Turkey",continent="Asia")
# Georgia=Country(xcoordinate=[2060],ycoordinate=[685],name="Georgia",continent="Asia")
# Armenia=Country(xcoordinate=[2080],ycoordinate=[700],name="Armenia",continent="Asia")
# Azerbaijan=Country(xcoordinate=[2110],ycoordinate=[700],name="Azerbaijan",continent="Asia")
# Syria=Country(xcoordinate=[2020],ycoordinate=[770],name="Syria",continent="Asia")
# Iraq=Country(xcoordinate=[2070],ycoordinate=[780],name="Iraq",continent="Asia")
# Jordan=Country(xcoordinate=[2000],ycoordinate=[810],name="Jordan",continent="Asia")
# Saudi_Arabia=Country(xcoordinate=[2050],ycoordinate=[888],name="Saudi Arabia",continent="Asia")
# United_Arab_Emirates=Country(xcoordinate=[2165],ycoordinate=[894],name="United Arab Emirates",continent="Asia")
# Qatar=Country(xcoordinate=[2143],ycoordinate=[873],name="Qatar",continent="Asia")
# Bahrain=Country(xcoordinate=[2130],ycoordinate=[860],name="Bahrain",continent="Asia")
# Israel=Country(xcoordinate=[1982],ycoordinate=[808],name="Israel",continent="Asia")
# Lebanon=Country(xcoordinate=[1994],ycoordinate=[776],name="Lebanon",continent="Asia")
# Maldives=Country(xcoordinate=[2354],ycoordinate=[1116],name="Maldives",continent="Asia")
# Brunei=Country(xcoordinate=[2762],ycoordinate=[1109],name="Brunei",continent="Asia")
# Singapore=Country(xcoordinate=[2658],ycoordinate=[1139],name="Singapore",continent="Asia")
# Sri_Lanka=Country(xcoordinate=[2431],ycoordinate=[1073],name="Sri Lanka",continent="Asia")

# Oman=Country(xcoordinate=[2195],ycoordinate=[920],name="Oman",continent="Asia")
# Yemen=Country(xcoordinate=[2110],ycoordinate=[980],name="Yemen",continent="Asia")
# Iran=Country(xcoordinate=[2160],ycoordinate=[780],name="Iran",continent="Asia")
# Kuwait=Country(xcoordinate=[2107],ycoordinate=[827],name="Kuwait",continent="Asia")
# Russia=Country(xcoordinate=[2130,1854,3037,1974,3033],ycoordinate=[500,543,595,650,635],name="Russia",continent="Asia")
# Kazakhstan=Country(xcoordinate=[2260],ycoordinate=[630],name="Kazakhstan",continent="Asia")
# Uzbekistan=Country(xcoordinate=[2265,2341,2323],ycoordinate=[689,700,695],name="Uzbekistan",continent="Asia")
# Turkmenistan=Country(xcoordinate=[2200],ycoordinate=[715],name="Turkmenistan",continent="Asia")
# Afghanistan=Country(xcoordinate=[2275],ycoordinate=[780],name="Afghanistan",continent="Asia")
# Pakistan=Country(xcoordinate=[2300],ycoordinate=[830],name="Pakistan",continent="Asia")
# India=Country(xcoordinate=[2400,2555,2505,2536],ycoordinate=[900,866,851,891],name="India",continent="Asia")
# Kyrgyzstan=Country(xcoordinate=[2375],ycoordinate=[690],name="Kyrgyzstan",continent="Asia")
# Tajikistan=Country(xcoordinate=[2350],ycoordinate=[723],name="Tajikistan",continent="Asia")
# Nepal=Country(xcoordinate=[2450],ycoordinate=[836],name="Nepal",continent="Asia")
# Bhutan=Country(xcoordinate=[2522],ycoordinate=[849],name="Bhutan",continent="Asia")
# China=Country(xcoordinate=[2517,2714],ycoordinate=[821,938],name="China",continent="Asia")
# Mongolia=Country(xcoordinate=[2630],ycoordinate=[640],name="Mongolia",continent="Asia")
# Myanmar=Country(xcoordinate=[2580,2541],ycoordinate=[920,906],name="Myanmar",continent="Asia")
# Thailand=Country(xcoordinate=[2630,2610],ycoordinate=[985,1062],name="Thailand",continent="Asia")
# Cambodia=Country(xcoordinate=[2660],ycoordinate=[1000],name="Cambodia",continent="Asia")
# Laos=Country(xcoordinate=[2640],ycoordinate=[935],name="Laos",continent="Asia")
# Bangladesh=Country(xcoordinate=[2519],ycoordinate=[881],name="Bangladesh",continent="Asia")
# Malaysia=Country(xcoordinate=[2640,2757,2783],ycoordinate=[1110,1120,1096],name="Malaysia",continent="Asia")
# Vietnam=Country(xcoordinate=[2670,2699],ycoordinate=[918,1014],name="Vietnam",continent="Asia")
# North_Korea=Country(xcoordinate=[2877],ycoordinate=[707],name="North Korea",continent="Asia")
# South_Korea=Country(xcoordinate=[2890],ycoordinate=[759],name="South Korea",continent="Asia")
# Japan=Country(xcoordinate=[3036,2998,2942,2922],ycoordinate=[672,747,783,793],name="Japan",continent="Asia")

# #North America
# United_States=Country(xcoordinate=[150,700],ycoordinate=[415,700],name="United States",continent="North America")
# Canada=Country(xcoordinate=[500,1024,1089],ycoordinate=[500,652,610],name="Canada",continent="North America")


# #Oceania
# Philippines=Country(xcoordinate=[2826,2847,2823,2836,2841,2844,2862,2862,2854,2847],ycoordinate=[975,1004,1011,1030,1047,1066,1070,1020,1020,1005],name="Philippines",continent="Oceania")
# Indonesia=Country(xcoordinate=[2633,2689,2757,2818,2827,2936,2985],ycoordinate=[1167,1233,1162,1179,1146,1172,1196],name="Indonesia",continent="Oceania")
# Papua_New_Guinea=Country(xcoordinate=[3047],ycoordinate=[1219],name="Papua New Guinea",continent="Oceania")
# Australia=Country(xcoordinate=[2980,3072],ycoordinate=[1441,1627],name="Australia",continent="Oceania")
# New_Zealand=Country(xcoordinate=[3300,3330,3339,3358],ycoordinate=[1661,1625,1553,1600],name="New Zealand",continent="Oceania")
# Timor_Leste=Country(xcoordinate=[2870],ycoordinate=[1254],name="Timor-Leste",continent="Oceania")


# #Africa
# Morocco=Country(xcoordinate=[1575],ycoordinate=[800],name="Morocco",continent="Africa")
# Algeria=Country(xcoordinate=[1676],ycoordinate=[830],name="Algeria",continent="Africa")
# Tunisia=Country(xcoordinate=[1730],ycoordinate=[775],name="Tunisia",continent="Africa")
# Libya=Country(xcoordinate=[1800],ycoordinate=[850],name="Libya",continent="Africa")
# Egypt=Country(xcoordinate=[1930],ycoordinate=[850],name="Egypt",continent="Africa")
# Morocco=Country(xcoordinate=[1950],ycoordinate=[1000],name="Sudan",continent="Africa")
# Chad=Country(xcoordinate=[1830],ycoordinate=[980],name="Chad",continent="Africa")
# Niger=Country(xcoordinate=[1750],ycoordinate=[970],name="Niger",continent="Africa")
# Mali=Country(xcoordinate=[1630],ycoordinate=[950],name="Mali",continent="Africa")
# Mauritania=Country(xcoordinate=[1550],ycoordinate=[930],name="Mauritania",continent="Africa")
# # Western_Sahara=Country(xcoordinate=[1510],ycoordinate=[880],name="Western Sahara",continent="Africa")
# Senegal=Country(xcoordinate=[1500],ycoordinate=[990],name="Senegal",continent="Africa")
# Guinea_Bissau=Country(xcoordinate=[1498],ycoordinate=[1019],name="Guinea-Bissau",continent="Africa")
# Guinea=Country(xcoordinate=[1520],ycoordinate=[1030],name="Guinea",continent="Africa")
# Sierra_Leone=Country(xcoordinate=[1525],ycoordinate=[1060],name="Sierra Leone",continent="Africa")
# Liberia=Country(xcoordinate=[1550],ycoordinate=[1085],name="Liberia",continent="Africa")
# Ivory_Coast=Country(xcoordinate=[1590],ycoordinate=[1070],name="Ivory Coast",continent="Africa")
# Ghana=Country(xcoordinate=[1630],ycoordinate=[1070],name="Ghana",continent="Africa")
# Burkina_Faso=Country(xcoordinate=[1622],ycoordinate=[1015],name="Burkina Faso",continent="Africa")
# Togo=Country(xcoordinate=[1652],ycoordinate=[1057],name="Togo",continent="Africa")
# Benin=Country(xcoordinate=[1665],ycoordinate=[1040],name="Benin",continent="Africa")
# Nigeria=Country(xcoordinate=[1715],ycoordinate=[1055],name="Nigeria",continent="Africa")
# Cameroon=Country(xcoordinate=[1762],ycoordinate=[1100],name="Cameroon",continent="Africa")
# Central_African_Republic=Country(xcoordinate=[1850],ycoordinate=[1080],name="Central African Republic",continent="Africa")
# Ethiopia=Country(xcoordinate=[2020],ycoordinate=[1050],name="Ethiopia",continent="Africa")
# Eritrea=Country(xcoordinate=[2015],ycoordinate=[978],name="Eritrea",continent="Africa")
# # Djibouti=Country(xcoordinate=[2053],ycoordinate=[1027],name="Djibouti",continent="Africa")
# Somalia=Country(xcoordinate=[2118],ycoordinate=[1048],name="Somalia",continent="Africa")
# Kenya=Country(xcoordinate=[2009],ycoordinate=[1150],name="Kenya",continent="Africa")
# Uganda=Country(xcoordinate=[1955],ycoordinate=[1140],name="Uganda",continent="Africa")
# Rwanda=Country(xcoordinate=[1932],ycoordinate=[1177],name="Rwanda",continent="Africa")
# Burundi=Country(xcoordinate=[1933],ycoordinate=[1195],name="Burundi",continent="Africa")
# DR_Congo=Country(xcoordinate=[1867],ycoordinate=[1190],name="Democratic Republic of the Congo",continent="Africa")
# Republic_of_the_Congo=Country(xcoordinate=[1800],ycoordinate=[1160],name="Republic of the Congo",continent="Africa")
# Gabon=Country(xcoordinate=[1755],ycoordinate=[1160],name="Gabon",continent="Africa")
# Angola=Country(xcoordinate=[1800],ycoordinate=[1300],name="Angola",continent="Africa")
# Zambia=Country(xcoordinate=[1925],ycoordinate=[1318],name="Zambia",continent="Africa")
# Mozambique=Country(xcoordinate=[1980],ycoordinate=[1360],name="Mozambique",continent="Africa")
# Malawi=Country(xcoordinate=[1972],ycoordinate=[1307],name="Malawi",continent="Africa")
# Zimbabwe=Country(xcoordinate=[1930],ycoordinate=[1370],name="Zimbabwe",continent="Africa")
# Namibia=Country(xcoordinate=[1803,1873],ycoordinate=[1387,1357],name="Namibia",continent="Africa")
# Botswana=Country(xcoordinate=[1872],ycoordinate=[1400],name="Botswana",continent="Africa")
# South_Africa=Country(xcoordinate=[1870],ycoordinate=[1500],name="South Africa",continent="Africa")
# Madagascar=Country(xcoordinate=[2100],ycoordinate=[1386],name="Madagascar",continent="Africa")
# Lesotho=Country(xcoordinate=[1917],ycoordinate=[1487],name="Lesotho",continent="Africa")
# Eswatini=Country(xcoordinate=[1950],ycoordinate=[1455],name="Eswatini",continent="Africa")
# Tanzania=Country(xcoordinate=[1982],ycoordinate=[1232],name="Tanzania",continent="Africa")
# Gambia=Country(xcoordinate=[1495],ycoordinate=[1007],name="Gambia",continent="Africa")
# Equatorial_Guinea=Country(xcoordinate=[1745],ycoordinate=[1140],name="Equatorial Guinea",continent="Africa")



# #Middle America
# Mexico=Country(xcoordinate=[645],ycoordinate=[915],name="Mexico",continent="Middle America")
# Guatemala=Country(xcoordinate=[757],ycoordinate=[986],name="Guatemala",continent="Middle America")
# Belize=Country(xcoordinate=[777],ycoordinate=[963],name="Belize",continent="Middle America")
# Cuba=Country(xcoordinate=[883],ycoordinate=[918],name="Cuba",continent="Middle America")
# Haiti=Country(xcoordinate=[936],ycoordinate=[940],name="Haiti",continent="Middle America")
# Dominican_Republic=Country(xcoordinate=[949],ycoordinate=[944],name="Dominican Republic",continent="Middle America")
# El_Salvador=Country(xcoordinate=[773],ycoordinate=[1002],name="El Salvador",continent="Middle America")
# Honduras=Country(xcoordinate=[793],ycoordinate=[991],name="Honduras",continent="Middle America")
# Nicaragua=Country(xcoordinate=[810],ycoordinate=[1015],name="Nicaragua",continent="Middle America")
# Costa_Rica=Country(xcoordinate=[820],ycoordinate=[1043],name="Costa Rica",continent="Middle America")
# Panama=Country(xcoordinate=[851,878],ycoordinate=[1063,1057],name="Panama",continent="Middle America")


# #South America
# Colombia=Country(xcoordinate=[926],ycoordinate=[1113],name="Colombia",continent="South America")
# Venezuela=Country(xcoordinate=[1000],ycoordinate=[1070],name="Venezuela",continent="South America")
# Suriname=Country(xcoordinate=[1095],ycoordinate=[1106],name="Suriname",continent="South America")
# Guyana=Country(xcoordinate=[1064],ycoordinate=[1093],name="Guyana",continent="South America")
# Ecuador=Country(xcoordinate=[880],ycoordinate=[1170],name="Ecuador",continent="South America")
# Peru=Country(xcoordinate=[900],ycoordinate=[1265],name="Peru",continent="South America")
# Brazil=Country(xcoordinate=[1100,1155],ycoordinate=[1250,1165],name="Brazil",continent="South America")
# Bolivia=Country(xcoordinate=[1000],ycoordinate=[1350],name="Bolivia",continent="South America")
# Chile=Country(xcoordinate=[966,930,926,946,965],ycoordinate=[1420,1684,1729,1742,1756],name="Chile",continent="South America")
# Argentina=Country(xcoordinate=[1000,979],ycoordinate=[1550,1765],name="Argentina",continent="South America")
# Paraguay=Country(xcoordinate=[1065],ycoordinate=[1410],name="Paraguay",continent="South America")
# Uruguay=Country(xcoordinate=[1090],ycoordinate=[1525],name="Uruguay",continent="South America")


#Micro
Gambia=Country(xcoordinate=[5081],ycoordinate=[3264],name="Gambia",continent="Africa")
Djibouti=Country(xcoordinate=[7535],ycoordinate=[3345],name="Djibouti",continent="Africa")
Timor_Leste=Country(xcoordinate=[11113],ycoordinate=[4347],name="Timor-Leste",continent="Oceania")
Luxembourg=Country(xcoordinate=[6011],ycoordinate=[1506],name="Luxembourg",continent="Europe")
Cyprus=Country(xcoordinate=[7090],ycoordinate=[2211],name="Cyprus",continent="Europe")
Qatar=Country(xcoordinate=[7863],ycoordinate=[2684],name="Qatar",continent="Asia")
Bahrain=Country(xcoordinate=[7805],ycoordinate=[2607],name="Bahrain",continent="Asia")
Maldives=Country(xcoordinate=[8750],ycoordinate=[4009],name="Maldives",continent="Asia")
Brunei=Country(xcoordinate=[10662],ycoordinate=[3682],name="Brunei",continent="Asia")
Singapore=Country(xcoordinate=[10197],ycoordinate=[3847],name="Singapore",continent="Asia")
Lebanon=Country(xcoordinate=[7207],ycoordinate=[2267],name="Lebanon",continent="Asia")
Bahamas=Country(xcoordinate=[2474],ycoordinate=[2733],name="Bahamas",continent="Middle America")
Jamaica=Country(xcoordinate=[2465],ycoordinate=[3043],name="Jamaica",continent="Middle America")
Trinidad_and_Tobago=Country(xcoordinate=[3108],ycoordinate=[3424],name="Trinidad and Tobago",continent="Middle America")
Cape_Verde=Country(xcoordinate=[4721],ycoordinate=[3179],name="Cape Verde",continent="Africa")
Malta=Country(xcoordinate=[6335],ycoordinate=[2202],name="Malta",continent="Europe")
Palestine=Country(xcoordinate=[7205],ycoordinate=[2371],name="Palestine",continent="Asia")
Comoros=Country(xcoordinate=[7596],ycoordinate=[4493],name="Comoros",continent="Africa")
Mauritius=Country(xcoordinate=[8162],ycoordinate=[4903],name="Mauritius",continent="Africa")
Macao=Country(xcoordinate=[10448],ycoordinate=[2852],name="Macao",continent="Asia")
Hong_Kong=Country(xcoordinate=[10543],ycoordinate=[2832],name="Hong Kong",continent="Asia")
Taiwan=Country(xcoordinate=[10794],ycoordinate=[2774],name="Taiwan",continent="Asia")
Fiji=Country(xcoordinate=[13265],ycoordinate=[4802],name="Fiji",continent="Asia")




# Europe
Iceland=Country(xcoordinate=[5207],ycoordinate=[819],name="Iceland",continent="Europe")
United_Kingdom=Country(xcoordinate=[5760,5558],ycoordinate=[1386,1278],name="United Kingdom",continent="Europe")
Ireland=Country(xcoordinate=[5500],ycoordinate=[1350],name="Ireland",continent="Europe")
Norway=Country(xcoordinate=[6134,6363,6518,6490,6456],ycoordinate=[1000,280,242,308,288],name="Norway",continent="Europe")
Sweden=Country(xcoordinate=[6300],ycoordinate=[1000],name="Sweden",continent="Europe")
Finland=Country(xcoordinate=[6650],ycoordinate=[912],name="Finland",continent="Europe")
Spain=Country(xcoordinate=[5600,5873],ycoordinate=[2000,1989],name="Spain",continent="Europe")
Portugal=Country(xcoordinate=[5440],ycoordinate=[1995],name="Portugal",continent="Europe")
France=Country(xcoordinate=[5871,6115],ycoordinate=[1666,1867],name="France",continent="Europe")
Switzerland=Country(xcoordinate=[6077],ycoordinate=[1650],name="Switzerland",continent="Europe")





Belgium=Country(xcoordinate=[5963],ycoordinate=[1459],name="Belgium",continent="Europe")
Netherlands=Country(xcoordinate=[5987],ycoordinate=[1400],name="Netherlands",continent="Europe")
Germany=Country(xcoordinate=[6157],ycoordinate=[1463],name="Germany",continent="Europe")    
Denmark=Country(xcoordinate=[6115,6162,6221,4590,6154],ycoordinate=[1205,1250,1241,513,1156],name="Denmark",continent="Europe")

Austria=Country(xcoordinate=[6319],ycoordinate=[1612],name="Austria",continent="Europe")
Czech_Republic=Country(xcoordinate=[6338],ycoordinate=[1500],name="Czech Republic",continent="Europe")
Poland=Country(xcoordinate=[6500],ycoordinate=[1400],name="Poland",continent="Europe")
Slovakia=Country(xcoordinate=[6492],ycoordinate=[1547] ,name="Slovakia",continent="Europe")

Hungary=Country(xcoordinate=[6518],ycoordinate=[1639],name="Hungary",continent="Europe")
Slovenia=Country(xcoordinate=[6338],ycoordinate=[1681],name="Slovenia",continent="Europe")
Croatia=Country(xcoordinate=[6392],ycoordinate=[1700],name="Croatia",continent="Europe")
Serbia=Country(xcoordinate=[6579],ycoordinate=[1793],name="Serbia",continent="Europe")

Bosnia_and_Herzegovina=Country(xcoordinate=[6459],ycoordinate=[1765],name="Bosnia and Herzegovina",continent="Europe")
Albania=Country(xcoordinate=[6543],ycoordinate=[1922],name="Albania")
North_Macedonia=Country(xcoordinate=[6616],ycoordinate=[1896],name="North Macedonia",continent="Europe")
Bulgaria=Country(xcoordinate=[6763],ycoordinate=[1840],name="Bulgaria",continent="Europe")

Romania=Country(xcoordinate=[6739],ycoordinate=[1680],name="Romania",continent="Europe")
Moldova=Country(xcoordinate=[6855],ycoordinate=[1626],name="Moldova",continent="Europe")
Ukraine=Country(xcoordinate=[7003,6896],ycoordinate=[1541,1691],name="Ukraine",continent="Europe")
Belarus=Country(xcoordinate=[6804],ycoordinate=[1327],name="Belarus",continent="Europe")


Greece=Country(xcoordinate=[6623,6640,6761,6705],ycoordinate=[1978,2094,2203,2041],name="Greece",continent="Europe")
Estonia=Country(xcoordinate=[6707],ycoordinate=[1105],name="Estonia",continent="Europe")
Latvia=Country(xcoordinate=[6706],ycoordinate=[1175],name="Latvia",continent="Europe")
Lithuania=Country(xcoordinate=[6666],ycoordinate=[1243],name="Lithuania",continent="Europe")

Italy=Country(xcoordinate=[6247,6327,6117],ycoordinate=[1829,2090,1954],name="Italy",continent="Europe")
Montenegro=Country(xcoordinate=[6513],ycoordinate=[1837],name="Montenegro",continent="Europe")



# Asia and Middle East
Turkey=Country(xcoordinate=[6826,7132],ycoordinate=[1914,1990],name="Turkey",continent="Asia")
Georgia=Country(xcoordinate=[7456],ycoordinate=[1870],name="Georgia",continent="Asia")
Armenia=Country(xcoordinate=[7517],ycoordinate=[1945],name="Armenia",continent="Asia")
Azerbaijan=Country(xcoordinate=[7663],ycoordinate=[1952],name="Azerbaijan",continent="Asia")
Syria=Country(xcoordinate=[7326],ycoordinate=[2214],name="Syria",continent="Asia")
Iraq=Country(xcoordinate=[7496],ycoordinate=[2340],name="Iraq",continent="Asia")
Jordan=Country(xcoordinate=[7228],ycoordinate=[2415],name="Jordan",continent="Asia")
Saudi_Arabia=Country(xcoordinate=[7592],ycoordinate=[2821],name="Saudi Arabia",continent="Asia")
United_Arab_Emirates=Country(xcoordinate=[8006],ycoordinate=[2759],name="United Arab Emirates",continent="Asia")
Israel=Country(xcoordinate=[7170],ycoordinate=[2415],name="Israel",continent="Asia")
Sri_Lanka=Country(xcoordinate=[9185],ycoordinate=[3543],name="Sri Lanka",continent="Asia")

Oman=Country(xcoordinate=[8131],ycoordinate=[2906],name="Oman",continent="Asia")
Yemen=Country(xcoordinate=[7824,8025],ycoordinate=[3133,3308],name="Yemen",continent="Asia")
Iran=Country(xcoordinate=[7946],ycoordinate=[2331],name="Iran",continent="Asia")
Kuwait=Country(xcoordinate=[7696],ycoordinate=[2484],name="Kuwait",continent="Asia")
Russia=Country(xcoordinate=[8608,11104,7479,7560,3033,8394,8472,8651,9856,9995,10036,10173,11322,7803],ycoordinate=[995,1496,521,401,635,214,247,280,384,394,468,410,559,1464],name="Russia",continent="Asia")
Kazakhstan=Country(xcoordinate=[8270,8035],ycoordinate=[1551,1708],name="Kazakhstan",continent="Asia")
Uzbekistan=Country(xcoordinate=[8233,8043],ycoordinate=[1882,1731],name="Uzbekistan",continent="Asia")
Turkmenistan=Country(xcoordinate=[8180],ycoordinate=[2020],name="Turkmenistan",continent="Asia")
Afghanistan=Country(xcoordinate=[8419],ycoordinate=[2267],name="Afghanistan",continent="Asia")
Pakistan=Country(xcoordinate=[8568],ycoordinate=[2537],name="Pakistan",continent="Asia")
India=Country(xcoordinate=[9026],ycoordinate=[2851],name="India",continent="Asia")
Kyrgyzstan=Country(xcoordinate=[8708],ycoordinate=[1890],name="Kyrgyzstan",continent="Asia")
Tajikistan=Country(xcoordinate=[8638],ycoordinate=[2044],name="Tajikistan",continent="Asia")
Nepal=Country(xcoordinate=[9161],ycoordinate=[2508],name="Nepal",continent="Asia")
Bhutan=Country(xcoordinate=[9471],ycoordinate=[2583],name="Bhutan",continent="Asia")
China=Country(xcoordinate=[9997,10585,10365],ycoordinate=[2204,2026,2991],name="China",continent="Asia")
Mongolia=Country(xcoordinate=[9659],ycoordinate=[1621],name="Mongolia",continent="Asia")
Myanmar=Country(xcoordinate=[9742],ycoordinate=[2858],name="Myanmar",continent="Asia")
Thailand=Country(xcoordinate=[10021,9978],ycoordinate=[3149,3509],name="Thailand",continent="Asia")
Cambodia=Country(xcoordinate=[10201],ycoordinate=[3300],name="Cambodia",continent="Asia")
Laos=Country(xcoordinate=[10066],ycoordinate=[2953],name="Laos",continent="Asia")
Bangladesh=Country(xcoordinate=[9497,9543],ycoordinate=[2738,2829],name="Bangladesh",continent="Asia")
Malaysia=Country(xcoordinate=[10107,10591],ycoordinate=[3740,3789],name="Malaysia",continent="Asia")
Vietnam=Country(xcoordinate=[10320],ycoordinate=[3209],name="Vietnam",continent="Asia")
North_Korea=Country(xcoordinate=[10778],ycoordinate=[1956],name="North Korea",continent="Asia")
South_Korea=Country(xcoordinate=[10899,10895],ycoordinate=[2157,2296],name="South Korea",continent="Asia")
Japan=Country(xcoordinate=[11332,11323,11297,11199,11108],ycoordinate=[2149,1814,1908,2275,2345],name="Japan",continent="Asia")

#North America
United_States=Country(xcoordinate=[2282,823,686,382,108,186,2862,2420,2727,1121,2906],ycoordinate=[2129,753,1018,1155,1031,890,1935,1623,2077,1613,3031],name="United States",continent="North America")
Canada=Country(xcoordinate=[2052,1085,1130,3646,2616,2479,2271,3500,3045,3036,3135,2826,2638,2896,2808,2573,2737,3090,3432,3419,3447,3463,3349,3326,3647,3463,3268,3051,3503,3110,2778,3130,3194,3223,3221,2857,2474,985,975,969,1062,1042,1051,1095,1092],ycoordinate=[1155,1505,1161,1561,1695,573,473,824,824,923,945,1353,389,512,647,338,473,474,704,1519,1669,1685,1666,1648,302,234,397,373,481,289,311,407,353,289,317,282,386,1313,1350,1365,1229,1169,1130,1140,1175],name="Canada",continent="North America")


#Oceania
Philippines=Country(xcoordinate=[11068,10868,10885,10947,10973,11051,11051,10790,10827,11034,11013,10988],ycoordinate=[3554,3112,3288,3376,3443,3325,3377,3453,3406,3438,3408,3317],name="Philippines",continent="Oceania")
Indonesia=Country(xcoordinate=[10117,10598,10486,10869,11634,10265,10351,10575,10561,10701,10742,10795,10888,10847,11033,11214,11275,11648,11154,11205,9909,9962],ycoordinate=[3987,3952,4287,4013,4110,4012,4057,4260,4306,4335,4345,4332,4335,4387,4400,3885,4066,4297,4086,3847,3864,3981],name="Indonesia",continent="Oceania")
Papua_New_Guinea=Country(xcoordinate=[11878,12151,12378,12279,12238],ycoordinate=[4186,4205,4223,4124,4077],name="Papua New Guinea",continent="Oceania")
Australia=Country(xcoordinate=[11373,11488,11316,11286,11283],ycoordinate=[5079,5953,4478,4483,5659],name="Australia",continent="Oceania")
New_Zealand=Country(xcoordinate=[12773,12774,12518,12153],ycoordinate=[5784,5644,5971,6198],name="New Zealand",continent="Oceania")


#Africa
Morocco=Country(xcoordinate=[5487],ycoordinate=[2361],name="Morocco",continent="Africa")
Algeria=Country(xcoordinate=[5832],ycoordinate=[2474],name="Algeria",continent="Africa")
Tunisia=Country(xcoordinate=[6107],ycoordinate=[2236],name="Tunisia",continent="Africa")
Libya=Country(xcoordinate=[6497],ycoordinate=[2585],name="Libya",continent="Africa")
Egypt=Country(xcoordinate=[6967],ycoordinate=[2594],name="Egypt",continent="Africa")
Sudan=Country(xcoordinate=[7030],ycoordinate=[3136],name="Sudan",continent="Africa")
Chad=Country(xcoordinate=[6489],ycoordinate=[3124],name="Chad",continent="Africa")
Niger=Country(xcoordinate=[6172],ycoordinate=[3040],name="Niger",continent="Africa")
Mali=Country(xcoordinate=[5604],ycoordinate=[3071],name="Mali",continent="Africa")
Mauritania=Country(xcoordinate=[5260],ycoordinate=[2968],name="Mauritania",continent="Africa")
# Western_Sahara=Country(xcoordinate=[1510],ycoordinate=[880],name="Western Sahara",continent="Africa")
Senegal=Country(xcoordinate=[5138],ycoordinate=[3202],name="Senegal",continent="Africa")
Guinea_Bissau=Country(xcoordinate=[5103],ycoordinate=[3325],name="Guinea-Bissau",continent="Africa")
Guinea=Country(xcoordinate=[5196],ycoordinate=[3386],name="Guinea",continent="Africa")
Sierra_Leone=Country(xcoordinate=[5224],ycoordinate=[3499],name="Sierra Leone",continent="Africa")
Liberia=Country(xcoordinate=[5292],ycoordinate=[3594],name="Liberia",continent="Africa")
Ivory_Coast=Country(xcoordinate=[5513],ycoordinate=[3545],name="Ivory Coast",continent="Africa")
Ghana=Country(xcoordinate=[5675],ycoordinate=[3530],name="Ghana",continent="Africa")
Burkina_Faso=Country(xcoordinate=[5674],ycoordinate=[3304],name="Burkina Faso",continent="Africa")
Togo=Country(xcoordinate=[5769],ycoordinate=[3487],name="Togo",continent="Africa")
Benin=Country(xcoordinate=[5827],ycoordinate=[3411],name="Benin",continent="Africa")
Nigeria=Country(xcoordinate=[6073],ycoordinate=[3478],name="Nigeria",continent="Africa")
Cameroon=Country(xcoordinate=[6279],ycoordinate=[3685],name="Cameroon",continent="Africa")
Central_African_Republic=Country(xcoordinate=[6596],ycoordinate=[3574],name="Central African Republic",continent="Africa")
Ethiopia=Country(xcoordinate=[7416],ycoordinate=[3461],name="Ethiopia",continent="Africa")
Eritrea=Country(xcoordinate=[7354],ycoordinate=[3153],name="Eritrea",continent="Africa")

Somalia=Country(xcoordinate=[7785],ycoordinate=[3471],name="Somalia",continent="Africa")
Kenya=Country(xcoordinate=[7340],ycoordinate=[3876],name="Kenya",continent="Africa")
Uganda=Country(xcoordinate=[7137],ycoordinate=[3802],name="Uganda",continent="Africa")
Rwanda=Country(xcoordinate=[7021],ycoordinate=[4006],name="Rwanda",continent="Africa")
Burundi=Country(xcoordinate=[7004],ycoordinate=[4073],name="Burundi",continent="Africa")
DR_Congo=Country(xcoordinate=[6769],ycoordinate=[4015],name="Democratic Republic of the Congo",continent="Africa")
Republic_of_the_Congo=Country(xcoordinate=[6357],ycoordinate=[4060],name="Republic of the Congo",continent="Africa")
Gabon=Country(xcoordinate=[6214],ycoordinate=[3935],name="Gabon",continent="Africa")
Angola=Country(xcoordinate=[6497,6253],ycoordinate=[4508,4182],name="Angola",continent="Africa")
Zambia=Country(xcoordinate=[6836],ycoordinate=[4616],name="Zambia",continent="Africa")
Mozambique=Country(xcoordinate=[7202],ycoordinate=[4796],name="Mozambique",continent="Africa")
Malawi=Country(xcoordinate=[7157],ycoordinate=[4575],name="Malawi",continent="Africa")
Zimbabwe=Country(xcoordinate=[6989],ycoordinate=[4791],name="Zimbabwe",continent="Africa")
Namibia=Country(xcoordinate=[6454],ycoordinate=[4997],name="Namibia",continent="Africa")
Botswana=Country(xcoordinate=[6731],ycoordinate=[4995],name="Botswana",continent="Africa")
South_Africa=Country(xcoordinate=[6737],ycoordinate=[5324],name="South Africa",continent="Africa")
Madagascar=Country(xcoordinate=[7710],ycoordinate=[4870],name="Madagascar",continent="Africa")
Lesotho=Country(xcoordinate=[6878],ycoordinate=[5362],name="Lesotho",continent="Africa")
Eswatini=Country(xcoordinate=[7040],ycoordinate=[5205],name="Eswatini",continent="Africa")
Tanzania=Country(xcoordinate=[7194],ycoordinate=[4193],name="Tanzania",continent="Africa")
Equatorial_Guinea=Country(xcoordinate=[6161],ycoordinate=[3839],name="Equatorial Guinea",continent="Africa")



#Middle America
Mexico=Country(xcoordinate=[1500],ycoordinate=[2857],name="Mexico",continent="Middle America")
Guatemala=Country(xcoordinate=[1899],ycoordinate=[3166],name="Guatemala",continent="Middle America")
Belize=Country(xcoordinate=[1967],ycoordinate=[3075],name="Belize",continent="Middle America")
Cuba=Country(xcoordinate=[2483,2246],ycoordinate=[2893,2864],name="Cuba",continent="Middle America")
Haiti=Country(xcoordinate=[2679,2643],ycoordinate=[2991,3001],name="Haiti",continent="Middle America")
Dominican_Republic=Country(xcoordinate=[2747],ycoordinate=[2998],name="Dominican Republic",continent="Middle America")
El_Salvador=Country(xcoordinate=[1937],ycoordinate=[3250],name="El Salvador",continent="Middle America")
Honduras=Country(xcoordinate=[2041],ycoordinate=[3194],name="Honduras",continent="Middle America")
Nicaragua=Country(xcoordinate=[2131],ycoordinate=[3274],name="Nicaragua",continent="Middle America")
Costa_Rica=Country(xcoordinate=[2134],ycoordinate=[3432],name="Costa Rica",continent="Middle America")
Panama=Country(xcoordinate=[2269],ycoordinate=[3502],name="Panama",continent="Middle America")


#South America
Colombia=Country(xcoordinate=[2571],ycoordinate=[3654],name="Colombia",continent="South America")
Venezuela=Country(xcoordinate=[2950,2737],ycoordinate=[3537,3337],name="Venezuela",continent="South America")
Suriname=Country(xcoordinate=[3350],ycoordinate=[3691],name="Suriname",continent="South America")
Guyana=Country(xcoordinate=[3181],ycoordinate=[3648],name="Guyana",continent="South America")
Ecuador=Country(xcoordinate=[2341,1812],ycoordinate=[3988,3954],name="Ecuador",continent="South America")
Peru=Country(xcoordinate=[2511],ycoordinate=[4352],name="Peru",continent="South America")
Brazil=Country(xcoordinate=[3540,3595],ycoordinate=[4466,3956],name="Brazil",continent="South America")
Bolivia=Country(xcoordinate=[2965],ycoordinate=[4720],name="Bolivia",continent="South America")
Chile=Country(xcoordinate=[2820,3285,2879],ycoordinate=[5375,6524,5998],name="Chile",continent="South America")
Argentina=Country(xcoordinate=[3076,3336,3264],ycoordinate=[5606,6542,5986],name="Argentina",continent="South America")
Paraguay=Country(xcoordinate=[3288],ycoordinate=[5039],name="Paraguay",continent="South America")
Uruguay=Country(xcoordinate=[3476],ycoordinate=[5517],name="Uruguay",continent="South America")


mycounter=0
finalimage=pngim
whichcountrydict=dict()




# for country in preallCountries:
#     print(country.name)
#     mycounter=mycounter+1
#     for coordinate in country.coordinatelist:

#         image2=pngim
#         seed=(coordinate[0],coordinate[1])
#         ImageDraw.floodfill(image2,seed,(0,255,0),thresh=400)
#         npimage=np.array(image2)
#         print(npimage.shape)
#         green=np.array([0,255,0],dtype=np.uint8)
#         greens=list(zip(*np.where(np.all((npimage==green),axis=-1))))
        
#         for tuplen in greens:
#             finalimage.putpixel((tuplen[1],tuplen[0]),(0,50+mycounter,0))
#         whichcountrydict[(0,50+mycounter,0)]=country.name

# with open("whichcountrydict_NEW","wb") as f:
#     pickle.dump(whichcountrydict,f)

# finalimage.save("hahah_NEW.png")
# print("done")







#eventuell nur dann appenden wenn Kontinente ausgewählt wurden
Iceland.neighboringcountries.append("United Kingdom")
Iceland.neighboringcountries.append("Norway")
Iceland.neighboringcountries.append("Denmark")
United_Kingdom.neighboringcountries.append("France")
# United_Kingdom.neighboringcountries.append("Netherlands")
Norway.neighboringcountries.append("Netherlands")
Norway.neighboringcountries.append("Iceland")
Japan.neighboringcountries.append("Russia")
Japan.neighboringcountries.append("South Korea")
Japan.neighboringcountries.append("China")
Japan.neighboringcountries.append("United States")
China.neighboringcountries.append("South Korea")
China.neighboringcountries.append("Pakistan")
China.neighboringcountries.append("Taiwan")
China.neighboringcountries.append("Hong Kong")
China.neighboringcountries.append("Macao")
Taiwan.neighboringcountries.append("Hong Kong")
Taiwan.neighboringcountries.append("Philippines")
Australia.neighboringcountries.append("New Zealand")
Australia.neighboringcountries.append("Papua New Guinea")
Australia.neighboringcountries.append("Indonesia")
Australia.neighboringcountries.append("Chile")
Australia.neighboringcountries.append("Fiji")
Chile.neighboringcountries.append("Fiji")
Philippines.neighboringcountries.append("Indonesia")
Philippines.neighboringcountries.append("Mexico")
Philippines.neighboringcountries.append("Vietnam")
United_States.neighboringcountries.append("Japan")
United_States.neighboringcountries.append("United Kingdom")
United_States.neighboringcountries.append("Portugal")
United_States.neighboringcountries.append("Bahamas")

Canada.neighboringcountries.append("Denmark")
Canada.neighboringcountries.append("Ireland")
Madagascar.neighboringcountries.append("Australia")
Madagascar.neighboringcountries.append("Mozambique")
Madagascar.neighboringcountries.append("Comoros")
Madagascar.neighboringcountries.append("Mauritius")
Mozambique.neighboringcountries.append("Comoros")

South_Africa.neighboringcountries.append("Australia")
Namibia.neighboringcountries.append("Argentina")
Brazil.neighboringcountries.append("Angola")
Venezuela.neighboringcountries.append("Mauritania")
Venezuela.neighboringcountries.append("Trinidad and Tobago")
Venezuela.neighboringcountries.append("Cape Verde")
Mauritania.neighboringcountries.append("Cape Verde")

Philippines.neighboringcountries.append("Indonesia")
Saudi_Arabia.neighboringcountries.append("Sudan")
Saudi_Arabia.neighboringcountries.append("Egypt")

Morocco.neighboringcountries.append("Spain")
Algeria.neighboringcountries.append("France")
Libya.neighboringcountries.append("Italy")
Libya.neighboringcountries.append("Malta")
Italy.neighboringcountries.append("Malta")
Italy.neighboringcountries.append("Albania")

Turkey.neighboringcountries.append("Egypt")
Greece.neighboringcountries.append("Albania")
Serbia.neighboringcountries.append("Albania")


United_States.neighboringcountries.append("Cuba")
Cuba.neighboringcountries.append("Belize")
Cuba.neighboringcountries.append("Haiti")
Cuba.neighboringcountries.append("Bahamas")
Cuba.neighboringcountries.append("Jamaica")
Jamaica.neighboringcountries.append("Haiti")
Jamaica.neighboringcountries.append("Honduras")
Jamaica.neighboringcountries.append("Colombia")
Dominican_Republic.neighboringcountries.append("Venezuela")

India.neighboringcountries.append("Yemen")
Yemen.neighboringcountries.append("Somalia")
India.neighboringcountries.append("Maldives")
Sri_Lanka.neighboringcountries.append("Maldives")
Sri_Lanka.neighboringcountries.append("Indonesia")

Malaysia.neighboringcountries.append("Singapore")
Singapore.neighboringcountries.append("Indonesia")
Cyprus.neighboringcountries.append("Turkey")
Cyprus.neighboringcountries.append("Egypt")
Timor_Leste.neighboringcountries.append("Indonesia")
Bahrain.neighboringcountries.append("Qatar")
Saudi_Arabia.neighboringcountries.append("Qatar")
Saudi_Arabia.neighboringcountries.append("Bahrain")
Vietnam.neighboringcountries.append("Philippines")
Philippines.neighboringcountries.append("Vietnam")
Estonia.neighboringcountries.append("Finland")
United_Arab_Emirates.neighboringcountries.append("Iran")
Mauritius.neighboringcountries.append("Australia")



Unknown_country=Country(xcoordinate=[0],ycoordinate=[0],name="Unknown Country",)


# DEPRECATED

# bettersetupdata("Number of wiki-languages of most famous UNESCO-World Heritage Site of that country (higher is better).csv",additional_information=True)
# bettersetupdata("City with most sons or daughter having a wiki-page by 1,000 inhabitans (of that city) (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
# bettersetupdata("Account with the most social media followers of that country (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
# bettersetupdata("Billionaires per million people (higher is better).csv",treatmissingdataasbad=True,dif=2)
# bettersetupdata("Percentage of minimum wage (PPP) over GDP per capita (higher is better).csv",treatmissingdataasbad=True,dif=3)
# bettersetupdata("Number of wiki-languages of most famous movie from that country (higher is better).csv",dif=3,treatmissingdataasbad=True,additional_information=True,additional_information_column=[2,3,4])
# bettersetupdata("Number of subscribers of most-subscribed youtube-channel from that country (higher is better).csv",treatmissingdataasbad=True,dif=3,additional_information=True)
# bettersetupdata("Number of wiki-languages of most famous journalist of that country (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
# bettersetupdata("Health expenditure per capita in Int$ (lower is better).csv",ascending=True,dif=3)

# bettersetupdata("Percentage of railway being electrified (higher is better).csv",treatmissingdataasbad=True,dif=3) 

# bettersetupdata("Length of rail per country size (in km) (higher is better).csv",1,0,ascending=False,treatmissingdataasbad=True,applyfrac=True,dif=3)

# bettersetupdata("Vehicles per 1000 population (higher is better).csv",treatmissingdataasbad=True,dif=2) #was unter vehicle

# bettersetupdata("Number of Nobel Laureates (by 10,000,000 population) (higher is better).csv",treatmissingdataasbad=True,dif=3)

# bettersetupdata("Number of police officers per 100,000 people (higher is better).csv",dif=3)

# bettersetupdata("Number of births per woman (higher is better).csv",treatmissingdataasbad=True,dif=2)

# bettersetupdata("Milk consumption per capita (in kg per year) (higher is better).csv",treatmissingdataasbad=True,dif=4)

# bettersetupdata("Homicides per 100,000 population (lower is better).csv",ascending=True,dif=3)

# bettersetupdata("Population of the capital (higher is better).csv",treatmissingdataasbad=True,dif=2,additional_information=True,additional_information_column=[2,3,4])

# bettersetupdata("Percentage of population living in the capital (higher is better).csv",treatmissingdataasbad=True,dif=2)

bettersetupdata("Forest area in 1000 hectars (by 100 km^2) (higher is better).csv",treatmissingdataasbad=True,dif=1)
bettersetupdata("Strength of passport (in countries enterable without need of visa) (higher is better).csv",treatmissingdataasbad=True,dif=2,additional_information=True,additional_information_column=[2,3,4]) #explain
bettersetupdata("Yearly average temperature in (in Celsius) (higher is better).csv",treatmissingdataasbad=True,dif=2)
bettersetupdata("Annual precipiation (in mm) (higher is better).csv",treatmissingdataasbad=True,dif=2)
bettersetupdata("Number of different established languages and dialects (higher is better).csv",treatmissingdataasbad=True,dif=3) #was ist eine Sprache
bettersetupdata("First use of current flag (older is better).csv",ascending=True,dif=4)
bettersetupdata("Gender Gap Index (more equal is better).csv",dif=2) #was ist das genau
bettersetupdata("Prison occupacy (lower is better).csv",ascending=True,dif=4)
bettersetupdata("Percentage of prisoners being female (higher is better).csv",treatmissingdataasbad=True,dif=5)
bettersetupdata("Number of prisoners per 100,000 population (lower is better).csv",ascending=True,dif=3)
bettersetupdata("Press Freedom Index (more free is better).csv",ascending=True,dif=2)

bettersetupdata("Percentage of alcohol being consumed is wine (higher is better).csv",treatmissingdataasbad=True,dif=3) #genauer 
bettersetupdata("Percentage of alcohol being consumed is beer (higher is better).csv",treatmissingdataasbad=True,dif=3) #genauer
bettersetupdata("Alcohol consumption per person per year (lower is better) (in l).csv",ascending=True,dif=2) #liter und lower is better umdrehen
bettersetupdata("Fishing in tons (by 1000 population) (higher is better).csv",treatmissingdataasbad=True,dif=2)
bettersetupdata("Garlic production in tons  (by 10,000 population) (higher is better).csv",treatmissingdataasbad=True,dif=4,cluster="productioncluster")
bettersetupdata("Soybean production in tons (by 10,000 population) (higher is better).csv",treatmissingdataasbad=True,dif=4,cluster="productioncluster")
bettersetupdata("Tomato production in tons (by 100 population) (higher is better).csv",treatmissingdataasbad=True,dif=3,cluster="productioncluster")
bettersetupdata("Pineapple production in tons (by 1000 population) (higher is better).csv",treatmissingdataasbad=True,dif=3,cluster="productioncluster")
bettersetupdata("Plum production in tons (by 1000 population) (higher is better).csv",treatmissingdataasbad=True,dif=4,cluster="productioncluster")
bettersetupdata("Grape production in tons (by 100 population) (higher is better).csv",treatmissingdataasbad=True,dif=4,cluster="productioncluster")
bettersetupdata("Eggplant production in tons (by 1000 population) (higher is better).csv",treatmissingdataasbad=True,dif=4,cluster="productioncluster")
bettersetupdata("Cherry production in tons (by 1000 population) (higher is better).csv",treatmissingdataasbad=True,dif=4,cluster="productioncluster")
bettersetupdata("Wine production in tons (by 100 population) (higher is better).csv",treatmissingdataasbad=True,dif=4,cluster="productioncluster")
bettersetupdata("Coffee production in tons (by 1000 population) (higher is better).csv",treatmissingdataasbad=True,dif=3,cluster="productioncluster")
bettersetupdata("Cucumber production in tons (by 1000 population) (higher is better).csv",dif=4,cluster="productioncluster")
bettersetupdata("Coconut prodcution in tons  (by 1000 population) (higher is better).csv",treatmissingdataasbad=True,dif=4,cluster="productioncluster")
bettersetupdata("Apricot production in tons (by 1000 population) (higher is better).csv",treatmissingdataasbad=True,dif=4,cluster="productioncluster")
bettersetupdata("Barley production in tons (by 100 population) (higher is better).csv",treatmissingdataasbad=True,dif=4,cluster="productioncluster")
bettersetupdata("Potato production in tons (by 100 population) (higher is better).csv",treatmissingdataasbad=True,dif=4,cluster="productioncluster")
bettersetupdata("Apple production in tons (by 100 population) (higher is better).csv",treatmissingdataasbad=True,dif=3,cluster="productioncluster")
bettersetupdata("Fishing in tons (by 1000 population) (higher is better).csv",treatmissingdataasbad=True,dif=4,cluster="productioncluster")
bettersetupdata("Industrial production growth rate 2017 in percent (higher is better).csv",dif=4) #erklären
bettersetupdata("Minimum wage PPP-adjusted in Int$ (higher is better).csv",treatmissingdataasbad=True,dif=2) #was ist PPP
bettersetupdata("Meat consumption in kg per year and person (lower is better).csv",dif=2,ascending=True)

bettersetupdata("Irrigated area (by 100 km^2 country size) (higher is better).csv",treatmissingdataasbad=True,dif=3,cluster="productioncluster")
bettersetupdata("Number of different breeding bird species (higher is better).csv",dif=4,cluster="number of animalcluster")
bettersetupdata("Number of different mammal species (higher is better).csv",dif=4,cluster="number of animalcluster")
bettersetupdata("Taxi price per 1km in US$ (lower is better).csv",ascending=True,dif=3,cluster="pricecluster")
bettersetupdata("Average price for public transport in US$ (one-way-ticket) (lower is better).csv",ascending=True,dif=3,cluster="pricecluster")
bettersetupdata("Average price for public transport in US$ (monthly pass) (lower is better).csv",ascending=True,dif=3,cluster="pricecluster")
bettersetupdata("Percentage of people feeling safe walking alone (during the day) (higher is better).csv",dif=2)
bettersetupdata("Percentage of people feeling safe walking alone (at night) (higher is better).csv",dif=2)

bettersetupdata("Price of 1l of milk in US$ (lower is better).csv",ascending=True,dif=4,cluster="pricecluster")
bettersetupdata("Price of 1kg of rice in US$ (lower is better).csv",ascending=True,dif=4,cluster="pricecluster")
bettersetupdata("Price of a dozen eggs in US$ (lower is better).csv",ascending=True,dif=4,cluster="pricecluster")
bettersetupdata("Price of a kg of apples in US$ (lower is better).csv",ascending=True,dif=4,cluster="pricecluster")
bettersetupdata("Price of a skinless, boneless chicken breast in US$ (lower is better).csv",ascending=True,dif=4,cluster="pricecluster")
bettersetupdata("Price of 1.5l water bottle in supermarket in US$ (lower is better).csv",ascending=True,dif=4,cluster="pricecluster")
bettersetupdata("Price of 0.5l local beer in supermarket in US$ (lower is better).csv",ascending=True,dif=4,cluster="pricecluster")
bettersetupdata("Price of one head of lettuce in supermarket in US$ (lower is better).csv",ascending=True,dif=4,cluster="pricecluster")
bettersetupdata("Price of 1kg of tomatoes in US$ (lower is better).csv",ascending=True,dif=4,cluster="pricecluster")
bettersetupdata("Price of 1kg of potatoes in US$ (lower is better).csv",ascending=True,dif=4,cluster="pricecluster")

bettersetupdata("Price of newest nike shoes in US$ (lower is better).csv",ascending=True,dif=3,cluster="pricecluster")
bettersetupdata("Price of one pair of Levi 501s or equivalent in US$ (lower is better).csv",ascending=True,dif=3,cluster="pricecluster")
bettersetupdata("Price for garbage, water, heating, electricity for 85 sqm apartment in US$ (lower is better).csv",ascending=True,dif=3,cluster="pricecluster")
bettersetupdata("Price of a regular cappuchino in a restaurant in US$ (lower is better).csv",ascending=True,dif=3,cluster="pricecluster")
bettersetupdata("Price of a mcdonalds menu in US$ (lower is better).csv",ascending=True,dif=3,cluster="pricecluster")
bettersetupdata("Price for a 3 course meal for 2 in a normal restaurant in US$ (lower is better).csv",ascending=True,dif=3,cluster="pricecluster")
bettersetupdata("Price of 0.5 l normal beer in a restaurant in US$ (lower is better).csv",ascending=True,dif=3,cluster="pricecluster")
bettersetupdata("Price of a bottled water in a restaurant in US$ (lower is better).csv",ascending=True,dif=3,cluster="pricecluster")
bettersetupdata("Price of a new Volkswagen Golf 1.4 in US$ (lower is better).csv",ascending=True,dif=4,cluster="pricecluster")
bettersetupdata("Monthly price of broadband internet 6Mpbs, uncapped data in US$ (lower is better).csv",ascending=True,dif=4,cluster="pricecluster")
bettersetupdata("Price of local 1kg cheese in US$ (lower is better).csv",ascending=True,dif=4,cluster="pricecluster")
bettersetupdata("Price of one pack of Marlboro in US$ (lower is better).csv",ascending=True,dif=4,cluster="pricecluster")

bettersetupdata("Obesity rate (lower is better).csv",ascending=True,dif=2)
bettersetupdata("Unemployment rate (lower is better).csv",ascending=True,dif=3)
bettersetupdata("Chess grandmasters per capita (higher is better).csv",treatmissingdataasbad=True,dif=4)
bettersetupdata("Number of guns per 100 inhabitants (lower is better).csv",ascending=True,dif=4)
bettersetupdata("Roller coasters per million inhabitants (higher is better).csv",dif=4)
bettersetupdata("Cinema ticket price in US$ (lower is better).csv",ascending=True,dif=3,cluster="pricecluster")
bettersetupdata("Believes crime increasing in 2010-2014 (lower is better).csv",ascending=True,dif=4)
bettersetupdata("Rapes per 100,000 population (lower is better).csv",ascending=True,dif=4)
bettersetupdata("Gasoline prices in US$ (lower is better).csv",ascending=True,dif=2)
bettersetupdata("Percentage of land being protected (higher is better).csv",dif=4)
bettersetupdata("Unpaid diplomatic parking fines in NYC (lower is better).csv",ascending=True,dif=4)
bettersetupdata("Minimum number of paid annual leave (higher is better).csv",dif=2)
bettersetupdata("Number of paid annual public holidays (higher is better).csv",dif=2)
bettersetupdata("Percentage of people using the internet (higher is better).csv",treatmissingdataasbad=True,dif=2)

bettersetupdata("Perception of corruption score (less corrupt is higher) (higher is better).csv",dif=2) #Erklären woher das kommt
bettersetupdata("Generosity score (higher is better).csv",dif=2) #Erklären woher das kommt
bettersetupdata("Freedom to make life choices score (higher is better).csv",dif=2) #Erklären woher das kommt
bettersetupdata("Healthy life expectancy score (higher is better).csv",dif=2) #Erklären woher das kommt
bettersetupdata("Social support score (higher is better).csv",dif=2) #Erklären woher das kommt
bettersetupdata("World Happiness Index (higher is better).csv",dif=1)
bettersetupdata("Number of mcdonalds restaurants (by 1,000,000 population) (higher is better).csv",treatmissingdataasbad=True,dif=2)
bettersetupdata("Suicides per 100,000 population (lower is better).csv",ascending=True,dif=2)
bettersetupdata("Percentage of people who are proficient in english (higher is better).csv",dif=1)
bettersetupdata("Size of largest island in km2 (higher is better).csv",treatmissingdataasbad=True,dif=1)
bettersetupdata("Number of UNESCO World Heritage Sites (higher is better).csv",treatmissingdataasbad=True,dif=2)
bettersetupdata("CO2 emission in tons per capita (lower is better).csv",ascending=True,dif=1)
bettersetupdata("Agreement to the statement religion is important (higher is better).csv",ascending=False,dif=2)
bettersetupdata("Percentage of people being atheist (higher is better).csv",dif=1)
bettersetupdata("Net migration rate per 1000 population (higher is better).csv",dif=2)
bettersetupdata("Number of soldiers per 1000 population (higher is better).csv",dif=3)
bettersetupdata("Percentage of population being christian (higher is better).csv",dif=2)
bettersetupdata("Percentage of population being hindu (higher is better).csv",dif=1)
bettersetupdata("Percentage of population being muslim (higher is better).csv",dif=2)
bettersetupdata("Chinese population (by 1000 population) (higher is better).csv",dif=3)
bettersetupdata("Number of urban areas with more than 1 mio. citizens (higher is better).csv",dif=1)
bettersetupdata("Side of traffic (left hand side beats right hand side) (higher is better).csv",dif=1)
bettersetupdata("Number of visits by an US-President (since formation of the country) (higher is better).csv",dif=2,treatmissingdataasbad=True)
bettersetupdata("Home ownership rate (higher is better).csv",dif=2)
bettersetupdata("Number of wiki-languages of most famous person from that country (higher is better).csv",dif=1,additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Number of wiki-languages of most famous architect of that country (higher is better).csv",dif=2,additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Number of urban areas with more than 1 mio. citizens (higher is better).csv",dif=1)
bettersetupdata("Number of twitter followers of head of state resp. head of government (higher is better).csv",dif=1,additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Number of models from that country with a wiki-page (by 1,000,000 population) (higher is better).csv",dif=2)
bettersetupdata("Number of first level administrative regions (i.e. states in the US or prefectures in Japan) (higher is better).csv",dif=4)
bettersetupdata("Number of airports (higher is better).csv",treatmissingdataasbad=True,dif=2)
bettersetupdata("Number of airports (by 1,000,000 population) (higher is better).csv",treatmissingdataasbad=True,dif=3)
bettersetupdata("Number of wiki-languages of head of state resp. head of government (higher is better).csv",dif=2,additional_information=True,treatmissingdataasbad=True,additional_information_column=[2,3,4])
bettersetupdata("Number of wiki-languages of most famous band from that country (higher is better).csv",dif=3,additional_information=True,treatmissingdataasbad=True,additional_information_column=[2,3,4])
bettersetupdata("Number of wiki-languages of most famous food from that country (higher is better).csv",treatmissingdataasbad=True,dif=1,additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Number of wiki-languages of most famous actor from that country (higher is better).csv",dif=2,treatmissingdataasbad=True,additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous singer of that country (higher is better).csv",additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous person from that country, who is still alive (higher is better).csv",dif=2,treatmissingdataasbad=True,additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Number of wiki-languages of most famous touristic sight of that country (higher is better).csv",treatmissingdataasbad=True,dif=1,additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Number of wiki-languages of most famous woman from that country (higher is better).csv",treatmissingdataasbad=True,dif=3,additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Facebook accounts (by 10 population) (higher is better).csv",treatmissingdataasbad=True,dif=2)
bettersetupdata("Prostitutes per 10,000 inhabitants (lower is better).csv",dif=3,ascending=True)
bettersetupdata("Air cleanliness in percent (higher is better).csv",dif=3)
bettersetupdata("Year of last executed death penalty (lower is better).csv",dif=3,ascending=True)
bettersetupdata("Global peace index (more peaceful is better) (lower is better).csv",dif=2,ascending=True)
bettersetupdata("Number of volcanos in that country (higher is better).csv",dif=2)
bettersetupdata("Percentage of parliament member being female (higher is better).csv",dif=2)
bettersetupdata("First year in which (some) women were granted (restricted) suffrage (lower is better) .csv",dif=2,ascending=True)
bettersetupdata("Pupil-teacher ratio (lower is better).csv",dif=2,ascending=True)
bettersetupdata("Number of wiki-languages of most famous city with at most 5000 citizens (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Number of wiki-languages of most famous city with at most 20,000 citizens (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Number of wiki-languages of most famous city with at most 100,000 citizens (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Number of wiki-languages of most famous historical person (at least 50 years dead) (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Number of wiki-languages of most famous historical person (at least 100 years dead) (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Number of wiki-languages of most famous historical person (at least 200 years dead) (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Number of wiki-languages of most famous historical person (at least 500 years dead) (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Literacy rate (higher is better).csv")
bettersetupdata("Number of wiki-languages of most famous one-day historic event at least 90 years ago (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Highest building of that country in meter (higher is better).csv",additional_information=True,additional_information_column=[2,3,4],dif=3)
bettersetupdata("Number of wiki-languages of most famous scientist of that country (higher is better).csv",additional_information=True,additional_information_column=[2,3,4],treatmissingdataasbad=True)
bettersetupdata("Minimum number of paid annual vacation (higher is better).csv")
bettersetupdata("Number of wiki-languages of most famous writer of that country (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Median age (lower is better).csv",ascending=True)
bettersetupdata("Number of wiki-languages of most famous one-day historic event in the 21st century (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Number of wiki-languages of most famous one-day historic event at least 200 years ago (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Number of wiki-languages of most famous one-day historic event (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Size of the lower house (or equivalent) of that country (higher is better).csv")
bettersetupdata("Person of that country with the most social media follower (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Percentage of marriages getting divorced in percent (lower is better).csv",ascending=True)
bettersetupdata("Percentage of GDP spent on education (higher is better).csv")
bettersetupdata("Number of wiki-languages of the capital (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Annual cannabis prevalence in percent (lower is better).csv",ascending=True)
bettersetupdata("Drug deaths per 100,000 population (lower is better).csv",ascending=True)
bettersetupdata("Highest mountain of that country (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Number of physicians by 10,000 population (higher is better).csv")
bettersetupdata("Average elevation (higher is better).csv")
bettersetupdata("Number of cigarettes smoked per year per person (lower is better).csv",ascending=True)
bettersetupdata("Oil production in barrel per day (higher is better).csv")
bettersetupdata("Oil production in barrel per year (by 1000 population) (higher is better).csv",treatmissingdataasbad=True)
bettersetupdata("Natural disaster risk in percent (lower is better).csv",ascending=True)
bettersetupdata("Electrical power consumption per capita per year (in watts) (lower is better).csv",ascending=True)
bettersetupdata("Number of wiki-languages of most famous soccer player (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Corporate tax in percent (lower is better).csv",ascending=True)
bettersetupdata("Highest possible individual income tax in percent (lower is better).csv",ascending=True)
bettersetupdata("VAT resp. GST in percent (lower is better).csv",ascending=True)
bettersetupdata("Democracy index (higher is better).csv")
bettersetupdata("Infant mortality (deaths in the first 5 years by 1000 births) (lower is better).csv",ascending=True)
bettersetupdata("Number of wiki-languages of most famous fashion person of that country (higher is better).csv",additional_information=True,treatmissingdataasbad=True,additional_information_column=[2,3,4])
bettersetupdata("Population growth rate in 2021 in percent (higher is better).csv")
bettersetupdata("GDP per capita in PPP (higher is better).csv")
bettersetupdata("Fragile state index (more stable is better) (lower is better).csv",ascending=True)
bettersetupdata("Homeless population by 10,000 population (lower is better).csv",ascending=True)
bettersetupdata("GDP growth in 2020 (higher is better).csv")
bettersetupdata("Population density (in citizens per km^2) (higher is better).csv")
bettersetupdata("Number of wiki-languages of most famous geographical feature of that country (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Number of wiki-languages of most famous one-day event between 1950 and 2000 (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Number of wiki-languages of most famous city with at most 500,000 citizens (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Number of wiki-languages of most famous city with at most 1,000,000 citizens (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Number of wiki-languages of most famous (real) building of that country (higher is better).csv",additional_information=True,additional_information_column=[2,3,4],)
bettersetupdata("Number of wiki-languages of most famous architectural structure of that country (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Percentage of urban population (higher is better).csv")
bettersetupdata("Gini wealth index (more equal is better) (lower is better).csv",ascending=True)
bettersetupdata("Gini income index (more equal is better) (lower is better).csv",ascending=True)
bettersetupdata("Religious diversity score (higher is better).csv")
bettersetupdata("Ethnic diversity score (higher is better).csv")
bettersetupdata("Male- to female income ratio (more equal is better) (lower is better).csv",ascending=True)
bettersetupdata("Number of international tourists arriving per year (higher is better).csv")
bettersetupdata("Percentage of people working in the agricultural sector (higher is better).csv")
bettersetupdata("Percentage of people working in the agricultural sector (lower is better).csv",ascending=True)
bettersetupdata("Import and exports as percentage of gdp (higher is better).csv")
bettersetupdata("Import and exports as percentage of gdp (lower is better).csv",ascending=True)
bettersetupdata("Percentage of GDP being remittances of international migrants (higher is better).csv")
bettersetupdata("Percentage of people trusting their national government (higher is better).csv")  
bettersetupdata("Percentage of people being satsified with environment policy of government (higher is better).csv")
bettersetupdata("Percentage of people having confidence in the judical system (higher is better).csv")
bettersetupdata("Percentage of people having volunteered at least once (higher is better).csv") 
bettersetupdata("Percentage of people saying that the local labour market is good (higher is better).csv")
bettersetupdata("Percentage of people being satisfied with their health care quality (higher is better).csv")
bettersetupdata("Percentage of people being satisfied with their standard of living (higher is better).csv")
bettersetupdata("Percentage of people being satisfied with their education quality (higher is better).csv")
bettersetupdata("Number of speakers of most spoken official language of that country (higher is better).csv",additional_information=True,additional_information_column=[2])
bettersetupdata("Number of wiki-languages of most famous painter of that country (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Population of the most populated city of that country (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])    
bettersetupdata("Population of the second most populated city of that country (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])    
bettersetupdata("Population of the third most populated city of that country (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])    
bettersetupdata("Sum of the three most populated cities of that country (higher is better).csv")
bettersetupdata("Number of wiki-languages of most famous city of that country (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Number of wiki-languages of second most famous city of that country (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Number of wiki-languages of third most famous city of that country (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Sum of wiki-languages of the three most famous cities of that country (higher is better).csv")
bettersetupdata("Number of wiki-languages of most famous company which is neither an airline nor a national bank (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Number of mentions of that countrys name in the NYT from 2000 to 2016 (higher is better).csv")
bettersetupdata("Number of wiki-languages of most famous airline of that country (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Gay friendly travel index (higher is better).csv")
bettersetupdata("Number of covid deaths per capita (lower is better).csv")
bettersetupdata("Number of wiki-languages of most famous newspaper of that country (higher is better).csv",additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous street - avenue - boulevard of that country (higher is better).csv",additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous road - highway - motor circuit of that country (higher is better).csv",additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous bridge of that country (higher is better).csv",additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous place of worship (church,mosque,temple etc.) of that country (higher is better).csv",additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous (real) museum of that country (higher is better).csv",additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of chambers of the government (two chambers beat one chamber) (higher is better).csv")
bettersetupdata("Drinking water quality score (higher is better).csv")
bettersetupdata("Number of wiki-languages of most famous athlete of that country which is not a soccer player (higher is better).csv",additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous criminal of that country (higher is better).csv",additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous health scientist of that country (higher is better).csv",additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous movie director of that country (higher is better).csv",additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous person from that country born after 2000 (higher is better).csv",additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous social scientist humanities scholar of that country (higher is better).csv",additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous cleric of that country (higher is better).csv",additional_information=True,treatmissingdataasbad=True,additional_information_column=[2,3,4])
bettersetupdata("Median wealth in US$ (nominal) (higher is better).csv",additional_information=False)
bettersetupdata("Index of Economic Freedom (higher is better).csv")
bettersetupdata("Ease of doing business index (easier is better).csv",ascending=True)
bettersetupdata("Economic Complexity Index (more complex is better).csv")
bettersetupdata("Percentage of GDP spent on R&D (higher is better).csv")
bettersetupdata("Number of scientific and technical journal articles in English from that country (by 1,000,000 population) (higher is better).csv")
bettersetupdata("Percentage of population being female (higher is better).csv")
bettersetupdata("Percentage of population being female (lower is better).csv")
bettersetupdata("Projected population in 2100 (higher is better).csv")
bettersetupdata("Projected population growth until 2100 in percent (higher is better).csv")
bettersetupdata("Estimated population growth 1950-2020 (higher is better).csv")
bettersetupdata("Estimated population in 1950 (higher is better).csv")
bettersetupdata("Annual HIV deaths (by 100,000 population) (lower is better).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Annual Malaria deaths (by 10,000 population) (lower is better).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Annual alcohol deaths (by 1,000,000 population) (lower is better).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Annual deaths by traffic related causes (by 10,000 population).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Annual Hepatitis deaths (by 1,000,000 population) (lower is better).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Annual deaths by fire and heat (by 100,000 population) (lower is better).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Annual deaths by digestive diseases (by 10,000 population) (lower is better).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Annual deaths by Cirrhosis and other chronic liver diseases (by 10,000 population) (lower is better).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Annual deaths by malnutrition (by 100,000 population) (lower is better).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Annual deaths by poisonings (by 1,000,000 population) (lower is better).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Annual deaths by chronic kidney diseases (by 10,000 population) (lower is better).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Annual deaths by Diabetes Mellitus (by 10,000 population) (lower is better).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Annual deaths by conflict and terrorism (by 10,000,000 population) (lower is better).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Annual deaths by neoplasms (by 1000 population) (lower is better) (lower is better).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Annual deaths by exposure to environmental cold or heat (by 1,000,000 population) (lower is better).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Annual deaths by exposure to force of nature (by 10,000,000 population) (lower is better).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Annual deaths by neonatal disorders (by 10,000 population) (lower is better).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Annual deaths by lower respiratory infections (by 10000 population) (lower is better).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Annual deaths by cardiovascular diseases (by 1000 population) (lower is better).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Annual deaths by Tuberculosis (by 100,000 population) (lower is better).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Annual deaths by maternal disorders (by 100,000 population) (lower is better).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Annual deaths by drowning (by 100,000 population) (lower is better).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Annual deaths by nutritional deficiencies (by 100,000 population).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Annual deaths by Parkinson's disease (by 100,000 population) (lower is better).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Annual deaths by Alzheimer's disease and other dementias (by 10,000 population).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Annual deaths by Meningitis (by 1,000,000 population) (lower is better).csv",ascending=True,cluster="death_by_cause_cluster")
bettersetupdata("Percentage of US-american citizens having a positive opinion about that country (higher is better).csv")
bettersetupdata("Percentage of US-american citizens having heard of that country (higher is better).csv")
bettersetupdata("Natural gas production (in million m^3 per year) (by 10,000 population) (higher is better).csv",treatmissingdataasbad=True)
bettersetupdata("Books published in that country per year (by 10,000 population) (higher is better).csv")
bettersetupdata("Annual cocaine prevalence (lower is better).csv",ascending=True)
bettersetupdata("Annual opioid prevalence (lower is better).csv",ascending=True)
bettersetupdata("Foreign currency reserves of that country (incl. gold and special drawing rights) (by 10,000 population) (higher is better).csv")
bettersetupdata("Global Terrorism Index (less incidents are better) (lower is better).csv",ascending=True)
bettersetupdata("Youth unemployment in 2021 (lower is better).csv",ascending=True)
bettersetupdata("Year of first KFC opening in that country (lower is better).csv",ascending=True)
bettersetupdata("Year of first Burger King opening in that country (lower is better).csv",ascending=True)
bettersetupdata("Inflation rate in 2021 (lower is better).csv",ascending=True)
bettersetupdata("Average import duty in % (lower is better).csv",ascending=True)
bettersetupdata("Average inflation rate 2017-2021 (lower is better).csv",ascending=True)
bettersetupdata("S&P credit rating (better rating is better) (lower is better).csv",ascending=True,additional_information=True,additional_information_column=[2])
bettersetupdata("Amount of currencies one US$ can buy (higher is better).csv",additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Export to import ratio (higher is better).csv")
bettersetupdata("Number of characters of official name of that country (higher is better).csv",additional_information=True)
bettersetupdata("Refugee population (by 100,000 population) (higher is better).csv")
bettersetupdata("Number of emigrants from that country (by 1,000 population) (higher is better).csv")
bettersetupdata("Percentage of population being immigrants (higher is better).csv")
bettersetupdata("Female labor force participation rate (higher is better).csv")
bettersetupdata("Male labor force participation rate (higher is better).csv")
bettersetupdata("Labor force participation rate (higher is better).csv")
bettersetupdata("Fertilizer use (lower is better).csv",ascending=True)
bettersetupdata("Shadow economy (lower is better).csv",ascending=True)
bettersetupdata("Road Quality Index (higher is better).csv",ascending=True)
bettersetupdata("Percentage of total stock market capitalization to GDP (higher is better).csv",)
bettersetupdata("Percentage of people being fully vaccinated against Covid (higher is better).csv",)
bettersetupdata("Maternal deaths by 100,000 births (lower is better).csv",ascending=True)
bettersetupdata("Neonatal deaths by 1000 births (lower is better).csv",ascending=True)
bettersetupdata("Percentage of people having a credit card (higher is better).csv",)
bettersetupdata("Share of clean energy (higher is better).csv",)
bettersetupdata("Number of different taxes (lower is better).csv",ascending=True)
bettersetupdata("Government debt as percentage of GDP (lower is better).csv",ascending=True)
bettersetupdata("Income from natural resources as percent of GDP (lower is better).csv",ascending=True)
bettersetupdata("Number of tanks (by 10,000,000 population) (higher is better).csv",treatmissingdataasbad=True)
bettersetupdata("Number of military ships (by 100,000,000 population) (higher is better).csv",treatmissingdataasbad=True)
bettersetupdata("Number of military aricrafts (by 10,000,000 population) (higher is better).csv",treatmissingdataasbad=True)
bettersetupdata("National Holiday (earlier in the year is better).csv",ascending=True,additional_information=True,additional_information_column=[2,3,4])
bettersetupdata("Number of wiki-languages of most famous desert of that country (higher is better).csv",dif=2,treatmissingdataasbad=True,additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous airport of that country (higher is better).csv",dif=2,treatmissingdataasbad=True,additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous national park - garden - zoo in that country (higher is better).csv",dif=2,treatmissingdataasbad=True,additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous historical woman (at least 50 years dead) of that country (higher is better).csv",dif=2,treatmissingdataasbad=True,additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous historical woman (at least 100 years dead) of that country (higher is better).csv",dif=2,treatmissingdataasbad=True,additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous historical woman (at least 200 years dead) of that country (higher is better).csv",dif=2,treatmissingdataasbad=True,additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous historical woman (at least 500 years dead) of that country (higher is better).csv",dif=2,treatmissingdataasbad=True,additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous historical woman (at least 500 years dead) of that country (higher is better).csv",dif=2,treatmissingdataasbad=True,additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous historical woman (at least 500 years dead) of that country (higher is better).csv",dif=2,treatmissingdataasbad=True,additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous historical woman (at least 500 years dead) of that country (higher is better).csv",dif=2,treatmissingdataasbad=True,additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous female scientist of that country (higher is better).csv",dif=2,treatmissingdataasbad=True,additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous female athlete of that country (higher is better).csv",dif=2,treatmissingdataasbad=True,additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous female actor of that country (higher is better).csv",dif=2,treatmissingdataasbad=True,additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous battle which took place in that country (higher is better).csv",dif=2,treatmissingdataasbad=True,additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous woman being born after 2000 (higher is better).csv",dif=2,treatmissingdataasbad=True,additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of wiki-languages of most famous female singer of that country (higher is better).csv",dif=2,treatmissingdataasbad=True,additional_information=True,additional_information_column=[2,7,8])
bettersetupdata("Number of mobile phone lines (by 100 population) (higher is better).csv")
bettersetupdata("Country size (higher is better).csv",is_end_only=True)
bettersetupdata("Population (higher is better).csv",is_end_only=True)
bettersetupdata("Latitude of northernmost point of that country (northern is better) (higher is better).csv",is_end_only=True)
bettersetupdata("Latitude of southernmost point of that country (southern is better) (lower is better).csv",is_end_only=True)

save_properties()
# print(clusterdict.keys())




IntroWindow()

# propertydict=dict()
# for country in allCountries:
#     propertydict[country.name]=country.dictofattributes

# with open("backenddata/attributedict","wb") as f:
#     pickle.dump(propertydict,f)
# print("success")

# root=tk.Tk()
# MainWindow(bild=im,main=root)
# root.mainloop()

# for i in range (100):
#     try:
#         for j in range (100):
#             try:
#                 finaldatalist.append(data[i]["data"][j])
#             except:
#                 break
#     except:
#         break

# df=pd.DataFrame(finaldatalist)
# print(df)