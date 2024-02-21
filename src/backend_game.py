from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from player import Player
    from country import Country
    from category import Category

from global_definitions import all_categories, all_countries_in_game
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

        self.rerolls : int = 3

        self.number_of_targets = 2

        self.pred_attribute_name = pred_attribute

        self.winning_condition = winning_condition
        
        self.number_of_rounds = number_of_rounds
        self.index = 0
        self.goldlist: list[Country] = list()
        self.choosing_index = -1
        self.starting_countries = starting_countries_preferences
        self.reversed_end_attribute = reversed_end_attribute

        self.list_of_players = list_of_players
        print(self.list_of_players)
        print(len(list_of_players))
        self.active_player_counter = 0
        self.active_player = self.list_of_players[self.active_player_counter]
        self.number_of_players = len(self.list_of_players)
        self.end_attribute: Category 
        self.wormhole_mode: str = wormhole_mode
        self.wormholed_countries: list[list[Country]] = list()
        self.number_of_wormholes = number_of_wormholes
        print(self.winning_condition)

        self.peacemode: bool = peacemode

        self.current_attribute: Category = all_categories[0]

    def get_starting_attribute(self):
        pass
    
    def find_top_n_countries(self, n : int, attribute_name : str):
        returnlist : list[Country] = list()
        for country in all_countries_in_game:
            try:
                if country.dict_of_attributes[attribute_name].rank <= n:
                    returnlist.append(country)
            except KeyError:
                continue
        returnlist.sort(key=lambda x: x.dict_of_attributes[attribute_name].rank)
        return returnlist

    def check_if_game_should_end(self):
        if self.active_player_counter == len(
                self.list_of_players) * self.number_of_rounds - 1:
            self.endscreen()
            return True
        if self.winning_condition == "claim 2 countries":
            if self.targetcountry1.owner != "Nobody" and self.targetcountry1.owner == self.targetcountry2.owner:
                self.endscreen(cause="twocountriesclaimed")
                return True
        if self.winning_condition == "get gold":
            if len(self.goldlist) == 0:
                self.endscreen(cause="all gold left")
                return True
        if self.winning_condition == "secret targets":
            if set(self.dict_of_targets[self.active_player]).issubset(
                    set(self.active_player.list_of_possessed_countries)):
                self.endscreen(cause="co")
                return True
        if self.winning_condition == "secret attribute":
            if len(
                    set(self.dict_of_targets[self.active_player]).intersection(
                        set(self.active_player.list_of_possessed_countries))
            ) >= 1:
                for country in self.active_player.list_of_possessed_countries:
                    if country in self.dict_of_targets[self.active_player]:
                        self.endscreen(cause="co",
                                       winner=self.active_player,
                                       gotcha_country=country)
                        break
                return True
        return False

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
