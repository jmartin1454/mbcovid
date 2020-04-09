from dash.dependencies import Input, State, Output
import dash_core_components as dcc
import dash_html_components as html

from dash import Dash
import dash_table

import pandas as pd
from collections import OrderedDict

import numpy as np
import datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)


INTERVAL = 30

# app layouts to choose from

def layout_func1():
    dates,news,totals,recov,hosp,ICU,death,ie,n,pm,south,wpg=get_data()
    print("Hi %d"%wpg)
    return html.Div(children=[
        html.H1(children='Manitoba COVID Cases'),
        #html.Div(children='''
        #Dash: A web application framework for Python.
        #'''),

        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': dates, 'y': news, 'type': 'bar', 'name': 'New Cases'},
                    {'x': dates, 'y': totals, 'type': 'bar', 'name': u'Total Cases'},
                ],
                'layout': {
                    'title': 'Manitoba COVID cases'
                }
            }
        )
    ])

def layout_func2():
    dates,news,totals,recov,hosp,ICU,death,ie,n,pm,south,wpg=get_data()
    print("Hi %d"%wpg)
    return html.Div(children=[
        html.H1(children='Manitoba COVID Cases'),
        #html.Div(children='''
        #Dash: A web application framework for Python.
        #'''),

        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': dates, 'y': news, 'type': 'bar', 'name': 'New Cases'},
                    #{'x': dates, 'y': totals, 'type': 'bar', 'name': u'Total Cases'},
                ],
                'layout': {
                    'title': 'New COVID cases in Manitoba',
                    'font-size': '26px'
                }
            }
        )
    ])

def layout_func3():
    dates,news,totals,recov,hosp,ICU,death,ie,n,pm,south,wpg=get_data()
    print("Hi %d"%wpg)
    return html.Div(children=[
        html.H1(children='Manitoba COVID Cases'),
        #html.Div(children='''
        #Dash: A web application framework for Python.
        #'''),

        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    #{'x': dates, 'y': news, 'type': 'bar', 'name': 'New Cases'},
                    {'x': dates, 'y': totals, 'type': 'bar', 'name': u'Total Cases'},
                ],
                #'layout': {
                #    'title': 'Dash Data Visualization'
                #}
            }
        )
    ])

def layout_func4():
    dates,news,totals,recov,hosp,ICU,death,ie,n,pm,south,wpg=get_data()
    data = OrderedDict(
        [
            ("Regions", ["Interlake-Eastern", "Northern", "Prairie-Mountain", "Southern", "Winnipeg", "Total"]),
            ("Total Cases", [ie,n,pm,south,wpg,totals[-1]])
        ])
    df = pd.DataFrame(data)
    return html.Div(children=[
        html.H1(children='Manitoba COVID Cases'),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            style_table={
                'width': '100%'
            },
            style_cell_conditional=[
                {
                    'if': {'column_id': 'Regions'},
                    'textAlign': 'left'
                },
            ],
            style_data_conditional=[
                {
                    'if': {'row_index': 5},
                    'backgroundColor': '#3D9970',
                    'color': 'white'
                }
            ],
            style_cell = {
                #'font-family': 'cursive',
                'font-size': '26px',
                'text-align': 'center'
            },
        )
    ])

APP_LAYOUTS=[layout_func1,layout_func2,layout_func4]

def get_data():
    filename="mbdata.dat"
    dates=[]
    derived_total=0
    news=[]
    totals=[]
    recov=0
    hosp=0
    ICU=0
    death=0
    ie=0
    n=0
    pm=0
    south=0
    wpg=0
    with open(filename,"r") as f:
        for line in f:
            line=line.partition('#')[0]
            line=line.rstrip()
            all_data=line.split()
            integers=list(map(int,all_data))
            if(len(integers)>=4):
                m=integers[0]
                d=integers[1]
                y=integers[2]
                new=integers[3]
                derived_total=derived_total+new
                thedatetime=datetime.datetime(y,m,d)
                thedate=np.datetime64(thedatetime)
                print(thedatetime,thedate,new,derived_total)
                dates.append(thedate)
                news.append(new)
                totals.append(derived_total)
            if(len(integers)>=14):
                total=integers[4]
                recov=integers[5]
                hosp=integers[6]
                ICU=integers[7]
                death=integers[8]
                ie=integers[9]
                n=integers[10]
                pm=integers[11]
                south=integers[12]
                wpg=integers[13]
    #print(dates,news,totals,recov,hosp,ICU,death,ie,n,pm,south,wpg)
    return dates,news,totals,recov,hosp,ICU,death,ie,n,pm,south,wpg

#app.config.supress_callback_exceptions = True
app.layout = html.Div([
    html.Div(id='app-container'),  # your rotating apps will be inserted in here
    dcc.Interval(
        id='interval-component',
        interval=INTERVAL*1000, # in milliseconds
        n_intervals=0
    )
])


@app.callback(Output('app-container', 'children'),
              [Input('interval-component', 'n_intervals')])
def CHANGE_PAGE(n_intervals):
    func = APP_LAYOUTS[n_intervals % len(APP_LAYOUTS)]
    return func()

if __name__ == '__main__':
    app.run_server(debug=False)