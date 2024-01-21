import pandas as pd
import traceback
import alternative_names
def apply_bypopulation(df):
    def good_multiplication(a,b):
        if b==float(-1) or a==float(-1):
            return float(-1)
        else:
            return a*b
    df.sort_values(by=["0","1"],ascending=False)
    df.drop_duplicates(subset=["0"])    
    popdf=pd.read_csv("data/important/populationlist.csv")
    namelist=df["0"].tolist()
    valuelist=df["1"].tolist()
    popdf.set_index("0",inplace=True)
    new_namelist=list()
    new_valuelist=list()
    for real_country_name in alternative_names.countries_for_language_en:
        for country_name in alternative_names.not_reverse_countries_alternative_names[real_country_name]:
            if country_name in namelist:
                index=namelist.index(country_name)
                new_namelist.append(real_country_name)
                try:
                    new_valuelist.append(float(valuelist[index])/(popdf.loc[real_country_name]["1"]))
                except KeyError:
                    new_valuelist.append(float(-1))
                except TypeError:
                    new_valuelist.append(float(-1))
                break
    i=0
    current_max=0
    new_valuelist_copy=new_valuelist.copy()
    new_valuelist_copy=[item  for item in new_valuelist_copy if item!=float(-1)]
    while True:        
        i+=1
        N=sum([(1<=item and item<=10) for item in new_valuelist_copy])
        if N>=current_max:
            optimal_pop=10**i
            current_max=N
        if sum([(1<=item) for item in new_valuelist_copy])==len(new_valuelist_copy):
            break
        new_valuelist_copy=[10*item for item in new_valuelist_copy]


    mydf=pd.DataFrame({"0":new_namelist,"1":[good_multiplication(item,optimal_pop) for item in new_valuelist]})
    mydf.to_csv("abc (by "+format(optimal_pop,",") + " population).csv",index=False)
        # print(namelist)

    
    return float(-1)

def delete_numbers(string):
    numbers=["0","1","2","3","4","5","6","7","8","9"]
    for d in numbers:
        string=string.replace(d,"")
    return string
def delete_doubles(string):
    i=0
    l=len(string)//2
    mstring=string[l::]
    return mstring

def find_year_in_string(string):
    try:
        for i in range (len(string)):
            try:
                subwindow=string[i:i+4]
                i=0
                for char in subwindow:
                    if char.isdigit():
                        i+=1
                    else:
                        break
                if i==4:
                    return int(subwindow) 
            except IndexError:
                return string
    except TypeError:
        return string

def try_function(function,x):
    try:
        return function(x)
    except:
        return x

def try_int(x):
    try:
        return int(x)
    except:
        return x

def try_lstrip(x):
    try:
        return x.lstrip()
    except:
        return x
def try_rstrip(x):
    try:
        return x.rstrip()
    except:
        return x


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

def replace_credit_rating(string):
    ratings=["AAA","AA+","AA","AA-","A+","A","A-","BBB+","BBB","BBB-","BB+","BB","BB-","B+","B","B-","CCC+","CCC","CCC-","SD"]
    return ratings.index(string)+1

def use_coordinates(string:str) -> float:
    string2=string
    k=1
    try:
        if "S" in string:
            k=-1
        string=string.replace("°",".")
        string=string.replace("N","")
        string=string.replace("S","")
        string=string.replace("′","")
    except TypeError:
        traceback.print_exc()
        print(string2)
    try:
        return float(string)*k 
    except ValueError:
        print(string2)
        traceback.print_exc()
    except TypeError:
        traceback.print_exc()
        print(string2)
