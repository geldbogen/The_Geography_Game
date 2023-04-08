from numpy import format_float_scientific
import pandas as pd
import datenbereinigung as db
import traceback
import wikipedia
import requests
import os
filename=os.path.realpath(__file__).replace("\\","/")



def fetch_pageid(path):
    pageidlist=list()
    new_itemlist=list()
    wikidata_descriptionlist=list()
    dataframe=pd.read_csv(path,index_col=False)
    wikidataidlist=dataframe["item_id"].tolist()
    wikidataidlist=["wd:" + item.replace("http://www.wikidata.org/entity/","") for item in wikidataidlist]
    print(wikidataidlist)
    dataframe["shortform"]=wikidataidlist
    i=0
    j=0
    while True:
        min=100*i
        i+=1
        max=100*i
        try:
            wikidataidlist[max]
        except:
            if j==1:
                break
            j+=1
            max=len(wikidataidlist)-1
        gigastring=""
        for item in wikidataidlist[min:max]:
            gigastring+=item+" "
        print(gigastring)
        url="https://query.wikidata.org/sparql"
        query= '''
        SELECT ?item ?pageid ?description WHERE {
        VALUES ?item {'''+gigastring + '''} 
  ?item schema:description ?description.
  filter(LANG(?description)="en")
        [ schema:about ?item ; schema:name ?name ;
        schema:isPartOf <https://en.wikipedia.org/> ]
        SERVICE wikibase:mwapi {
            bd:serviceParam wikibase:endpoint "en.wikipedia.org" .
            bd:serviceParam wikibase:api "Generator" .
            bd:serviceParam mwapi:generator "allpages" .
            bd:serviceParam mwapi:gapfrom ?name .
            bd:serviceParam mwapi:gapto ?name .
            ?pageid wikibase:apiOutput "@pageid" .
        }
    }
        '''
        headers= {"User-Agent":"geogame-image-fetcher/1.0 (juliusniemeyer1995@gmail.com) python requests"}
        r = requests.get(url, params = {'format': 'json', 'query': query},headers=headers)
        data = r.json()
        k=0
        while True:
            try:
                new_itemlist.append(data["results"]["bindings"][k]["item"]["value"])
                pageidlist.append(data["results"]["bindings"][k]["pageid"]["value"])
                wikidata_descriptionlist.append(data["results"]["bindings"][k]["description"]["value"])
                k+=1
            except IndexError:
                break
    print(pageidlist)
    print(new_itemlist)
    newdataframe=pd.DataFrame({"item_id":new_itemlist,"pageid":pageidlist,"wikidata_description":wikidata_descriptionlist})
    dataframe=pd.merge(dataframe,newdataframe, on="item_id",how="outer")
    dataframe=dataframe.drop_duplicates()
    print(dataframe)
    dataframe.to_csv(path,index=False)

def filter_for_words_in_wiki(path,wordlist,with_wikidatadesciription=True,countrycolumn="country",numbercolumn="number",pageidcolumn="pageid",wikidata_descritpioncolumn="wikidata_description"):
    def checkifvalid(wikisummary2,wikidatadescription,wordlist=wordlist,with_wikidatadesciription=with_wikidatadesciription):
        def check_if_string_is_first(smallstring,bigstring):
            if smallstring not in bigstring and bigstring!="":
                return False
            index1=bigstring.find(",")
            print(index1)
            if index1==-1:
                print("j")
                index1=99999999
            print(index1)
            index2=bigstring.find(" and")
            if index2==-1:
                index2=999999999
            index3=bigstring.find(smallstring)
            if index3==-1:
                return False
            else:
                if index3 <=min(index1,index2):
                    return True
                else:
                    return False
        

        firstyes=False
        for item in wordlist:
            if item in wikisummary2:
                firstyes=True
                break
        if not firstyes:
            return False
        if with_wikidatadesciription:
            for item in wordlist:
                if check_if_string_is_first(item,wikidatadescription) or wikidatadescription=="":
                    return True
            return False
        else:
            return True


    dataframe=pd.read_csv(path,index_col=False)
    newpath=path
    dataframe=dataframe.drop_duplicates()
    # dataframe.to_csv(newpath.replace("/","/backups_directly_after_fetching/"),index=False)
    dataframe=dataframe.sort_values(by=[countrycolumn,numbercolumn],ascending=[True,False],ignore_index=True,)
    i=-1
    temp=""
    temp2=""
    alreadyfound=False
    summarylist=list()
    wikiurllist=list()
    print(dataframe)
    while True:
        try:
            i+=1
            temp2=temp
            temp=dataframe.at[i,countrycolumn]
            pageid=dataframe.at[i,pageidcolumn]
            pageid=int(pageid)
            wikipage=wikipedia.page(pageid=pageid)
            wikidatadescription=dataframe.at[i,wikidata_descritpioncolumn]
            wikisummary=wikipage.summary
                        

            if temp2==temp and alreadyfound:
                wikiurllist.append("NNN")
                summarylist.append("NNN")
                continue
            else:
                alreadyfound=False
            wikisummary2=wikisummary.partition(".")[0]
            wikisummary2=db.allesinklammernlöschen(wikisummary2,"[","]")
            print(wikisummary2)
            print(wordlist)
            wikisummary3=wikisummary.partition(".")[0]+wikisummary.partition(".")[1]+wikisummary.partition(".")[2]
            if checkifvalid(wikisummary3,wikidatadescription):
                alreadyfound=True
                wikiurllist.append(wikipage.url)
                summarylist.append(wikisummary3)
            else:
                wikiurllist.append("NNN")
                summarylist.append("NNN")    
            print(wikiurllist[-1])
        except KeyError:
            traceback.print_exc()
            if i>2000:
                break
        except:
            traceback.print_exc()
            wikiurllist.append("--")
            summarylist.append("--")
            continue
    
    dataframe=dataframe.join(pd.DataFrame({"wikipedia_summary":summarylist,"wikipedia_url":wikiurllist}),how="outer")
    dataframe=dataframe[dataframe["wikipedia_url"]!="NNN"]
    try:
        dataframe.columns=list(range(len(dataframe.columns)))
    except:
        traceback.print_exc()
        print("ES HAT NICHT GEKLAPPT DAS DATAFRAME NEU ZU BENENNEN!!!!!!!!!!!!!!!!!!!!")
    dataframe.to_csv(path,index=False)      



def clean_everything(path,wordlist,extra_columns=[3,8,9],namecolumn=1,columnsconverttonumbers=[2],with_wikidatadescription=True):
    fetch_pageid(path)
    print("pageids fetched")
    filter_for_words_in_wiki(path,wordlist=wordlist,with_wikidatadesciription=with_wikidatadescription)
    print("filtered for words")
    df=pd.read_csv(path,index_col=False)
    mypath=path.replace("rawdata_with_fetcher/","")
    mypath="data/" + mypath
    db.cleancolumncountry(dataframe=df,extra_columns=extra_columns,namecolumn=namecolumn,columnstoconverttonumbers=columnsconverttonumbers,path=mypath)


# filter_for_words_in_wiki("rawdata_with_fetcher/buildings_by_countries_writer.csv",["novelist","poet"," writer","philosopher","dramatist","author","playwright"])
# fetch_pageid("rawdata_with_fetcher/most_famous_battle.csv")
filter_for_words_in_wiki("rawdata/female_singer.csv",wordlist=[""],with_wikidatadesciription=False)
# fetch_pageid("rawdata/person_after_2000.csv")
# clean_everything("rawdata_with_fetcher/")
