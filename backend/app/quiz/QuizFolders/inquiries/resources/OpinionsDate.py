# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 10:39:33 2018

@author: jimmybow
"""
from dash import Dash
from dash.dependencies import Input, State, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objects as go
from flask_pymongo import PyMongo
from bson.json_util import dumps, loads
from datetime import datetime as dt, time
from datetime import date, timedelta
import datetime
import requests
import dash_bootstrap_components as dbc
import re
import random
url_base = '/dash/app3/'


properties2 = ['clarity', 'content', 'difficulty',
              'interactivity', 'knowledge', 'time']

def str_to_date(d_str):
    d_time = d_str.split('-')
    ret = date(int(d_time[0]),int(d_time[1]),int(d_time[2][:2]))

    return ret

def getAllDataInquiry_json(mongo,inquiry):
    ad = mongo.db.opinions.find({'Inquiry_id': inquiry})
    return loads(dumps(ad))

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

inqueritosType = [{'label':'Sistema','value':'PTSYFS01'},{'label':'Sessão','value':'PTSEFS01'},{'label':'Questão','value':'INPTQU0001'}]

def generate_color_array(columns):
    colors={}
    for c in columns:
        color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        colors[c]=color
    return colors

def getColumnsTable(columns):
    columns_table=[]
    for doc in columns:
        if(doc['label']!= 'Todas'):
            json = {
                'name': doc['label'],
                'id': doc['label']
            }
            columns_table.append(json)
    return columns_table

def get_proerties_json(mongo):
        propers = mongo.db.opinions.distinct("InquiryAnswer.Properties")
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
        propers_json_table=[]
        for p in propers_Array:
            json={
                'label':p,
                'value':p
            }
            propers_json.append(json)
            json_table={
                'name':p,
                'id':p
            }
            propers_json_table.append(json_table)

        return (propers_json,propers_json_table)


def getData_Propers(json):
    propers =[]
    for doc in json:
        if(not(doc['label'] in propers)):
            propers.append(doc['label'])
    
    return propers

def json_to_DataFrame(propers_json,json,dataInicial,dataFinal):
    datas = []
    delta = dataFinal - dataInicial
    for i in range(delta.days + 1): 
        day = dataInicial + timedelta(days=i) 
        ob={
                'Date': day,
                'numberOfinquiry': 0,
            }    
        for proper in propers_json:
            ob[proper] = 0
        datas.append(ob)

    datasDF = pd.DataFrame(datas)

    for doc in json:
        my_date = str_to_date(doc["Dim_Calendar"]["Date"])
        datasDF.loc[datasDF['Date']==my_date, 'numberOfinquiry'] += 1
        for proper in doc["InquiryAnswer"]["Properties"]:
            datasDF.loc[datasDF['Date']==my_date,proper] += doc["InquiryAnswer"]["Properties"][proper]

    for proper in propers_json:
        datasDF[proper] = round(datasDF[proper]/datasDF['numberOfinquiry'],2)
            
    return datasDF




def Add_Dash(server):
    external_stylesheets = [dbc.themes.BOOTSTRAP,
                        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css']

    app = Dash(server=server, url_base_pathname=url_base,
               external_stylesheets=external_stylesheets)

    mongoDW = PyMongo()
    mongoDW.init_app(server, 'mongodb://localhost:27017/teste')

    properties = get_proerties_json(mongoDW)
    properties_dropdown = properties[0]
    properties_dropdown.pop(0)
    properties_table = properties[1]
    prop_inquiry = getPropertiesInquiry(mongoDW,'PTSEFS01')
    opinionsJson = getAllDataInquiry_json(mongoDW,'PTSEFS01')


    app.layout = html.Div(
        
        #style={"background": "HF7F7F7"},
        children=[
            dbc.Card(
                style={"height":"800px","overflow-y":"auto","overflow-x":"hidden"},
                children=[
                    dbc.CardHeader([
                        html.H5(
                            "Análise de Propriedades", 
                            style={'color': '#73879C'}
                        )
                    ]),
                    dbc.CardBody([
                        dcc.Tabs(
                            parent_style={
                                'flex-direction': 'column',
                                '-webkit-flex-direction': 'column',
                                '-ms-flex-direction': 'column',
                                'display': 'flex'
                            },
                            children=[
                                dcc.Tab(
                                    label="Tabela", 
                                    selected_style={
                                        'color': '#73879C',
                                        'font-family': 'Arial',
                                        'font-size': '13px',
                                        'font-weight': '400',
                                        'line-weight': '1.471',
                                        'fontWeight': 'bold'
                                    },
                                    style={
                                        'color': '#73879C',
                                        'font-family': 'Arial',
                                        'font-size': '13px',
                                        'font-weight': '400',
                                        'line-weight': '1.471',
                                        'fontWeight': 'bold'},
                                    children=[
                                        dbc.Row([
                                            dbc.Col([
                                                html.Div(
                                                    children=[
                                                        html.P(
                                                            'Número de entradas:',
                                                            style={
                                                                'color': '#73879C',
                                                                'font-weight': '400',
                                                                'fontWeight': 'bold'
                                                            }
                                                        ),
                                                        dcc.Dropdown(
                                                            id='entries-table',
                                                            options=[{'label': i, 'value': i} for i in ['10','25','50','100','todas']],
                                                            value='10',
                                                            clearable=False
                                                        )
                                                    ],
                                                    style={
                                                        'marginBottom': '1em', 
                                                        'marginLeft': '1em',
                                                        'marginTop': '1em',
                                                        'font-family': 'Arial',
                                                        'font-size': '13px',
                                                        'font-weight': '400',
                                                        'line-weight': '1.471'
                                                    }
                                                )
                                            ],md=1.5),
                                            dbc.Col([
                                                html.Div(
                                                    children=[
                                                        html.P(
                                                            'Tipo de inquérito:',
                                                            style={
                                                                'color': '#73879C',
                                                                'font-weight': '400',
                                                                'fontWeight': 'bold'
                                                            }
                                                        ),
                                                        dcc.Dropdown(
                                                            id='inquiry-type',
                                                            options= inqueritosType,
                                                            value='PTSEFS01',
                                                            clearable=False
                                                        )
                                                    ],
                                                    style={
                                                        'marginBottom': '1em', 
                                                        'marginLeft': '1em',
                                                        'marginTop': '1em',
                                                        'font-family': 'Arial',
                                                        'font-size': '13px',
                                                        'font-weight': '400',
                                                        'line-weight': '1.471',
                                                    }
                                                )
                                            ],md=1.5),
                                            dbc.Col([
                                                html.Div(
                                                    children=[
                                                        html.P(
                                                            'Selecionar propriedade:',
                                                            style={
                                                                'color': '#73879C',
                                                                'font-weight': '400',
                                                                'fontWeight': 'bold'
                                                            }
                                                        ),
                                                        dcc.Dropdown(
                                                            id='select-table',
                                                            options=prop_inquiry,
                                                            value='Todas',
                                                            multi=True,
                                                        )
                                                    ],
                                                    style={
                                                        'marginBottom': '1em', 
                                                        'marginLeft': '1em',
                                                        'marginTop': '1em',
                                                        'font-family': 'Arial',
                                                        'font-size': '13px',
                                                        'font-weight': '400',
                                                        'line-weight': '1.471',
                                                    }
                                                )
                                            ],md=1.5),
                                        ]),
                                        dbc.Row([
                                            dbc.Col([
                                                dash_table.DataTable(
                                                    id='table-paging-with-graph',
                                                    css=[{'selector': '.row', 'rule': 'margin:0'},{'selector': '.previous-page, .next-page, .first-page, .last-page', 'rule': 'color: #73879C'},{'selector':'.current-page','rule': 'color: #73879C !important'}],
                                                    style_table={"overflowX":"auto"},
                                                    columns=(
                                                        [{"name": 'Date', "id": 'Date'}] +
                                                        [{"name": 'Number of inquiries', "id": 'numberOfinquiry'}] +
                                                        properties_table
                                                    ),
                                                    style_as_list_view=True,
                                                    style_data_conditional=[
                                                        {
                                                            'if': {'row_index': 'pair'},
                                                            'backgroundColor': '#f9f9f9',
                                                            'box-sizing': 'border-box',
                                                        }
                                                    ],
                                                    style_cell={
                                                        'textAlign': 'center', 
                                                        'padding': '5px',
                                                        'color': '#73879C',
                                                        'font-size': '13px',
                                                        'font-weight': '400',
                                                        'font-family': 'Arial',
                                                        'line-weight': '1.471',
                                                        'line-height': '2.0'
                                                    },
                                                    style_header={
                                                        'backgroundColor': 'white',
                                                        'color': '#73879C',
                                                        'font-family': 'Arial',
                                                        'font-size': '13px',
                                                        'font-weight': '400',
                                                        'line-weight': '1.471',
                                                        'fontWeight': 'bold'
                                                    },

                                                    filter_action="custom",
                                                    filter_query='',
                                                    page_action="custom",
                                                    page_current= 0,
                                                    #page_size= 3,
                                                    sort_action="custom",
                                                    sort_mode="single",
                                                    sort_by=[],
                                                ),
                                            ])
                                        ])
                                    ]
                                ),
                                dcc.Tab(
                                    label="Gráfico", 
                                    selected_style={
                                        'color': '#73879C',
                                        'font-family': 'Arial',
                                        'font-size': '13px',
                                        'font-weight': '400',
                                        'line-weight': '1.471',
                                        'fontWeight': 'bold'
                                    },
                                    style={
                                        'color': '#73879C',
                                        'font-family': 'Arial',
                                        'font-size': '13px',
                                        'font-weight': '400',
                                        'line-weight': '1.471',
                                        'fontWeight': 'bold'
                                    },
                                    children=[
                                        dbc.Row([
                                            dbc.Col([
                                                html.Div(
                                                    children=[
                                                        html.P(
                                                            'Tipo:',
                                                            style={
                                                                'color': '#73879C',
                                                                'font-weight': '400',
                                                                'fontWeight': 'bold'
                                                            }
                                                        ),
                                                        dcc.Dropdown(
                                                            id='type-dropdown',
                                                            options=[
                                                                {'label': 'barras', 'value': 'bar'},
                                                                {'label': 'linhas', 'value': 'lines'}
                                                            ],
                                                            value='bar',
                                                        )
                                                    ],
                                                    style={
                                                        'marginTop': '1em',
                                                        'font-family': 'Arial',
                                                        'font-size': '13px',
                                                        'font-weight': '400',
                                                        'line-weight': '1.471'
                                                    }
                                                )
                                            ],md=2),
                                        ]),
                                         dbc.Row([
                                            dbc.Col([
                                                html.Div(
                                                    id='table-graph',
                                                    children=[],
                                                )
                                            ])
                                        ])
                                    ]
                                )
                            ],
                            colors={
                                "border":"white",
                                "primary":"#1ABB9C",
                                "background":"rgba(0,0,0,.03)"
                            },
                            style={
                                'width': '21%',
                                'float': 'left'
                            },
                        )
                    ])
                ]
            )
        ]
    )
    
    @app.callback(
        [Output('select-table','options'),
         Output('select-table','value')],
        [Input('inquiry-type','value')])
    def update_dropdown(inquiry):
        return getPropertiesInquiry(mongoDW,inquiry), 'Todas'

    operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


    def split_filter_part(filter_part):
        for operator_type in operators:
            for operator in operator_type:
                if operator in filter_part:
                    name_part, value_part = filter_part.split(operator, 1)
                    name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                    value_part = value_part.strip()
                    value_part = value_part.strip('\"')
                    v0 = value_part[0]
                    if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                        value = value_part[1: -1].replace('\\' + v0, v0)
                    else:
                        try:
                            value = float(value_part)
                        except ValueError:
                            value = value_part

                    # word operators need spaces after them in the filter string,
                    # but we don't want these later
                    return name, operator_type[0].strip(), value

        return [None] * 3

    @app.callback(
        [Output('table-paging-with-graph', 'data'),
         Output('table-paging-with-graph', 'columns')],
        [Input('table-paging-with-graph', 'page_current'),
         Input('entries-table', 'value'),
         Input('inquiry-type','value'),
         Input('select-table', 'value'),
         Input('select-table','options'),
         Input('table-paging-with-graph', 'sort_by'),
         Input('table-paging-with-graph','filter_query')],
         [State('table-paging-with-graph', 'columns')])
    def update_table(page_current, page_size_value,inquiry, select_properties,columnsTable,sort_by, filter,existing_columns):
        propers_list = getData_Propers(properties_dropdown)
        opinionsJson = getAllDataInquiry_json(mongoDW,inquiry)
        starting = date(2020,6,12)
        ending = date.today()
        df = json_to_DataFrame(propers_list,opinionsJson,starting,ending)
        dff = df[df['numberOfinquiry']>0]
        
        columns_table = getColumnsTable(columnsTable)
        existing_columns = [{"name": 'Date', "id": 'Date'}] + [{"name": 'Number of inquiries', "id": 'numberOfinquiry'}] + columns_table

        if not 'Todas' in select_properties:
            for prop  in propers_list:
                if not prop in select_properties:
                    for c in existing_columns:
                        if c['name'] == prop:
                            existing_columns.remove(c)
                    del(dff[prop])

        filtering_expressions = filter.split(' && ')
        flag = 0
        for filter_part in filtering_expressions:
            if '{' in filter_part or flag == 0:
                col_name, operator, filter_value = split_filter_part(filter_part)
                flag = 1
            else:
                col, operator, filter_value = split_filter_part(filter_part)
            
            if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
                # these operators match pandas series operator method names
                if col_name == 'Date':
                    filter_value = str_to_date(filter_value)
                dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
            elif operator == 'contains':
                dff = dff.loc[dff[col_name].str.contains(filter_value)]
            elif operator == 'datestartswith':
                # this is a simplification of the front-end filtering logic,
                # only works with complete fields in standard format
                dff = dff.loc[dff[col_name].str.startswith(filter_value)]
        if(len(sort_by)):
            dff = dff.sort_values(
                sort_by[0]['column_id'],
                ascending=sort_by[0]['direction'] == 'asc',
                inplace=False)
        if(page_size_value=='todas'):
            return dff.to_dict('records'), existing_columns
        else:
            page_size = int(page_size_value)
            return dff.iloc[page_current*page_size:(page_current+1)*page_size].to_dict('records'), existing_columns

    @app.callback(
        Output('table-graph', 'children'),
        [Input('table-paging-with-graph','data'),
        Input('table-paging-with-graph','columns'),
        Input('type-dropdown','value')])
    def update_graph(data,table_columns,type_graph,):

        fig = go.Figure()
        dff = pd.DataFrame(data)
        columns = list(dff.columns)

        if not dff.empty:
            my_color = generate_color_array(columns)
            if(type_graph=='bar'):
                for c in table_columns:
                    properName = c['id']
                    if properName!='Date' and properName!='numberOfinquiry':
                        fig.add_trace(go.Bar(x=dff['Date'],y=dff[properName],marker={'color':my_color[properName]},name=properName))
                
            else:
                for c in table_columns:
                    properName = c['id']
                    if properName!='Date' and properName!='numberOfinquiry':
                        fig.add_trace(go.Scatter(x=dff['Date'],y=dff[properName],name=properName,connectgaps=True,marker={'color':my_color[properName]}))

        fig.update_layout({
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'title': 'Propriedades por data',
            'xaxis':{'title':'date','showline':True, 'linecolor':'#73879C'},
            'yaxis':{'title':'average','showline':True, 'linecolor':'#73879C'},
            'autosize':True
        })
        return dcc.Graph(figure=fig)


    return app.server
