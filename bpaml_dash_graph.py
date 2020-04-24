# -*- coding: utf-8 -*-
import dash
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children="Beginners' Python and Machine Learning - Dash web apps"),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

])

if __name__ == '__main__':
    app.run_server(debug=True)
