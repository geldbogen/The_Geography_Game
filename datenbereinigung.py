
from ast import Str
from audioop import reverse
from typing import final
from urllib.error import HTTPError
import pandas as pd
import os
from country_list import countries_for_language
import requests
import json
import wikipedia
import urllib.request
import requests
os.chdir("C:\\Users\juliu\Google Drive\Infoprojekte\geogame")
pd.options.display.max_rows = None
url="https://wikitable2json.com/api/Age_of_criminal_responsibility"
notimportanturl="https://wikitable2json.com/api/"
interestingurl=url
interestingurl=interestingurl.replace(notimportanturl,"")
WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='
bing_key="6abdffb72a6448eba9dd3dc37e1cf302"
bing_url="https://api.bing.microsoft.com/v7.0/images/search"

headers = {"Ocp-Apim-Subscription-Key" : bing_key}
search_term="Gandhi"



# for subdir, dirs, files in os.walk("data"):
#     for file in files:
#         filepath="data\\" + file
#         print(filepath)
#         dataframe=pd.read_pickle(filepath)
#         filepath2="data\\exceldata\\" + file +".csv"
#         dataframe.to_csv(filepath2)
#         print("yay")



  

countries_alternative_names={\
    "United Arab Emirates":["Arab Emirates"],\
    "Macao":["Macao SAR China","Macau","Macau *","Macau, China","Macau (China)"],\
    "Papua New Guinea":["New Guinea"],\
    "Republic of the Congo":["Congo (Brazzaville)","Congo","Republic of the Congo","Congo, Republic of the","Congo, Republic of","Congo-Brazzaville"],\
    "Democratic Republic of the Congo":["DR Congo *","Dr Congo","Congo DR","DR Congo *","Congo (Kinshasa)","DR Congo","Democratic Republic of Congo","Congo, Democratic Republic of the","Congo, Democratic Republic of","Zaire","Congo-Kinshasa"],\
    "Dominican Republic":["Dominican Rep."],\
    "Central African Republic":["Central Africa"],\
    "Eswatini":["Swaziland"],\
    "Equatorial Guinea":["Equ. Guinea"],\
    "São Tomé & Príncipe":["Sao Tome","São Tomé and Príncipe","São Tomé and Príncipe","São Tomé and Príncipe","São Tomé and Príncipe *","Sao Tome and Principe","Sao Tome and Prinicipe"],\
    "Trinidad & Tobago":["Trinidad/Tob.","Trinidad and Tobago"],\
    "Palestinian Territories":["Palestine","State of Palestine","Palestine (Gaza Strip)","Palestine"],\
    "Timor-Leste":["East Timor","East Timor *","East Timor","Timor-Leste"," East Timor"],\
    "United States":["the United States"],\
    "Czech Republic":["Czechia"],\
    "North Macedonia":["Macedonia"],\
    "Vatican City":["Vatican"],\
    "Curaçao":["Curacao"],\
    "Taiwan":["Republic of China"],\
    "Kyrgyzstan":["Kyrgyz Republic"],\
    "Côte d’Ivoire":["Côte d'Ivoire","Ivory Coast *","Ivory Coast","Cote d'Ivoire","Ivory Coast","Cote D Ivoire","Côte d'Ivoire","Côte d'Ivoire","Côte d'Ivoire","Cﾃｴte d'Ivoire"],\
    "South Korea":["Korea, Rep.","Republic of Korea","Korea, South"],\
    "United Kingdom":["England and Wales * [Note]", "England &  Wales"],\
    "Western Sahara":["Sahrawi Arab Democratic Republic"],\
    "Trinidad & Tobago":["Trinidad and Tobago"],\
    "Vietnam":["Vietnam","Viet Nam"],\
    "Myanmar":["Burma"],\
    "Antigua & Barbuda":["Antigua and Barbuda","British Leeward Islands"],\
    "Cape Verde":["Cape Verde","Cabo Verde"],\
    "Laos":["Laos","Lao People's Democratic Republic"],\
    "North Korea":["Korea, North","Democratic People's Republic of Korea"],\
    "Netherlands":["Kingdom of the Netherlands"]
    }




