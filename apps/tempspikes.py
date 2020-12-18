import base64
import io
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import datetime as dt
from datetime import timedelta
import numpy as np
import plotly.graph_objects as go

from app import app
from navbar import Navbar

nav = Navbar()

body = dbc.Container([
    dbc.Row(dbc.Col([
        html.Hr(
            style={
                "border": "none",
                "border-top": "3px double #333",
                "color": "#333",
                "overflow": "visible",
                "text-align": "center",
                "height": "5px",
            }),
        html.H1('Hourly Temperature Spike Analysis',
                style={
                    "color": "black",
                    "text-align": "center",
                    "font-weight": "bold",
                }),
        html.Hr(
            style={
                "border": "none",
                "border-top": "3px double #333",
                "color": "#333",
                "overflow": "visible",
                "text-align": "center",
                "height": "5px",
            })],
    )),

    dbc.Row([
        dbc.Col([
            html.H5('Notes:', style={'text-decoration-line': 'underline'}),
            html.H6('* This tool was design for analyzing hourly (Group 2) temperature data.'),
            html.H6('* Use this tool to find hourly temperature spikes and determine if they need to be removed from '
                    'Group 1.'),
            html.H6('* Keep in mind the more the data you upload the slower this tool will run.'),
            html.H6('* Clicking refresh on browser will reset the tool and data will need to be uploaded again.'),
            html.H6('* "Cleaning" CSV data is required before uploading.  See Warnings ->'),
        ]),
        dbc.Col([
            html.H5('Warnings:', style={'text-decoration-line': 'underline'}),
            html.H6('* Top row must contain the column headers. If necessary, delete all rows above column headers.'),
            html.H6('* Check for and remove mid-data headers (rows). These will exist if sensor configuration was '
                    'changed.'),
            html.H6('* You do not need to remove "end" from last row.  This tool omits the last row of data ("end").'),
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            html.Hr(
                style={
                    "border": "none",
                    "border-top": "3px double #333",
                    "color": "#333",
                    "overflow": "visible",
                    "text-align": "center",
                    "height": "5px",
                }
            ),
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dcc.ConfirmDialog(
                id='alert',
                message='Data Uploaded Successfully',
            ),
            html.H3('Upload .CSV File'),
            dcc.Upload(
                id='datatable_upload',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files', style={'color': 'blue', 'text-decoration': 'underline'}),
                ]),
                style={
                    'width': '100%', 'height': '60px', 'lineHeight': '60px',
                    'borderWidth': '1px', 'borderStyle': 'dashed',
                    'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
                },
            ),
            html.Div(id='print_filename'),
        ]),
        dbc.Col([
            html.Div([
                html.Div([
                    html.H3('Select Metric'),
                    dcc.Dropdown(id='metric'),
                    html.Br(),
                ]),
                html.Div([
                    html.H3('Select Maximum Temperature Change (c)'),
                    dcc.Input(id='max_delta', value=6, placeholder=6, type='number'),
                ]),
                html.H1(''),
                html.Button(id='submit_button', n_clicks=0, children='Submit'),
                html.Div(id='stored_metric', style={'display': 'none'}),
                html.Div(id='stored_max_delta', style={'display': 'none'}),
            ]),
        ]),
    ]),

    dbc.Row(dbc.Col(
        html.Hr(
            style={
                "border": "none",
                "border-top": "3px double #333",
                "color": "#333",
                "overflow": "visible",
                "text-align": "center",
                "height": "5px",
            }
        )
    )),

    dbc.Row(dbc.Col([
        html.H3('Potential Temperature Spikes'),
        html.H6('Note: Select row for 24hr data'),
        html.Div(dash_table.DataTable(id='print_spikes', row_selectable='single'))
    ])),

    dbc.Row(dbc.Col([
        html.H3('Table - 24hr Data from Selected Row'),
        html.Div(id='selected_date'),
        html.Div(id='table_length', style={'display': 'none'})
    ])),

    dbc.Row(dbc.Col([
        html.Div(dash_table.DataTable(id='print_24hr', sort_action='native')),
        html.Hr(),
    ])),

    dbc.Row(dbc.Col([
        html.H3('Graph - 24hr Data from Selected Row'),
        html.H6('Note: Click on legend items to remove/add metrics'),
    ])),

    dbc.Row(dbc.Col([
        dcc.Graph(id='scatter_plot')
    ])),

], fluid=True)


def Tempspikes():
    layout = html.Div([
        nav,
        body
    ])
    return layout


start_table_df = pd.DataFrame(columns=[''])


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), header=0, parse_dates=[['Date', 'Time']],
                     skipfooter=1, error_bad_lines=False, engine='python', na_values='-99.9').set_index('Date_Time')

    df.columns = df.columns.str.replace(r'(^.*TOBS.*$)', 'TOBS degC')
    df.columns = df.columns.str.replace(r'(^.*TMAX.*$)', 'TMAX degC')
    df.columns = df.columns.str.replace(r'(^.*TMIN.*$)', 'TMIN degC')
    df.columns = df.columns.str.replace(r'(^.*TAVG.*$)', 'TAVG degC')

    df = df.replace(to_replace='-99.9', value=10000)

    valid_headers = ['TOBS degC', 'TMAX degC', 'TMIN degC', 'TAVG degC']
    all_headers = list(df.columns.values)
    actual_headers = set(valid_headers) & set(all_headers)
    df = df[actual_headers]

    return df


@app.callback([Output('print_filename', 'children')],
              [Input('datatable_upload', 'filename')])
def filename(filename):
    if filename is None:
        return ['Filename: None']

    return ['Filename: ' + str(filename)]


