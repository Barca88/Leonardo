import math
import json
from bson import json_util, ObjectId
import dash_core_components as dcc
from flask_cors import CORS
from dash import Dash
from flask_pymongo import PyMongo, MongoClient
from pandas import json_normalize
import pandas as pd
import flask
import dash
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from datetime import datetime as dttime

url_base = '/dash/app/'

mongo = PyMongo()
df1 = None

def Add_Dash(server):
    global df1
    
    mongo.init_app(server,'mongodb://localhost:27017/teste')

    # MongoDB Connections
    col = mongo.db.opinions

    cursor = col.find({})

    # load data into dataframe
    sanitized = json.loads(json_util.dumps(cursor))
    normalized = json_normalize(sanitized)
    df1 = pd.DataFrame(normalized)

    app = dash.Dash(server=server, url_base_pathname=url_base)

    modules = [
        {
            'label': 'All',
            'value': 'All'
        },
        {
            'label': 'SY',
            'value': 'SY'
        },
        {
            'label': 'SE',
            'value': 'SE'
        },
        {
            'label': 'QF',
            'value': 'QF'
        }    
    ]


    # main app layout
    app.layout = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.H4('Inquérito'),
                            dcc.Dropdown(
                                id='module',
                                options=modules,
                                value='All'
                            ),
                            html.H4('Domínio'),
                            dcc.Dropdown(
                                id='description',
                                value='All'
                            ),
                            html.H4('Subdomínio'),
                            dcc.Dropdown(
                                id='subdomain',
                                value='All'
                            ),
                            html.H4('Questão'),
                            dcc.Dropdown(
                                id='questions',
                                value='All'
                            ),
                            html.H4('Utilizador'),
                            dcc.Dropdown(
                                id='users',
                                value='All'
                            ),
                        ],
                        style={
                            'padding': '6px 8px 6px 16px',
                            'text-decoration': 'none',
                            'font-size': '15px',
                            'color': '#aaa',
                            'display': 'bock',
                            'justify-content': 'center',
                        }
                    ),
                ],
                style={
                    'width': '300px',
                    'height' : '100%',
                    'position': 'fixed',
                    'z-index': '1',
                    'top': '0',
                    'bottom': '0',
                    'right': '0',
                    'background-color': '#2a3f54',
                    'overflow-x': 'hidden',
                    'overflow-y ': 'scroll',
                    'padding-top': '20px'
                }
            ),
            html.Div(
                [
                    html.H1('Análise de Opiniões'),
                    html.Br(),
                    html.P(id = "inquiry_nr_avg"),
                    html.Br(),
                    html.Div(
                        [
                            html.Br(),
                            dcc.Graph(
                                id='linear-graph',

                            ),
                        ],
                        style = {
                            'height' : '600px'
                        }
                    ),
                    html.Br(),
                    html.Div(
                        id='hidden-data',
                        style={
                            'display': 'none'
                        }
                    )
                ],
                style={
                    'margin-right': '300px',
                    'padding': '0px 10px',
                    'height' : '600px',
                    'color' : '#2a3f54',
                }
            ),
        ],
        style={
            'text-align': 'center',
            'justify-content': 'center',
            'width': '85%',
            'margin': 'auto',
            'height' : '100%'
        }
    )

    # app callback that fills the domain dropdown
    @app.callback(
        [
            Output('description', 'options'),
            Output('description', 'value')
        ],
        [
            Input('module', 'value')
        ]
    )

    # function that fills the domain dropdown
    def fill_domain_dropdown(module):
        global df1

        # MongoDB Connections
        col = mongo.db.opinions

        cursor = col.find({})

        # load data into dataframe
        sanitized = json.loads(json_util.dumps(cursor))
        normalized = json_normalize(sanitized)
        df1 = pd.DataFrame(normalized)

        # get dataframe's columns
        available_indicators = list(df1)

        domains = []
        if (module == 'All'):
            domains = []
        else:
            df1 = df1[df1['Module'] == module]
            domains = df1['Dim_Question.Domain'].unique().tolist()

        domains.insert(0, 'All')
        return [[{'label': i, 'value': i} for i in domains], 'All']

    # app.callback that fills the theme / subdomain dropdown
    @app.callback(
        [
            Output('subdomain', 'options'),
            Output('subdomain', 'value')
        ],
        [
            Input('description', 'value'),
            Input('module', 'value')
        ]
    )
    # function to fill the theme / subdomain dropdown
    def fill_subdomain_dropdown(description, module):
        global df1

        if (module != 'All'):
            # MongoDB Connections
            col = mongo.db.opinions

            cursor = col.find({})

            # load data into dataframe
            sanitized = json.loads(json_util.dumps(cursor))
            normalized = json_normalize(sanitized)
            df1 = pd.DataFrame(normalized)

            df1 = df1[df1['Module'] == module]
            if (description != 'All'):
                # if Module and Domain are not All then the relevant Subdomains are loaded
                df1 = df1[df1['Dim_Question.Domain'] == description]
                subdomains = df1['Dim_Question.Subdomain'].unique().tolist()
            else:
                # if not, then the Domain and Subdomains will only have All option
                subdomains = []
            subdomains.insert(0, 'All')
        else:
            subdomains = ['All']

        return [[{'label': i, 'value': i} for i in subdomains], 'All']

    # app callback that fills the date picker range, user and question dropdowns
    @app.callback(
        [
            Output('questions', 'options'),
            Output('users', 'options'),
            Output('hidden-data', 'children')
        ],
        [
            Input('module', 'value'),
            Input('description', 'value'),
            Input('description', 'options'),
            Input('subdomain', 'value'),
            Input('subdomain', 'options'),
            Input('questions', 'value'),
            Input('users', 'value')
        ]
    )
    # function that fills the date picker range, user and question dropdowns
    def grapherino(module, description, description_opts, subdomain_val, subdomain_opts, quest_val, user_val):
        global df1
        # checking if the description and subdomain value are correct so that the graph can be plotted
        if (description is not None and subdomain_val is not None):
            val_in_opts = False
            for elem in subdomain_opts:
                if (subdomain_val == elem["label"]):
                    val_in_opts = True
                    break

            # subdomain value is in options array which means that the graph can be plotted
            if (val_in_opts):
                if (module != 'All'):
                    prov_df = df1[df1['Module'] == module]
                else:
                    prov_df = df1

                if (description != 'All'):
                    prov_df = df1[df1['Dim_Question.Domain'] == description]

                if (subdomain_val != 'All'):
                    prov_df = prov_df[(prov_df['Dim_Question.Subdomain'] == subdomain_val)]

                datetime = prov_df['Dim_Calendar.Date']

                years = []

                for it in datetime:
                    dt = dttime.strptime(it, '%Y-%m-%d')
                    if str(dt.year) not in years:
                        years.append(str(dt.year))

                years.sort()

                year_res = [{'label': 'All', 'value': 'All'}]
                for y in years:
                    year_res.append({'label': str(y), 'value': str(y)})

                # load Description, Subdomain Value and Options into a hidden data HTML element
                hidden_data = {
                    "description": description,
                    "subdomain_val": subdomain_val,
                    "subdomain_opts": subdomain_opts
                }

                # only fills question and username dropdown if description and subdomain are different than All
                if ((description != 'All') & (subdomain_val != 'All')):
                    if (quest_val != 'All'):
                        # if Question is not All then we limit the data to the things relevant to that Question
                        prov_df = prov_df[prov_df['Dim_Question.QuestionId'] == quest_val]
                    if (user_val != 'All'):
                        # if User is not All then we limit the data to the things relevant to that User
                        prov_df = prov_df[prov_df['Dim_User.User_id'] == user_val]

                    # listing unique question id's and add All option to Question Dropdown
                    quest_list = prov_df['Dim_Question.QuestionId'].unique().tolist()
                    quest_list.insert(0, 'All')
                    questions = [{'label': i, 'value': i} for i in quest_list]

                    # listing unique user id's and add All option to User Dropdown
                    user_list = prov_df['Dim_User.User_id'].unique().tolist()
                    user_list.insert(0, 'All')
                    users = [{'label': i, 'value': i} for i in user_list]

                else:
                    questions = [{'label': 'All', 'value': 'All'}]
                    users = [{'label': 'All', 'value': 'All'}]

                return [
                    questions,
                    users,
                    json.dumps(hidden_data)
                ]
            else:
                return [[{'label': 'All', 'value': 'All'}], [{'label': 'All', 'value': 'All'}], []]
        else:
            return [[{'label': 'All', 'value': 'All'}], [{'label': 'All', 'value': 'All'}], []]

    # app callback that plots graph
    @app.callback(
        [
            Output('linear-graph', 'figure'),
            Output('inquiry_nr_avg', 'children')
        ],
        [
            Input('hidden-data', 'children'),
            Input('questions', 'value'),
            Input('users', 'value'),
        ]
    )
    # fuction that plots graph
    def update_graph(hidden_data, quest_val, user_val):
        global df1
        ctx = dash.callback_context

        user_filter = False
        quest_filter = False

        if ctx.triggered:
            for elem in ctx.triggered:
                if (user_val != 'All'):
                    user_filter = True
                if (quest_val != 'All'):
                    quest_filter = True

        # load json data stored in the Hidden Data HTML element
        hidden_data = json.loads(hidden_data)

        # check what fields are All and which aren't, as done before, and filter based upon the result
        if (hidden_data["description"] != 'All'):
            prov_df = df1[df1['Dim_Question.Domain'] == hidden_data["description"]]
        else:
            prov_df = df1

        if (hidden_data["subdomain_val"] != 'All'):
            prov_df = prov_df[(prov_df['Dim_Question.Subdomain'] == hidden_data["subdomain_val"])]

        if (quest_filter and user_filter):
            prov_df = prov_df[(prov_df['Dim_Question.QuestionId'] == quest_val) & (prov_df['Dim_User.User_id'] == user_val)]

        else:
            if (quest_filter):
                prov_df = prov_df[prov_df['Dim_Question.QuestionId'] == quest_val]

            if (user_filter):
                prov_df = prov_df[prov_df['Dim_User.User_id'] == user_val]

        # list all the years featured in the dataframe
        years = prov_df['Dim_Calendar.Year'].unique()
        years.sort()

        # list 52 weeks, so that the graph displays correctly
        weeks = range(52)

        nr_inquiries = 0
        avg_inquiries = 0
        valid_weeks = 1

        data_array = []

        for y in years:
            # iterate every year so that it's plotted by a line
            p_dict = {
                'x' : [],
                'y' : [],
                'name' : str(y),
                'type' : 'scatter',
                'mode' : 'lines+markers',
                'connectgaps' : True,
                'showlegend' : True,
                'range' : [0,52],
                'margin' : {
                    'l' : 40,
                    'r' : 0,
                    't' : 40,
                    'b' : 30
                }
            }
            for w in weeks:
                # iterate each week within the year so as to load the data
                p_dict['x'].append(w)

                week_score = round(prov_df[(prov_df['Dim_Calendar.Year'] == y) & (prov_df['Dim_Calendar.Week'] == w)]['Review_Final_Score'].mean(), 2)
                p_dict['y'].append(week_score)

                if math.isnan(week_score):
                    # often the first week score is nan so here's a workaround
                    week_score = 0
                else:
                    valid_weeks = valid_weeks + 1

                # update variables
                nr_inquiries = nr_inquiries + prov_df[(prov_df['Dim_Calendar.Year'] == y) & (prov_df['Dim_Calendar.Week'] == w)]['Review_Final_Score'].count()
                avg_inquiries = avg_inquiries + week_score

            data_array.append(p_dict)

        # set total number of inquiries and average inquiry score to be displayed in front page
        avg_inquiries = round((avg_inquiries / valid_weeks), 2)
        inquiries_str = f'Nº inquéritos: {nr_inquiries}. Média: {avg_inquiries}'

        # feed collected data into structure that will be fed into graph
        linearGraph = {
            'data': data_array,
            'layout' : {
                'xaxis' : {
                    'range' : [0, 52]
                },
                'yaxis' : {
                    'range' : [0, 5.5]
                },
                'height' : '600',
                'min-width' : '800'
            }
        }

        return [linearGraph,inquiries_str]
    return app.server