useless_countries=["Åland Islands","American Samoa","Andorra","Anguilla","Antarctica","Aruba","Bouvet Island","Caribbean Netherlands","Christmas Island","Cocos (Keeling) Islands",\
    "Faroe Islands","French Polynesia","French Southern Territories","Gibraltar","Guadeloupe","Guernsey","Jersey","Isle of Man","Marshall Islands","Martinique","Mayotte","Montserrat","New Caledonia",\
        "Niue","Norfolk Island","Northern Mariana Islands","Pitcairn Islands","Palau","Réunion","San Marino","Sint Maarten","Solomon Islands","South Georgia & South Sandwich Islands","St. Barthélemy","St. Helena",\
            "St. Kitts & Nevis","St. Lucia","St. Martin","St. Pierre & Miquelon","St. Vincent & Grenadines","Svalbard & Jan Mayen","Tokelau","Turks & Caicos Islands","Tuvalu","U.S. Outlying Islands","Wallis & Futuna","British Indian Ocean Territory","British Virgin Islands","Cayman Islands","French Guiana","Heard & McDonald Islands","U.S. Virgin Islands","Puerto Rico",\
                "Guam","Greenland","Falkland Islands","Bermuda","Cook Islands","Curaçao"]



r=requests.get(url)
data=json.loads(r.text)

countrynamelist=list()


# for person in list_of_historical:
#     print("go")
#     print(person)
#     downloader.download(person,limit=1,output_dir="dataset",timeout=60)





#eventuell alle "&" durch "and" ersetzen!!

for country in countries_for_language("en"):
    if country[1]=="Czechia":
        countrynamelist.append("Czech Republic")
        continue
    if country[1]=="Myanmar (Burma)":
        countrynamelist.append("Myanmar")
        continue
    if country[1]=="Bosnia & Herzegovina":
        countrynamelist.append("Bosnia and Herzegovina")
        continue
    if country[1]=="Hong Kong SAR China":
        countrynamelist.append("Hong Kong")
        continue
    if country[1]=="Macao SAR China":
        countrynamelist.append("Macao")
        continue
    if country[1]=="Congo - Brazzaville":
        countrynamelist.append("Republic of the Congo")
        continue
    if country[1]=="Congo - Kinshasa":
        countrynamelist.append("Democratic Republic of the Congo")
        continue
    countrynamelist.append(country[1])

def findyeardateinstring(string,number):
    output=""
    counter=0
    for character in string:
        if character.isnumeric():
            output=output+character
            counter=counter+1
        else:
            counter=0
            output=""
        if counter==number:
            return output
    pass



def get_wiki_image(search_term,index):
    
    try:
        correct_string=wikipedia.suggest(search_term)
        if correct_string==None:
            correct_string=search_term
        
        title=wikipedia.page(title=correct_string).title
        pageid=wikipedia.page(title=correct_string).pageid
        pageid=str(pageid)
        wikiurl="https://en.wikipedia.org/w/api.php?action=query&titles="+ title + "&prop=pageimages&format=json&pithumbsize=1000"
        response=requests.get(wikiurl)
        json_data=json.loads(response.text)
        print(json_data)
        try:
            return json_data["query"]["pages"][pageid]["thumbnail"]["source"]
        except KeyError:
            pass
        result=wikipedia.page(title=correct_string).images[index]
    except:
        result=0
    return result
    
def get_wiki_image_2(search_term):
    try:
        result = wikipedia.search(search_term, results = 1)
        wikipedia.set_lang('en')
        wkpage = wikipedia.WikipediaPage(title = result[0])
        title = wkpage.title
        response  = requests.get(WIKI_REQUEST+title)
        json_data = json.loads(response.text)
        img_link = list(json_data['query']['pages'].values())[0]['original']['source']
        return img_link        
    except:
        return 0

def fetch_images(link):
    df=pd.read_csv(link)
    list_of_historical=df["2"].tolist()
    errorlist=list()
    for person in list_of_historical:
        try:
            params  = {"q": person,"count":"10",}
            response=requests.get(bing_url,params=params,headers=headers)
            search_results = response.json()
            i=-1
            while i<10:
                i=i+1
                try:

                    url=search_results["value"][i]["thumbnailUrl"]
                    filename="picturedata/" + person +".jpg"
                    print(url)
                    urllib.request.urlretrieve(url,filename)
                except Exception as e:
                    print("error")
                    print(e.__traceback__)
                    print(e.text)
                    continue
                else:
                    break
        except:
            errorlist.append(person)
    with open("picturedata/errorlist.txt","wb") as f:
        for element in errorlist:
            f.write(element + "\n")
    
    # i=-1
    # try:
    #     while True:
            
    #         if "Bahraini" in person:
    #             break
    #         i=i+1
            
    #         print(person)
    #         print(type(person))
    #         person2=person + " (film)"
    #         url=get_wiki_image_2(person2)
    #         print(url)
    #         print(i)
    #         if url==0:
    #             errorlist.append(person)
    #             print("Error")
    #             break
    #         if ".svg" in url:
    #             continue
    #         else:
    #             
    #             print(len(requests.get(url).content))
    #             # with open(filename, 'w') as f:
    #             #     f.write(requests.get(url).content)
    #             
    #             print(os.path.getsize(filename))
    #             print("yay")
    #         break
    # except:
    #     errorlist.append(person)






