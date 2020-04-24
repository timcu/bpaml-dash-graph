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

    html.Div(children="", id="text-selected-country"),

])

# - figure_cumulative_doubling has been provided from meetup053
# - add a dash_core_components Graph object with id="graph-doubling-days" and a figure=fig_for_location(data=data)
# - define a function update_graph(country, state) which returns a figure based on selected country and state
# - Use the @app.callback decorator to call the function when "value" of "input-country" or "input-state" changes


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
     Input('input-state', 'value')])
def update_graph(country=None, state=None):
    global data
    return figure_cumulative_doubling.fig_for_location(data, country, state)


if __name__ == '__main__':
    app.run_server(debug=True)
