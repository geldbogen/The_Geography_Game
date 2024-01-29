from PIL import ImageDraw, Image, ImageTk
import numpy as np

from globalDefinitions import resize_ratio, all_countries_available, countries_for_language_en, all_countries, country_name_list
from Image import pngImage
from LocalAttribute import LocalAttribute


class Country:

    def __init__(self, xcoordinate, ycoordinate, name, continent=None):

        self.coordinate_list = []

        for i in range(len(xcoordinate)):
            self.coordinate_list.append((xcoordinate[i], ycoordinate[i]))
        self.neighboring_countries = []

        
        self.xcoordinate = xcoordinate
        self.ycoordinate = ycoordinate

        # a dict of attributes with key the dictionary name and value a dict 
        # TODO change it, so that it is a property of categories, not of countries
        self.dict_of_attributes = dict[str, LocalAttribute]

        # the name of the country
        self.name = name

        # the current owner of the country
        self.owner = "Nobody"

        # the continent the country belongs to
        self.continent = continent

        all_countries_available.append(self)

        self.save_location = "data/npdata/" + self.name + "-nparray.npy"

        # the screen coordinate, where the wormhole is going to if it goes to the country
        self.wormhole_coordinates = [
            resize_ratio[0] * xcoordinate[0], resize_ratio[1] * ycoordinate[0]
        ]

    def get_color(self, image):
        output = []
        for coordinates in self.coordinate_list:
            output.append(image.getpixel(coordinates))
        return output

    def get_two_country_code(self) -> str:
        if self.name == "Ivory Coast":
            return "ci"
        if self.name == "Myanmar":
            return "mm"
        if self.name == "Democratic Republic of the Congo":
            return "cd"
        if self.name == "Bosnia and Herzegovina":
            return "ba"
        if self.name == "Czech Republic":
            return "cz"
        if self.name == "Republic of the Congo":
            return "cg"
        for item in countries_for_language_en:
            if item[1] == self.name:
                return item[0]
        return "noflag"

    def set_pixels(self, image):
        if self.name == "Unknown Country":
            return None
        print(self.name)
        save_array = np.zeros(shape=(1, 2))
        for coordinate in self.coordinate_list:
            image2 = image
            seed = (coordinate[0], coordinate[1])
            ImageDraw.floodfill(image2, seed, (0, 255, 0), thresh=200)
            npImage = np.array(image2)
            print(npImage.shape)
            green = np.array([0, 255, 0], dtype=np.uint8)
            greens = list(zip(*np.where(np.all((npImage == green), axis=-1))))
            s_array = np.array([*greens])
            save_array = np.append(save_array, s_array, axis=0)
            print(s_array)
            print(s_array.shape)
            print(save_array.shape)
        with open(self.save_location, "wb") as f:
            np.save(f, save_array)

    def get_resized_flag(self, height):
        country_url = "pictures/flag_pictures/w1280/" + self.get_two_country_code(
        ).lower() + ".png"
        flag_image = (Image.open(country_url))
        w = float(flag_image.width)
        h = float(flag_image.height)
        return ImageTk.PhotoImage(
            flag_image.resize((int(height * w / h), int(height)),
                             Image.LANCZOS))

    def load_pixels(self):
        global all_countries
        global country_name_list
        if self.name == "Unknown Country":
            self.set_of_pixels = set()
            all_countries.append(self)
            country_name_list.append(self.name)
            return None
        try:
            print(self.name)
            marray = np.load(self.save_location, allow_pickle=True)
            marray = marray.T
            self.set_of_pixels = set(zip(marray[0], marray[1]))
        except Exception as e:
            print(str(e))
            self.set_pixels(pngImage)
        all_countries.append(self)
        country_name_list.append(self.name)


Unknown_country = Country(
    xcoordinate=[0],
    ycoordinate=[0],
    name="Unknown Country",
)

#Micro
Gambia = Country(xcoordinate=[5081],
                 ycoordinate=[3264],
                 name="Gambia",
                 continent="Africa")
Djibouti = Country(xcoordinate=[7535],
                   ycoordinate=[3345],
                   name="Djibouti",
                   continent="Africa")
Timor_Leste = Country(xcoordinate=[11113],
                      ycoordinate=[4347],
                      name="Timor-Leste",
                      continent="Oceania")
Luxembourg = Country(xcoordinate=[6011],
                     ycoordinate=[1506],
                     name="Luxembourg",
                     continent="Europe")