def allesinklammernlöschen(string,startcharacter,endcharacter):
    try:
        output=""
        k=""
        for character in string:
            if character==startcharacter:
                k="stop"
            if character==endcharacter:
                k="go"
                continue
            if k=="stop":
                pass
            else:
                output=output + character
        return output
    except:
        return float(-1)

def most_common(lst):
    return max(set(lst), key=lst.count)

def cleancolumncountry(namecolumn,dataframe,columnstoconverttonumbers,bypopulation=False,byarea=False,killdoubles=False,killdoubles_column=0,extra_columns=[],path="data/"):
    def multiply_two(string,separator):
        try:
            x=string.split(separator)
            return float(x[0])*float(x[1])
        except:
            return float(string)

    
    
    def findpercentagenumberinstring(x):
        i=0
        k=0
        for i in range (len(x)):
            if x[i]=="%":
                k=i
                while (x[i] in ["%",",","."] or x[i].isdigit()) and i>=0:
                    i=i-1
                if i==len(x):
                    return x
                else:
                    return x[i+1:k]
        return x

    def findlongestfloatinstring(x):
        endstring=""
        k=0
        if x.isdigit():
            return x
        for character in x:
            if character.isdigit() or character in [",","."]:
                k=1
                endstring=endstring + character
            else:
                if k==1:
                    return endstring
        return endstring
    def tryconvertofloat(x):
        if isinstance(x,float):
            return x
        try:
            return float(x)
        except:
            print(x)
            print(type(x))
            print("float conversion negative")
            return float(-1)
    
    if killdoubles:
        pass
    



    dataframe.columns=range(len(dataframe.columns))


    # dataframe[namecolumn]=dataframe[namecolumn].apply(lambda x: str(x))
    # dataframe[namecolumn]=dataframe[namecolumn].apply(lambda x: x.replace(" *",""))
    # dataframe[namecolumn]=dataframe[namecolumn].apply(lambda x: allesinklammernlöschen(x,"(",")"))
    # dataframe[namecolumn]=dataframe[namecolumn].apply(lambda x: x.rstrip())


    global countrynamelist
    global countries_alternative_names
    global useless_countries
    countrynamelist2=countrynamelist.copy()
    additional=""
    zeroarray=[0]*dataframe.index
    dataframe["to_keepZZ"]=zeroarray
    for i in range(5000):
        try:
            for country in countrynamelist2:
                try:
                    alternativenames=countries_alternative_names[country]
                except Exception as e:
                    alternativenames=list()

                if country == dataframe.iloc[i,namecolumn]:
                    countrynamelist2.remove(country)
                    dataframe.at[i,"to_keepZZ"]=1
                    dataframe.at[i,namecolumn]=country
                    continue
                for name in alternativenames:
                    string=dataframe.iloc[i,namecolumn]
                    if name==string:
                        dataframe.iat[i,namecolumn]=country
                        countrynamelist2.remove(country)
                        dataframe.at[i,"to_keepZZ"]=1
                        dataframe.at[i,namecolumn]=country
        except Exception as e:
            continue
    for i in range(5000):
        try:
            for country in countrynamelist2:
                
                if country in dataframe.iloc[i,namecolumn]:
                    if country=="Niger" and "Nigeria" in dataframe.iloc[i,namecolumn]:
                        continue
                    if country=="Guinea" and "Guinea-Bissau" in dataframe.iloc[i,namecolumn]:
                        continue
                    if country=="Guinea" and "Equatorial Guinea" in dataframe.iloc[i,namecolumn]:
                        continue
                    if country=="Guinea" and "Papua New Guinea" in dataframe.iloc[i,namecolumn]:
                        continue
                    if country=="China" and "Taiwan" in dataframe.iloc[i,namecolumn]:
                        continue
                    if country=="China" and "Hong Kong" in dataframe.iloc[i,namecolumn]:
                        continue
                    if country=="China" and "Macao" in dataframe.iloc[i,namecolumn]:
                        continue

                    dataframe.iat[i,namecolumn]=country
                    countrynamelist2.remove(country)
                    dataframe.at[i,"to_keepZZ"]=1
                    
                    continue
        except:
            continue
    print("setupdone, those countries are not found:")
    dataframe=dataframe.loc[dataframe["to_keepZZ"]==1]
    for country in countrynamelist2:
        if not country in useless_countries:
            print(country)
    print("This is the number of countries which were not found:")
    print(len(set(countrynamelist2)-set(useless_countries)))
    for i in columnstoconverttonumbers:
        dataframe[i]=dataframe[i].apply(lambda x: str(x))
        # #dataframe[i]=dataframe[i].apply(lambda x: x.split("-")[0] if "-" in x)
        dataframe[i]=dataframe[i].apply(lambda x: x.rstrip(" sq km"))
        # dataframe[i]=dataframe[i].apply(lambda x: "-1" if x==None  else x)
        
        dataframe[i]=dataframe[i].apply(lambda x: x.replace(",",""))
        # dataframe[i]=dataframe[i].apply(lambda x: x.replace("$",""))
        # dataframe[i]=dataframe[i].apply(lambda x: x.replace("<",""))
        
        # dataframe[i]=dataframe[i].apply(lambda x: x.replace("k","A1000"))
        # dataframe[i]=dataframe[i].apply(lambda x: x.replace("K","A1000"))
        # dataframe[i]=dataframe[i].apply(lambda x: x.replace("M","A1000000"))
        # dataframe[i]=dataframe[i].apply(lambda x: multiply_two(x,"A"))
        # dataframe[i]=dataframe[i].apply(lambda x : x.replace("LHT","1"))
        # dataframe[i]=dataframe[i].apply(lambda x: x.replace("RHT","0"))
        # dataframe[i]=dataframe[i].apply(lambda x: "-1" if x=="N/A" else x)
        # # dataframe[i]=dataframe[i].apply(lambda x: "x[0,1,2]" if "-" in x else x)
        # # dataframe[i]=dataframe[i].apply(lambda x: "-1" if x=="—" else x)
        # # dataframe[i]=dataframe[i].apply(lambda x: "-1" if x=="–" else x)
        
        # dataframe[i]=dataframe[i].apply(lambda x: "-1" if x=="" else x) 
        # dataframe[i]=dataframe[i].apply(lambda x: "-1" if x=="Barley production(tonnes)" else x)
        # dataframe[i]=dataframe[i].apply(lambda x: allesinklammernlöschen(x,startcharacter="(",endcharacter=")"))
        dataframe[i]=dataframe[i].apply(lambda x: allesinklammernlöschen(x,startcharacter="[",endcharacter="]"))
        # dataframe[i]=dataframe[i].apply(lambda x: x if len(x)<=3 else findyeardateinstring(x,4))
        # dataframe[i]=dataframe[i].apply(lambda x: "-1" if x==''  else x)
        # dataframe[i]=dataframe[i].str.rstrip("%").astype(float)
        
        # dataframe[i]=dataframe[i].apply(lambda x: findpercentagenumberinstring(x))
        # dataframe[i]=dataframe[i].apply(lambda x: findlongestfloatinstring(x))
        dataframe[i]=dataframe[i].apply(lambda x: tryconvertofloat(x))
        pass

    if bypopulation:
        countrynamelist3=countrynamelist.copy()
        countrylist=list()
        datalist=list()
        factorlist=list()
        populationdata=pd.read_csv("data/List_of_countries_and_dependencies_by_population.csv")
        populationdata.columns=range(len(populationdata.columns))
        print(populationdata)
        for i in columnstoconverttonumbers:
            print(countrynamelist3)
            for country in countrynamelist3:
                try: 
                    data=dataframe[dataframe[namecolumn]==country]
                    population=populationdata[populationdata[0]==country]
                    if data.iloc[0,i] in [float(-1),float(0)]:
                        countrylist.append(country)
                        datalist.append(data.iloc[0,i])
                        continue
                    factor=dividenumbers(data.iat[0,i],population.iat[0,1])
                    datalist.append(factor[0])
                    factorlist.append(factor[1])
                    countrylist.append(country)
                except Exception as e:
                    print(e)
                    print(country + " FAIL")
                    datalist.append(float(-1))
                    countrylist.append(country)
        
        finalfactor=most_common(factorlist)
        dataframe=pd.DataFrame({0:countrylist,1:datalist})
        additional=" (by " +str(finalfactor) + " population)"
        dataframe[1]=dataframe[1].apply(lambda x: float(-1) if x==float(-1) else x*finalfactor)

    if byarea:
        countrynamelist4=countrynamelist.copy()
        countrylist=list()
        datalist=list()
        factorlist=list()
        populationdata=pd.read_csv("data/List_of_countries_and_dependencies_by_area.csv")
        for i in columnstoconverttonumbers:
            for country in countrynamelist4:
                try:
                    data=dataframe[dataframe[namecolumn]==country]
                    population=populationdata[populationdata[0]==country]
                    if data.iloc[0,i] in [float(-1),float(0)]:
                        countrylist.append(country)
                        datalist.append(data.iloc[0,i])
                        continue
                    factor=dividenumbers(data.iloc[0,i],population.iloc[0,1])
                    datalist.append(factor[0])
                    factorlist.append(factor[1])
                    countrylist.append(country)
                except Exception as e:
                    #print(traceback.print_exception())
                    # print(traceback.format_exc())
                    # print(str(e))
                    # print(e)
                    # print(country[1] + "FAIL")
                    datalist.append(float(-1))
                    countrylist.append(country)

        finalfactor=most_common(factorlist)
        dataframe=pd.DataFrame({0:countrylist,1:datalist})
        additional=" (by " +str(finalfactor) + " km^2)"
        dataframe[1]=dataframe[1].apply(lambda x: float(-1) if x==float(-1) else x*finalfactor)

    savelist=[namecolumn]+columnstoconverttonumbers+extra_columns
    if byarea or bypopulation:
        savelist=[0,1]
    columns=list(range(len(dataframe.columns)))
    dataframe.reindex(columns=columns)
    print(savelist)
    dataframe=dataframe[savelist]
    dataframe.columns=list(range(len(savelist)))
    saveurl=path
    dataframe.to_csv(saveurl)
    print(dataframe)




