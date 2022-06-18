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
from .dw_access.domains import getSubdomains, getSubdomainsInfo, getCorrections, getOldRecord, getOldRecord_Domain, answers_by_level, score_by_level_gender, getYears_Domain
from .dw_access.domains import get_answers_degree, general_dm_answers, get_answers_domain, get_questions_domain, get_evaluation_history, get_top_students, get_questions_domain
from .dw_access.users import get_general_right_wrong
from .dw_access.materialized import getMaterializedDates
import threading

url_base = '/dash/home/'

def Add_Dash(server):
    start_timer = dt.now()
    external_stylesheets = [dbc.themes.BOOTSTRAP,'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css']
    app = Dash(server=server, url_base_pathname=url_base, external_stylesheets=external_stylesheets)

    mongoDW = PyMongo(server,'mongodb://localhost:27017/dw_leonardo')

    domains = mongoDW.db.dm_answers.distinct("Dim_Question.Domain")
    general_answers = general_dm_answers(mongoDW)

    app.layout=html.Div(
                    style={"background": "#F7F7F7"},
                    children=[
                        dbc.Col([
                            dbc.Card(
                                style={"background":"transparent", "border":"none"},
                                children=[
                                    dbc.CardBody([
                                        dbc.Row([
                                            dbc.Col([
                                                html.I(className="fa fa-database", children=[" Domínios"], style={'color': '#73879C'}),
                                                html.H2(general_answers[0]['total']['domains'], style={'color': '#1ABB9C'}),
                                                html.I(className="fa fa-sort-asc", 
                                                children=[
                                                    html.Label(str(general_answers[1]['semana']['domains'])+'%'),
                                                    html.Label(" Na ultima semana",style={'color': '#73879C'})
                                                    ], 
                                                style={'color': '#1ABB9C'})
                                            ],style={'border-right': 'dashed #bbb'}),
                                            dbc.Col([
                                                html.I(className="fa fa-database", children=[" Respostas Certas"], style={'color': '#73879C'}),
                                                html.H2(general_answers[0]['total']['right'],style={'color': '#1ABB9C'}),
                                                html.I(className="fa fa-sort-asc", 
                                                children=[
                                                    html.Label(str(general_answers[1]['semana']['right'])+'%'),
                                                    html.Label(" Na ultima semana",style={'color': '#73879C'})
                                                    ], 
                                                style={'color': '#1ABB9C'})
                                            ],style={'border-right': 'dashed #bbb'}),
                                            dbc.Col([
                                                html.I(className="fa fa-database", children=[" Respostas Erradas"], style={'color': '#73879C'}),
                                                html.H2(general_answers[0]['total']['wrong'], style={'color': '#1ABB9C'}),
                                                html.I(className="fa fa-sort-asc", 
                                                children=[
                                                    html.Label(str(general_answers[1]['semana']['wrong'])+'%'),
                                                    html.Label(" Na ultima semana",style={'color': '#73879C'})
                                                    ], 
                                                style={'color': '#1ABB9C'})
                                            ],style={'border-right': 'dashed #bbb'}),
                                            dbc.Col([
                                                html.I(className="fa fa-clock-o", children=[" Tempo médio de Resposta"], style={'color': '#73879C'}),
                                                html.H2(general_answers[0]['total']['avg'], style={'color': '#1ABB9C'}),
                                                html.I(className="fa fa-sort-asc", 
                                                children=[
                                                    html.Label(str(general_answers[1]['semana']['avg'])+'%'),
                                                    html.Label(" Na ultima semana",style={'color': '#73879C'})
                                                    ], 
                                                style={'color': '#1ABB9C'})
                                            ],style={'border-right': 'dashed #bbb'}),
                                            dbc.Col([
                                                html.I(className="fa fa-star", children=[" Avaliações"], style={'color': '#73879C'}),
                                                html.H2(general_answers[0]['total']['wrong']+general_answers[0]['total']['right'], style={'color': '#1ABB9C'}),
                                                html.I(className="fa fa-sort-asc", 
                                                children=[
                                                    html.Label(str(general_answers[1]['semana']['wrong']+general_answers[1]['semana']['right'])+'%'),
                                                    html.Label(" Na ultima semana",style={'color': '#73879C'})
                                                    ], 
                                                style={'color': '#1ABB9C'})
                                            ],style={'border-right': 'solid #bbb'}),
                                            dbc.Col([
                                                html.I(className="fa fa-clock-o", children=["Ultima Atualização"], style={'color': '#73879C'}),
                                                html.H5(id="refresh-date",style={'color': '#858484'}),
                                                dbc.Button( "Atualizar", id="refresh-button", outline=True, color="secondary", className="mr-1", size="sm"),
                                            ])
                                    ])])
                                    ]
                            )
                        ]),
                    #dcc.Loading(
                    dbc.Card(
                        style={"height": "600px"},
                        children=[
                        dbc.CardHeader([html.H4("Número de respostas por domínio de avaliação",style={'color': '#73879C'})]),
                        dbc.CardBody([
                            html.Div([
                            dbc.Row([
                                dbc.Col([
                                    dcc.DatePickerRange(
                                        id='my-date-picker-range',
                                        day_size=30,
                                        display_format= "YYYY-MM-DD",
                                    )
                                ]),
                                dbc.Col([
                                    html.Div(
                                        children=[
                                            html.H4('Domínio:', style={'color': '#73879C'}),
                                            dcc.Dropdown(
                                                id='domain-dropdown',
                                                placeholder='Dominio...',
                                            )
                                        ])
                                ],md=4),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.Div(
                                        id='lines_graph',
                                        children=[],
                                    )
                                ])
                            ])
                            ]),
                        ]),
                    ]),
                    dbc.Card(
                        style={'margin-top':'20px'},
                        children=[
                        dbc.CardHeader("Informações gerais",style={'color': '#73879C'}),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Div(
                                        children=[
                                            html.H4('Subdomínio:', style={'color': '#73879C',"marginBottom":'10px'}),
                                            dcc.Dropdown(
                                                id='subdomain-dropdown',
                                                placeholder='Subdomínio...',
                                            )
                                    ])
                                ],md=4)
                            ]),
                            dbc.Row(
                                style={'margin-top':'10px'},
                                children=[
                                dbc.Col([
                                    dbc.Card([
                                        dbc.CardHeader("Histórico de avaliações",style={'color': '#73879C'}),
                                        dbc.CardBody([
                                            dbc.Row([
                                                dbc.Col([
                                                    dcc.Dropdown(
                                                    id='year-dropdown',
                                                    placeholder='Ano...',
                                                    )
                                                ]),
                                                dbc.Col([
                                                    dcc.Dropdown(
                                                    id='month-dropdown',
                                                    placeholder='Mês...',
                                                    )
                                                ])
                                            ]),
                                            html.Div(
                                                id='bar_chart_evaluation',
                                                children=[]
                                            ),
                                        ])
                                    ])
                                ],md=4),
                                dbc.Col([
                                    dbc.Card(
                                        id='card_questions',                                        
                                    )
                                ],md=4),
                                dbc.Col([
                                    dbc.Card([
                                        dbc.CardHeader("Classificações",style={'color': '#73879C'}),
                                        dbc.CardBody([
                                            dbc.ListGroup(
                                                id="list_top_alunos"
                                            )
                                        ])
                                    ])
                                ],md=4)
                            ])
                        ])
                    ])
        ])
    
    @app.callback(
    [Output('refresh-date', 'children'),
    Output('domain-dropdown', 'value'),
    Output('domain-dropdown', 'options')],
    [Input('refresh-button', 'n_clicks')])
    def refresh(clicks):
        print("click!")
        domains_json=[]
        domains = mongoDW.db.dm_answers.distinct("Dim_Question.Domain")
        for d in domains:
            json={
                'label':d,
                'value':d
            }
            domains_json.append(json)
    
        return dt.now().strftime('%Y-%m-%d %H:%M:%S'), domains_json[0]['value'], domains_json

    @app.callback(
    [Output('my-date-picker-range','start_date'),
        Output('my-date-picker-range','initial_visible_month'),
        Output('my-date-picker-range','min_date_allowed'),
        Output('my-date-picker-range','end_date'),
        Output('my-date-picker-range','max_date_allowed')],
    [Input('domain-dropdown', 'value'),])
    def update_dates(dom):
        dates = getMaterializedDates(dom,mongoDW)
        start = dates[0]['Start_Date'].date()
        end = dates[0]['End_Date'].date()
        if dates is not None:
            months_ago = end - relativedelta(months=3)
        
        return months_ago, start, start, end, end

    @app.callback(
    [Output('subdomain-dropdown', 'options'),
        Output('subdomain-dropdown', 'value')],
    [Input('domain-dropdown', 'value')])
    def update_subdomains(dom):
        subdoms=getSubdomains(dom,mongoDW)
        if subdoms is not None:
            return subdoms, subdoms[0]['value']
    
    @app.callback(
    [Output('year-dropdown', 'options'),
    Output('year-dropdown', 'value'),
    Output('month-dropdown', 'options'),
    Output('month-dropdown', 'value')],
    [Input('subdomain-dropdown', 'value')],
    [State('domain-dropdown','value')])
    def update_years_months(subdom,dom):
        years = getYears_Domain(dom,subdom,mongoDW)
        years.sort(reverse=True)
        mes_json=[]
        for i in range(1,13):
            mes = calendar.month_name[i]
            mes_json.append({'label':mes,'value':mes})
        years_json=[]
        for y in years:
            json={
                'label':y,
                'value':y
            }
            years_json.append(json)
        return years_json,years_json[0]['value'], mes_json, mes_json[0]['value']

    @app.callback(
    Output('lines_graph','children'),
    [Input('domain-dropdown','value'),
    Input('my-date-picker-range','end_date')],   #ver se não há race_condition, inputs são lidos por ordem?????
    [State('my-date-picker-range','start_date')])
    def create_line_graph(dom,end_date,start_date):
        start_date = dt.strptime(start_date, '%Y-%m-%d')
        end_date = dt.strptime(end_date, '%Y-%m-%d')
        answers_number = get_answers_domain(dom,start_date,end_date,mongoDW)
        fig = go.Figure()
        for a in answers_number:
            fig.add_trace(go.Scatter(x=a['dates'], y=a['list_a'], name=a['_id']))
        fig.update_traces(mode='markers+lines')
        fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            'title':'Respostas por Subdomínio'
        })
        return dcc.Graph(figure=fig)

    @app.callback(
    Output('bar_chart_evaluation', 'children'),
    [Input('month-dropdown', 'value'),
    Input('subdomain-dropdown','value'),
    Input('year-dropdown', 'value')],
    [State('domain-dropdown', 'value')])
    def create_evaluation_history(month,subdom,year,dom):
        history = get_evaluation_history(month,subdom,year,dom,mongoDW)
        my_layout = go.Layout({"title": "Pontuação média por semana",
                                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                'xaxis':{ 'showgrid': False}
        })

        if history is not None:
            fig = go.Figure(data=[go.Bar(y=history[0]['week_list'], x=history[0]['answerpoints_avg_list'],marker={'color':'#6ea865'},orientation='h',width=0.5)]
                            ,layout = my_layout)
            return dcc.Graph(figure=fig)
    
    @app.callback(
        Output('list_top_alunos','children'),
        [Input('my-date-picker-range','end_date'),
        Input('subdomain-dropdown', 'value')],
        [State('my-date-picker-range','start_date'),
        State('domain-dropdown', 'value')])
    def get_top_stud(end,subdom,start,dom):
        start = dt.strptime(start, '%Y-%m-%d')
        end = dt.strptime(end, '%Y-%m-%d')
        top = get_top_students(dom,subdom,start,end,mongoDW)
        list_items=[]
        for i in range(0,len(top)):
            list_items.append(dbc.ListGroupItemHeading(top[i]['_id']['name'], style={'color':'#73879C'}))
            list_items.append(
                dbc.ListGroupItemText([
                    dbc.Row([
                        dbc.Col([
                        html.Img(src="/static/images/avatars/user.png", style={'width':'50%'})
                        ],md=4),
                        dbc.Col([
                            dcc.Markdown('''
                            **Pontuação: **'''+ str(top[i]['points_user'])),

                            dcc.Markdown('''
                            **Curso: **'''+top[i]['_id']['degree'],
                            style={'display':'inline-flex'}
                        )
                        ])
                    ])
                ])
            )
        return list_items
    
    @app.callback(
        Output('card_questions','children'),
        [Input('domain-dropdown','value'),
        Input('subdomain-dropdown', 'options')])
    def get_top_stud(domain, subdomains):
        list_questions = get_questions_domain(domain,mongoDW)
        colors=['#6ea865','#375573']
        total = len(subdomains)
        perc_list=[]
        labels=[]
        for q in list_questions:
            labels.append(q['_id'])
            perc_list.append((len(q['questions_subdomain'])/total)*100)
        my_layout = go.Layout({'legend':{
                                'y':-2,
                            }}
        )
        fig = go.Figure(data=[go.Pie(labels=labels, values=perc_list, hole=.3, marker_colors=colors)],layout=my_layout)
        card=[
            dbc.CardHeader("Relatório de Questões - "+domain,style={'color': '#73879C'}),
            dbc.CardBody([
                (dcc.Graph(figure=fig))
            ])]
        return card

    return app.server




