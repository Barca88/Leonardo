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
from flask_pymongo         import PyMongo
from bson.json_util import dumps, loads
from datetime import datetime as dt, time
from dateutil.relativedelta import relativedelta
import calendar
import requests
import re
from .dw_access.domains import getSubdomains, getSubdomainsInfo, getCorrections, getOldRecord, answers_by_level, score_by_level_gender, get_answers_degree, get_top_students
import threading
from pymongo import MongoClient

url_base = '/dash/app1/'

def Add_Dash(server):
    start_timer = dt.now()
    external_stylesheets = [dbc.themes.BOOTSTRAP,'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css']
    app = Dash(server=server, routes_pathname_prefix=url_base, external_stylesheets=external_stylesheets)

    mongoDW = PyMongo(server,'mongodb://localhost:27017/dw_leonardo')

    filter_options=[{'label':'Semestre','value':1},{'label':'Trimestre','value':2},
                    {'label':'Mês','value':3}]

    domains = mongoDW.db.dm_answers.distinct("Dim_Question.Domain")
    years = mongoDW.db.dm_answers.distinct("Dim_Calendar.Year")
    subdomainOfDomain = []
    if domains is not None and domains != []:
        subdomainOfDomain = mongoDW.db.dm_answers.distinct('Dim_Question.Subdomain',{'Dim_Question.Domain':domains[0]})

    app.layout=html.Div(
                    style={"background": "#F7F7F7"},
                    children=[
                    dbc.Card(
                        style={"height": "1500px"},
                        children=[
                        dbc.CardHeader([html.H4("Desempenho por domínio de avaliação",style={'color': '#73879C'})]),
                        dbc.CardBody([
                            html.Div([
                            dbc.Row([
                                dbc.Col([
                                    dcc.DatePickerRange(
                                        id='my-date-picker-range',
                                        day_size=30,
                                        display_format= "YYYY-MM-DD",
                                    ),
                                html.Div(
                                    id='domains_graph',
                                    children=[],
                                )
                                ],md=9),
                                dbc.Col([
                                    html.Div(
                                        children=[
                                            html.H4('Domínio:', style={'color': '#73879C'}),
                                            dcc.Dropdown(
                                                id='domain-dropdown',
                                                options=[{'label': i, 'value': i} for i in domains],
                                                value=domains[0] if (domains is not None and domains != []) else None,
                                                placeholder='Dominio...',
                                            ),
                                            html.H4('Subdomínio:', style={'color': '#73879C',
                                                                        'margin-top':'20px'}),
                                            dcc.Dropdown(
                                                id='subdomain-dropdown',
                                                options=[{'label': i, 'value': i} for i in subdomainOfDomain],
                                                value=subdomainOfDomain[0] if (subdomainOfDomain is not None and subdomainOfDomain != []) else None,
                                                placeholder='Subdominio...',
                                                optionHeight=45,
                                            )
                                        ]
                                    ),
                                ],md=3)
                                ])
                            ])
                    ]),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Div(
                                    id='bar_chart_dom_1'
                                )
                            ],md=4),
                            dbc.Col([
                                html.Div(
                                    id='bar_chart_dom_2'
                                )
                            ],md=4),
                            dbc.Col([
                                html.Div(
                                    id='bar_chart_dom_3'
                                )
                            ],md=4)
                        ])
                    ]),
                    dbc.CardBody(
                        dbc.Row([
                            dbc.Col([
                                html.Div(
                                    id='line_chart_course'
                                )
                            ],md=8),
                            dbc.Col([
                                html.H4('Top Alunos:', style={'color': '#375573'}),
                                dbc.ListGroup(
                                    id="list_top_alunos"
                                )
                            ],md=4)
                            
                        ])
                        
                    )
                ]),
                dbc.Card(
                    style={"margin-top":"10px","height": "520px"},
                    children=[
                        dbc.CardHeader([html.H4("Desempenho por nível de desempenho",style={'color': '#73879C'})]),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                dcc.Dropdown(
                                    id='year-dropdown',
                                    options=[{'label': i, 'value': i} for i in years],
                                    value=years[0] if (years is not None and years != []) else None,
                                    placeholder='Ano',
                                )],md=2),
                                dbc.Col([
                                dcc.Dropdown(
                                    id='dropdown-options',
                                    options=filter_options,
                                    value=filter_options[0]['value'],
                                    placeholder='Opção...',
                                )],md=2),
                                dbc.Col([
                                    dcc.Dropdown(
                                        id='optionsFilter',
                                    ),
                                ],md=1)
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.Div(
                                        id='bar_chart_level_1',
                                    )
                                ],md=4),
                                dbc.Col([
                                    html.Div(
                                        id='bar_chart_level_2',
                                    )
                                ],md=4),
                                dbc.Col([
                                    html.Div(
                                        id='bar_chart_level_3',
                                    )
                                ],md=4),
                            ])
                        ])
                    ]
                ),
            ])

