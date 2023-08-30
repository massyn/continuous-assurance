from dash import Dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container
from dash import html, dash

from data import df

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], use_pages=True)

search_bar = dbc.Row(
    [
        dcc.Dropdown(
            id="selected_mapping",
            options = [{'label': i, 'value': i} for i in sorted(df.mapping.unique())],
            multi=False,
            value="/",
            placeholder="Select a mapping",
            className=".dropdown",
            style={
                'width': "40%",
                'color': 'gray'
            },
        ),
    ],
    #className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href='/')),
    ],
    brand="Continuous Assurance",
    brand_href="#",
    color="dark",
    dark=True,
)

app.layout = html.Div(
    children = [
        navbar,
        search_bar,
        dash.page_container,
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)