import random
import tkinter as tk

from global_definitions import all_players, realgrey, all_categories_names_and_clusters, dictionary_attribute_name_to_attribute
from country import Country, call_country_by_name
from category import Category


class Player:

    def __init__(self, color: str, name: str, reroll_number: int = 3):
        # name of the player
        self.name = name

        # color of the player (on the map)
        self.color = color

        # a collection of the flags of the countries that player possesses
        self.labeldict = dict()

        # a list of all countries the player currently controls
        self.list_of_possessed_countries: list[Country] = []

        # a list of all countries with gold, which the player currently controls
        self.list_of_possessed_countries_gold: list[Country] = []

        # a dictionary needed to translate between
        # the name of the player and the corresponding class
        all_players[self.name] = self

        # the number of rerolls the player has left
        self.rerolls_left = reroll_number

    def reroll(self, to_update_category_label: tk.Label,
               to_update_reroll_button_label: tk.Label):
        if self.rerolls_left == 0:
            return None
        self.rerolls_left -= 1

        self.current_attribute = self.get_good_attribute()

        self.current_attribute.replace_A_and_B_in_category_name(to_update_category_label,
                                         )
        to_update_reroll_button_label.configure(
            text="rerolls left:\n " + str(self.active_player.rerolls_left))

    def attack_with_attribute(self,
                              attribute_name: str,
                              country_a: Country,
                              country_b: Country,
                              treat_missing_data_as_bad=False) -> str:

        local_attribute_a = country_a.dict_of_attributes[attribute_name]
        local_attribute_b = country_b.dict_of_attributes[attribute_name]

        if local_attribute_a.rank == -1 or local_attribute_b.rank == -1:
            if not treat_missing_data_as_bad:
                return 'no data'
            elif local_attribute_a.rank == local_attribute_b.rank:
                return 'no data'
            elif local_attribute_a.rank == -1:
                return 'True'
            else:
                return 'False'

        if local_attribute_a.value == local_attribute_b.value:
            return 'draw!'

        if local_attribute_a.rank < local_attribute_b.rank:
            if local_attribute_a.rank + 99 < local_attribute_b.rank:
                return 'hard defeat!'
            else:
                return 'True'
            
        return 'False'

    def get_random_attribute_with_cluster(self) -> Category:

        # get a random attribute name (including the name of a cluster)

        self.current_attributename_with_cluster = random.choice(
            all_categories_names_and_clusters)

        # if a cluster is chosen choose a random attribute from that cluster
        if len(dictionary_attribute_name_to_attribute[
                self.current_attributename_with_cluster]) > 1:
            return random.choice(dictionary_attribute_name_to_attribute[
                self.current_attributename_with_cluster])
        # if it is not a cluster, just return the attribute
        else:
            return dictionary_attribute_name_to_attribute[
                self.current_attributename_with_cluster][0]

    def get_good_attribute(self, counter: int = 0, i: int = 0) -> Category:
        i = 0
        counter = 0
        at_least_one = False
        self.current_attribute = self.get_random_attribute_with_cluster()

        # if the attribute is end only it should not be a valid attribute
        if self.current_attribute.is_end_only:
            self.get_good_attribute()

        for country in self.list_of_possessed_countries:
            # TODO:make it better if just some continents are chosen

            # simulate attacks in order to get an attribute, with which one can actually do something (to not frustrate players)
            for neighboring_country_string in list(
                    set(country.neighboring_countries)):
                i += 1

                if self.attack_with_attribute(
                        self.current_attribute.name, country,
                        call_country_by_name(
                            neighboring_country_string)) == "no data":
                    counter = counter + 1
                    print(neighboring_country_string + " \n" + country.name)

                if self.attack_with_attribute(
                        self.current_attribute.name, country,
                        call_country_by_name(neighboring_country_string)) in [
                            "draw", "True"
                        ]:
                    if not call_country_by_name(
                            neighboring_country_string
                    ) in self.list_of_possessed_countries:
                        at_least_one = True

        print(float(counter) / float(i))
        if float(counter) / float(i) > 0.25 or not at_least_one:
            print(self.current_attribute.name)
            print(
                "doesn't work because of the missing above we get a new attribute!"
            )
            self.get_good_attribute()
        else:
            if self.current_attribute.number_of_chosen_already == 1:
                self.current_attribute.number_of_chosen_already = 0
                self.get_good_attribute()
            else:
                self.current_attribute.number_of_chosen_already += 1

def call_player_by_name(name : str) -> Player:
    for playername in all_players.keys():
        if playername == name:
            return all_players[playername]
    return mr_nobody


mr_nobody = Player(color="white", name="Nobody")
No_Data_Body = Player(color=realgrey, name="Nobody")