Cyprus = Country(xcoordinate=[7090],
                 ycoordinate=[2211],
                 name="Cyprus",
                 continent="Europe")
Qatar = Country(xcoordinate=[7863],
                ycoordinate=[2684],
                name="Qatar",
                continent="Asia")
Bahrain = Country(xcoordinate=[7805],
                  ycoordinate=[2607],
                  name="Bahrain",
                  continent="Asia")
Maldives = Country(xcoordinate=[8750],
                   ycoordinate=[4009],
                   name="Maldives",
                   continent="Asia")
Brunei = Country(xcoordinate=[10662],
                 ycoordinate=[3682],
                 name="Brunei",
                 continent="Asia")
Singapore = Country(xcoordinate=[10197],
                    ycoordinate=[3847],
                    name="Singapore",
                    continent="Asia")
Lebanon = Country(xcoordinate=[7207],
                  ycoordinate=[2267],
                  name="Lebanon",
                  continent="Asia")
Bahamas = Country(xcoordinate=[2474],
                  ycoordinate=[2733],
                  name="Bahamas",
                  continent="Middle America")
Jamaica = Country(xcoordinate=[2465],
                  ycoordinate=[3043],
                  name="Jamaica",
                  continent="Middle America")
Trinidad_and_Tobago = Country(xcoordinate=[3108],
                              ycoordinate=[3424],
                              name="Trinidad and Tobago",
                              continent="Middle America")
Cape_Verde = Country(xcoordinate=[4721],
                     ycoordinate=[3179],
                     name="Cape Verde",
                     continent="Africa")
Malta = Country(xcoordinate=[6335],
                ycoordinate=[2202],
                name="Malta",
                continent="Europe")
Palestine = Country(xcoordinate=[7205],
                    ycoordinate=[2371],
                    name="Palestine",
                    continent="Asia")
Comoros = Country(xcoordinate=[7596],
                  ycoordinate=[4493],
                  name="Comoros",
                  continent="Africa")
Mauritius = Country(xcoordinate=[8162],
                    ycoordinate=[4903],
                    name="Mauritius",
                    continent="Africa")
Macao = Country(xcoordinate=[10448],
                ycoordinate=[2852],
                name="Macao",
                continent="Asia")
Hong_Kong = Country(xcoordinate=[10543],
                    ycoordinate=[2832],
                    name="Hong Kong",
                    continent="Asia")
Taiwan = Country(xcoordinate=[10794],
                 ycoordinate=[2774],
                 name="Taiwan",
                 continent="Asia")
Fiji = Country(xcoordinate=[13265],
               ycoordinate=[4802],
               name="Fiji",
               continent="Asia")

# Europe
Iceland = Country(xcoordinate=[5207],
                  ycoordinate=[819],
                  name="Iceland",
                  continent="Europe")
United_Kingdom = Country(xcoordinate=[5760, 5558],
                         ycoordinate=[1386, 1278],
                         name="United Kingdom",
                         continent="Europe")
Ireland = Country(xcoordinate=[5500],
                  ycoordinate=[1350],
                  name="Ireland",
                  continent="Europe")
Norway = Country(xcoordinate=[6134, 6363, 6518, 6490, 6456],
                 ycoordinate=[1000, 280, 242, 308, 288],
                 name="Norway",
                 continent="Europe")
Sweden = Country(xcoordinate=[6300],
                 ycoordinate=[1000],
                 name="Sweden",
                 continent="Europe")
Finland = Country(xcoordinate=[6650],
                  ycoordinate=[912],
                  name="Finland",
                  continent="Europe")
Spain = Country(xcoordinate=[5600, 5873],
                ycoordinate=[2000, 1989],
                name="Spain",
                continent="Europe")
Portugal = Country(xcoordinate=[5440],
                   ycoordinate=[1995],
                   name="Portugal",
                   continent="Europe")
France = Country(xcoordinate=[5871, 6115],
                 ycoordinate=[1666, 1867],
                 name="France",
                 continent="Europe")
Switzerland = Country(xcoordinate=[6077],
                      ycoordinate=[1650],
                      name="Switzerland",
                      continent="Europe")
Belgium = Country(xcoordinate=[5963],
                  ycoordinate=[1459],
                  name="Belgium",
                  continent="Europe")
Netherlands = Country(xcoordinate=[5987],
                      ycoordinate=[1400],
                      name="Netherlands",
                      continent="Europe")
Germany = Country(xcoordinate=[6157],
                  ycoordinate=[1463],
                  name="Germany",
                  continent="Europe")
