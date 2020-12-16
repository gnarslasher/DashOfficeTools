import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from navbar import Navbar

nav = Navbar()

# body = dbc.Container([
#     dbc.Row(
#         dbc.Col(html.Br()),
#     ),
#     dbc.Row([
#         dbc.Col([
#             html.H3('Data Editing Tools'),
#             dcc.Link('Temperature Spike Analysis', href='/tempspikes'),
#             html.Br(),
#             dcc.Link('More Apps Coming Soon', href='/comingsoon'),
#         ]),
#         dbc.Col([
#             html.H3('Site Health Tools'),
#             dcc.Link('More Apps Coming Soon', href='/comingsoon'),
#         ])
#     ]),
# ], fluid=True)

body = dbc.Container([
    dbc.Row(
        dbc.Col(html.Br()),
    ),
    dbc.Row([
        dbc.Col([
            html.H3('Data Editing Tools'),
            dcc.Link('Temperature Spike Analysis', href='/tempspikes'),
            html.Br(),
            dcc.Link('More Coming Soon...', href='/comingsoon'),
            html.Br(),
            html.Br(),
            html.Br(),
            html.H3('Sensor Health Tools'),
            dcc.Link('More Coming Soon...', href='/comingsoon'),
        ]),
    ]),
], fluid=True)


def Homepage():
    layout = html.Div([
        nav,
        body
    ])
    return layout
