import dash_mantine_components as dmc

def get_popup_extra_information_window_card(image_path : str, wiki_title : str, wiki_description : str, wiki_link: str):
    action = (
        dmc.Anchor(
            dmc.Button("See more on Wikipedia", justify="center", variant="light", radius="xl", fullWidth=True),
            href=wiki_link,
            target="_blank",
        )
        if wiki_link else
        dmc.Button("No Wikipedia link", justify="center", variant="subtle", radius="xl", fullWidth=True, disabled=True)
    )

    card = dmc.Card(
        [
            dmc.CardSection(
                dmc.Image(
                    src=image_path,
                    fallbackSrc='/assets/pictures/no_image_available.png',
                    h=220,
                    fit="cover",
                )
            ),
            dmc.Stack(
                [
                    dmc.Title(
                        order=4,
                        children=wiki_title or "No extra information",
                        ta="center",
                        style={'minHeight': '3.5rem'}
                    ),
                    dmc.ScrollArea(
                        dmc.Text(
                            wiki_description or "No summary available for this entry.",
                            ta="left",
                            style={'lineHeight': '1.65', 'color': '#425466'}
                        ),
                        h=170,
                        offsetScrollbars=True,
                    ),
                    action,
                ],
                gap="md",
                justify="space-between",
                style={'height': '100%', 'padding': '20px'}
            ),
        ],
        withBorder=True,
        shadow="md",
        radius="xl",
        h=520,
        style={
            'background': 'linear-gradient(180deg, #ffffff 0%, #f7fafc 100%)',
            'borderColor': 'rgba(148, 163, 184, 0.35)',
        }
    )

    return card

def get_two_popup_extra_information_window_cards(
    image_path_1: str, wiki_title_1: str, wiki_description_1: str, wiki_link_1: str,
    image_path_2: str, wiki_title_2: str, wiki_description_2: str, wiki_link_2: str
):
    return [
        get_popup_extra_information_window_card(image_path_1, wiki_title_1, wiki_description_1, wiki_link_1),
        get_popup_extra_information_window_card(image_path_2, wiki_title_2, wiki_description_2, wiki_link_2),
    ]
