from __future__ import annotations
from typing import TYPE_CHECKING
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
        
        self.list_of_players : list[Player] = list_of_players
        self.winning_condition :str = winning_condition
        self.rerolls : int = 3

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
        self.end_attribute: Category 
        self.wormhole_mode: str = wormhole_mode
        self.wormholed_countries: list[list[Country]] = list()
        self.number_of_wormholes = number_of_wormholes
        print(self.winning_condition)

        self.peacemode: bool = peacemode

        self.current_attribute: Category = all_categories[0]

        # just declaration

        # for claimtwo countries
        self.targetcountry1 : Country
        self.targetcountry2 : Country

        # for end attribute
        self.end_attribute: Category 


        # for secret targets
        self.dict_of_targets : dict[Player,list[Country]] = dict()

        # for secret attribute
        self.dict_of_target_attribute_name: dict[Player, str] = dict()
        self.winning_country : Country = Unknown_country

    def get_starting_attribute(self):
        pass
    
    def find_top_n_countries(self, n : int, attribute_name : str):

        all_countries_with_data = [country for country in all_countries_in_game if country.dict_of_attributes[attribute_name].rank != -1]
        all_countries_with_data.sort(key= lambda x: x.dict_of_attributes[attribute_name].rank)
        return all_countries_with_data[:n]
        
        
    def reroll(self, activating_player : Player, to_update_category_label: tk.Label,
               to_update_reroll_button: tk.Button):
        if activating_player.rerolls_left == 0:
            return None
        activating_player.rerolls_left -= 1

        self.current_attribute = activating_player.get_good_attribute()

        self.current_attribute.replace_A_and_B_in_category_name(to_update_category_label,
                                                                )
        to_update_reroll_button.configure(
            text="rerolls left:\n " + str(activating_player.rerolls_left))

    def check_if_game_should_end(self):

        print('the game is asked to end')
        print('active_player_counter')
        print(self.active_player_counter)
        if self.active_player_counter == len(
                self.list_of_players) * self.number_of_rounds - 1:
            return True
        match self.winning_condition:
            case "claim 2 countries":
                if self.targetcountry1.owner_name != "Nobody" and self.targetcountry1.owner_name == self.targetcountry2.owner_name:
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

    def claim_country_backend(self, loose_player : Player, win_player: Player, country : Country):
        win_player.list_of_possessed_countries.append(country)
        country.owner_name = win_player.name
        if loose_player.name != "Nobody" and not self.winning_condition in [
                "get gold"
        ]:
            loose_player.list_of_possessed_countries.remove(
                country)
            loose_player.labeldict[country].destroy()
        
        if self.winning_condition == "get gold":
            if win_player.name != "Nobody":
                if country in self.goldlist:
                    win_player.gold = win_player.gold + 1
                    self.goldlist.remove(country)
                    win_player.list_of_possessed_countries_gold.append(country)


    def score(self, countrylist : list[Country]) -> list[float]:

        def helphelp(number : float, list1 : list[float]) -> float:
            if self.higherorlower == "higher":
                return float(sum([item <= number for item in list1]))
            if self.higherorlower == "lower":
                return float(sum([item >= number for item in list1]))
            
            return 0.0

        # higherorlower : str = ""
        propertylist : list[float] = list()
        mcountrylist : list[Country] = list()
        dlist : list[Country] = list()
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
                if (country.dict_of_attributes[self.end_attribute.name].value
                        ) != float(-1):
                    propertylist.append(
                        (country.dict_of_attributes[self.end_attribute.name].value))
                    mcountrylist.append(country)
                else:
                    dlist.append(country)
            except KeyError:
                dlist.append(country)
        print(propertylist)
        returnlist : list[float] = list()
        for country in countrylist:
            if country in dlist:
                returnlist.append(30.0)
            else:
                returnlist.append(
                    helphelp(
                        country.dict_of_attributes[self.end_attribute.name].value,
                        propertylist))
        returnlist = [float(item) / float(5) for item in returnlist]
        return returnlist