def dividenumbers(number1,number2):
    i=0
    d=float(number1/number2)
    
    while not 1 < d < 10:
        d=d*10
        i=i+1
        print(i)
    return [float(number1/number2),10**i]
    



# print("hey")
# df=pd.DataFrame(data[0])
# df=pd.read_csv("rawdata/prostitution_by_capita.csv")
# print(df)






# df2=pd.read_csv("rawdata/people_in_Oceania.csv")
# df3=pd.read_csv("rawdata/people_in_North_America.csv")
# df4=pd.read_csv("rawdata/people_in_South_America.csv")
# df5=pd.read_csv("rawdata/people_in_Asia.csv")
# df6=pd.read_csv("rawdata/people_in_Europe.csv")


# df=df.append(df2)     
# df=df.append(df3)
# df=df.append(df4)
# df=df.append(df5)
# df=df.append(df6)

# df.columns=range(len(df.columns))



# df.sort_values(by=2,inplace=True,ignore_index=True,ascending=False)
# df.drop_duplicates(subset=[2],inplace=True,ignore_index=True)
# print(len(df))


#df.columns=[0,1,2]
#df=df[:-15]
#print(df.iloc[177][0])

# cleancolumncountry(0,df,[1])




# df=df[1:]
# namelist=list()
# airline_namelist=list()
# number_of_airlines=list()
# for country in countries_for_language("en"):
    
