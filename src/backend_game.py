from __future__ import annotations
from typing import TYPE_CHECKING
import random

import tkinter as tk

if TYPE_CHECKING:
    from player import Player

    from category import Category


from global_definitions import all_categories, all_countries_in_game
from country import Country, Unknown_country


class BackendGame():

    def __init__(self,
                 list_of_players: list[Player],
                 wormhole_mode: str,
                 starting_countries_preferences: str = "random",
                 number_of_rounds: int = 99999999999,
                 winning_condition: str = "number of countries",
                 number_of_wormholes: int = 3,
                 pred_attribute: str = "random",
                 peacemode: bool = False,
                 reversed_end_attribute: int = 0):

        self.list_of_players: list[Player] = list_of_players
        self.winning_condition: str = winning_condition
        self.rerolls: int = 3

        self.number_of_targets = 2

        self.pred_attribute_name = pred_attribute

        # for the rounds
        self.number_of_rounds = number_of_rounds
        self.index = 0
        self.goldlist: list[Country] = list()
        self.choosing_index = -1
        self.starting_countries = starting_countries_preferences
        self.reversed_end_attribute = reversed_end_attribute

        # for the players
        self.active_player_counter = 0
        self.list_of_players = list_of_players
        print(self.list_of_players)
        print(len(list_of_players))
        self.active_player = self.list_of_players[self.active_player_counter]
        self.number_of_players = len(self.list_of_players)
        self.end_attribute: Category = None
        self.wormhole_mode: str = wormhole_mode
        self.wormholed_countries: list[list[Country]] = list()
        self.number_of_wormholes = number_of_wormholes
        print(self.winning_condition)

        self.peacemode: bool = peacemode

        self.current_attribute: Category = all_categories[0]

        # just declaration

        # for claimtwo countries
        self.targetcountry1: Country
        self.targetcountry2: Country

        # for end attribute
        self.end_attribute: Category

        # for secret targets
        self.dict_of_targets: dict[Player, list[Country]] = dict()

        # for secret attribute
        self.dict_of_target_attribute_name: dict[Player, str] = dict()
        self.winning_country: Country = Unknown_country

    def get_starting_attribute(self):
        pass

    def find_top_n_countries(self, n: int, attribute_name: str):
        """
        Finds the top N countries based on a specified attribute.
        This method filters the countries in the game to include only those
        that have a valid rank (not equal to 0) for the given attribute.
        It then sorts the countries by their rank for the specified attribute
        in ascending order and returns the top N countries.
        Args:
            n (int): The number of top countries to retrieve.
            attribute_name (str): The name of the attribute to rank the countries by.
        Returns:
            list: A list of the top N countries sorted by the specified attribute's rank.
        """

        all_countries_with_data = [
            country for country in all_countries_in_game if country.dict_of_attributes[attribute_name].rank != 0]
        all_countries_with_data.sort(
            key=lambda x: x.dict_of_attributes[attribute_name].rank)
        return all_countries_with_data[:n]

    def reroll(self, activating_player: Player, to_update_category_label: tk.Label,
               to_update_reroll_button: tk.Button) -> None:
        """
        Handles the reroll action for a player, allowing them to randomly choose a new current attribute
        if they have rerolls left. Subtracts one reroll from the player's count and updates the current attribute.
        Updates the category label and reroll button accordingly.
        Args:
            activating_player (Player): The player who is activating the reroll.
            to_update_category_label (tk.Label): The label widget to update with the new category name.
            to_update_reroll_button (tk.Button): The button widget to update with the remaining rerolls.
        Returns:
            None
        """
        if activating_player.rerolls_left == 0:
            return None
        activating_player.rerolls_left -= 1

        self.current_attribute = activating_player.get_good_attribute()

        self.current_attribute.replace_A_and_B_in_category_name(to_update_category_label,
                                                                )
        to_update_reroll_button.configure(
            text="rerolls left:\n " + str(activating_player.rerolls_left))
        return None

    def check_if_game_should_end(self):
        """
        Determines whether the game should end based on the current game state 
        and the specified winning condition.
        Winning Conditions:
            - "claim 2 countries": The game ends if both target countries have 
              the same owner and the owner's name is not "Nobody".
            - "get gold": The game ends if the gold list is empty (i.e. all goldcountries have been claimed).
            # TODO: end game if somebody has the majority of the gold
            - "secret targets": The game ends if the active player's possesses all of their target countries.
            - "secret attribute": The game ends if the active player possesses 
              at least one of their target countries. Additionally, the winning 
              country is set if a match is found.
            - Default: If the winning condition is invalid, the game will not end and it will print a warning message.
        Additional Condition:
            The game also ends if the active player counter reaches the total 
            number of turns (calculated as the number of players multiplied by 
            the number of rounds) minus one.
        Returns:
            bool: True if the game should end, False otherwise.
        """

        print('the game is asked to end')
        print('active_player_counter')
        print(self.active_player_counter)
        
        if self.active_player_counter == len(
                self.list_of_players) * self.number_of_rounds - 1:
            return True
        match self.winning_condition:
            case "claim 2 countries":
                if self.targetcountry1.owner.name != "Nobody" and self.targetcountry1.owner == self.targetcountry2.owner:
                    return True
            case "get gold":
                if len(self.goldlist) == 0:
                    return True
            case "secret targets":
                if set(self.dict_of_targets[self.active_player]).issubset(
                        set(self.active_player.list_of_possessed_countries)):
                    return True
            case "secret attribute":
                if len(
                        set(self.dict_of_targets[self.active_player]).intersection(
                            set(self.active_player.list_of_possessed_countries))
                ) >= 1:
                    for country in self.active_player.list_of_possessed_countries:
                        if country in self.dict_of_targets[self.active_player]:
                            self.winning_country = country
                            return True
                    return True
            case _:
                print('illegal winning condition will never end')
                return False

    def claim_country_backend(self, loose_player: Player, win_player: Player, country: Country):
        """
        Transfers ownership of a country from one player to another.
        This method handles the backend logic of claiming a country, including:
        updating player's possessed countries list,
        setting the country's owner,
        and handling gold acquisition when the winning condition is "get gold".
        Parameters:
        -----------
        loose_player : Player
            The player who is losing the country. Can be Mr_Nobody for unclaimed countries.
        win_player : Player
            The player who is claiming the country.
        country : Country
            The country being claimed.
        Notes:
        ------
        - If loose_player's name is not "Nobody",
            the country is removed from loose_player's possession and the GUI label is destroyed.
        - If the winning condition is "get gold" and the country contains gold,
            win_player's gold count is incremented and the country is added to their
            list of gold-containing countries.
        """

        win_player.list_of_possessed_countries.append(country)
        country.owner = win_player

        if loose_player.name != "Nobody":
            loose_player.list_of_possessed_countries.remove(
                country)
            loose_player.labeldict[country].destroy()

        if self.winning_condition == "get gold":
            if win_player.name != "Nobody":
                if country in self.goldlist:
                    win_player.gold = win_player.gold + 1
                    self.goldlist.remove(country)
                    win_player.list_of_possessed_countries_gold.append(country)

    def score(self, countrylist: list[Country]) -> list[float]:
        """
        Calculates a score for a list of countries based on their attributes and a specified end attribute.
        Args:
            countrylist (list[Country]): A list of Country objects for which the scores are to be calculated.
        Returns:
            list[float]: A list of scores (as floats) corresponding to the input countries.
        The scoring is determined by comparing the value of the specified end attribute for each country
        against the values of the same attribute for all countries in the game. The comparison is influenced
        by whether "higher is better" or "lower is better" for the attribute, and whether the attribute's
        ranking is reversed.
        Internal logic:
            - If the attribute is missing or treated as bad, the country is assigned a default score.
            - Otherwise, the score is calculated based on the number of countries with better or worse
              attribute values, depending on the "higher or lower" rule.
            - The scores are normalized by dividing by 5.
        Note:
            - The function assumes the existence of `self.end_attribute`, which contains the name and
              properties of the attribute being evaluated.
            - The `self.higherorlower` variable determines the comparison direction ("higher" or "lower").
            - The `self.reversed_end_attribute` variable indicates whether the ranking is reversed.
            - The `all_countries_in_game` variable is expected to be a list of all Country objects in the game.
        """

        def helphelp(number: float, list1: list[float]) -> float:
            if self.higherorlower == "higher":
                return float(sum([item <= number for item in list1]))
            if self.higherorlower == "lower":
                return float(sum([item >= number for item in list1]))

            return 0.0

        # higherorlower : str = ""
        propertylist: list[float] = list()
        mcountrylist: list[Country] = list()
        dlist: list[Country] = list()

        if self.reversed_end_attribute == 0:
            if "higher is better" in self.end_attribute.name:
                self.higherorlower = "higher"
            else:
                self.higherorlower = "lower"
        else:
            if "higher is better" in self.end_attribute.name:
                self.higherorlower = "lower"
            else:
                self.higherorlower = "higher"

        for country in all_countries_in_game:
            try:
                if (country.dict_of_attributes[self.end_attribute.name].rank != 0
                    ) or (self.end_attribute.treat_missing_data_as_bad):
                    propertylist.append(
                        (country.dict_of_attributes[self.end_attribute.name].value))
                    mcountrylist.append(country)
                else:
                    dlist.append(country)
            except KeyError:
                dlist.append(country)
        print(propertylist)
        print('this is dlist')
        print([d.name for d in dlist])

        returnlist: list[float] = list()
        for country in countrylist:
            if country in dlist:
                returnlist.append(
                    country.dict_of_attributes[self.end_attribute.name].number_of_countries_ranked // 2)
            else:
                returnlist.append(
                    helphelp(
                        country.dict_of_attributes[self.end_attribute.name].value,
                        propertylist))
        returnlist = [float(item) / float(5) for item in returnlist]
        return returnlist

    def find_distance(self, country_a: Country, country_b: Country) -> None:
        """
        Calculates the shortest distance (in terms of the number of connections) 
        between two countries in the game using a breadth-first search algorithm.

        Args:
            country_a (Country): The starting country.
            country_b (Country): The target country.

        Returns:
            int: The shortest distance between country_a and country_b in terms of 
                 the number of connections, or None if no path exists.
        """
        mydict = dict()
        myset = set(country_a.name)
        q = [[country_a.name, 0]]
        print(q)
        for country in all_countries_in_game:
            mydict[country.name] = country.neighboring_countries
        while country_b.name not in myset:
            temp = q[0]
            q.pop(0)
            for countryname in mydict[temp[0]]:
                if countryname in myset:
                    pass
                else:
                    myset.add(countryname)
                    q.append([countryname, temp[1] + 1])
                    if countryname == country_b.name:
                        return temp[1] + 1
            pass
        return None
    
    def find_all_countries_with_max_distance_of_n(self, country: Country, n: int) -> list[Country]:
        """
        Finds all countries that are at a maximum distance of n connections from a given country.

        Args:
            country (Country): The starting country.
            n (int): The maximum distance in terms of connections.

        Returns:
            list[Country]: A list of countries that are at a maximum distance of n from the starting country.
        """
        called_country = country
        mydict = dict()
        myset = set(country.name)
        q = [[country.name, 0]]
        print(q)
        for country in all_countries_in_game:
            mydict[country.name] = country.neighboring_countries
        while q[0][1] < n:
            temp = q[0]
            q.pop(0)
            for countryname in mydict[temp[0]]:
                if countryname in myset:
                    pass
                else:
                    myset.add(countryname)
                    q.append([countryname, temp[1] + 1])
                    if temp[1] + 1 == n:
                        returnlist = [country for country in all_countries_in_game if country.name in myset]
                        print(f'find_all_countries_with_max_distance_of_n: {called_country.name} -> {[c.name for c in returnlist]}')
                        return returnlist
        

    def get_two_countries_for_wormhole_connection(self, player: Player = None) -> tuple[Country, Country]:
        """
        Gets two countries for a wormhole connection that meet specific criteria.

        This method selects two countries that:
        - Are not neighbors
        - Are from different continents
        - If player is provided, one country MUST NOT be owned by the player
        - Neither country is the Unknown_country
        - In peace mode, at least one country must be unowned

        Args:
            player (Player, optional): The player for whom to create a wormhole connection.
                If None, default countries will be returned without validation.

        Returns:
            tuple[Country, Country]: A pair of countries suitable for creating a wormhole connection.
        """
        country1 = Unknown_country
        country2 = Unknown_country
        if player != None:
            while (
                country2.name in country1.neighboring_countries
                or country1.name in country2.neighboring_countries
                or country1.continent_name == country2.continent_name
                or country2 in player.list_of_possessed_countries
                or country1 == Unknown_country
                or country2 == Unknown_country
                or
                    (self.peacemode and
                     #  TODO in case of end_attribute don't connect with Mr_Nobody country
                     (country1.owner != "Nobody" and country2.owner != "Nobody"))
            ):

                country1 = random.choice(player.list_of_possessed_countries)
                country2 = random.choice(all_countries_in_game)
        return country1, country2
