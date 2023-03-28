from inspect import trace
from msilib.schema import File
import os
import pandas as pd
import requests
import traceback
import wikipedia
# import datenbereinigung as db
# import sparql_cleaner as sc
import os
filename=os.path.realpath(__file__).replace("\\","/")

wikipedia.set_user_agent("geogame-image-fetcher/1.0 (juliusniemeyer1995@gmail.com) python requests")

sparqllist=[\
"wd:Q889"\
,"wd:Q222"\
,"wd:Q262"\
,"wd:Q228"\
,"wd:Q916"\
,"wd:Q781"\
,"wd:Q414"\
,"wd:Q399"\
,"wd:Q408"\
,"wd:Q40"\
,"wd:Q227"\
,"wd:Q778"\
,"wd:Q398"\
,"wd:Q902"\
,"wd:Q244"\
,"wd:Q184"\
,"wd:Q31"\
,"wd:Q242"\
,"wd:Q962"\
,"wd:Q917"\
,"wd:Q750"\
,"wd:Q225"\
,"wd:Q963"\
,"wd:Q155"\
,"wd:Q921"\
,"wd:Q219"\
,"wd:Q965"\
,"wd:Q967"\
,"wd:Q1011"\
,"wd:Q424"\
,"wd:Q1009"\
,"wd:Q16"\
,"wd:Q929"\
,"wd:Q657"\
,"wd:Q298"\
,"wd:Q148"\
,"wd:Q739"\
,"wd:Q970"\
,"wd:Q974"\
,"wd:Q971"\
,"wd:Q800"\
,"wd:Q1008"\
,"wd:Q224"\
,"wd:Q241"\
,"wd:Q229"\
,"wd:Q213"\
,"wd:Q35"\
,"wd:Q977"\
,"wd:Q784"\
,"wd:Q786"\
,"wd:Q736"\
,"wd:Q79"\
,"wd:Q792"\
,"wd:Q983"\
,"wd:Q986"\
,"wd:Q191"\
,"wd:Q1050"\
,"wd:Q115"\
,"wd:Q712"\
,"wd:Q33"\
,"wd:Q142"\
,"wd:Q1000"\
,"wd:Q1005"\
,"wd:Q230"\
,"wd:Q183"\
,"wd:Q117"\
,"wd:Q41"\
,"wd:Q769"\
,"wd:Q774"\
,"wd:Q1006"\
,"wd:Q1007"\
,"wd:Q734"\
,"wd:Q790"\
,"wd:Q783"\
,"wd:Q28"\
,"wd:Q189"\
,"wd:Q668"\
,"wd:Q252"\
,"wd:Q794"\
,"wd:Q796"\
,"wd:Q27"\
,"wd:Q801"\
,"wd:Q38"\
,"wd:Q766"\
,"wd:Q17"\
,"wd:Q810"\
,"wd:Q232"\
,"wd:Q114"\
,"wd:Q710"\
,"wd:Q1246"\
,"wd:Q817"\
,"wd:Q813"\
,"wd:Q819"\
,"wd:Q211"\
,"wd:Q822"\
,"wd:Q1013"\
,"wd:Q1014"\
,"wd:Q1016"\
,"wd:Q347"\
,"wd:Q37"\
,"wd:Q32"\
,"wd:Q1019"\
,"wd:Q1020"\
,"wd:Q833"\
,"wd:Q826"\
,"wd:Q912"\
,"wd:Q233"\
,"wd:Q709"\
,"wd:Q1025"\
,"wd:Q1027"\
,"wd:Q96"\
,"wd:Q702"\
,"wd:Q217"\
,"wd:Q235"\
,"wd:Q711"\
,"wd:Q236"\
,"wd:Q1028"\
,"wd:Q1029"\
,"wd:Q836"\
,"wd:Q1030"\
,"wd:Q697"\
,"wd:Q837"\
,"wd:Q55"\
,"wd:Q664"\
,"wd:Q811"\
,"wd:Q1032"\
,"wd:Q1033"\
,"wd:Q423"\
,"wd:Q221"\
,"wd:Q20"\
,"wd:Q842"\
,"wd:Q843"\
,"wd:Q695"\
,"wd:Q219060"\
,"wd:Q804"\
,"wd:Q691"\
,"wd:Q733"\
,"wd:Q419"\
,"wd:Q928"\
,"wd:Q36"\
,"wd:Q45"\
,"wd:Q846"\
,"wd:Q218"\
,"wd:Q159"\
,"wd:Q1037"\
,"wd:Q763"\
,"wd:Q760 "\
,"wd:Q757 "\
,"wd:Q683"\
,"wd:Q238"\
,"wd:Q1039"\
,"wd:Q851"\
,"wd:Q1041"\
,"wd:Q403"\
,"wd:Q1042"\
,"wd:Q1044"\
,"wd:Q334"\
,"wd:Q214"\
,"wd:Q215"\
,"wd:Q685"\
,"wd:Q1045"\
,"wd:Q258"\
,"wd:Q884"\
,"wd:Q958"\
,"wd:Q29"\
,"wd:Q854"\
,"wd:Q1049"\
,"wd:Q730"\
,"wd:Q34"\
,"wd:Q39"\
,"wd:Q858"\
,"wd:Q865"\
,"wd:Q863"\
,"wd:Q924"\
,"wd:Q869"\
,"wd:Q574"\
,"wd:Q945"\
,"wd:Q678"\
,"wd:Q754"\
,"wd:Q948"\
,"wd:Q43"\
,"wd:Q874"\
,"wd:Q672"\
,"wd:Q1036"\
,"wd:Q212"\
,"wd:Q878"\
,"wd:Q145"\
,"wd:Q30"\
,"wd:Q77"\
,"wd:Q265"\
,"wd:Q686"\
,"wd:Q237"\
,"wd:Q717"\
,"wd:Q881"\
,"wd:Q805"\
,"wd:Q953"\
,"wd:Q954"\
]
sparqllist2=[
"wd:Q228",\
"wd:Q916",\
"wd:Q781",\
"wd:Q917",\
"wd:Q963",\
"wd:Q967",\
"wd:Q1011",\
"wd:Q929",\
"wd:Q657",\
"wd:Q970",\
"wd:Q971",\
"wd:Q977",\
"wd:Q792",\
"wd:Q983",\
"wd:Q1006",\
"wd:Q1007",\
"wd:Q710",\
"wd:Q819",\
"wd:Q1013",\
"wd:Q1019",\
"wd:Q1020",\
"wd:Q826",\
"wd:Q1027",\
"wd:Q702",\
"wd:Q697",\
"wd:Q695",\
"wd:Q691",\
"wd:Q846",\
"wd:Q763",\
"wd:Q757",\
"wd:Q1039",\
"wd:Q1042",\
"wd:Q685",\
"wd:Q958",\
"wd:Q863",\
"wd:Q574",\
"wd:Q945",\
"wd:Q678",\
"wd:Q874",\
"wd:Q672",\
"wd:Q686",\
"wd:Q237",\
"wd:Q953"
]
def read_errorlists(itemname):
    global sparqllist
    global sparqllist_indexerror
    global sparqllist_timeout
    try:
        with open("rawdata_with_fetcher/errorlist_indexerror_"+itemname+".txt","r") as f:
            sparqllist_indexerror=f.readlines()
            
    except FileNotFoundError:
        sparqllist_indexerror=[]

    sparqllist_indexerror=[item.replace("\n","") for item in sparqllist_indexerror]
    print(sparqllist_indexerror)
    try:
        with open("rawdata_with_fetcher/errorlist_prob_timeout_"+itemname+".txt","r") as f:
            sparqllist_timeout=f.readlines()
        
    except FileNotFoundError:
        traceback.print_exc()
        sparqllist_timeout=[]
    
    sparqllist_timeout=[item.replace("\n","") for item in sparqllist_timeout]

















