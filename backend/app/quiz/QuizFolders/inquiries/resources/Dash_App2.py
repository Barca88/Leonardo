# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 10:39:33 2018
@author: jimmybow
"""
from dash import Dash
import dash
from dash.dependencies import Input, State, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
#import dash_table
from datetime import date, timedelta
import pandas as pd
import plotly.graph_objects as go
from flask_pymongo         import PyMongo
from bson.json_util import dumps, loads
from datetime import datetime as dt
import random

url_base = '/dash/app2/'

def get_last_month(today):
    if(today.month == 1): # Mês de janeiro. O ano tem de ser o anterior e o mês é 12
        year = today.year - 1
        month = 12
        day = today.day

        return date(year,month,day)
    else:
        year = today.year
        month = today.month - 1
    
    if(today.month == 3 and today.day > 28): # Mês de março a partir do dia 29. Devido ao número de dias de fevereiro ser 28 ou 29, vamos assumir que 30 dias para trás é o dia 28 de fevereiro.
        day = 28
        return date(year,month,day)
    
    try: # Dias sem problemas
        return date(year,month,today.day)
    except: # Quando estamos no dia 31 e o mês anterior só tem 30 dias
        return date(year,month,today.day-1)


def getAllData_json(mongoDW):
    ad = mongoDW.db.opinions.find()
    return loads(dumps(ad))

def getDomains_json(mongoDW):
    domains = mongoDW.db.opinions.distinct("Dim_Question.Domain")
    domains_json=[]
    json = {
        'label': 'Todos',
        'value': 'All'
    }
    domains_json.append(json)
    for d in domains:
        json={
            'label':d,
            'value':d
        }
        domains_json.append(json)
    return domains_json
    

def getSubdomains_json(domain,mongoDW):
        subdomains_json=[]
        
        if (domain != 'All'):
            subdomains = mongoDW.db.opinions.distinct("Dim_Question.Subdomain",
                                            {"Dim_Question.Domain":domain} )
            subdomains_json=[]
            json = {
                'label':'Todos',
                'value':'All'
            }
            subdomains_json.append(json)
            
            for d in subdomains:
                json={
                    'label':d,
                    'value':d
                }
                subdomains_json.append(json)
        else:
            json={
                'label':'Todos',
                'value':'All'
            }
            subdomains_json.append(json)
        return subdomains_json

def getUsers_json(mongoDW):
    users = mongoDW.db.opinions.distinct("Dim_User.User_id")
    users_json=[]
    json = {
        'label': 'Todos',
        'value': 'All'
    }
    users_json.append(json)
    for u in users:
        json={
            'label':u,
            'value':u
        }
        users_json.append(json)
    
    return users_json

def getGenders_json():
    genders_json=[]
    json={
        'label':'Todos',
        'value':'All'
    }
    genders_json.append(json)

    json_f={
        'label':'Feminino',
        'value':'F'
    }
    genders_json.append(json_f)

    json_m = {
        'label':'Masculino',
        'value':'M'
    }
    genders_json.append(json_m)

    return genders_json

def getPropers_json(mongoDW):
    propers = mongoDW.db.opinions.distinct("InquiryAnswer.Properties")

    propers_Array= []
    for proper in propers:
        for p in proper:
            aux = p.split()
            if(not(aux[0] in propers_Array)):
                propers_Array.append(aux[0])  

    propers_json=[]
    json = {
        'label': 'Todas',
        'value': 'All'
    }
    propers_json.append(json)
    for p in propers_Array:
        json={
            'label':p,
            'value':p
        }
        propers_json.append(json)

    return propers_json

def getInquiryType_json():
    inq_type_json=[]
    json_sys = {
        'label':'Sistema',
        'value':'PTSYFS01'
    }
    inq_type_json.append(json_sys)
    
    json_q={
        'label':'Questão',
        'value':'INPTQU0001'
    }
    inq_type_json.append(json_q)

    json_sess = {
        'label':'Sessão',
        'value':'PTSEFS01'
    }
    inq_type_json.append(json_sess)

    return inq_type_json

def getPropertiesInquiry(mongo, type):
    data = mongo.db.templates.find({'inquiry_id': type},{'properties':1})
    propers = loads(dumps(data))
    properties = []
    json = {
            'label': 'Todas',
            'value': 'Todas'
        }
    properties.append(json)
    for d in propers[0]['properties']:
        json={
                'label': d['property'],
                'value':d['property']
            }
        properties.append(json)
    return properties

##-------------------------------------------------------##
def getQuestionData(json):
    ret = []
    for doc in json:
        try:
            if( (doc['Inquiry_id']!="PTSEFS01") and (doc['Inquiry_id']!="PTSYFS01")):
                ret.append(doc)
        except:
            try:
                if(doc['Dim_Question']):
                    ret.append(doc)
            except:
                print('Não é questão')
    return ret


def getInquiryType_Data(inquiry_type,dados):
    ret = []
    for d in dados:
        try:
            if(d['Inquiry_id'] == inquiry_type):
                ret.append(d)
        except:
            print('Este não tem id, ignora-se')
    return ret 


def getData_Propers(json):
    propers =[]
    for doc in json:
        for prop in doc["InquiryAnswer"]["Properties"]:
            if(not(prop in propers)):
                propers.append(prop)
    
    return propers

def getDomain_Data(dados, domain):
    ret = []
    try:
        for d in dados:
            if(domain in d["Dim_Question"]["Domain"]):
                ret.append(d)
        return ret
    except:
        return dados

def getSubdomain_Data(dados, subdomain):
    ret = []
    try:
        for d in dados:
            if(subdomain in d["Dim_Question"]["Subdomain"]):
                ret.append(d)
        return ret
    except:
        return dados

def getUser_Data(dados, user):
    ret = []
    for d in dados:
        if(d["Dim_User"]["User_id"] == user):
            ret.append(d)
    return ret

def getGender_Data(dados, gender):
    ret = []
    for d in dados:
        if(d["Dim_User"]["Gender"] == gender):
            ret.append(d)
    return ret

def getProperty_Data(dados, proper):
    ret = []
    for d in dados:
        for p in d["InquiryAnswer"]["Properties"]:
            if(p.split()[0] == proper):   
                ret.append(d)
    return ret

def getAfterDate_Data(dados, dataInicial):
    ret = []
    for d in dados:
        d_time = d["Dim_Calendar"]["Date"].split('-')
        my_date = date(int(d_time[0]),int(d_time[1]),int(d_time[2][:2]))
        if(my_date >= dataInicial):
            ret.append(d)
    return ret

def getBeforeDate_Data(dados, dataFinal):
    ret = []
    for d in dados:
        d_time = d["Dim_Calendar"]["Date"].split('-')
        my_date = date(int(d_time[0]),int(d_time[1]),int(d_time[2][:2]))
        if(my_date <= dataFinal):
            ret.append(d)
    return ret

##-------------------------------------------------------##
##-------------------------------------------------------##
def getData(mongoDW, inquiry_type, domain=None, subdomain=None, user = None, propriedade=None, gender=None, dataInicial = None, dataFinal = None):
    json = getAllData_json(mongoDW)

    if(inquiry_type == 'INPTQU0001'):
        json = getQuestionData(json)
        
        if (domain != 'All'):
           json = getDomain_Data(json, domain)

        if (subdomain != 'All'):
            json = getSubdomain_Data(json, subdomain)
    else:
        json= getInquiryType_Data(inquiry_type,json)

    if (user != 'All'):
        json = getUser_Data(json,user)

    if (propriedade != 'All'):
        json = getProperty_Data(json,propriedade)

    if (gender != 'All'):
        json = getGender_Data(json,gender)
 
    if(dataInicial is not None):
        json = getAfterDate_Data(json, dataInicial)

    if(dataFinal is not None):
        json = getBeforeDate_Data(json, dataFinal)

    if(len(json) == 0):
        return None
    return json

##-------------------------------------------------------##
def get_interval_dates(di,df):
    days= []
    di = str_to_date(di)
    df = str_to_date(df)
    delta = df - di      
    for i in range(delta.days + 1):
        day = di + timedelta(days=i)
        days.append(day)
    return days

def increment_Freq(array,date,p,value):
    for a in array:
        if(p == a['Prop']):
            for dt in a['Data']:
                if (dt['Date'] == date):
                    dt['Frequência'] +=1
                    dt['Sum'] += value
                    dt['Média'] = dt['Sum']/dt['Frequência']
    return array

def json_to_DataFrame(propers_json,json,dataInicial,dataFinal):
    data_freqs_media=[];datas = [];freqs = [];

    for proper in propers_json:
        obj={
            'Prop':proper,
            'Data':[],
        }
        delta = dataFinal - dataInicial      
        for i in range(delta.days + 1):
            day = dataInicial + timedelta(days=i)
            ob={
                'Date': day,
                'Frequência': 0,
                'Sum':0,
                'Média':0
            }
            obj['Data'].append(ob)
        data_freqs_media.append(obj)

    for doc in json:
        my_date = str_to_date(doc["Dim_Calendar"]["Date"])
        for proper in doc["InquiryAnswer"]["Properties"]:
            data_freqs_media = increment_Freq(data_freqs_media,my_date,proper,doc["InquiryAnswer"]["Properties"][proper])

    for obj in data_freqs_media:
        datas.append(obj['Prop'])
        freqs.append(obj['Data'])
    
    return datas,freqs



def str_to_date(d_str):
    d_time = d_str.split('-')
    ret = date(int(d_time[0]),int(d_time[1]),int(d_time[2][:2]))
    return ret
##-------------------------------------------------------##

def Add_Dash(server):
    external_stylesheets = [dbc.themes.BOOTSTRAP,'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css']
    app = Dash(server=server, url_base_pathname=url_base,external_stylesheets=external_stylesheets)
    mongoDW       = PyMongo()
    mongoDW.init_app(server,'mongodb://localhost:27017/teste')

    today = date.today()
    last_month = get_last_month(today)
    domains_json = getDomains_json(mongoDW)
    genders_json = getGenders_json()
    users_json = getUsers_json(mongoDW)
    propers_json = getPropers_json(mongoDW)
    inquiry_type_json = getInquiryType_json()
    json = getAllData_json(mongoDW)
    

    my_style= {
        'marginBottom': '1em', 
        'marginLeft': '0em',
        'marginTop': '1em',
        'font-family': 'Arial',
        'font-size': '13px',
        'font-weight': '400',
        'line-weight': '1.471'
    }

    app.layout = html.Div(                
                    style={'background': '#F7F7F7'},
                    children=[
                    dbc.Row([
                        dbc.Col([
                            dbc.Card(
                                style={"background":"transparent", "border":"none",'border-right': 'dashed #bbb'},
                                children=[
                                    dbc.CardBody([
                                        html.I(className="fa fa-database", children=[" Domínios"], style={'color': '#73879C'}),
                                        html.H2(len(domains_json)-1, style={'color': '#1ABB9C'}),
                                    ])]
                            )
                        ]),
                        dbc.Col([
                            dbc.Card(
                                style={"background":"transparent", "border":"none",'border-right': 'dashed #bbb'},
                                children=[
                                    dbc.CardBody([
                                        html.I(className="fa fa-database", children=[" Utilizadores"], style={'color': '#73879C'}),
                                        html.H2(len(users_json)-1,style={'color': '#1ABB9C'}),
                                    ])]
                            )
                        ]),
                        dbc.Col([
                            dbc.Card(
                                style={"background":"transparent", "border":"none"},
                                children=[
                                    dbc.CardBody([
                                        html.I(className="fa fa-database", children=[" Número de inquéritos"], style={'color': '#73879C'}),
                                        html.H2(len(json)-1,style={'color': '#1ABB9C'}),
                                    ])]
                            )
                        ]),
                    ]),
                
                    dbc.Card(
                        style={'margin-top':'20px'},
                        children=[
                            dbc.CardHeader([html.H5("Análise dos Valores das Propriedades",style={'color': '#73879C'})]),
                            dbc.CardBody([
                                html.Div([
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Row([
                                                dbc.Col([
                                                    html.Div(
                                                        style=my_style,
                                                        id='data-section',
                                                        children=[
                                                            html.P('Período de Análise', style={'color': '#73879C','font-family': 'Arial','font-size':'13px'}),
                                                            dcc.DatePickerRange(
                                                                style={'margin-top':'-10px','width':'100%','height':'30%','font-family':'Arial','font-size':'13px'},
                                                                id='my-date-picker-range',
                                                                day_size=30,
                                                                initial_visible_month=today,
                                                                min_date_allowed=dt(2020, 1, 1),
                                                                max_date_allowed=dt(2030,12,31),
                                                                display_format="YYYY-MM-DD",
                                                                start_date=last_month,
                                                                end_date=today,
                                                            )
                                                        ],  
                                                    )
                                                ]),
                                                dbc.Col([
                                                    html.Div(
                                                        children=[
                                                            html.P('Tipo de inquérito', style={'color': '#73879C','font-family': 'Arial','font-size':'13px','line-weight': '1.471'}),
                                                            dcc.Dropdown(
                                                                id='inquiry_type_dropdown',
                                                                options=inquiry_type_json,
                                                                value='PTSYFS01',
                                                                style={'margin-top':'-5px','position':'absolute','width':'70%'}
                                                            ),
                                                        ],
                                                        style=my_style
                                                    )  
                                                ])
                                            ]),
                                            dbc.Row(
                                                html.Div(
                                                    style={"margin-top":"0px",'float':'top','width':'100%','font-family': 'Arial','font-size': '13px','font-weight': '400'},
                                                    id='lines_graph',
                                                    children=[],
                                                )
                                            )
                                        ], width=10),
                                        dbc.Col([
                                            html.Div(
                                                id="drops",
                                                style=my_style,
                                                children=[
                                                    html.Span('Domínio', style={'color': '#73879C','font-family': '"Helvetica Neue", Roboto, Arial, "Droid Sans", sans-serif','font-size':'13px'}),
                                                    dcc.Dropdown(
                                                        id='domain-dropdown',
                                                        options=domains_json,
                                                        value='All',
                                                        style={'padding-top':'1rm'}
                                                    ),
                                                    html.Hr(style={'color': '#73879C'}),

                                                    html.Span('Subdomínio', style={'color': '#73879C','font-family': '"Helvetica Neue", Roboto, Arial, "Droid Sans", sans-serif','font-size':'13px'}),
                                                    dcc.Dropdown(
                                                        id='subdomain-dropdown',
                                                        options={}
                                                    ),
                                                    html.Hr(style={'color':'#73879C'}),

                                                    html.Span('Utilizadores', style={'color': '#73879C','font-family': '"Helvetica Neue", Roboto, Arial, "Droid Sans", sans-serif','font-size':'13px'}),
                                                    dcc.Dropdown(
                                                        id='utilizadores-dropdown',
                                                        options=users_json,
                                                        value='All'
                                                    ),
                                                    html.Hr(style={'color':'#73879C'}),

                                                    html.Span('Propriedades', style={'color': '#73879C','font-family': '"Helvetica Neue", Roboto, Arial, "Droid Sans", sans-serif','font-size':'13px'}),
                                                    dcc.Dropdown(
                                                        id='propriedades-dropdown',
                                                        options=propers_json,
                                                        value='All'
                                                    ),
                                                    html.Hr(style={'color':'#73879C'}),

                                                    html.Span('Género', style={'color': '#73879C','font-family': '"Helvetica Neue", Roboto, Arial, "Droid Sans", sans-serif','font-size':'13px'}),
                                                    dcc.Dropdown(
                                                        id='genero-dropdown',
                                                        options=genders_json,
                                                        value='All'
                                                    ),
                                                ])
                                        ], width=2)
                                    ]),
                                ]),
                            ])
                        ]
                    ),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card(
                                style={'margin-top':'20px'},
                                children=[
                                    dbc.CardHeader([html.H5("Valorização das Propriedades",style={'color': '#73879C'})]),
                                    dbc.CardBody([
                                        html.Div(
                                            id="propers_bars",
                                            style=my_style,
                                            children=[]
                                        )
                                    ])
                                ]
                            ),
                        ],width=7),
                        dbc.Col([
                            dbc.Card(
                                style={'margin-top':'20px'},
                                children=[
                                    dbc.CardHeader([html.H5("Indíce de Opinião",style={'color': '#73879C'})]),
                                    dbc.CardBody([
                                        html.Div(
                                            id="propers_geral",
                                            style=my_style,
                                            children=[]
                                        )
                                    ])
                                ]
                            ),
                        ],width=5)
                    ]),   
                ])

    
    @app.callback(
    [dash.dependencies.Output('domain-dropdown','options'),
    dash.dependencies.Output('domain-dropdown','value')],
    [dash.dependencies.Input('inquiry_type_dropdown','value')])
    def update_drops_dropdown(inquiry_t):
        if(inquiry_t != 'INPTQU0001'):
            json =[]
            obj={
                'label': 'Não aplicável',
                'value': 'None'
            }
            json.append(obj)
            return json,json[0]
        else:
            return domains_json,domains_json[0]
    
    @app.callback(
    [dash.dependencies.Output('subdomain-dropdown', 'options'),
    dash.dependencies.Output('subdomain-dropdown', 'value')],
    [dash.dependencies.Input('domain-dropdown', 'value')])   
    def update_dropdown_subdom(dom):
        try:
            if(dom['value'] == 'None'):
                json =[]
                obj={
                    'label': 'Não aplicável',
                    'value': 'None'
                }
                json.append(obj)
                return json,json[0]
            else:
                subdoms=getSubdomains_json(dom['value'],mongoDW)
                return subdoms,subdoms[0]
        except:
            subdoms=getSubdomains_json(dom,mongoDW) 
            return subdoms,subdoms[0]['value']
    
    @app.callback(
    [dash.dependencies.Output('lines_graph', 'children'),
    dash.dependencies.Output('propers_bars','children'),
    dash.dependencies.Output('propers_geral','children')],
    [dash.dependencies.Input('inquiry_type_dropdown','value'),
    dash.dependencies.Input('domain-dropdown', 'value'),
    dash.dependencies.Input('subdomain-dropdown', 'value'),
    dash.dependencies.Input('utilizadores-dropdown', 'value'),
    dash.dependencies.Input('propriedades-dropdown', 'value'),
    dash.dependencies.Input('genero-dropdown', 'value'),
    dash.dependencies.Input('my-date-picker-range', 'start_date'),
    dash.dependencies.Input('my-date-picker-range', 'end_date')]) 
    def update_graphs(inquiry_type,dom,subdom,user,props,gender,data_initial,data_final):
        di = str_to_date(data_initial)
        df = str_to_date(data_final)
        json = getData(mongoDW,inquiry_type,dom,subdom,user,props,gender,di,df)

        
        config ={'displayModeBar': False}
        fig_layout = {'layout': {'paper_bgcolor': "rgba(0,0,0,0)"},
                      'font':{'family':'Arial', 'size':12}}

        fig2_layout = go.Layout({
                                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                'xaxis':{ 'showgrid': False, 'title_text': 'Media'},
                                'yaxis':{ 'showgrid': False, 'title_text': 'Propriedades'},
                                'font':{'family':'Arial', 'size':12}
                        })
        
        fig3_layout = go.Layout({
                                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                'xaxis':{ 'showgrid': False},
                                'font':{'family':'Arial', 'size':12}
                        })

        if json is None:
            dates = get_interval_dates(data_initial,data_final)
            
            
            fig = go.Figure(fig_layout)
            fig.add_trace(go.Scatter(x=dates, y = [0,0,0,0,0,0]))
            fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)'
            })
            fig.update_xaxes(showgrid=True, gridwidth=0.1, gridcolor='LightGrey',title_text='Dia')
            fig.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='LightGrey',title_text='Classificação')

            
            fig2 = go.Figure(data=[go.Bar(x=['','','','',''],y=[0,0,0,0,0], marker={'color': '#1ABB9C'},orientation='h',width=0.5)]
                        ,layout = fig2_layout)
            
            fig3 = go.Figure(data=[go.Pie(labels=['none'],values=['100'],hole=0)],layout=fig3_layout)
            fig3.update_traces(textfont_size=10, textinfo='none',marker=dict(colors=['#f7f7f7']),hoverinfo='skip')
            fig3.update_layout(annotations=[dict(text=0,x=0.5, y=0.5, font_size=30, showarrow=False)],showlegend=False)

            return dcc.Graph(figure=fig,config=config),dcc.Graph(figure=fig2,config=config),dcc.Graph(figure=fig3,config=config)


        new_propers = getData_Propers(json)
        print('\n\n\n')
        print(new_propers)
        print('\n\n\n')


        fig = go.Figure(fig_layout)

        propers,my_data = json_to_DataFrame(new_propers,json,di,df)
        for i in range(len(propers)):
            d_t = my_data[i]
            datas = []
            medias = []
            for d in d_t:
                datas.append(d['Date'])
                medias.append(d['Média'])
            fig.add_trace(go.Scatter(x=datas, y = medias, name=propers[i]))
        fig.update_traces(mode='markers+lines')
        fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)'
        })
        fig.update_xaxes(showgrid=True, gridwidth=0.1, gridcolor='LightGrey',title_text='Dia')
        fig.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='LightGrey',title_text='Classificação')

        
        medias = []
        total_sum = 0
        total_freq = 0
        for data in my_data:
            f = 0; tot = 0
             
            for dt in data:
                f += dt['Frequência']; total_freq += dt['Frequência']
                tot += dt['Sum']; total_sum += dt['Sum']
            med = float("%.2f" % (tot/f))
            medias.append(med)
        
        fig2 = go.Figure(data=[go.Bar(x=medias, y=propers, marker={'color': '#1ABB9C'},orientation='h',width=0.5)]
                        ,layout = fig2_layout)
        
        media_geral = float("%.2f" % (total_sum/total_freq))
        
        fig3 = go.Figure(data=[go.Pie(labels=["Geral",'none'],sort= False,values=[media_geral,5-media_geral,],hole=0)],layout=fig3_layout)
        fig3.update_traces(textfont_size=10, textinfo='none',marker=dict(colors=['#1ABB9C','#f7f7f7']),hoverinfo='skip')
        fig3.update_layout(annotations=[dict(text=media_geral,x=0.5, y=0.5, font_size=30, showarrow=False)],showlegend=False)

        return dcc.Graph(figure=fig,config=config),dcc.Graph(figure=fig2,config=config),dcc.Graph(figure=fig3,config=config)

    return app.server
