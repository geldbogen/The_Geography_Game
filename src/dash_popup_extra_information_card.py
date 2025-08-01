
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import html

def get_popup_extra_information_window_card(image_path : str, wiki_title : str, wiki_description : str, wiki_link: str):
    card = dmc.Card(
        [
            dmc.CardSection(
                [
                    dmc.Image(src=image_path, fallbackSrc='assets/pictures/no_image_available.png'),
                    dmc.Title(order=4, children=wiki_title),
                    dmc.Text(
                        wiki_description,
                    ),
                ],
                className='overflow-auto'
            ),
        dmc.Button("See more on Wikipedia", justify="center",),
        ],
    withBorder=True,
    shadow="sm",
    radius="md",
    w=700,
    h=500,
    
    )

    return card

def get_two_popup_extra_information_window_cards(
    image_path_1: str, wiki_title_1: str, wiki_description_1: str, wiki_link_1: str,
    image_path_2: str, wiki_title_2: str, wiki_description_2: str, wiki_link_2: str
):
    return dmc.Group([
        get_popup_extra_information_window_card(image_path_1, wiki_title_1, wiki_description_1, wiki_link_1),
        get_popup_extra_information_window_card(image_path_2, wiki_title_2, wiki_description_2, wiki_link_2),
    ], 
    justify='space-around',
    grow=True
    )