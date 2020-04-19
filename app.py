from dash.dependencies import Input, State, Output
import dash_core_components as dcc
import dash_html_components as html

from dash import Dash
import dash_table

import pandas as pd
from collections import OrderedDict

import numpy as np
import datetime

app = Dash(__name__)

INTERVAL = 30

# app layouts to choose from

def layout_func1():
    dates,news,totals,recov,hosp,ICU,death,ie,n,pm,south,wpg,tested=get_data()
    return html.Div(children=[
        html.H1(children='Manitoba COVID Cases'),
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': dates, 'y': news, 'type': 'bar', 'name': 'New Cases'},
                    {'x': dates, 'y': totals, 'type': 'scatter','mode':'lines+markers', 'name': u'Cumulative'},
                ],
                'layout': {
                    'title': 'Cumulative and New COVID cases',
                    'font': {'family':'Oswald, sans-serif','size':'26'}
                }
            }
        )
    ])

def layout_func2():
    dates,news,totals,recov,hosp,ICU,death,ie,n,pm,south,wpg,tested=get_data()
    return html.Div(children=[
        html.H1(children='Manitoba COVID Cases'),
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': dates, 'y': news, 'type': 'bar', 'name': 'New Cases'},
                ],
                'layout': {
                    'title': 'New COVID cases in Manitoba',
                    'font': {'family':'Oswald, sans-serif','size':'26'}
                }
            }
        )
    ])


def layout_func4():
    dates,news,totals,recov,hosp,ICU,death,ie,n,pm,south,wpg,tested=get_data()
    data = OrderedDict(
        [
            ("Regions", ["Interlake-Eastern", "Northern", "Prairie-Mountain", "Southern", "Winnipeg", "Total"]),
            ("Total Cases", [ie,n,pm,south,wpg,totals[-1]])
        ])
    df = pd.DataFrame(data)
    return html.Div(children=[
        html.H1(children='Manitoba COVID Cases'),
        html.Div(className='left'),
        html.Div(className='middle',children=[
            html.H1(children='Regional Distribution'),
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
                    'font-family': "'Oswald', sans-serif",
                    'font-size': '26px',
                    'text-align': 'center'
                },
            )
        ]),
        html.Div(className='right')
    ])

def layout_day():
    weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
    now=datetime.date.today().weekday()
    return html.Div(children=[
        html.H1(children='Manitoba COVID Cases'),
        html.Div(className='left'),
        html.Div(className='middle',children=[
            html.H1(children='What day is it?'),
            html.H1(children='Today is:'),
            html.Div(className='fwinfo',children=html.H1(children=weekDays[now]),style={'color':'#F00'})
        ]),
        html.Div(className='right')
    ])

def layout_totals():
    dates,news,totals,recov,hosp,ICU,death,ie,n,pm,south,wpg,tested=get_data()
    return html.Div(children=[
        html.H1(children='Manitoba COVID Cases'),
        html.Div(className='left'),
        html.Div(className='middle',children=[
            html.H1(children='Statistics'),
            html.Div(className='note',children=[
                html.Div(className='info2',children=[html.H3('Total Cases'),html.H1(totals[-1])]),
                html.Div(className='success',children=[html.H3('Recovered'),html.H1(recov)]),
                html.Div(className='warning',children=[html.H3('Active Cases'),html.H1(totals[-1]-recov-death)]),
                html.Div(className='danger',children=[html.H3('Deaths'),html.H1(death)]),
                html.Div(className='info',children=[html.H3('Tests Completed'),html.H1(tested)]),
            ])
        ]),
        html.Div(className='right')
    ])


APP_LAYOUTS=[layout_day,layout_totals,layout_func1,layout_func2,layout_func4]

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
    tested=0
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
                #print(thedatetime,thedate,new,derived_total)
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
            if(len(integers)>=15):
                tested=integers[14]
    return dates,news,totals,recov,hosp,ICU,death,ie,n,pm,south,wpg,tested

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
    app.run_server(debug=True)
