import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from navbar import Navbar

nav = Navbar()

body = dbc.Container([
    dbc.Row(
        dbc.Col(html.Br()),
    ),
    dbc.Row([
        dbc.Col([
            html.H3('Data Editing Tools'),
            dcc.Link('Editing QC Tool', href='/editing_qc'),
            html.Br(),
            html.Br(),
            html.Br(),
            html.H3('Sensor Health Tools'),
            dcc.Link('Coming Soon...', href='/comingsoon'),
            html.Br(),
            html.Br(),
            html.Br(),
            html.H3('Data Analysis Tools'),
            dcc.Link('Site Correlator', href='/site_correlator'),
        ]),
    ]),
], fluid=True)


def Homepage():
    layout = html.Div([
        nav,
        body
    ])
    return layout