#-----------------DASHBOARD DESEMPENHO POR DOMINIO -------------------#
    @app.callback(
    [Output('subdomain-dropdown', 'options'),
        Output('subdomain-dropdown', 'value')],
    [Input('domain-dropdown', 'value')])
    def update_subdomains(dom):
        subdoms=getSubdomains(dom,mongoDW)
        if subdoms is not None:
            return subdoms, subdoms[0]['value']

    @app.callback(
    [Output('my-date-picker-range', 'start_date'),
        Output('my-date-picker-range', 'end_date'),
        Output('my-date-picker-range', 'min_date_allowed'),
        Output('my-date-picker-range', 'max_date_allowed'),
        Output('my-date-picker-range', 'initial_visible_month')],
    [Input('subdomain-dropdown', 'value')],
    [State('domain-dropdown', 'value')])
    def update_dates(subdom,dom):
        date_limits=getOldRecord(dom,subdom,mongoDW)
        if date_limits is not None:
            semester_ago = date_limits[0]['Dim_Calendar']['Date'] - relativedelta(months=3)
            start=date_limits[len(date_limits)-1]['Dim_Calendar']['Date']
            end=date_limits[0]['Dim_Calendar']['Date']
        else:
            semester_ago=dt.now()
            start=dt.now()
            end=dt.now()
        history={}
        return semester_ago.date(),end.date(),start.date(),end.date(),semester_ago.date()
    
    @app.callback(
    Output('domains_graph', 'children'),
    [Input('my-date-picker-range', 'end_date')] ,
    [State('my-date-picker-range', 'start_date'),
    State('domain-dropdown', 'value'),
    State('subdomain-dropdown', 'value')])
    def update_graph_dates(end,start_date,dom,subdom):
        return create_domains_graph(dom,subdom,start_date,end)

    def create_domains_graph(dom, subdom, start_date,end_date):
        start_date = dt.strptime(start_date, '%Y-%m-%d')
        end_date = dt.strptime(end_date, '%Y-%m-%d')
        json = getCorrections(dom,subdom,start_date,end_date,mongoDW)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=json['dates'], y=json['total_right_answers'], fill='tozeroy',name="Corretas",
                                line = dict(color='#6ea865')))
        fig.add_trace(go.Scatter(x=json['dates'], y=json['total_wrong_answers'], fill='tonexty',name="Erradas",
                                line = dict(color='#375573')))
        fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })
        return dcc.Graph(figure=fig)

    @app.callback(
    [Output('bar_chart_dom_1', 'children'),
        Output('bar_chart_dom_2', 'children'),
        Output('bar_chart_dom_3', 'children')],
    [Input('my-date-picker-range', 'end_date')],
    [State('my-date-picker-range', 'start_date'),
    State('domain-dropdown', 'value')])
    def create_bar_graph_1(end,start,dom):
        start = dt.strptime(start, '%Y-%m-%d')
        end = dt.strptime(end, '%Y-%m-%d')
        doms_info = getSubdomainsInfo(dom,start,end,mongoDW)
        my_layout = go.Layout({"title": "Respostas por domínio",
                                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                'xaxis':{ 'showgrid': False,
                                        'showticklabels':False,
                                        #'showspikes':False,
                                        #'ticks':""
                                        } #tickcolor ticklen,
        })
        if doms_info is not None:
            fig1 = go.Figure(data=[go.Bar(x=doms_info[0]['subs_list'], y=doms_info[0]['questions_list'],marker={'color':'#375573'})],layout = my_layout)
            fig2 = go.Figure(data=[go.Bar(x=doms_info[0]['subs_list'], y=doms_info[0]['points_f_list'],marker={'color':'#6ea865'},name='Feminino'),
                                    go.Bar(x=doms_info[0]['subs_list'], y=doms_info[0]['points_m_list'],marker={'color':'#375573'},name='Masculino')],layout = my_layout)
            fig3 = go.Figure(data=[go.Bar(x=doms_info[0]['subs_list'], y=doms_info[0]['answertime_avg_list'],marker={'color':'#375573'})],layout = my_layout)

        fig2.update_layout(title='Pontuação por género')
        fig3.update_layout(title='Tempo médio de Resposta')
        return dcc.Graph(figure=fig1),dcc.Graph(figure=fig2),dcc.Graph(figure=fig3)
    
    #   Adicionar logica pras datas
