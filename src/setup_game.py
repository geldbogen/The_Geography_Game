from global_definitions import (
    all_countries_in_game, all_countries_available, country_name_list, neighboring_countries, my_property_dict)
from country import Unknown_country
from player import all_players
from main_window import MainWindow
from image import im


def gogo(self):
    self.activecontinents = list()
    if self.africavar.get() == 1:
        self.activecontinents.append("Africa")
    if self.asiavar.get() == 1:
        self.activecontinents.append("Asia")
    if self.europevar.get() == 1:
        self.activecontinents.append("Europe")
    if self.north_americavar.get() == 1:
        self.activecontinents.append("North America")
    if self.middle_americavar.get() == 1:
        self.activecontinents.append("Middle America")
    if self.south_americavar.get() == 1:
        self.activecontinents.append("South America")
    if self.oceaniavar.get() == 1:
        self.activecontinents.append("Oceania")

    for country in all_countries_available:
        if country.continent in self.activecontinents:
            all_countries_in_game.append(country)
    all_countries_in_game.append(Unknown_country)
    self.numberofrounds = self.numberofroundsentry.get()

    for country in all_countries_in_game:
        name = country.name
        country_name_list.append(name)

    for acountry in all_countries_in_game:
        try:
            if acountry == Unknown_country:
                continue
            data = neighboring_countries[neighboring_countries[0] ==
                                         acountry.name]
            for bcountry in all_countries_in_game:
                if bcountry == Unknown_country:
                    continue
                if bcountry.name in data.iat[0, 5]:
                    bcountry.neighboring_countries.append(acountry.name)
        except:
            continue

    for country in all_countries_in_game:
        try:
            country.dict_of_attributes = my_property_dict[country.name]
        except:
            pass

    if len(self.list_of_players) == 0:
        return None

    for player in all_players.values():
        try:
            player.rerolls_left = int(self.numberofroundsentry.get()) // 3
        except ValueError:
            player.rerolls_left = 3

    self.root.destroy()
    if self.numberofrounds == "":
        MainWindow(bild=im,
                   list_of_players=self.list_of_players,
                   starting_countries=self.start_country.get(),
                   winning_condition=self.winning_condition.get(),
                   pred_attribute=self.current_var.get() + ".csv",
                   wormholemode=self.wormhole_option.get(),
                   peacemode=self.peacemode_var.get(),
                   reversed_end_attribute=self.reverse_yes_or_novar.get())
    else:
        MainWindow(bild=im,
                   list_of_players=self.list_of_players,
                   starting_countries=self.start_country.get(),
                   number_of_rounds=int(self.numberofrounds),
                   winning_condition=self.winning_condition.get(),
                   pred_attribute=self.current_var.get() + ".csv",
                   wormholemode=self.wormhole_option.get(),
                   peacemode=self.peacemode_var.get(),
                   reversed_end_attribute=self.reverse_yes_or_novar.get())
