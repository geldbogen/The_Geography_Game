
import os
import pandas as pd
from PIL import Image, ImageDraw, ImageTk
import pickle

#local files
import alternative_names
import additional_explanations
import categoryname_to_displayed_name

from Country import Country
from Player import Player
from setupData import bettersetupdata
from helpFunctions import save_properties
from IntroWindow import IntroWindow



filename=os.path.realpath(__file__).replace("\\","/")
# filename=filename.rstrip("/Backup/start.py")
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


p = pd.read_csv("data/important/countrylist.csv",index_col=False,keep_default_na=False)
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


# a dictionary which takes a string and if it is a clustername
# returns the list of categories associated to it. If it is just a normal 
# categoryname it returns a list with only the asked category in it.
dictionary_attribute_name_to_attribute={}


Mr_Nobody=Player(color="white",name="Nobody")
No_Data_Body=Player(color=realgrey,name="Nobody")


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



if __name__ == '__main__':
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