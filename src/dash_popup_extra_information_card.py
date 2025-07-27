

import dash_bootstrap_components as dbc
from dash import html

def get_popup_extra_information_window_card(image_path : str, wiki_title : str, wiki_description : str, wiki_link: str):
    card = dbc.Card(
        [
            dbc.CardImg(src=image_path, top=True, alt='assets/pictures/no_image_available.png'),
            dbc.CardBody(
                [
                    html.H4(wiki_title, className="card-title"),
                    html.P(
                        wiki_description,
                        className="card-text",
                        style={'height': '200px', 'width': '300px', 'overflow-y': 'scroll'}
                    ),
                    dbc.Button("See more on Wikipedia", color="primary", href=wiki_link,),
                ]
            ),
        ],
        style={"width": "18rem"},
    )

    return card

def get_two_popup_extra_information_window_cards(
    image_path_1: str, wiki_title_1: str, wiki_description_1: str, wiki_link_1: str,
    image_path_2: str, wiki_title_2: str, wiki_description_2: str, wiki_link_2: str
):
    return dbc.Row([
        dbc.Col(get_popup_extra_information_window_card(image_path_1, wiki_title_1, wiki_description_1, wiki_link_1), width=6),
        dbc.Col(get_popup_extra_information_window_card(image_path_2, wiki_title_2, wiki_description_2, wiki_link_2), width=6)
    ])