import dash
from dash import html
import dash_mantine_components as dmc

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = dmc.MantineProvider([
    dmc.Group([
        dmc.Text('You cannot hover me, but'),
        dmc.HoverCard(
            withArrow=True,
            width=200,
            shadow="md",
            children=[
                dmc.HoverCardTarget(
                    dmc.Text("hover me!", style={"color": "blue", "cursor": "pointer", "textDecoration": "underline"})
                ),
                dmc.HoverCardDropdown(
                    dmc.Text(
                        " Hover card is revealed when user hovers over target element, it will be hidden once mouse is not over",
                        size="sm",
                    )
                ),
            ],
        )
    ],)
])

# Run the app
if __name__ == "__main__":
    app.run(debug=True)