Denmark = Country(xcoordinate=[6115, 6162, 6221, 4590, 6154],
                  ycoordinate=[1205, 1250, 1241, 513, 1156],
                  name="Denmark",
                  continent="Europe")
Austria = Country(xcoordinate=[6319],
                  ycoordinate=[1612],
                  name="Austria",
                  continent="Europe")
Czech_Republic = Country(xcoordinate=[6338],
                         ycoordinate=[1500],
                         name="Czech Republic",
                         continent="Europe")
Poland = Country(xcoordinate=[6500],
                 ycoordinate=[1400],
                 name="Poland",
                 continent="Europe")
Slovakia = Country(xcoordinate=[6492],
                   ycoordinate=[1547],
                   name="Slovakia",
                   continent="Europe")
Hungary = Country(xcoordinate=[6518],
                  ycoordinate=[1639],
                  name="Hungary",
                  continent="Europe")
Slovenia = Country(xcoordinate=[6338],
                   ycoordinate=[1681],
                   name="Slovenia",
                   continent="Europe")
Croatia = Country(xcoordinate=[6392],
                  ycoordinate=[1700],
                  name="Croatia",
                  continent="Europe")
Serbia = Country(xcoordinate=[6579],
                 ycoordinate=[1793],
                 name="Serbia",
                 continent="Europe")
Bosnia_and_Herzegovina = Country(xcoordinate=[6459],
                                 ycoordinate=[1765],
                                 name="Bosnia and Herzegovina",
                                 continent="Europe")
Albania = Country(xcoordinate=[6543], ycoordinate=[1922], name="Albania")
North_Macedonia = Country(xcoordinate=[6616],
                          ycoordinate=[1896],
                          name="North Macedonia",
                          continent="Europe")
Bulgaria = Country(xcoordinate=[6763],
                   ycoordinate=[1840],
                   name="Bulgaria",
                   continent="Europe")
Romania = Country(xcoordinate=[6739],
                  ycoordinate=[1680],
                  name="Romania",
                  continent="Europe")
Moldova = Country(xcoordinate=[6855],
                  ycoordinate=[1626],
                  name="Moldova",
                  continent="Europe")
Ukraine = Country(xcoordinate=[7003, 6896],
                  ycoordinate=[1541, 1691],
                  name="Ukraine",
                  continent="Europe")
Belarus = Country(xcoordinate=[6804],
                  ycoordinate=[1327],
                  name="Belarus",
                  continent="Europe")
Greece = Country(xcoordinate=[6623, 6640, 6761, 6705],
                 ycoordinate=[1978, 2094, 2203, 2041],
                 name="Greece",
                 continent="Europe")
Estonia = Country(xcoordinate=[6707],
                  ycoordinate=[1105],
                  name="Estonia",
                  continent="Europe")
Latvia = Country(xcoordinate=[6706],
                 ycoordinate=[1175],
                 name="Latvia",
                 continent="Europe")
Lithuania = Country(xcoordinate=[6666],
                    ycoordinate=[1243],
                    name="Lithuania",
                    continent="Europe")
Italy = Country(xcoordinate=[6247, 6327, 6117],
                ycoordinate=[1829, 2090, 1954],
                name="Italy",
                continent="Europe")
Montenegro = Country(xcoordinate=[6513],
                     ycoordinate=[1837],
                     name="Montenegro",
                     continent="Europe")

# Asia and Middle East
Turkey = Country(xcoordinate=[6826, 7132],
                 ycoordinate=[1914, 1990],
                 name="Turkey",
                 continent="Asia")
Georgia = Country(xcoordinate=[7456],
                  ycoordinate=[1870],
                  name="Georgia",
                  continent="Asia")
Armenia = Country(xcoordinate=[7517],
                  ycoordinate=[1945],
                  name="Armenia",
                  continent="Asia")
Azerbaijan = Country(xcoordinate=[7663],
                     ycoordinate=[1952],
                     name="Azerbaijan",
                     continent="Asia")
Syria = Country(xcoordinate=[7326],
                ycoordinate=[2214],
                name="Syria",
                continent="Asia")
Iraq = Country(xcoordinate=[7496],
               ycoordinate=[2340],
               name="Iraq",
               continent="Asia")
Jordan = Country(xcoordinate=[7228],
                 ycoordinate=[2415],
                 name="Jordan",
                 continent="Asia")
