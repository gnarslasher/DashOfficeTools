import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from app import server

from apps.homepage import Homepage
from apps.comingsoon import Comingsoon
from apps.tempspikes import Tempspikes

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/tempspikes':
        return Tempspikes()
    elif pathname == '/comingsoon':
        return Comingsoon()
    else:
        return Homepage()


if __name__ == '__main__':
    app.run_server(debug=True)
