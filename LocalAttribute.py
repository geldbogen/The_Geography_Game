from dataclasses import dataclass

# a specific datatype to save the information of a specific's country stance on a category
@dataclass
class LocalAttribute():
    value: float = 0.0
    rank: int = -1
    how_many_ranked : int = 1
    additional_information_name : str = ''
    additional_information: str = ''
    wikipedia_link: str = ''

    