Saudi_Arabia = Country(xcoordinate=[7592],
                       ycoordinate=[2821],
                       name="Saudi Arabia",
                       continent="Asia")
United_Arab_Emirates = Country(xcoordinate=[8006],
                               ycoordinate=[2759],
                               name="United Arab Emirates",
                               continent="Asia")
Israel = Country(xcoordinate=[7170],
                 ycoordinate=[2415],
                 name="Israel",
                 continent="Asia")
Sri_Lanka = Country(xcoordinate=[9185],
                    ycoordinate=[3543],
                    name="Sri Lanka",
                    continent="Asia")

Oman = Country(xcoordinate=[8131],
               ycoordinate=[2906],
               name="Oman",
               continent="Asia")
Yemen = Country(xcoordinate=[7824, 8025],
                ycoordinate=[3133, 3308],
                name="Yemen",
                continent="Asia")
Iran = Country(xcoordinate=[7946],
               ycoordinate=[2331],
               name="Iran",
               continent="Asia")
Kuwait = Country(xcoordinate=[7696],
                 ycoordinate=[2484],
                 name="Kuwait",
                 continent="Asia")
Russia = Country(xcoordinate=[
    8608, 11104, 7479, 7560, 3033, 8394, 8472, 8651, 9856, 9995, 10036, 10173,
    11322, 7803
],
                 ycoordinate=[
                     995, 1496, 521, 401, 635, 214, 247, 280, 384, 394, 468,
                     410, 559, 1464
                 ],
                 name="Russia",
                 continent="Asia")
Kazakhstan = Country(xcoordinate=[8270, 8035],
                     ycoordinate=[1551, 1708],
                     name="Kazakhstan",
                     continent="Asia")
Uzbekistan = Country(xcoordinate=[8233, 8043],
                     ycoordinate=[1882, 1731],
                     name="Uzbekistan",
                     continent="Asia")
Turkmenistan = Country(xcoordinate=[8180],
                       ycoordinate=[2020],
                       name="Turkmenistan",
                       continent="Asia")
Afghanistan = Country(xcoordinate=[8419],
                      ycoordinate=[2267],
                      name="Afghanistan",
                      continent="Asia")
Pakistan = Country(xcoordinate=[8568],
                   ycoordinate=[2537],
                   name="Pakistan",
                   continent="Asia")
India = Country(xcoordinate=[9026],
                ycoordinate=[2851],
                name="India",
                continent="Asia")
Kyrgyzstan = Country(xcoordinate=[8708],
                     ycoordinate=[1890],
                     name="Kyrgyzstan",
                     continent="Asia")
Tajikistan = Country(xcoordinate=[8638],
                     ycoordinate=[2044],
                     name="Tajikistan",
                     continent="Asia")
Nepal = Country(xcoordinate=[9161],
                ycoordinate=[2508],
                name="Nepal",
                continent="Asia")
Bhutan = Country(xcoordinate=[9471],
                 ycoordinate=[2583],
                 name="Bhutan",
                 continent="Asia")
China = Country(xcoordinate=[9997, 10585, 10365],
                ycoordinate=[2204, 2026, 2991],
                name="China",
                continent="Asia")
Mongolia = Country(xcoordinate=[9659],
                   ycoordinate=[1621],
                   name="Mongolia",
                   continent="Asia")
Myanmar = Country(xcoordinate=[9742],
                  ycoordinate=[2858],
                  name="Myanmar",
                  continent="Asia")
Thailand = Country(xcoordinate=[10021, 9978],
                   ycoordinate=[3149, 3509],
                   name="Thailand",
                   continent="Asia")
Cambodia = Country(xcoordinate=[10201],
                   ycoordinate=[3300],
                   name="Cambodia",
                   continent="Asia")
Laos = Country(xcoordinate=[10066],
               ycoordinate=[2953],
               name="Laos",
               continent="Asia")
Bangladesh = Country(xcoordinate=[9497, 9543],
                     ycoordinate=[2738, 2829],
                     name="Bangladesh",
                     continent="Asia")
Malaysia = Country(xcoordinate=[10107, 10591],
                   ycoordinate=[3740, 3789],
                   name="Malaysia",
                   continent="Asia")
Vietnam = Country(xcoordinate=[10320],
                  ycoordinate=[3209],
                  name="Vietnam",
                  continent="Asia")
North_Korea = Country(xcoordinate=[10778],
                      ycoordinate=[1956],
                      name="North Korea",
                      continent="Asia")
