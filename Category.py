from globalDefinitions import all_categories, all_categories_names_and_clusters, dictionary_attribute_name_to_attribute


class Category:

    def __init__(self,
                 name: str,
                 isActive: bool,
                 treatMissingDataAsBad: bool,
                 difficulty: int,
                 explanation: str = "",
                 cluster: str = "",
                 is_end_only: bool = False):
        pass

        # the name of the category
        self.name = name

        # whether a category is active, i.e. whether the player
        # can "guess" before taking a move in order to get a freee turn
        self.isActive = isActive

        # In order to prevent that the same category is chosen too often,
        # a counter which tracks how often a category has already been chosen
        self.numberOfChosenAlready = 0

        # whether the category is a "treat missing data as a loss" - category
        self.treatMissingDataAsBad = treatMissingDataAsBad

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
            # add category name to list of category names
            all_categories_names_and_clusters.append(self.name)

            # map categoryname to single item list of corresponding class
            dictionary_attribute_name_to_attribute[self.name] = [self]
