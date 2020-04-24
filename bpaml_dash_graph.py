# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import data_cache
import utilities

data = data_cache.DataCache()
ar_country = data.df_for_case_type()['Country/Region'].unique()
ar_country.sort()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children="Beginners' Python and Machine Learning - Dash web apps"),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

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


@app.callback(
    dash.dependencies.Output('input-state', 'options'),
    [dash.dependencies.Input('input-country', 'value')])
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


if __name__ == '__main__':
    app.run_server(debug=True)