South_Korea = Country(xcoordinate=[10899, 10895],
                      ycoordinate=[2157, 2296],
                      name="South Korea",
                      continent="Asia")
Japan = Country(xcoordinate=[11332, 11323, 11297, 11199, 11108],
                ycoordinate=[2149, 1814, 1908, 2275, 2345],
                name="Japan",
                continent="Asia")

#North America
United_States = Country(
    xcoordinate=[2282, 823, 686, 382, 108, 186, 2862, 2420, 2727, 1121, 2906],
    ycoordinate=[
        2129, 753, 1018, 1155, 1031, 890, 1935, 1623, 2077, 1613, 3031
    ],
    name="United States",
    continent="North America")
Canada = Country(xcoordinate=[
    2052, 1085, 1130, 3646, 2616, 2479, 2271, 3500, 3045, 3036, 3135, 2826,
    2638, 2896, 2808, 2573, 2737, 3090, 3432, 3419, 3447, 3463, 3349, 3326,
    3647, 3463, 3268, 3051, 3503, 3110, 2778, 3130, 3194, 3223, 3221, 2857,
    2474, 985, 975, 969, 1062, 1042, 1051, 1095, 1092
],
                 ycoordinate=[
                     1155, 1505, 1161, 1561, 1695, 573, 473, 824, 824, 923,
                     945, 1353, 389, 512, 647, 338, 473, 474, 704, 1519, 1669,
                     1685, 1666, 1648, 302, 234, 397, 373, 481, 289, 311, 407,
                     353, 289, 317, 282, 386, 1313, 1350, 1365, 1229, 1169,
                     1130, 1140, 1175
                 ],
                 name="Canada",
                 continent="North America")

#Oceania
Philippines = Country(xcoordinate=[
    11068, 10868, 10885, 10947, 10973, 11051, 11051, 10790, 10827, 11034,
    11013, 10988
],
                      ycoordinate=[
                          3554, 3112, 3288, 3376, 3443, 3325, 3377, 3453, 3406,
                          3438, 3408, 3317
                      ],
                      name="Philippines",
                      continent="Oceania")
Indonesia = Country(xcoordinate=[
    10117, 10598, 10486, 10869, 11634, 10265, 10351, 10575, 10561, 10701,
    10742, 10795, 10888, 10847, 11033, 11214, 11275, 11648, 11154, 11205, 9909,
    9962
],
                    ycoordinate=[
                        3987, 3952, 4287, 4013, 4110, 4012, 4057, 4260, 4306,
                        4335, 4345, 4332, 4335, 4387, 4400, 3885, 4066, 4297,
                        4086, 3847, 3864, 3981
                    ],
                    name="Indonesia",
                    continent="Oceania")
Papua_New_Guinea = Country(xcoordinate=[11878, 12151, 12378, 12279, 12238],
                           ycoordinate=[4186, 4205, 4223, 4124, 4077],
                           name="Papua New Guinea",
                           continent="Oceania")
Australia = Country(xcoordinate=[11373, 11488, 11316, 11286, 11283],
                    ycoordinate=[5079, 5953, 4478, 4483, 5659],
                    name="Australia",
                    continent="Oceania")
New_Zealand = Country(xcoordinate=[12773, 12774, 12518, 12153],
                      ycoordinate=[5784, 5644, 5971, 6198],
                      name="New Zealand",
                      continent="Oceania")

#Africa
Morocco = Country(xcoordinate=[5487],
                  ycoordinate=[2361],
                  name="Morocco",
                  continent="Africa")
Algeria = Country(xcoordinate=[5832],
                  ycoordinate=[2474],
                  name="Algeria",
                  continent="Africa")
Tunisia = Country(xcoordinate=[6107],
                  ycoordinate=[2236],
                  name="Tunisia",
                  continent="Africa")
Libya = Country(xcoordinate=[6497],
                ycoordinate=[2585],
                name="Libya",
                continent="Africa")
Egypt = Country(xcoordinate=[6967],
                ycoordinate=[2594],
                name="Egypt",
                continent="Africa")
Sudan = Country(xcoordinate=[7030],
                ycoordinate=[3136],
                name="Sudan",
                continent="Africa")
Chad = Country(xcoordinate=[6489],
               ycoordinate=[3124],
               name="Chad",
               continent="Africa")
Niger = Country(xcoordinate=[6172],
                ycoordinate=[3040],
                name="Niger",
                continent="Africa")
