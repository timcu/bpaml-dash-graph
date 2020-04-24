# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import data_cache

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

    html.Div(children="", id="text-selected-country"),

])


@app.callback(
    Output('text-selected-country', 'children'),
    [Input('input-country', 'value')])
def update_text_selected_country(country):
    if country:
        return f"You have selected {country}"
    else:
        return f"You haven't selected any country"


if __name__ == '__main__':
    app.run_server(debug=True)