def fetchitems(itemname,errorlist_index=False,errorlist_timeout=False):
    global sparqllist
    if errorlist_index:
        sparqllist=sparqllist_indexerror
    if errorlist_timeout:
        sparqllist=sparqllist_timeout
    countrylist=list()
    numberlist=list()
    itemlist=list()
    itemidlist=list()
    j=0
    errorlist=list()
    indexerrorlist=list()
    for item in sparqllist:
        print(item +"\n" +"Let's go \n\n\n\n")
        counter=0
        try:
            url = 'https://query.wikidata.org/sparql'
            query='''
            SELECT DISTINCT ?pageid ?novelist ?novelistLabel ?countryLabel ?sitelinks WHERE {
    
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            hint:Query hint:optimizer "None".
            
            VALUES ?country {'''+item+'''}
            
            wd:Q40050 ^wdt:P279*/^wdt:P31* ?novelist.
            ?novelist wdt:P495 ?country;
                      wikibase:sitelinks ?sitelinks
            }
            ORDER BY DESC(?sitelinks)
            LIMIT 50
            '''
            query2='''
            SELECT DISTINCT ?pageid ?novelist ?novelistLabel ?countryLabel ?sitelinks WHERE {
    
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            hint:Query hint:optimizer "None".
            
            VALUES ?country {'''+ item + '''}
            
            
            {?novelist wdt:P27 ?country;
                        wikibase:sitelinks ?sitelinks
            filter(?sitelinks>0)} 
            UNION
            {?novelist wdt:P19 [wdt:P17 ?country];
                        wikibase:sitelinks ?sitelinks.
            filter(?sitelinks>0)}
                    
            ?novelist wdt:P569 ?date.
            filter(YEAR(?date)>=2000)
            
            }
            ORDER BY DESC(?sitelinks)
            LIMIT 50
            '''
            query2 = '''
            SELECT DISTINCT ?pageid ?novelist ?novelistLabel ?countryLabel ?sitelinks WHERE {
    
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            hint:Query hint:optimizer "None".
            
            VALUES ?country {'''+ item + '''}
            
            
            {?novelist wdt:P27 ?country;
                        wikibase:sitelinks ?sitelinks
            filter(?sitelinks>30)} 
            UNION
            {?novelist wdt:P19 [wdt:P17 ?country];
                        wikibase:sitelinks ?sitelinks.
            filter(?sitelinks>30)}
                    
            wd:Q16727193 ^wdt:P279*/^wdt:P106 ?novelist
            
            }
            ORDER BY DESC(?sitelinks)
            LIMIT 50
            '''
            query2='''  
            SELECT DISTINCT ?novelist ?novelistLabel ?countryLabel ?sitelinks WHERE {
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } 
            VALUES ?country {'''+item+'''}
            wd:Q33506 ^wdt:P279*/^wdt:P31 ?novelist.
            ?novelist wdt:P17 ?country;
                        wikibase:sitelinks ?sitelinks.
            filter(?sitelinks>0)
            
            
            }
            ORDER BY DESC(?sitelinks)
            LIMIT 10
            '''
            
            
            query2='''
            SELECT ?pageid ?novelist ?novelistLabel (COUNT(?person) AS ?sitelinks) ?countryLabel WHERE {
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            VALUES ?country {''' + item + '''}
            {?person wdt:P27 ?country.}
            UNION
            {?person wdt:P19 [ wdt:P17 ?country]}
            ?person wdt:P569 ?dateofbirth.
            ?person wikibase:sitelinks ?real_sitelinks.
            
            filter(?real_sitelinks >0)
            filter(YEAR(?dateofbirth)>1900)
            }
            GROUP BY ?countryLabel ?pageid ?novelist ?novelistLabel
            '''
            query2='''
            SELECT DISTINCT ?novelist ?novelistLabel ?countryLabel ?sitelinks WHERE { 
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            hint:Query hint:optimizer "None".
                        VALUES ?country {'''+item+ '''}
                        ?novelist wdt:P17 ?country.
                        ?novelist wikibase:sitelinks ?sitelinks.    
                        filter(?sitelinks>70)
                        
                        
                        wd:Q811979 ^wdt:P279*/^wdt:P31 ?novelist
                        
            MINUS {?novelist wdt:P31 wd:Q1248784}
            MINUS {?novelist wdt:P31 wd:Q644371}
            }
            ORDER BY DESC(?sitelinks)
            
            
            '''
    	    
            query2='''
            SELECT DISTINCT ?pageid ?novelist ?novelistLabel ?countryLabel ?sitelinks WHERE {
    
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            hint:Query hint:optimizer "None".
            
            VALUES ?country {'''+item+ '''}
            
            ?novelist wdt:P159 [wdt:P17 ?country].
            ?novelist wdt:P17 ?country;
             wikibase:sitelinks ?sitelinks
            filter(?sitelinks>0) 
            
                    
            wd:Q46970 ^wdt:P279*/^wdt:P31 ?novelist
            
            }
            ORDER BY DESC(?sitelinks)
            LIMIT 200
            
            '''

            query2='''
            SELECT DISTINCT ?pageid ?novelist ?novelistLabel ?countryLabel ?sitelinks WHERE {
    
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            hint:Query hint:optimizer "None".
            
            VALUES ?country {'''+item+ '''}
            
            ?novelist wdt:P159 [wdt:P17 ?country].
            ?novelist wdt:P17 ?country;
             wikibase:sitelinks ?sitelinks
            filter(?sitelinks>50) 
            
                    
            wd:Q6881511 ^wdt:P279*/^wdt:P31 ?novelist
            MINUS {
            ?novelist wdt:P31 wd:Q46970
            }
            MINUS {
            ?novelist wdt:P31 wd:Q66344
            }
            
            }
            ORDER BY DESC(?sitelinks)
            LIMIT 200'''

            query2='''
            SELECT DISTINCT ?pageid ?novelist ?novelistLabel ?countryLabel ?sitelinks WHERE {
    
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            hint:Query hint:optimizer "None".
            
            VALUES ?country {'''+item+ '''}
            
            
            ?novelist wdt:P17 ?country;
             wdt:P1082 ?sitelinks
            filter(?sitelinks>200000)  
            
                    
            wd:Q515 ^wdt:P279*/^wdt:P31 ?novelist
            
            }
            ORDER BY DESC(?sitelinks)
            LIMIT 10
            '''
            query2='''
            SELECT DISTINCT ?novelist ?novelistLabel ?sitelinks ?countryLabel WHERE {
            hint:Query hint:optimizer "None".
            VALUES ?country {'''+item+ '''}
            ?novelist wdt:P17 ?country.
            ?novelist wikibase:sitelinks ?sitelinks.
            filter(?sitelinks>20)
            wd:Q35145263 ^wdt:P279*/^wdt:P31 ?novelist.
            ?novelist rdfs:label ?novelistLabel.
            filter(LANG(?novelistLabel)="en")
            ?country rdfs:label ?countryLabel.
            filter(LANG(?countryLabel)="en")
            }
            ORDER BY DESC(?sitelinks)
            '''


            query2='''
            SELECT ?countryLabel (COUNT(distinct *) as ?sumcompany) ?novelist ?novelistLabel  ?population (10000*xsd:float(?sumcompany)/xsd:float(?population) AS ?sitelinks) WHERE {
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            VALUES ?country {'''+item+ '''}
            ?company wdt:P19 ?novelist.
            ?novelist wdt:P17 ?country.
            wd:Q515 ^wdt:P279*/^wdt:P31 ?novelist.
            ?novelist wdt:P1082 ?population.
            filter(?population>100000)
            
            }
            GROUP BY ?novelistLabel ?sitelinks ?population ?countryLabel ?novelist
            ORDER BY DESC(?sitelinks)
            '''



            query2='''
            SELECT DISTINCT ?novelist ?novelistLabel ?sitelinks ?country ?countryLabel ?pointtime ?duration WHERE
            {
            hint:Query hint:optimizer "None".
            VALUES ?country {'''+ item + '''
            }
            {?novelist wdt:P276 [ wdt:P17 ?country]}
            UNION 
            {?novelist wdt:P17 ?country}
            UNION
            {?novelist wdt:P276 ?country}
            
            ?novelist wikibase:sitelinks ?sitelinks.
            filter(?sitelinks>0)
            
            {?novelist wdt:P585 ?pointtime
            OPTIONAL {?novelist wdt:P580 ?s_time.
            ?novelist wdt:P582 ?e_time.
            BIND(?e_time - ?s_time AS ?duration)}
            }
            UNION
            {?novelist wdt:P580 ?s_time.
            ?novelist wdt:P582 ?e_time.
            BIND(?e_time - ?s_time AS ?duration)
            }
            
            MINUS {?novelist wdt:P31/wdt:P279* wd:Q27020041}
            MINUS {?novelist wdt:P31 wd:Q82414}
            MINUS {?novelist wdt:P31 wd:Q159821}
            filter(YEAR(?pointtime)<2001 && YEAR(?pointtime)>1949 || (YEAR(?s_time)<2001 && YEAR(?s_time)>1949))
            filter(?duration<3 || !BOUND(?duration))
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            }
            ORDER BY DESC(?sitelinks)
            LIMIT 100
            
            
            
            '''

            # query='''
            # SELECT DISTINCT ?pageid ?novelist ?novelistLabel ?countryLabel ?sitelinks ?dateofbirth WHERE {
    
            # SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            # hint:Query hint:optimizer "None".

            # VALUES ?country {'''+ item + '''}


            # {?novelist wdt:P27 ?country.
            #             ?novelist wdt:P569 ?dateofbirth.
            # BIND(YEAR(?dateofbirth) AS ?sitelinks)
            #             filter(?sitelinks<1800)} 
            # UNION
            # {?novelist wdt:P19 [wdt:P17 ?country].
            #             ?novelist wdt:P569 ?dateofbirth.
            # BIND(YEAR(?dateofbirth) AS ?sitelinks)
            # filter(?sitelinks<2000)}

            

            # }
            # ORDER BY ASC(?dateofbirth)
            # LIMIT 20
            # '''

            #city with at most x inhabitants
            query2='''
            
            SELECT DISTINCT ?pageid ?novelist ?novelistLabel ?countryLabel ?sitelinks ?dateofbirth WHERE {
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            VALUES ?country {'''+ item +'''}
            
            ?novelist wdt:P17 ?country.
            ?novelist wikibase:sitelinks ?sitelinks.
            filter(?sitelinks>0)
            wd:Q702492 ^wdt:P279*/^wdt:P31 ?novelist.
            ?novelist wdt:P1082 ?population.
            filter(?population<1000000)
            
            
            }
            ORDER BY DESC(?sitelinks)
            LIMIT 100
            
            '''
            headers= {"User-Agent":"geogame-image-fetcher/1.0 (juliusniemeyer1995@gmail.com) python requests"}
            r = requests.get(url, params = {'format': 'json', 'query': query},headers=headers)
            data = r.json()
            for i in range(50):
                a=data["results"]["bindings"][i]["novelistLabel"]["value"]
                # a="--"
                b=data["results"]["bindings"][i]["countryLabel"]["value"]
                c=data["results"]["bindings"][i]["sitelinks"]["value"]
                d=data["results"]["bindings"][i]["novelist"]["value"]
                # d="--"
                print(b)
                print(a)
                print(c)
                print(d)
                itemlist.append(a)
                countrylist.append(b)
                numberlist.append(c)
                itemidlist.append(d)
                counter=1


        except Exception as e:
            print(e.__class__.__name__)
            print("\n\n\n\n")
            traceback.print_exc() 
            j=j+1
            print(j)
            if counter==0 and e.__class__.__name__=="IndexError":
                indexerrorlist.append(item)
            else:  
                if counter==0:
                    errorlist.append(item)


    da = {"country":countrylist, "number":numberlist, "item":itemlist, "item_id":itemidlist}
    df = pd.DataFrame(data=da)

    try:
        df_old=pd.read_csv("rawdata_with_fetcher/"+itemname+".csv")
        print(df_old)
        df=pd.concat([df_old,df],ignore_index=True)
        print(df_old)
        print("done")
        df_old.to_csv("rawdata_with_fetcher/"+ itemname+".csv",index=False)
    except FileNotFoundError:
        # traceback.print_exc()
        print("catched")
    print(df)
    df.to_csv("rawdata_with_fetcher/"+ itemname +".csv",index=False)


    try:
        os.remove("rawdata_with_fetcher/errorlist_indexerror_"+itemname+".txt")
    except FileNotFoundError:
        pass
    with open("rawdata_with_fetcher/errorlist_indexerror_"+ itemname+".txt","w") as f:
        for item in indexerrorlist:
            f.write(item +"\n")

    try:
        os.remove("rawdata_with_fetcher/errorlist_prob_timeout_"+itemname+".txt")
    except FileNotFoundError:
        pass
    with open("rawdata_with_fetcher/errorlist_prob_timeout_"+itemname+".txt","w") as f:
        for item in errorlist:
            f.write(item +"\n")

    print("the indexerrorlist now contains the following:")
    print(indexerrorlist)
    print("the prob_timeoutlist now contains the following:")
    print(errorlist)
    print("the keyword was the following:")
    print(itemname)

# read_errorlists("most_famous_person_after_2000") 
fetchitems("most_famous_drink")