Mali = Country(xcoordinate=[5604],
               ycoordinate=[3071],
               name="Mali",
               continent="Africa")
Mauritania = Country(xcoordinate=[5260],
                     ycoordinate=[2968],
                     name="Mauritania",
                     continent="Africa")
# Western_Sahara=Country(xcoordinate=[1510],ycoordinate=[880],name="Western Sahara",continent="Africa")
Senegal = Country(xcoordinate=[5138],
                  ycoordinate=[3202],
                  name="Senegal",
                  continent="Africa")
Guinea_Bissau = Country(xcoordinate=[5103],
                        ycoordinate=[3325],
                        name="Guinea-Bissau",
                        continent="Africa")
Guinea = Country(xcoordinate=[5196],
                 ycoordinate=[3386],
                 name="Guinea",
                 continent="Africa")
Sierra_Leone = Country(xcoordinate=[5224],
                       ycoordinate=[3499],
                       name="Sierra Leone",
                       continent="Africa")
Liberia = Country(xcoordinate=[5292],
                  ycoordinate=[3594],
                  name="Liberia",
                  continent="Africa")
Ivory_Coast = Country(xcoordinate=[5513],
                      ycoordinate=[3545],
                      name="Ivory Coast",
                      continent="Africa")
Ghana = Country(xcoordinate=[5675],
                ycoordinate=[3530],
                name="Ghana",
                continent="Africa")
Burkina_Faso = Country(xcoordinate=[5674],
                       ycoordinate=[3304],
                       name="Burkina Faso",
                       continent="Africa")
Togo = Country(xcoordinate=[5769],
               ycoordinate=[3487],
               name="Togo",
               continent="Africa")
Benin = Country(xcoordinate=[5827],
                ycoordinate=[3411],
                name="Benin",
                continent="Africa")
Nigeria = Country(xcoordinate=[6073],
                  ycoordinate=[3478],
                  name="Nigeria",
                  continent="Africa")
Cameroon = Country(xcoordinate=[6279],
                   ycoordinate=[3685],
                   name="Cameroon",
                   continent="Africa")
Central_African_Republic = Country(xcoordinate=[6596],
                                   ycoordinate=[3574],
                                   name="Central African Republic",
                                   continent="Africa")
Ethiopia = Country(xcoordinate=[7416],
                   ycoordinate=[3461],
                   name="Ethiopia",
                   continent="Africa")
Eritrea = Country(xcoordinate=[7354],
                  ycoordinate=[3153],
                  name="Eritrea",
                  continent="Africa")

Somalia = Country(xcoordinate=[7785],
                  ycoordinate=[3471],
                  name="Somalia",
                  continent="Africa")
Kenya = Country(xcoordinate=[7340],
                ycoordinate=[3876],
                name="Kenya",
                continent="Africa")
Uganda = Country(xcoordinate=[7137],
                 ycoordinate=[3802],
                 name="Uganda",
                 continent="Africa")
Rwanda = Country(xcoordinate=[7021],
                 ycoordinate=[4006],
                 name="Rwanda",
                 continent="Africa")
Burundi = Country(xcoordinate=[7004],
                  ycoordinate=[4073],
                  name="Burundi",
                  continent="Africa")
DR_Congo = Country(xcoordinate=[6769],
                   ycoordinate=[4015],
                   name="Democratic Republic of the Congo",
                   continent="Africa")
Republic_of_the_Congo = Country(xcoordinate=[6357],
                                ycoordinate=[4060],
                                name="Republic of the Congo",
                                continent="Africa")
Gabon = Country(xcoordinate=[6214],
                ycoordinate=[3935],
                name="Gabon",
                continent="Africa")
Angola = Country(xcoordinate=[6497, 6253],
                 ycoordinate=[4508, 4182],
                 name="Angola",
                 continent="Africa")
Zambia = Country(xcoordinate=[6836],
                 ycoordinate=[4616],
                 name="Zambia",
                 continent="Africa")
Mozambique = Country(xcoordinate=[7202],
                     ycoordinate=[4796],
                     name="Mozambique",
                     continent="Africa")
Malawi = Country(xcoordinate=[7157],
                 ycoordinate=[4575],
                 name="Malawi",
                 continent="Africa")
Zimbabwe = Country(xcoordinate=[6989],
                   ycoordinate=[4791],
                   name="Zimbabwe",
                   continent="Africa")
Namibia = Country(xcoordinate=[6454],
                  ycoordinate=[4997],
                  name="Namibia",
                  continent="Africa")
