from __future__ import annotations

import random
import tkinter as tk

from global_definitions import (
    all_players,
    realgrey,
    white,
    dictionary_attribute_name_to_attribute,
    all_categories_names_and_clusters,
)



from typing import TYPE_CHECKING, Literal
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

        # only relevant for the gold mode
        self.gold : int = 0

    

    def check_if_attack_is_succesful(self,
                                     category: Category,
                                     country_a: Country,
                                     country_b: Country,
                                     ) -> Literal['no data', 'draw', 'win', 'loose', 'hard defeat']:
        """
        Determines if an attack is successful based on comparing attributes of two countries.
        This method compares the specified category attribute between country_a and country_b
        and returns the outcome of the attack.
        Parameters:
            category (Category): The category to compare between countries.
            country_a (Country): The attacking country.
            country_b (Country): The defending country.
        Returns:
            str: The result of the attack, which can be one of:
                - 'no data': If data is missing in either of the two countries (and missing data is not treated as bad).
                - 'draw': If both countries have equal attribute values.
                - 'win': If country_a's rank is better than country_b's rank.
                - 'loose': If country_a's rank is worse than country_b's rank.
                - 'hard defeat': If country_a's rank is significantly better (99+ ranks difference).
        Note:
            The ranking system is assumed to be where lower rank numbers are better.
            A rank of 0 indicates missing data for that attribute.
        """
        local_attribute_a = country_a.dict_of_attributes[category.name]
        local_attribute_b = country_b.dict_of_attributes[category.name]

        if local_attribute_a.rank == 0 or local_attribute_b.rank == 0:
            if not category.treat_missing_data_as_bad:
                return 'no data'
            
            # treat missing data from here
            elif local_attribute_a.rank == local_attribute_b.rank:
                return 'draw'
            elif local_attribute_a.rank == 0:
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

    def get_random_attribute_with_cluster(self, list_of_clusters : list[str] = []) -> Category:
        """
        Selects a random attribute from a randomly chosen cluster in the provided list.
        This method first randomly selects a cluster name from the provided list of clusters,
        then returns a random attribute from that cluster using the dictionary mapping
        cluster names to attributes.
        Args:
            list_of_clusters (list[str], optional): List of cluster names to choose from.
                Defaults to an empty list.
        Returns:
            Category: A random attribute from the randomly selected cluster.
        Note:
            Sets self.current_clustername as a side effect.
        """

        # get a random attribute name (including the name of a cluster)
        self.current_clustername : str = random.choice(
            list_of_clusters)
        return random.choice(dictionary_attribute_name_to_attribute[
            self.current_clustername])

  
        
    def player_win_analysis(self, category: Category, peacemode: bool = False) -> dict[str, int]:
        """
        Returns a dictionary in the form {'win' : 10, 'no data' : 1, 'draw' : 2, 'loose': 2} 
        (according to the outcome of the eventual attacks of a player)

        Utilizes the win_analysis method of the countries the player possesses.

        PARAMS:
            category (Category): The attribute with which the player wants to attack.
            peacemode (bool): If True, the player cannot attack countries which are possessed by other players.

        RETURNS:
            dict[str, int]: A dictionary with the number of wins, draws, losses and no data outcomes.
        """

        returndict = {'win': 0, 'no data': 0, 'draw': 0, 'loose': 0}
        for country in self.list_of_possessed_countries:
            ansdict = country.win_analysis(category, peacemode=peacemode)

            returndict['win'] += ansdict['win']
            returndict['no data'] += ansdict['no data']
            returndict['draw'] += ansdict['draw']
            returndict['loose'] += ansdict['loose']

        return returndict


    def get_good_attribute(self,
                           threshold: float = 0.25,
                           at_least_one_win: bool = True,
                           peacemode : bool = False,
                           list_of_clusters : list[str] | None = None) -> Category:
        """
        Selects a random attribute that provides a reasonably good chance of winning attacks.
        This method repeatedly selects random attributes until finding one that meets
        the specified criteria for being "good" (i.e., useful for attacks). An attribute
        is considered good if:
        1. The probability of winning or drawing attacks with it exceeds the threshold
        2. It's not an "end only" attribute
        3. If at_least_one_win is True, there must be at least one possible winning attack
        Args:
            threshold (float, optional): Minimum probability of win+draw outcomes required.
                Defaults to 0.25.
            at_least_one_win (bool, optional): Whether to require at least one possible
                winning attack. Defaults to True.
            peacemode (bool, optional): Ignores countries owned by other players, due to peacemode if set to True.
                Defaults to False.
        Returns:
            Category: A suitable attribute meeting the specified criteria
        """

        cluster_pool = list_of_clusters if list_of_clusters is not None else all_categories_names_and_clusters.copy()
        if len(cluster_pool) == 0:
            cluster_pool = all_categories_names_and_clusters.copy()
        if len(cluster_pool) == 0:
            raise ValueError("No categories are available to choose from.")

        # Remember the first playable option so we can still return a sensible
        # attribute if none of the random picks meets the win/draw threshold.
        backup_attribute: Category | None = None
        backup_cluster_name: str | None = None
        max_attempts = max(len(cluster_pool) * 3, 1)

        for _ in range(max_attempts):
            current_attribute = self.get_random_attribute_with_cluster(cluster_pool)
            current_cluster_name = self.current_clustername

            if backup_attribute is None and not current_attribute.is_end_only:
                backup_attribute = current_attribute
                backup_cluster_name = current_cluster_name

            attack_analysis_dict = self.player_win_analysis(current_attribute, peacemode=peacemode)
            number_of_all_possible_attacks = sum(attack_analysis_dict.values())

            if number_of_all_possible_attacks == 0:
                continue

            probability = (
                float(attack_analysis_dict['win'] + attack_analysis_dict['draw'])
                / float(number_of_all_possible_attacks)
            )
            threshold_condition = probability >= threshold
            at_least_one_req = (attack_analysis_dict['win'] >= 1) if at_least_one_win else True

            if threshold_condition and not current_attribute.is_end_only and at_least_one_req:
                if list_of_clusters is not None and current_cluster_name in list_of_clusters:
                    list_of_clusters.remove(current_cluster_name)
                return current_attribute

        if backup_attribute is None:
            backup_attribute = self.get_random_attribute_with_cluster(cluster_pool)
            backup_cluster_name = self.current_clustername

        if list_of_clusters is not None and backup_cluster_name in list_of_clusters:
            list_of_clusters.remove(backup_cluster_name)

        return backup_attribute


def call_player_by_name(name: str) -> Player:
    """
    Retrieve a player object by their name.

    This function searches through all registered players and returns the player
    object that matches the provided name. If no player is found with the given name,
    it returns the default 'mr_nobody' player.

    Args:
        name (str): The name of the player to search for.

    Returns:
        Player: The player object if found, otherwise returns 'mr_nobody'.
    """
    return all_players.get(name, mr_nobody)


mr_nobody = Player(color = white, name="Nobody")
No_Data_Body = Player(color=realgrey, name="Nobody")
