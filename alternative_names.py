import pandas as pd
p=pd.read_csv("data/important/countrylist.csv",index_col=False,keep_default_na=False)
countries_for_language_en=p.values.tolist()
countries_for_language_en=[item[1] for item in countries_for_language_en]

countries_alternative_names={\
    "United Arab Emirates":["Arab Emirates","UAE","UA Emirates"],\
    "Macao":["China, Macao SAR","Macao SAR China","Macau","Macau *","Macau, China","Macau (China)"],\
    "Papua New Guinea":["New Guinea","Papua N.G."],\
    "Republic of the Congo":["R. of Congo","Congo-Brazzaville","Congo (Brazzaville)","Congo","Republic of the Congo","Congo, Republic of the","Congo, Republic of"],\
    "Democratic Republic of the Congo":["Congo, D. R.","Congo-Kinshasa","DR Congo *","Dr Congo","Congo DR","DR Congo *","Congo (Kinshasa)","DR Congo","Democratic Republic of Congo","Congo, Democratic Republic of the","Congo, Democratic Republic of"],\
    "Dominican Republic":["Dominican Rep.","Domin. Rep."],\
    "Central African Republic":["Central Africa","C.A. Republic"],\
    "Eswatini":["Swaziland"],\
    "Equatorial Guinea":["Equ. Guinea"],\
    "São Tomé & Príncipe":["Sao Tome","São Tomé and Príncipe","São Tomé and Príncipe","São Tomé and Príncipe","São Tomé and Príncipe *","Sao Tome and Principe","Sao Tome and Prinicipe"],\
    "Trinidad and Tobago":["Trinidad/Tob.","Trinidad and Tobago","Trinidad & Tobago","Tr.&Tobago"],\
    "Palestine":["Palestine","State of Palestine","Palestine (Gaza Strip)","Palestine","Palestinian Territories"],\
    "Timor-Leste":["Timor Leste","East Timor","East Timor *","East Timor","Timor-Leste"," East Timor"],\
    "United States":["the United States","US","USA","United States of America"],\
    "Czech Republic":["Czechia","Czech Republic"],\
    "North Macedonia":["Macedonia"],\
    "Vatican City":["Vatican"],\
    "Curaçao":["Curacao"],\
    "Taiwan":["Republic of China"],\
    "Kyrgyzstan":["Kyrgyz Republic"],\
    "Ivory Coast":["Côte d’Ivoire","Côte d’Ivoire","Côte d’Ivoire","Côte d'Ivoire","Ivory Coast *","Ivory Coast","Cote d'Ivoire","Ivory Coast","Cote D Ivoire","Côte d'Ivoire","Côte d'Ivoire","Côte d'Ivoire","Cﾃｴte d'Ivoire"],\
    "South Korea":["Korea, Rep.","Republic of Korea","Korea, South"],\
    "United Kingdom":["England and Wales * [Note]", "England &  Wales","UK"],\
    "Western Sahara":["Sahrawi Arab Democratic Republic"],\
    "Vietnam":["Vietnam","Viet Nam"],\
    "Myanmar":["Burma"],\
    "Antigua & Barbuda":["Antigua and Barbuda"],\
    "Cape Verde":["Cape Verde","Cabo Verde"],\
    "Laos":["Laos","Lao People's Democratic Republic"],\
    "North Korea":["Dem. People's Republic of Korea","Korea, North","Democratic People's Republic of Korea"],\
    "Netherlands":["Kingdom of the Netherlands"],\
    "China":["People's Republic of China"],\
    "Ireland":["Republic of Ireland"],\
    "Turkey":["Republic of Turkey"],\
    "Brunei":["Brunei Darussalam"],\
    "Gambia":["The Gambia"],\
    "Russia":["Russian Federation"],\
    "Hong Kong":["China, Hong Kong SAR"],\
    "Moldova":["Republic of Moldova"],\
    "Syria":["Syrian Arab Republic"],\
    "Iran":["Iran (Islamic Republic of)"],\
    "Tanzania":["United Republic of Tanzania"],\
    "Venezuela":["Venezuela (Bolivarian Republic of)"],\
    "Bolivia":["Bolivia (Plurinational State of)"]
    
    }
reverse_countries_alternative_names=dict()
for item in countries_alternative_names.keys():
    countries_alternative_names[item].append(item)    
not_reverse_countries_alternative_names=countries_alternative_names.copy()
for country in countries_for_language_en:
    try:
        not_reverse_countries_alternative_names[country].append(country)
    except KeyError:
        not_reverse_countries_alternative_names[country]=[country]
for mlist in countries_alternative_names.values():
    for key in countries_alternative_names.keys():
        if countries_alternative_names[key]==mlist:
            for item in mlist:
                reverse_countries_alternative_names[item]=key

# for item in countries_for_language_en:
#     reverse_countries_alternative_names[item]=item

