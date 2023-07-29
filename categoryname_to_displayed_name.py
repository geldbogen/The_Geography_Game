# A dictionary which translates the categorynames how they are displayed at the beginning of the game 
# and internally to how they should be displayed during the game
# BBBB stands for text, which will be displayed in bold, IIII stands for text, to which 'more information' exists 

import pandas as pd

df = pd.read_csv("categoryname_to_displayed_sentences.csv")
df = df.fillna("")
category_to_displayed_name_dict = df.set_index("original categorynames")["how categorynames should look"].to_dict()
category_to_displayed_guess_hint = df.set_index("original categorynames")["guessing extra"].to_dict()
category_to_displayed_extra_information_category = df.set_index("original categorynames")["extra information category"].to_dict()

print(category_to_displayed_guess_hint)