#   Se ja tiver dados da bd:
#       if start_date>=points[0]['dates'][0] and end_ate=<points[0]['dates'][0]
#           não faço get apenas set do xaxis_range
#       else
#           vou a bd e faço match pelas datas 
#
#   posso passar isto pra cima e filtrar por dominio fica melhor???? i think so

    @app.callback(
    Output('line_chart_course','children'),
    [Input('subdomain-dropdown', 'value'),
    Input('my-date-picker-range','end_date')],
    [State('my-date-picker-range','start_date'),
    State('domain-dropdown', 'value')])
    def create_course_graph(subdom,end_date,start_date,dom):
        start_date = dt.strptime(start_date, '%Y-%m-%d')
        end_date = dt.strptime(end_date, '%Y-%m-%d')
        points = get_answers_degree(dom,subdom,start_date,end_date,mongoDW)
        fig = go.Figure()
        colors=['#6ea865','#375573']
        c=0
        for p in points:
            fig.add_trace(go.Scatter(x=p['dates'], y=p['list_p'],name=p['_id'],line = dict(color=colors[c])))
            c=c+1
        fig.update_traces(mode='markers+lines')
        fig.update_layout(xaxis_range=[start_date,end_date])
        fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            'title':'Desempenho por Curso'
        })
        return dcc.Graph(figure=fig)

    @app.callback(
        Output('list_top_alunos','children'),
        [Input('my-date-picker-range','end_date'),
        Input('subdomain-dropdown', 'value')],
        [State('my-date-picker-range','start_date'),
        State('domain-dropdown', 'value')]
    )
    def get_top_stud(end,subdom,start,dom):
        start = dt.strptime(start, '%Y-%m-%d')
        end = dt.strptime(end, '%Y-%m-%d')
        top = get_top_students(dom,subdom,start,end,mongoDW)
        list_items=[]
        for i in range(0,len(top)):
            list_items.append(dbc.ListGroupItemHeading(top[i]['_id']['name'], style={'color':'#73879C'}))
            list_items.append(dbc.ListGroupItemText(dcc.Markdown('''
                                                    **Pontuação: **'''+ str(top[i]['points_user'])+'''

                                                    **Curso: **'''+top[i]['_id']['degree']) 
            ))
        return list_items

#-------------------------------------------------------FIM--------------------------------------------------------#