@app.callback([Output('metric', 'options')],
              [Input('datatable_upload', 'contents')],
              [State('datatable_upload', 'filename')])
def dropdown_values(contents, filename):
    if contents and filename:

        df = parse_contents(contents, filename)
        actual_headers = list(df.columns.values)
        options = []

        for i in actual_headers:
            options.append({'label': i, 'value': i})

        return [options]

    else:

        no_headers = [{'label': '', 'value': ''}]
        return [no_headers]


@app.callback(Output('alert', 'displayed'),
              Input('metric', 'options'),
              State('datatable_upload', 'filename'))
def display_confirm(options, filename):
    if filename:
        if options:
            return True
    return False


@app.callback([Output('stored_metric', 'children'),
               Output('stored_max_delta', 'children')],
              [Input('submit_button', 'n_clicks')],
              [State('metric', 'value'),
               State('max_delta', 'value')])
def store_params(n_clicks, metric, max_delta):
    return metric, max_delta


@app.callback([Output('print_spikes', 'data'),
               Output('print_spikes', 'columns'),
               Output('selected_date', 'children')],
              [Input('stored_metric', 'children'),
               Input('stored_max_delta', 'children'),
               Input('print_spikes', 'selected_rows')],
              [State('datatable_upload', 'contents'),
               State('datatable_upload', 'filename')])
def temp_spikes(metric, max_delta, selected_row, contents, filename):
    if contents and filename:

        df = parse_contents(contents, filename)

        idx = pd.date_range(df.index.min(), df.index.max(), freq='H')
        df = df[[metric]]
        df = df.reindex(idx, fill_value=10000)

        df_shift_up = df.shift(-1)
        df_shift_down = df.shift(1)

        df_shift_up = df_shift_up.fillna(10000)
        df_shift_down = df_shift_down.fillna(10000)

        df_up_math = df.sub(df_shift_up, fill_value=10000).abs().round(1)
        df_down_math = df.sub(df_shift_down, fill_value=10000).abs().round(1)

        df_up_math = df_up_math[(df_up_math[metric] > max_delta) & (df_up_math[metric] < 9000)]
        df_down_math = df_down_math[(df_down_math[metric] > max_delta) & (df_down_math[metric] < 9000)]

        df_temp_spikes_math = df_up_math.merge(df_down_math, left_index=True, right_index=True,
                                               suffixes=['_down', '_up'])
        df_temp_spikes = df.merge(df_temp_spikes_math, left_index=True, right_index=True)
        df_temp_spikes = df_temp_spikes.replace(to_replace=10000, value=np.nan)
        df_temp_spikes = df_temp_spikes.reset_index()

        if selected_row and len(df_temp_spikes.index) > 0:
            if selected_row[0] <= len(df_temp_spikes.index):
                picked_row = df_temp_spikes.iloc[selected_row]
                date = picked_row['index']
            else:
                date = 'No Selection'
        else:
            date = 'No Selection'

        return df_temp_spikes.to_dict('records'), [{'name': i, 'id': i} for i in df_temp_spikes.columns], date

    else:

        return start_table_df.to_dict('records'), [{'id': '', 'name': ''}], 'No Selection'


@app.callback([Output('print_24hr', 'data'),
               Output('print_24hr', 'columns'),
               Output('table_length', 'children')],
              [Input('selected_date', 'children'),
               Input('datatable_upload', 'contents'),
               Input('datatable_upload', 'filename')])
def table24(date, contents, filename):
    if contents and filename and date != 'No Selection':

        date = date[0]
        date = dt.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')

        if date.hour == 0:
            date1 = date - timedelta(hours=23)
            date2 = date
        else:
            date1 = date.strftime('%Y-%m-%d')
            date1 = dt.datetime.strptime(date1, '%Y-%m-%d') + timedelta(hours=1)
            date2 = date1 + timedelta(hours=23)

        df = parse_contents(contents, filename)

        idx = pd.date_range(df.index.min(), df.index.max(), freq='H')
        df = df.reindex(idx, fill_value=10000)
        df = df.loc[date1:date2]
        df = df.replace(10000, np.nan)
        df = df.reset_index()

        length = len(df.index)

        return df.to_dict('records'), [{'name': i, 'id': i} for i in df.columns], length

    else:

        return start_table_df.to_dict('records'), [{'id': '', 'name': ''}], 0


@app.callback([Output('scatter_plot', 'figure')],
              [Input('metric', 'options'),
               Input('table_length', 'children'),
               Input('selected_date', 'children'),
               Input('datatable_upload', 'contents'),
               Input('datatable_upload', 'filename')])
def graph24(metrics, table24length, date, contents, filename):
    if table24length == 0:
        date = 'No Selection'

    if contents and filename and date != 'No Selection':

        date = date[0]
        date = dt.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')

        if date.hour == 0:
            date1 = date - timedelta(hours=23)
            date2 = date
        else:
            date1 = date.strftime('%Y-%m-%d')
            date1 = dt.datetime.strptime(date1, '%Y-%m-%d') + timedelta(hours=1)
            date2 = date1 + timedelta(hours=23)

        df = parse_contents(contents, filename)

        idx = pd.date_range(df.index.min(), df.index.max(), freq='H')
        df = df.reindex(idx, fill_value=10000)
        df = df.loc[date1:date2]
        df = df.replace(10000, np.nan)
        df = df.reset_index()

        actual_metrics = []
        for i in metrics:
            actual_metrics.append(i['value'])

        fig = go.Figure()

        for m in actual_metrics:
            fig.add_trace(go.Scatter(x=df['index'], y=df[m], mode='lines+markers', name=m))

        return [fig]

    else:

        fig = go.Figure()

        return [fig]
