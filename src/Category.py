import tkinter as tk

from global_definitions import (
    all_categories, all_categories_names_and_clusters,
      dictionary_attribute_name_to_attribute, category_to_displayed_name_dict,
      category_to_displayed_extra_information_category)

import country


class Category:

    def __init__(self,
                 name: str,
                 is_active: bool,
                 treat_missing_data_as_bad: bool,
                 difficulty: int,
                 explanation: str = "",
                 cluster: str = "",
                 is_end_only: bool = False):
        

        # the name of the category
        self.name = name

        # whether a category is active, i.e. whether the player
        # can "guess" before taking a move in order to get a free turn
        self.is_active = is_active

        # In order to prevent that the same category is chosen too often,
        # a counter which tracks how often a category has already been chosen
        self.number_of_chosen_already = 0

        # whether the category is a "treat missing data as a loss" - category
        self.treat_missing_data_as_bad = treat_missing_data_as_bad

        # the difficulty on the category on a scale of 1 (easiest) to 5 (hardest)
        self.difficulty = difficulty

        # if provided, an explanation, which gives some details on the category (what it exactly means, the source etc.)
        self.explanation = explanation

        # whether a category is only used as a target attribute
        # for the end of game and can not appear in the normal flow of the game
        # (usually because it is too easy)
        self.is_end_only = is_end_only

        # append the global list of all categories with this instance.
        all_categories.append(self)

        # if there is a real cluster
        if not cluster == "":
            # append the name of cluster in the namelist.
            # One can specify the probabily of choosing this cluster by appending it multiple times.
            if not cluster in all_categories_names_and_clusters:
                # here one can tune the probability of choosing the specific cluster
                # set it as 5/number of attribute
                for i in range(5):
                    all_categories_names_and_clusters.append(cluster)

            try:
                # map clustername to the list of categories it refers to
                dictionary_attribute_name_to_attribute[cluster].append(self)

                # map categoryname to single item list of corresponding class
                dictionary_attribute_name_to_attribute[self.name] = [self]

            except KeyError:
                # map clustername to the list of categories it refers to
                dictionary_attribute_name_to_attribute[cluster] = [self]

                # map categoryname to single item list of corresponding class
                dictionary_attribute_name_to_attribute[self.name] = [self]

        else:
            # add category name to list of category namesi
            all_categories_names_and_clusters.append(self.name)

            # map categoryname to single item list of corresponding class
            dictionary_attribute_name_to_attribute[self.name] = [self]

    def replace_A_and_B_in_category_name(self, tk_label: tk.Label,
                                         first_country: country.Country = None,
                                         second_country: country.Country = None) -> tk.Label:

        categoryname = self.name.rstrip(".csv")
        try:
            displaystring = category_to_displayed_name_dict[categoryname]
            if (displaystring in ["", "TODO"]):
                displaystring = categoryname + " (TODO)"
        except KeyError:
            displaystring = categoryname + " (ERROR)"

        if (second_country == None):
            displaystring = displaystring.replace("CountryB", " (...) ")
        else:
            displaystring = displaystring.replace(
                "CountryB", second_country.name)

        if (first_country == None):
            displaystring = displaystring.replace("CountryA", " (...) ")
        else:
            displaystring = displaystring.replace(
                "CountryA", first_country.name)

        extra_information_displayed = ""

        try:
            if (category_to_displayed_extra_information_category[categoryname] ==
                    "person"):
                extra_information_displayed = "\n (citizenship or birthplace in the current territory of the country)"
            if (category_to_displayed_extra_information_category[categoryname] ==
                    "historical event"):
                extra_information_displayed = "\n (took place in the current territory of the country)"
        except KeyError:
            pass

        displaystring += extra_information_displayed

        # TODO: append guessing hint

        # guessing_hint = ""
        # try:
        #     guessing_hint = " \n (guess the "+ +")"
        # except KeyError:
        #     pass

        # displaystring+= guessing_hint

        tk_label.configure(text=displaystring)

        return tk_label
