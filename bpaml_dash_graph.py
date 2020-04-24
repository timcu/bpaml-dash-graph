# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import data_cache
import figure_cumulative_doubling
import utilities

data = data_cache.DataCache()
ar_country = data.df_for_case_type()['Country/Region'].unique()
ar_country.sort()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children="Beginners' Python and Machine Learning - Dash web apps"),

    html.H2(children='COVID-19 data from Johns Hopkins CSSE'),

    dcc.Graph(
        id='graph-doubling-days',
        figure=figure_cumulative_doubling.fig_for_location(data=data),
    ),

    html.Div(children=[
        html.Div(children=[
            html.Label("Country", htmlFor="input-country"),
            dcc.Dropdown(
                id="input-country",
                value="",
                options=[{"label": country, "value": country} for country in ar_country],
            ),
            html.Label("State", htmlFor="input-state"),
            dcc.Dropdown(
                id="input-state",
                value="",
                options=[],
            ),
        ], style={"breakInside": "avoid"}),

        html.Div(children=[
            html.Label("Averaged days", htmlFor="input-averaged-days"),
            dcc.Slider(
                id="input-averaged-days",
                min=1,
                max=10,
                value=5,
                marks={str(n+1): str(n+1) for n in range(10)}
            ),
            html.Label("Starting number", htmlFor="input-num-start"),
            dcc.Input(
                id="input-num-start",
                min=1,
                value=100,
                type="number",
            ),
        ], style={"breakInside": "avoid"}),

        html.Div(children=[
            html.Label("Case type", htmlFor="input-case-type"),
            dcc.RadioItems(
                id="input-case-type",
                value="confirmed",
                options=[{"label": s, "value": s} for s in ("confirmed", "recovered", "deaths")],
                labelStyle={"display": "inline-block"},
            ),
            html.Label("Graph type", htmlFor="input-yaxes-type"),
            dcc.RadioItems(
                id="input-yaxes-type",
                value="log",
                options=[{"label": s, "value": s} for s in ("linear", "log")],
                labelStyle={"display": "inline-block"},
            ),
        ], style={"breakInside": "avoid"}),
    ], style={"columnCount": 3}),


    html.Div(children="", id="text-selected-country"),

])


@app.callback(
    Output('input-state', 'options'),
    [Input('input-country', 'value')])
def update_ar_state(country):
    global data
    if country:
        df = data.df_for_case_type()
        df = df[df["Country/Region"] == country]
        ar = df["Province/State"].dropna().unique()
        ar.sort()
    else:
        ar = data.df_for_case_type()["Province/State"].dropna().unique()
        ar.sort()
    lst = [{'label': state, 'value': state} for state in ar]
    return lst


@app.callback(
    Output('text-selected-country', 'children'),
    [Input('input-country', 'value'),
     Input('input-state', 'value')])
def update_text_selected_country(country=None, state=None):
    return f"You have selected {utilities.location_name(country, state)}"


@app.callback(
    Output('graph-doubling-days', 'figure'),
    [Input('input-country', 'value'),
     Input('input-state', 'value'),
     Input('input-num-start', 'value'),
     Input('input-case-type', 'value'),
     Input('input-averaged-days', 'value'),
     Input('input-yaxes-type', 'value')])
def update_graph(country, state, num_start, case_type, averaged_days, yaxes_type):
    global data
    parameters = {}
    if num_start:
        parameters['num_start'] = num_start
    return figure_cumulative_doubling.fig_for_location(data, country, state, case_type=case_type, averaged_days=averaged_days, yaxes_type=yaxes_type, **parameters)


if __name__ == '__main__':
    app.run_server(debug=True)
