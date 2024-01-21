
from ast import Str
from tokenize import String
import traceback
import pandas as pd
pd.set_option('display.max_rows', None)
import os

os.chdir("C:\\Users\juliu\Google Drive\Infoprojekte\geogame")

def replace(string):
    if type(string)==str:
        string=string.replace("/","-")
        string=string.replace("\\","")
        string=string.replace("?","")
        string=string.replace("*","")
        string=string.replace(":","")
        string=string.replace("<","")
        string=string.replace(">","")
        string=string.replace("|","-")
        string=string.replace("Cﾃｴte d・E・EIvoire","Ivory Coast")
        string=string.replace("・Eｾ・E・Eｽ｣","a")
        string=string.replace("・EEｾ・EE・EEｽｧ","c")
        string=string.replace("・EEｾ・EE・EEｽｶ","oe")
        string=string.replace("・EEｾ・EE・EEｽｼ","ue")
        string=string.replace("・EEｾ・EE・EEｽｺ","u")
        string=string.replace("・EEｾ・EE・EEｽ｣","a")
        string=string.replace("・EEｾ・EE・EEｽ｡","a")
        string=string.replace("・EEｾ・EE・EEｽｩ","e")
        string=string.replace("・EEｾ・EE・EE・EEｻ","O")
        string=string.replace("・EEｾ・EE・EE・EEｻ","・EEｾ・EE・EE・EEｻ")
        string=string.replace("・・ｻﾂ・・ｻ","-")
        string=string.replace("・ｾ・・・ｻ","o")
        string=string.replace("・Eｾ・E・Eｽｩ","e")
        string=string.replace("・Eｾ・E・Eｽｭ","i")
        string=string.replace("・Eｾ・E・Eｽｨ","e")
        string=string.replace("・Eｾ・E・Eｽｳ","o")
        string=string.replace("・Eｾ・E・Eｽ｡","a")
        string=string.replace("・ｾ・・ｽｺ","u")
        string=string.replace("・ｾ・・ｽｫ","e")
        string=string.replace("ﾃｱ","n")
        string=string.replace("ﾃｺ","u")
        string=string.replace("ﾈ・E","s")
        string=string.replace("ﾅｫ","u")
        string=string.replace("ﾃｰ","d")
        string=string.replace("ﾃｫ","e")
        string=string.replace("・Eｾ・E・E・EｻE","c")
        string=string.replace("・ｾ・・ｽｰ","d")
        string=string.replace("ﾄ・EE","c")
        string=string.replace("・E・E","")
        string=string.replace("ﾃ､","ae")
        string=string.replace("ﾅ・E","o")
        string=string.replace("ﾅ","s")
        string=string.replace("ﾅｾ","z")
        string=string.replace("ﾇ・E"," ")
        string=string.replace("ﾄ・E","c")
        string=string.replace("ﾅ｡","s")
        string=string.replace("ﾄｰ","I")
        string=string.replace("ﾄｱ","i")
        string=string.replace("ﾅｽ","Z")
        string=string.replace("ﾃｨ","e")
        string=string.replace("ﾊｻ","")
        string=string.replace("ﾃｼ","ue")
        string=string.replace("ﾃ｡","a")
        string=string.replace("ﾃ・E","O")
        string=string.replace("ﾃｧ","c")
        string=string.replace("ﾃ｣","a")
        string=string.replace("ﾃｩ","e")
        string=string.replace("ﾃｭ","i")
        string=string.replace("ﾃｶ","oe")
        string=string.replace("ﾃｸ","o")
        string=string.replace("ﾃｳ","o")
        string=string.replace("ﾄｫ","i")
        string=string.replace("ﾃ｢","a")
        string=string.replace("ﾃｯ","i")
        string=string.replace("ﾃｽ","y")
        string=string.replace("・ｾ・・ｽｦ","ae")
        
    else:
        
        pass
    return string
for dirs, subdirs, files in os.walk("data_correction"):
    for file in files:
        try:
            print(file)
            dataframe=pd.read_csv("data_correction/" + file)
            if "novelist" in file:
                print(dataframe)
            try:
                print(dataframe.iloc[165+21])
            except:
                pass
            i=0
            while True:
                try:
                    dataframe.iloc[:,i]=dataframe.iloc[:,i].map(lambda x: replace(x))
                    i=i+1
                except:
                    print(i)
                    print("fail")
                    break
            dataframe.to_csv("data_correction/" + file,index=False)
        except:
            traceback.print_exc()
            pass
