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
import flask
from bson.json_util import dumps, loads
from datetime import datetime as dt, time
from dateutil.relativedelta import relativedelta
import calendar
import re
from .dw_access.users import get_info_user, get_general_right_wrong, getOldRecord, getCorrections, getSubdomainsInfo, answers_by_level, getLevelsByDates, general_dm_users, get_answers_domain_user
from .dw_access.domains import getSubdomains, get_answers_domain
import threading
from pymongo import MongoClient

url_base = '/dash/users/'

def Add_Dash(server):
    external_stylesheets = [dbc.themes.BOOTSTRAP,'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css']
    app = Dash(server=server, url_base_pathname=url_base, external_stylesheets=external_stylesheets)

    mongoDW = PyMongo(server,'mongodb://localhost:27017/dw_leonardo')

    user_list = mongoDW.db.dm_answers.distinct("Dim_User.Name")

    domains = mongoDW.db.dm_answers.distinct("Dim_Question.Domain")

    subdomainOfDomain = []

    if domains is not None and domains != []:
        subdomainOfDomain = mongoDW.db.dm_answers.distinct('Dim_Question.Subdomain',{'Dim_Question.Domain':domains[0]})

    years = mongoDW.db.dm_answers.distinct("Dim_Calendar.Year")

    filter_options=[{'label':'Semestre','value':1},{'label':'Trimestre','value':2},
                    {'label':'Mês','value':3}]

    app.layout=html.Div(
        style={"background": "#F7F7F7"},
        children=[
            dbc.Col(id="general_answers"),
            dbc.Card(
                id="select_card",
                children=[
                    dbc.CardHeader([html.H4("Selecionar Aluno",style={'color': '#73879C'})]),
                    dbc.CardBody([
                        html.Div(
                            dbc.Row([
                                dbc.Col([
                                    dcc.Dropdown(
                                        id='students-dropdown',
                                        options=[{'label': i, 'value': i} for i in user_list],
                                        value=user_list[0] if (user_list is not None and user_list != []) else None,
                                        placeholder='Aluno...',
                                        optionHeight=45,
                                    ),
                                ])
                            ])
                        )
                    ])
                ]
            ),
            dbc.Card(
                id="user_card",
                style={'marginTop':'20px'},
                children=[
                    dbc.CardHeader(id="title_name"),
                    dbc.CardBody([
                        html.Div(
                            dbc.Row([
                                dbc.Col([
                                    html.Div(
                                        id="foto",
                                        children=[
                                            html.Img(src="/static/images/avatars/user.png")
                                        ]
                                    )
                                ],md=2),
                                dbc.Col([
                                    html.Div(
                                        id="dadosPessoais",
                                    )
                                ],md=3),
                                dbc.Col([
                                    html.Div(
                                        id='pie-char-user',
                                        style={
                                            'width':'80%'
                                        }
                                    )
                                ],md=4)
                            ])
                        )
                    ])
                ]
            ),
            dbc.Card(
                style={'marginTop':'20px'},
                children=[
                    dbc.CardHeader([html.H4("Nivel de dificuldade das questões respondidas",style={'color': '#73879C'})]),
                    dbc.CardBody([
                        html.Div([
                        dbc.Row([
                            dbc.Col([
                                    dcc.DatePickerRange(
                                        id='picker-range-level',
                                        day_size=30,
                                        display_format= "YYYY-MM-DD"
                                    )
                                ]),
                        ]),
                            html.Div(
                                id='lines_graph_levels',
                            )
                        ])
                    ]),
                ]
            ),
            dbc.Card(
                style={'marginTop':'20px'},
                children=[
                dbc.CardHeader([html.H4("Desempenho por domínio de avaliação",style={'color': '#73879C'})]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dcc.DatePickerRange(
                                id='my-date-picker-range',
                                day_size=30,
                                display_format= "YYYY-MM-DD"
                            ),
                            html.Div(
                                id='performance_domain_line_chart'
                            ),
                            html.Div(
                                id='bar-domains-graph'
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
                ]),
            ]),
             dbc.Card(
                    style={"margin-top":"10px","height": "520px"},
                    children=[
                        dbc.CardHeader([html.H4("Desempenho por nível de avaliação",style={'color': '#73879C'})]),
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
        ]
    )

    @app.callback(
        Output('title_name','children'),
        [Input('students-dropdown', 'value')])
    def display_title(name):
        return html.H4(name,style={'color': '#73879C'})

    @app.callback(
        Output('general_answers','children'),
        [Input('students-dropdown', 'value')])
    def display_general_bar(name):
        general_answers=general_dm_users(name,mongoDW)

        output=dbc.Card(
                style={"background":"transparent", "border":"none"},
                children=[
                    dbc.CardBody([
                        dbc.Row([
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
                            ]),
                    ])])
                    ]
            )
        
        return output

    @app.callback(
    [Output('subdomain-dropdown', 'options'),
        Output('subdomain-dropdown', 'value')],
    [Input('domain-dropdown', 'value')])
    def update_subdomains(dom):
        subdoms=getSubdomains(dom,mongoDW)
        return subdoms, subdoms[0]['value']

    @app.callback(
        [Output('my-date-picker-range', 'start_date'),
        Output('my-date-picker-range', 'end_date'),
        Output('my-date-picker-range', 'min_date_allowed'),
        Output('my-date-picker-range', 'max_date_allowed'),
        Output('my-date-picker-range', 'initial_visible_month'),

        Output('picker-range-level', 'start_date'),
        Output('picker-range-level', 'end_date'),
        Output('picker-range-level', 'min_date_allowed'),
        Output('picker-range-level', 'max_date_allowed'),
        Output('picker-range-level', 'initial_visible_month')],
        [Input('students-dropdown', 'value')])
    def calculate_range_dates(name):
        date_limits = getOldRecord(name,mongoDW)
        if date_limits is not None:
            semester_ago = date_limits[0]['Dim_Calendar']['Date'] - relativedelta(months=4)
            start_date = date_limits[len(date_limits)-1]['Dim_Calendar']['Date']
            end=date_limits[0]['Dim_Calendar']['Date']

        return semester_ago.date(),end.date(),start_date.date(),end.date(),semester_ago.date(),semester_ago.date(),end.date(),start_date.date(),end.date(),semester_ago.date()
    
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
        Output('dadosPessoais','children'),
        [Input('students-dropdown', 'value')])
    def display_title(name):
        list_users = get_info_user(name,mongoDW)
        if list_users is not None and list_users != []:
            return [
                dbc.ListGroupItemHeading("Informação Pessoal", style={'color':'#73879C'}),
                dbc.ListGroupItemText(dcc.Markdown('''
                                                        **Código de Aluno: **'''+list_users[0]['UserId']+'''

                                                        **Nome: **'''+ list_users[0]['Name']+'''

                                                        **Género: **'''+ list_users[0]['Gender']+'''

                                                        **Curso: **'''+ list_users[0]['Degree']
                                                        ))
            ]

    @app.callback(
        Output('pie-char-user','children'),
        [Input('students-dropdown','value')])
    def get_top_stud(student):
        list_right_wrong = get_general_right_wrong(student,mongoDW)
        labels=['Corretas', 'Erradas']
        colors=['#6ea865','#375573']
        if list_right_wrong is not None:
            total = list_right_wrong[0]['right_answers_subdomain']+list_right_wrong[0]['wrong_answers_subdomain']
            perc_list=[]
            perc_list.append((list_right_wrong[0]['right_answers_subdomain']/total)*100)
            perc_list.append((list_right_wrong[0]['wrong_answers_subdomain']/total)*100)
            fig = go.Figure(data=[go.Pie(labels=labels, values=perc_list, hole=.3, marker_colors=colors)])
            return (dcc.Graph(figure=fig))

    @app.callback(
        Output('performance_domain_line_chart', 'children'),
        [Input('my-date-picker-range', 'end_date'),
        Input('domain-dropdown', 'value'),
        Input('subdomain-dropdown', 'value'),
        Input('students-dropdown','value')] ,
        [State('my-date-picker-range', 'start_date')])
    def update_graph_dates(end,dom,subdom,student,start_date):
        return create_domains_graph(dom,subdom,start_date,end,student)

    def create_domains_graph(dom, subdom, start_date,end_date,student):
        start_date = dt.strptime(start_date, '%Y-%m-%d')
        end_date = dt.strptime(end_date, '%Y-%m-%d')
        json = getCorrections(dom,subdom,start_date,end_date,student,mongoDW)
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
        [Output('bar_chart_level_1', 'children'),
        Output('bar_chart_level_2', 'children')],
        [Input('optionsFilter', 'value'),
        Input('year-dropdown', 'value')],
        [State('dropdown-options', 'value'),
        State('students-dropdown','value')])
    def create_bar_levels(optionNumber,year,sem_qua_mon,student):
        if sem_qua_mon==1:
            bar_data = answers_by_level(year,optionNumber,None,None,student,mongoDW)
        else:
            if sem_qua_mon==2:
                bar_data = answers_by_level(year,None,optionNumber,None,student,mongoDW)
            else:
                bar_data = answers_by_level(year,None,None,optionNumber,student,mongoDW)
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
        Output('bar-domains-graph','children'),
        [Input('students-dropdown','value'),
        Input('domain-dropdown', 'value'),
        Input('my-date-picker-range','end_date')], 
        [State('my-date-picker-range','start_date')])
    def create_bar_answer_domains(student,domain,end,start):
        start = dt.strptime(start, '%Y-%m-%d')
        end = dt.strptime(end, '%Y-%m-%d')
        bar_data = get_answers_domain_user(domain,student,start,end,mongoDW)

        my_layout = go.Layout({"title": "Numero de respostas por dominio",
                                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                'xaxis':{ 'showgrid': False,
                                        'showticklabels':False}
        })

        if not bar_data: 
            fig1={}     
        else:
            fig1 = go.Figure(data=[go.Bar(x=bar_data[0]['subdomains_list'], y=bar_data[0]['right_list'],marker={'color':'#6ea865'},name='Corretas'),
                    go.Bar(x=bar_data[0]['subdomains_list'], y=bar_data[0]['wrong_list'],marker={'color':'#375573'},name='Erradas')],layout=my_layout)
                        
        return dcc.Graph(figure=fig1)

    @app.callback(
    Output('lines_graph_levels','children'),
    [Input('students-dropdown','value'),
    Input('picker-range-level','end_date')], 
    [State('picker-range-level','start_date')])
    def create_line_graph(student,end_date,start_date):
        start_date = dt.strptime(start_date, '%Y-%m-%d')
        end_date = dt.strptime(end_date, '%Y-%m-%d')
        answers_number = get_answers_domain("Data Warehousing",start_date,end_date,mongoDW)
        levels_number=getLevelsByDates(start_date,end_date,student,mongoDW)
        fig = go.Figure()
        for a in levels_number:
            print(len(a['dates']),len(a['levels']))
            fig.add_trace(go.Scatter(x=a['dates'], y=a['levels'], name="Niveis",marker={'color':'#6ea865'}))
        fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })
        return dcc.Graph(figure=fig)

    @app.callback(
        Output('bar_chart_level_3', 'children'),
        [Input('optionsFilter', 'value'),
        Input('year-dropdown', 'value')],
        [State('dropdown-options', 'value'),
        State('students-dropdown','value')])
    def create_bar_level_3(optionNumber,year,sem_qua_mon,student):
        return

    return app.server