Botswana = Country(xcoordinate=[6731],
                   ycoordinate=[4995],
                   name="Botswana",
                   continent="Africa")
South_Africa = Country(xcoordinate=[6737],
                       ycoordinate=[5324],
                       name="South Africa",
                       continent="Africa")
Madagascar = Country(xcoordinate=[7710],
                     ycoordinate=[4870],
                     name="Madagascar",
                     continent="Africa")
Lesotho = Country(xcoordinate=[6878],
                  ycoordinate=[5362],
                  name="Lesotho",
                  continent="Africa")
Eswatini = Country(xcoordinate=[7040],
                   ycoordinate=[5205],
                   name="Eswatini",
                   continent="Africa")
Tanzania = Country(xcoordinate=[7194],
                   ycoordinate=[4193],
                   name="Tanzania",
                   continent="Africa")
Equatorial_Guinea = Country(xcoordinate=[6161],
                            ycoordinate=[3839],
                            name="Equatorial Guinea",
                            continent="Africa")

#Middle America
Mexico = Country(xcoordinate=[1500],
                 ycoordinate=[2857],
                 name="Mexico",
                 continent="Middle America")
Guatemala = Country(xcoordinate=[1899],
                    ycoordinate=[3166],
                    name="Guatemala",
                    continent="Middle America")
Belize = Country(xcoordinate=[1967],
                 ycoordinate=[3075],
                 name="Belize",
                 continent="Middle America")
Cuba = Country(xcoordinate=[2483, 2246],
               ycoordinate=[2893, 2864],
               name="Cuba",
               continent="Middle America")
Haiti = Country(xcoordinate=[2679, 2643],
                ycoordinate=[2991, 3001],
                name="Haiti",
                continent="Middle America")
Dominican_Republic = Country(xcoordinate=[2747],
                             ycoordinate=[2998],
                             name="Dominican Republic",
                             continent="Middle America")
El_Salvador = Country(xcoordinate=[1937],
                      ycoordinate=[3250],
                      name="El Salvador",
                      continent="Middle America")
Honduras = Country(xcoordinate=[2041],
                   ycoordinate=[3194],
                   name="Honduras",
                   continent="Middle America")
Nicaragua = Country(xcoordinate=[2131],
                    ycoordinate=[3274],
                    name="Nicaragua",
                    continent="Middle America")
Costa_Rica = Country(xcoordinate=[2134],
                     ycoordinate=[3432],
                     name="Costa Rica",
                     continent="Middle America")
Panama = Country(xcoordinate=[2269],
                 ycoordinate=[3502],
                 name="Panama",
                 continent="Middle America")

#South America
Colombia = Country(xcoordinate=[2571],
                   ycoordinate=[3654],
                   name="Colombia",
                   continent="South America")
Venezuela = Country(xcoordinate=[2950, 2737],
                    ycoordinate=[3537, 3337],
                    name="Venezuela",
                    continent="South America")
Suriname = Country(xcoordinate=[3350],
                   ycoordinate=[3691],
                   name="Suriname",
                   continent="South America")
Guyana = Country(xcoordinate=[3181],
                 ycoordinate=[3648],
                 name="Guyana",
                 continent="South America")
Ecuador = Country(xcoordinate=[2341, 1812],
                  ycoordinate=[3988, 3954],
                  name="Ecuador",
                  continent="South America")
Peru = Country(xcoordinate=[2511],
               ycoordinate=[4352],
               name="Peru",
               continent="South America")
Brazil = Country(xcoordinate=[3540, 3595],
                 ycoordinate=[4466, 3956],
                 name="Brazil",
                 continent="South America")
Bolivia = Country(xcoordinate=[2965],
                  ycoordinate=[4720],
                  name="Bolivia",
                  continent="South America")
Chile = Country(xcoordinate=[2820, 3285, 2879],
                ycoordinate=[5375, 6524, 5998],
                name="Chile",
                continent="South America")
Argentina = Country(xcoordinate=[3076, 3336, 3264],
                    ycoordinate=[5606, 6542, 5986],
                    name="Argentina",
                    continent="South America")
Paraguay = Country(xcoordinate=[3288],
                   ycoordinate=[5039],
                   name="Paraguay",
                   continent="South America")
