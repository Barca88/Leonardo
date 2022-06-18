from dash import Dash
import pymongo
import dash
from dash.dependencies import Input, State, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from flask_pymongo         import PyMongo
from bson.json_util import dumps, loads
from datetime import datetime as dt, time
from dateutil.relativedelta import relativedelta
import calendar
import requests
import re
from .dw_access.users import get_general_right_wrong
from .dw_access.materialized import getMaterializedDatesSystem, getMaterializedDatesLogin
from .dw_access.system import getRecentAndOldRecord, getRequestsGetNumber, getLongAndLat, general_dm_system, getRecentAndOldRecordLogins, get_last_sevenDays_logins
import threading

url_base = '/dash/system/'

def Add_Dash(server):
    start_timer = dt.now()
    external_stylesheets = [dbc.themes.BOOTSTRAP,'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css']
    app = Dash(server=server, url_base_pathname=url_base, external_stylesheets=external_stylesheets)

    mongoDW = PyMongo(server,'mongodb://localhost:27017/dw_leonardo')

    domains = mongoDW.db.dm_answers.distinct("Dim_Question.Domain")

    general_dm = general_dm_system(mongoDW)

    app.layout=html.Div(
                    style={"background": "#F7F7F7"},
                    children=[
                        dbc.Col([
                            dbc.Card(
                                id="div1",
                                style={"background":"transparent", "border":"none"},
                                children=[
                                    dbc.CardBody([
                                        dbc.Row([
                                            dbc.Col([
                                                html.I(className="fa fa-database", children=[" Número de Utilizadores"], style={'color': '#73879C'}),
                                                html.H2(general_dm[0]['total']['users'], style={'color': '#1ABB9C'}),
                                                html.I(className="fa fa-sort-asc", 
                                                children=[
                                                    html.Label(str(general_dm[1]['semana']['users'])+'%'),
                                                    html.Label(" Na ultima semana",style={'color': '#73879C'})
                                                    ], 
                                                style={'color': '#1ABB9C'})
                                            ],style={'border-right': 'dashed #bbb'}),
                                            dbc.Col([
                                                html.I(className="fa fa-database", children=[" Número de Quizz Respondidos"], style={'color': '#73879C'}),
                                                html.H2(general_dm[0]['total']['quizz'],style={'color': '#1ABB9C'}),
                                                html.I(className="fa fa-sort-asc", 
                                                children=[
                                                    html.Label(str(general_dm[1]['semana']['quizz'])+'%'),
                                                    html.Label(" Na ultima semana",style={'color': '#73879C'})
                                                    ], 
                                                style={'color': '#1ABB9C'})
                                            ],style={'border-right': 'dashed #bbb'}),
                                            dbc.Col([
                                                html.I(className="fa fa-database", children=[" Número de Opiniões"], style={'color': '#73879C'}),
                                                html.H2(general_dm[0]['total']['opiniao'], style={'color': '#1ABB9C'}),
                                                html.I(className="fa fa-sort-asc", 
                                                children=[
                                                    html.Label(str(general_dm[1]['semana']['opiniao'])+'%'),
                                                    html.Label(" Na ultima semana",style={'color': '#73879C'})
                                                    ], 
                                                style={'color': '#1ABB9C'})
                                            ])
                                    ])])
                                    ]
                            )
                        ]),
                        dbc.Card(
                            style={"height": "600px"},
                            children=[
                            dbc.CardHeader(children=[html.H4("Número de acessos ao sistema",style={'color': '#73879C'})]),
                            dbc.CardBody(
                                children=[
                                    dbc.Row([
                                        dcc.DatePickerRange(
                                            id='picker-range-logins',
                                            day_size=30,
                                            display_format= "YYYY-MM-DD",
                                        )
                                    ]),
                                html.Div(
                                    id='bar-login-requests-graph',
                                )
                                ])
                        ]),
                        dbc.Card(
                            style={"margin-top":"10px","height": "600px"},
                            children=[
                            dbc.CardHeader(children=[html.H4("Número de pedidos por página",style={'color': '#73879C'})]),
                            dbc.CardBody(
                                children=[
                                    dbc.Row([
                                        dcc.DatePickerRange(
                                            id='my-date-picker-range',
                                            day_size=30,
                                            display_format= "YYYY-MM-DD",
                                        )
                                    ]),
                                html.Div(
                                    id='bar-get-requests-graph',
                                )
                                ])
                        ]),
                        dbc.Card(
                            style={"margin-top":"10px","height": "1000px"},
                            children=[
                            dbc.CardHeader(children=[html.H4("Volume de Utilizadores por País",style={'color': '#73879C'})]),
                            dbc.CardBody(
                                children=[
                                html.Div(
                                    id='map-graph',
                                )
                                ])
                        ]),
        ])
    
    @app.callback(
    [Output('my-date-picker-range','start_date'),
        Output('my-date-picker-range','initial_visible_month'),
        Output('my-date-picker-range','min_date_allowed'),
        Output('my-date-picker-range','end_date'),
        Output('my-date-picker-range','max_date_allowed')],
    [Input('div1', 'children')]
    )
    def update_dates(random):
        dates=getMaterializedDatesSystem(mongoDW)
        start = dates[0]['Start_Date'].date()
        end = dates[0]['End_Date'].date()
        if dates is not None:
            months_ago = end - relativedelta(months=3)
        
        return months_ago, start, start, end, end

    @app.callback(
    [Output('picker-range-logins', 'start_date'),
        Output('picker-range-logins', 'initial_visible_month'),
        Output('picker-range-logins', 'min_date_allowed'),
        Output('picker-range-logins', 'end_date'),
        Output('picker-range-logins', 'max_date_allowed'),
    ],
        [Input('div1', 'children')]
    )
    def update_dates_login(random):
        dates=getMaterializedDatesLogin(mongoDW)
        start = dates[0]['Start_Date'].date()
        end = dates[0]['End_Date'].date()
        if dates is not None:
            months_ago = end - relativedelta(days=7)
        return months_ago, start, start, end, end

    @app.callback(
    Output('bar-get-requests-graph', 'children'),
    [Input('my-date-picker-range', 'end_date')],
    [State('my-date-picker-range', 'start_date')])
    def create_bar_graph_1(end,start):
        start = dt.strptime(start, '%Y-%m-%d')
        end = dt.strptime(end, '%Y-%m-%d')
        requestsGet = getRequestsGetNumber(start,end,mongoDW)
        layout_get = go.Layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                'margin':dict(l=40, r=25, b=150, t=10),
                                'xaxis':{ 'showgrid': False}
        })

        fig1={}

        if requestsGet != []:
            fig1 = go.Figure(data=[go.Bar(x=requestsGet[0]['url_list'], y=requestsGet[0]['request_list_get'],marker={'color':'#6ea865'},name='GET'),
                                    go.Bar(x=requestsGet[0]['url_list'], y=requestsGet[0]['request_list_post'],marker={'color':'#375573'},name='POST')], layout=layout_get)
        return dcc.Graph(figure=fig1)
    
    @app.callback(
    Output('bar-login-requests-graph', 'children'),
    [Input('picker-range-logins', 'end_date')],
    [State('picker-range-logins', 'start_date')])
    def create_bar_graph_1(end,start):
        start = dt.strptime(start, '%Y-%m-%d')
        end = dt.strptime(end, '%Y-%m-%d')
        requests = get_last_sevenDays_logins(start,end,mongoDW)
        layout = go.Layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                #'margin':dict(l=40, r=25, b=150, t=10),
                                'xaxis':{ 'showgrid': False}
        })

        fig1={}

        if requests is not None:
            fig1 = go.Figure(data=[go.Bar(x=requests['date_list'], y=requests['authorized_logins'],marker={'color':'#6ea865'},name='Autorizados'),
                                    go.Bar(x=requests['date_list'], y=requests['unauthorized_logins'],marker={'color':'#375573'},name='Não Autorizados')], layout=layout)

        return dcc.Graph(figure=fig1)
    
    @app.callback(
    Output('map-graph', 'children'),
    [Input('my-date-picker-range', 'end_date')],
    [State('my-date-picker-range', 'start_date')])
    def create_bar_graph_1(end,start):
        start = dt.strptime(start, '%Y-%m-%d')
        end = dt.strptime(end, '%Y-%m-%d')

        token="pk.eyJ1IjoibmV0aWVsbCIsImEiOiJja2YyeTI2N2UwemUwMnNtamFtNGZncDF2In0.zsDTVICb0t0bNkKpr38wtw"
        
        fig = go.Figure()

        list_users = getLongAndLat(mongoDW)

        for u in list_users:
            size=len(u['users'])
            fig.add_trace(go.Scattermapbox(
                lat = [str(u['users'][0]['Latitude'])],
                lon = [str(u['users'][0]['Longitude'])],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=size*10
                ),
                text=u['_id']+' - '+str(size)+" utilizadores",
                hoverinfo='text'
            ))

        fig.update_layout(
            autosize=True,
            hovermode='closest',
            showlegend=False,
            mapbox=dict(
                accesstoken=token,
                bearing=0,
                center=dict(
                    lat=u['users'][0]['Latitude'],
                    lon=u['users'][0]['Longitude']
                ),
                pitch=0,
                zoom=6,
                style='light'
            ),
        )
        return dcc.Graph(figure=fig,style={"height": 900})

    return app.server