#--------------------------------------DASHBOARD POR NIVEL---------------------------------------------------------#
    @app.callback(
        [Output('optionsFilter', 'value'),
        Output('optionsFilter', 'options'),
        Output('optionsFilter', 'style')],
        [Input('dropdown-options', 'value')])
    def toggle_container(opcao):
        if(opcao==1):
            semester_json=[{'label':'1','value':'1'},{'label':'2','value':'2'}]
            return semester_json[0]['value'], semester_json,{}
        if(opcao==2):
            quarter_json=[{'label':'1','value':'1'},{'label':'2','value':'2'},
                {'label':'3','value':'3'},{'label':'4','value':'4'}]
            return quarter_json[0]['value'], quarter_json,{}
        if(opcao==3):
            mes_json=[]
            for i in range(1,13):
                mes = calendar.month_name[i]
                mes_json.append({'label':mes,'value':mes})
            return mes_json[0]['value'], mes_json,{'width':'120%'}
        else:
            return "", [],{'display':'none'}
    
    @app.callback(
        [Output('bar_chart_level_1', 'children'),
        Output('bar_chart_level_2', 'children')],
        [Input('optionsFilter', 'value'),
        Input('year-dropdown', 'value')],
        [State('dropdown-options', 'value')])
    def create_bar_levels(optionNumber,year,sem_qua_mon):
        if sem_qua_mon==1:
            bar_data = answers_by_level(year,optionNumber,None,None,mongoDW)
        else:
            if sem_qua_mon==2:
                bar_data = answers_by_level(year,None,optionNumber,None,mongoDW)
            else:
                bar_data = answers_by_level(year,None,None,optionNumber,mongoDW)
        my_layout = go.Layout({"title": "Respostas por nível",
                                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                'xaxis':{ 'showgrid': False,
                                        'showticklabels':False}
        })

        if not bar_data: 
            fig1={}     
            fig3={}              
        else:
            fig1 = go.Figure(data=[go.Bar(x=bar_data[0]['levels_list'], y=bar_data[0]['right_list'],marker={'color':'#6ea865'},name='Corretas'),
                    go.Bar(x=bar_data[0]['levels_list'], y=bar_data[0]['wrong_list'],marker={'color':'#375573'},name='Erradas')],layout=my_layout)
            fig3 = go.Figure(data=[go.Bar(x=bar_data[0]['levels_list'], y=bar_data[0]['answertime_avg_list'],marker={'color':'#375573'})],layout = my_layout)
            fig3.update_layout(title='Tempo médio de Resposta')
                        
        return dcc.Graph(figure=fig1),dcc.Graph(figure=fig3)
    
    @app.callback(
        Output('bar_chart_level_3', 'children'),
        [Input('optionsFilter', 'value'),
        Input('year-dropdown', 'value')],
        [State('dropdown-options', 'value')])
    def create_bar_level_3(optionNumber,year,sem_qua_mon):
        if sem_qua_mon==1:
            bar_data = score_by_level_gender(year,optionNumber,None,None,mongoDW)
        else:
            if sem_qua_mon==2:
                bar_data = score_by_level_gender(year,None,optionNumber,None,mongoDW)
            else:
                bar_data = score_by_level_gender(year,None,None,optionNumber,mongoDW)
        my_layout = go.Layout({"title": "Pontuação por nível",
                                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                'xaxis':{ 'showgrid': False,
                                        'showticklabels':False}
        })
        if not bar_data: 
            fig1={}                   
        else:
            fig1 = go.Figure(data=[go.Bar(x=bar_data[0]['levels_list'], y=bar_data[0]['points_f_list'],marker={'color':'#6ea865'},name='Feminino'),
                    go.Bar(x=bar_data[0]['levels_list'], y=bar_data[0]['points_m_list'],marker={'color':'#375573'},name='Masculino')],layout=my_layout)
                        
        return dcc.Graph(figure=fig1)

    return app.server