Uruguay = Country(xcoordinate=[3476],
                  ycoordinate=[5517],
                  name="Uruguay",
                  continent="South America")

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
Iceland.neighboring_countries.append("United Kingdom")
Iceland.neighboring_countries.append("Norway")
Iceland.neighboring_countries.append("Denmark")
United_Kingdom.neighboring_countries.append("France")
# United_Kingdom.neighboringcountries.append("Netherlands")
Norway.neighboring_countries.append("Netherlands")
Norway.neighboring_countries.append("Iceland")
Japan.neighboring_countries.append("Russia")
Japan.neighboring_countries.append("South Korea")
Japan.neighboring_countries.append("China")
Japan.neighboring_countries.append("United States")
China.neighboring_countries.append("South Korea")
China.neighboring_countries.append("Pakistan")
China.neighboring_countries.append("Taiwan")
China.neighboring_countries.append("Hong Kong")
China.neighboring_countries.append("Macao")
Taiwan.neighboring_countries.append("Hong Kong")
Taiwan.neighboring_countries.append("Philippines")
Australia.neighboring_countries.append("New Zealand")
Australia.neighboring_countries.append("Papua New Guinea")
Australia.neighboring_countries.append("Indonesia")
Australia.neighboring_countries.append("Chile")
Australia.neighboring_countries.append("Fiji")
Chile.neighboring_countries.append("Fiji")
Philippines.neighboring_countries.append("Indonesia")
Philippines.neighboring_countries.append("Mexico")
Philippines.neighboring_countries.append("Vietnam")
United_States.neighboring_countries.append("Japan")
United_States.neighboring_countries.append("United Kingdom")
United_States.neighboring_countries.append("Portugal")
United_States.neighboring_countries.append("Bahamas")

Canada.neighboring_countries.append("Denmark")
Canada.neighboring_countries.append("Ireland")
Madagascar.neighboring_countries.append("Australia")
Madagascar.neighboring_countries.append("Mozambique")
Madagascar.neighboring_countries.append("Comoros")
Madagascar.neighboring_countries.append("Mauritius")
Mozambique.neighboring_countries.append("Comoros")

South_Africa.neighboring_countries.append("Australia")
Namibia.neighboring_countries.append("Argentina")
Brazil.neighboring_countries.append("Angola")
Venezuela.neighboring_countries.append("Mauritania")
Venezuela.neighboring_countries.append("Trinidad and Tobago")
Venezuela.neighboring_countries.append("Cape Verde")
Mauritania.neighboring_countries.append("Cape Verde")

Philippines.neighboring_countries.append("Indonesia")
Saudi_Arabia.neighboring_countries.append("Sudan")
Saudi_Arabia.neighboring_countries.append("Egypt")

Morocco.neighboring_countries.append("Spain")
Algeria.neighboring_countries.append("France")
Libya.neighboring_countries.append("Italy")
Libya.neighboring_countries.append("Malta")
Italy.neighboring_countries.append("Malta")
Italy.neighboring_countries.append("Albania")

Turkey.neighboring_countries.append("Egypt")
Greece.neighboring_countries.append("Albania")
Serbia.neighboring_countries.append("Albania")

United_States.neighboring_countries.append("Cuba")
Cuba.neighboring_countries.append("Belize")
Cuba.neighboring_countries.append("Haiti")
Cuba.neighboring_countries.append("Bahamas")
Cuba.neighboring_countries.append("Jamaica")
Jamaica.neighboring_countries.append("Haiti")
Jamaica.neighboring_countries.append("Honduras")
Jamaica.neighboring_countries.append("Colombia")
Dominican_Republic.neighboring_countries.append("Venezuela")

India.neighboring_countries.append("Yemen")
Yemen.neighboring_countries.append("Somalia")
India.neighboring_countries.append("Maldives")
Sri_Lanka.neighboring_countries.append("Maldives")
Sri_Lanka.neighboring_countries.append("Indonesia")

Malaysia.neighboring_countries.append("Singapore")
Singapore.neighboring_countries.append("Indonesia")
Cyprus.neighboring_countries.append("Turkey")
Cyprus.neighboring_countries.append("Egypt")
Timor_Leste.neighboring_countries.append("Indonesia")
Bahrain.neighboring_countries.append("Qatar")
Saudi_Arabia.neighboring_countries.append("Qatar")
Saudi_Arabia.neighboring_countries.append("Bahrain")
Vietnam.neighboring_countries.append("Philippines")
Philippines.neighboring_countries.append("Vietnam")
Estonia.neighboring_countries.append("Finland")
United_Arab_Emirates.neighboring_countries.append("Iran")
Mauritius.neighboring_countries.append("Australia")
