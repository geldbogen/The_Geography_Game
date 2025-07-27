


def setup_the_game(continent_list: list[str] = [],
                   list_of_players: list[Player] = [],
                   number_of_rounds: int = -1,
                   number_of_rerolls: int = 0,
                   ):
    
    for country in all_countries_available:
        if country.continent_name in continent_list:
            all_countries_in_game.append(country)

    all_countries_in_game.append(Unknown_country)

    for country in all_countries_in_game:
        country_name_list.append(country.name)

    # TODO: this is quite ugly
    for country_1 in all_countries_in_game:
        if country_1 == Unknown_country:
            continue
        data = neighboring_countries[neighboring_countries[0] ==
                                     country_1.name]
        for country_2 in all_countries_in_game:
            if country_2 == Unknown_country:
                continue
            if not data.empty:
                if country_2.name in str(data.iat[0, 5]):
                    country_2.neighboring_countries.append(country_1.name)

    # breakpoint()

    # remove self-connectedness
    for country in all_countries_available:
        if country.name in country.neighboring_countries:
            country.neighboring_countries.remove(country.name)

    # breakpoint()

    for country1 in all_countries_available:
        print(country1.name)
        for country2 in all_countries_available:
            if country1 == country2:
                continue
            if country1.name in country2.neighboring_countries and not country2.name in country1.neighboring_countries:
                country1.neighboring_countries.append(country2.name)
    
    # assigns the countries all the local attributes
    # for country in all_countries_in_game:
    #     country.dict_of_attributes = my_property_dict[country.name]

    if list_of_players == []:
        return None

    for player in all_players.values():
        player.rerolls_left = number_of_rerolls
