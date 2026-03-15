import dash_mantine_components as dmc

from global_definitions import (
    all_categories, all_categories_names_and_clusters,
    dictionary_attribute_name_to_attribute, category_to_displayed_name_dict,
    category_to_displayed_extra_information_category)

from country import Country


class Category:

    def __init__(self,
                 name: str,
                 is_active: bool,
                 treat_missing_data_as_bad: bool,
                 difficulty: int,
                 explanation: str = "",
                 cluster: str = "",
                 is_end_only: bool = False):
        """
        Initializes a Category instance with specified attributes and updates global collections.
        Parameters:
        ----------
        name : str
            The name of the category.
        is_active : bool
            Whether the category is active, allowing players to "guess" before moving for a free turn.
        treat_missing_data_as_bad : bool
            Whether missing data in this category should be treated as a loss.
        difficulty : int
            The difficulty level of the category on a scale from 1 (easiest) to 5 (hardest).
        explanation : str, optional
            Additional details about the category, such as its meaning or source. Default is empty string.
        cluster : str, optional
            The cluster group this category belongs to. Default is empty string 
            If a category belongs to a cluster the probability of showing up is only as large as the probability of chosing the cluster.
        is_end_only : bool, optional
            Whether this category should only be used at the end of the game. Default is False.
        Notes:
        -----
        Upon initialization, the category is added to global collections:
        - Added to the global list of all categories
        - If part of a cluster, the cluster name is added to the global list of category names/clusters
        - Category name to category instance mapping is created in the global dictionary
        """

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

        if self.is_end_only:
            # if the category is only used at the end of the game, we do not want to add it to the list of categories
            # which are used in the normal flow of the game
            return

        # if there is a real cluster
        if not cluster == "":
            # append the name of cluster in the namelist.
            # One can specify the probabily of choosing this cluster by appending it multiple times.
            if not cluster in all_categories_names_and_clusters:
                # here one can tune the probability of choosing the specific cluster
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

    def get_number_of_missing_data(self, list_of_countries_in_game: list[Country]) -> int:
        """
        Returns the number of countries in the game that have missing data (rank = 0) for this category.

        Args:
            list_of_countries_in_game (list[Country]): A list of Country objects representing countries in the game.

        Returns:
            int: The number of countries with missing data for this category.
        """
        no_data_list = [country.dict_of_attributes[self.name].rank ==
                        0 for country in list_of_countries_in_game]
        return sum(no_data_list)

    def replace_A_and_B_in_category_name(self, first_country: Country | None = None,
                                         second_country: Country | None = None) -> dmc.Highlight:
        """
        Replace placeholders in category name with actual country names for display.
        This method customizes the display text for a category by replacing 'CountryA' and 'CountryB' 
        placeholders with the names of the provided countries (or generic descriptions, like '(your country)' resp. '(other country)' if countries 
        are not provided). 
        It also appends additional context information for specific category types.
        It does change the provided Tkinter label in place but also returns it for convenience.
        Parameters
        ----------
        tk_label : tk.Label
            The Tkinter label widget that will display the category name.
        first_country : Country | None, optional
            The first country to replace 'CountryA' in the display text. If None, replaces the name with '(your country)'.
        second_country : Country | None, optional
            The second country to replace 'CountryB' in the display text. If None, replaces the name with '(target country)'.
        Returns
        -------
        tk.Label
            The updated Tkinter label with the configured text.
        Notes
        -----
        The method handles several special cases:
        - Uses a dictionary lookup to convert internal category names to display names
        - Adds '(TODO)' suffix for categories marked as incomplete in the dictionary
        - Adds '(ERROR)' suffix for categories not found in the dictionary
        - Appends explanatory text for categories about people or historical events
        - Has a commented-out section for future implementation of guessing hints
        """

        categoryname = self.name.rstrip(".csv")
        try:
            formatted_category_string = category_to_displayed_name_dict[categoryname]
            if (formatted_category_string in ["", "TODO"]):
                formatted_category_string = dmc.Highlight(categoryname + " (TODO)", highlight=[])
                return formatted_category_string
        except KeyError:
            formatted_category_string = dmc.Highlight(categoryname + " (ERROR)", highlight=[])
            return formatted_category_string

        # assert isinstance(formatted_category_label.children, str)

        match first_country, second_country:
            case None, None:
                ans = dmc.Highlight(formatted_category_string.replace("CountryA", "(your country)").replace("CountryB", "(target country)"), highlight=[])
            case _, None:
                ans = dmc.Highlight(formatted_category_string.replace("CountryA", first_country.name).replace("CountryB", "(target country)"),
                                     highlight=[first_country.name],
                                         highlightStyles={"backgroundImage": "linear-gradient(45deg, var(--mantine-color-cyan-5), var(--mantine-color-indigo-5))",
                                            "fontWeight": 500,
                                            "WebkitBackgroundClip": "text",
                                            "WebkitTextFillColor": "transparent",
                                                }) # type: ignore
            case None, _:
                ans = dmc.Highlight(formatted_category_string.replace("CountryA", "(your country)").replace("CountryB", second_country.name),
                                     highlight=[second_country.name]) # (this should never happen though)
            case _, _:
                ans = dmc.Highlight(formatted_category_string.replace("CountryA", first_country.name).replace("CountryB", second_country.name),
                                     highlight=[first_country.name, second_country.name], highlightStyles={
                                         "backgroundImage": "linear-gradient(45deg, var(--mantine-color-cyan-5), var(--mantine-color-indigo-5))",
                                            "fontWeight": 500,
                                            "WebkitBackgroundClip": "text",
                                            "WebkitTextFillColor": "transparent",
                                                }) # type: ignore
        
        return ans


        #  if (second_country is None):
        #     formatted_category_string.children = formatted_category_string.children.replace(
        #         "CountryB", " (target country) ")
        # else:
        #     formatted_category_string.children = formatted_category_string.children.replace(
        #         "CountryB", second_country.name)
        #     formatted_category_string.highlight.append()

        # if (first_country is None):
        #     formatted_category_string.children = formatted_category_string.children.replace(
        #         "CountryA", " (your country) ")
        # else:
        #     formatted_category_string.children = formatted_category_string.children.replace(
        #         "CountryA", first_country.name)

        # extra_information_displayed = ""

        # try:
        #     if (category_to_displayed_extra_information_category[categoryname] ==
        #             "person"):
        #         extra_information_displayed = "\n (citizenship or birthplace in the current territory of the country)"
        #     if (category_to_displayed_extra_information_category[categoryname] ==
        #             "historical event"):
        #         extra_information_displayed = "\n (took place in the current territory of the country)"
        # except KeyError:
        #     pass

        # formatted_category_string += extra_information_displayed

        # return formatted_category_string