#     countryname=country[1].replace(" ","_")
#     url="https://wikitable2json.com/api/List_of_airlines_of_" + countryname
#     print(countryname)
#     try:
#         s=""
#         r=requests.get(url)
#         data=json.loads(r.text)
#         df=pd.DataFrame(data[0]["data"])
#         if len(df.index)==1:
#             print("YWS")
#             newdf=pd.DataFrame(data[1]["data"])
#             df=newdf
#         if len(df.index)==1:
#             print("YWS")
#             newdf=pd.DataFrame(data[2]["data"])
#             df=newdf
#         print("\n\n\n\n")
#         df=df[1:]
#         print(df)
#         airline_names=df[0].tolist()

#         for name in airline_names:
#             s=s+name +","
#         print(s)
#         namelist.append(countryname)
#         airline_namelist.append(s)
#         number_of_airlines.append(len(airline_names))
#         print(namelist)
#         print(airline_namelist)
#     except:
#         print("HAHAHAHAHAH")
    
# cdf=pd.DataFrame({0:namelist,1:airline_namelist,2:number_of_airlines})


#cleancolumncountry(0,df,[2])
# df=pd.read_csv("")
#df.columns=[0,1,2,3]


#cleancolumncountry(0,df,[3])
#print(df)

# df=df[3:]


#print(df)