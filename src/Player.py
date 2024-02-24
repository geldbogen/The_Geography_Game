from __future__ import annotations

import random
import tkinter as tk

from global_definitions import all_players, realgrey, white, all_categories_names_and_clusters, dictionary_attribute_name_to_attribute



from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from category import Category
    from country import Country


class Player:

    def __init__(self, color: tuple[int,int,int], name: str, reroll_number: int = 3):
        # name of the player
        self.name = name

        # color of the player (on the map)
        self.color : tuple[int,int,int] = color

        # a collection of the flags of the countries that player possesses
        self.labeldict : dict[Country,tk.Label]= dict()

        # a list of all countries the player currently controls
        self.list_of_possessed_countries: list[Country] = []

        # a list of all countries with gold, which the player currently controls
        self.list_of_possessed_countries_gold: list[Country] = []

        # a dictionary needed to translate between
        # the name of the player and the corresponding class
        all_players[self.name] = self

        # the number of rerolls the player has left
        self.rerolls_left = reroll_number

        self.gold : int = 0

    

    def check_if_attack_is_succesful(self,
                                     category: Category,
                                     country_a: Country,
                                     country_b: Country,
                                     ) -> str:

        local_attribute_a = country_a.dict_of_attributes[category.name]
        local_attribute_b = country_b.dict_of_attributes[category.name]

        if local_attribute_a.rank == -1 or local_attribute_b.rank == -1:
            if not category.treat_missing_data_as_bad:
                return 'no data'
            # treat missing data from here
            elif local_attribute_a.rank == local_attribute_b.rank:
                return 'draw'
            elif local_attribute_a.rank == -1:
                return 'loose'
            else:
                return 'win'

        if local_attribute_a.value == local_attribute_b.value:
            return 'draw'

        if local_attribute_a.rank < local_attribute_b.rank:
            if local_attribute_a.rank + 99 < local_attribute_b.rank:
                return 'hard defeat'
            else:
                return 'win'

        return 'loose'

    def get_random_attribute_with_cluster(self) -> Category:

        # get a random attribute name (including the name of a cluster)

        self.current_attributename_with_cluster : str = random.choice(
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
        
        return Category()
    def player_win_analysis(self, category: Category, peacemode: bool = False) -> dict[str, int]:
        """
        returns a dictionary in the form {'win' : 10, 'no data' : 1, 'draw' : 2, 'loose': 2} 
        (according to the outcome of the eventual attacks of a player)
        """

        returndict = {'win': 0, 'no data': 0, 'draw': 0, 'loose': 0}
        for country in self.list_of_possessed_countries:
            ansdict = country.win_analysis(category, peacemode=peacemode)

            returndict['win'] += ansdict['win']
            returndict['no data'] += ansdict['no data']
            returndict['draw'] += ansdict['draw']
            returndict['loose'] += ansdict['loose']

        return returndict


    def get_good_attribute(self, threshold: float = 0.25, at_least_one_win: bool = True, peacemode : bool = False) -> Category:

        is_good_attribute = False

        while (not is_good_attribute):

            current_attribute = self.get_random_attribute_with_cluster()
            is_good_attribute = True
            
            attack_analysis_dict = self.player_win_analysis(current_attribute,peacemode=peacemode)

            number_of_all_possible_attacks = sum(
                [value for _, value in attack_analysis_dict.items()])
            probability = float(
                attack_analysis_dict['win'] + attack_analysis_dict['draw']) / float(number_of_all_possible_attacks)
            threshold_condition = probability >= threshold

            is_good_attribute = is_good_attribute and threshold_condition
            is_good_attribute = is_good_attribute and not current_attribute.is_end_only

            if at_least_one_win:
                at_least_one_req = attack_analysis_dict['win'] >= 1
                is_good_attribute = is_good_attribute and at_least_one_req

        return current_attribute

        # # if the attribute is end only it should not be a valid attribute
        # if self.current_attribute.is_end_only:
        #     self.get_good_attribute()

        # for country in self.list_of_possessed_countries:
        #     # TODO: make it better if just some continents are chosen

        #     # simulate attacks in order to get an attribute, with which one can actually do something (to not frustrate players)
        #     for neighboring_country_string in list(
        #             set(country.neighboring_countries)):
        #         i += 1

        #         if self.check_if_attack_is_succesful(
        #                 self.current_attribute.name, country,
        #                 call_country_by_name(
        #                     neighboring_country_string)) == "no data":
        #             counter = counter + 1
        #             print(neighboring_country_string + " \n" + country.name)

        #         if self.check_if_attack_is_succesful(
        #                 self.current_attribute.name, country,
        #                 call_country_by_name(neighboring_country_string)) in [
        #                     "draw", "win"
        #         ]:
        #             if not call_country_by_name(
        #                     neighboring_country_string
        #             ) in self.list_of_possessed_countries:
        #                 at_least_one = True

        # print(float(counter) / float(i))
        # if float(counter) / float(i) > 0.25 or not at_least_one:
        #     print(self.current_attribute.name)
        #     print(
        #         "doesn't work because of the missing above we get a new attribute!"
        #     )
        #     self.get_good_attribute()
        # else:
        #     if self.current_attribute.number_of_chosen_already == 1:
        #         self.current_attribute.number_of_chosen_already = 0
        #         self.get_good_attribute()
        #     else:
        #         self.current_attribute.number_of_chosen_already += 1


def call_player_by_name(name: str) -> Player:
    for playername in all_players.keys():
        if playername == name:
            return all_players[playername]
    return mr_nobody


mr_nobody = Player(color = white, name="Nobody")
No_Data_Body = Player(color=realgrey, name="Nobody")
