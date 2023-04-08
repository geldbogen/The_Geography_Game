import pandas as pd
import urllib
import requests
import os
import traceback
os.chdir("C:\\Users\juliu\Google Drive\Infoprojekte\The_Geography_Game")
bing_key="30b59034981d4e8292aed74ebcd97383"
bing_url="https://api.bing.microsoft.com/v7.0/images/search"

headers = {"Ocp-Apim-Subscription-Key" : bing_key}

def fetch_images(link,search_term:str=""):
    
    df=pd.read_csv(link)
    list_of_historical=df["2"].tolist()
    list_of_countries=df["0"].tolist()
    errorlist=list()
    link=link.lstrip("data/")
    link=link.rstrip(".csv")
    try:
        os.mkdir("pictures/attribute_pictures/" + link)
    except FileExistsError:
        pass
    for index,person in enumerate(list_of_historical):
        country=list_of_countries[index]
        if search_term=="":
            person2=person
        else:
            person2=person + " (" +search_term + ")" 
        try:
            params  = {"q": person2,"count":"10",}
            response=requests.get(bing_url,params=params,headers=headers)
            search_results = response.json()
            i=-1
            while i<10:
                i=i+1
                try:           
                    url=search_results["value"][i]["thumbnailUrl"]
                    filename="pictures/attribute_pictures/" + link  + "/" + person + ".jpg"
                    print(url)
                    urllib.request.urlretrieve(url,filename)
                except Exception as e:
                    print("error")
                    print(person)
                    traceback.print_exc()
                    if not person in errorlist:
                        errorlist.append(person)
                    continue
                else:
                    break
        except:
            # traceback.print_exc()
            if not person in errorlist:
                errorlist.append(person)
    with open("pictures/attribute_pictures/" + link +"/errorlist.txt","w") as f:
        for element in errorlist:
            try:
                f.write(element + "\n")
            except UnicodeEncodeError:
                index=list_of_historical.index(person)
                country=list_of_countries[index]
                f.write(country + "\n")
    

fetch_images("data/Number of wiki-languages of most famous battle which took place in that country (higher is better).csv")