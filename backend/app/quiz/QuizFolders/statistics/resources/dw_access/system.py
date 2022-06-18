from datetime import datetime, date, timedelta

def getRecentAndOldRecord(mongoDW):
    json = None
    try:
        old = mongoDW.db.dm_logs.find().sort('Dim_Calendar.Date',1).limit(1)
        recent = mongoDW.db.dm_logs.find().sort('Dim_Calendar.Date',-1).limit(1)
        for r in recent:
            for o in old:
                json={
                    'recent':r['Dim_Calendar']['Date'],
                    'old':o['Dim_Calendar']['Date']
                }
    except:
        print("Can't get recent and old record from db")

    return json

def getRecentAndOldRecordLogins(mongoDW):
    json=None
    try:
        old = mongoDW.db.dm_logs.find({"Dim_Request.URL":"/", "Dim_Request.Method":"POST"}).sort('Dim_Calendar.Date',1).limit(1)
        recent = mongoDW.db.dm_logs.find({"Dim_Request.URL":"/", "Dim_Request.Method":"POST"}).sort('Dim_Calendar.Date',-1).limit(1)
        json=None
        for r in recent:
            for o in old:
                json={
                    'recent':r['Dim_Calendar']['Date'],
                    'old':o['Dim_Calendar']['Date']
                }
    except:
        print("Can't get recent and old record for logins from db")

    return json


def getRequestsGetNumber(begin_date,end_date,mongoDW):
    requestsGet=[]
    try:
        requestsGet = mongoDW.db.dm_logs.aggregate([{"$match":{"Dim_Calendar.Date":{"$gte":(begin_date), "$lte": (end_date)},
                                                    "Dim_Request.URL": { "$not": {"$regex": "\\?"}}}},
                                                    {'$project':{"Dim_Calendar":1,"_id":0,"Dim_Request":1,
                                                    "get":{
                                                        "$cond":[ { "$eq": ["$Dim_Request.Method", "GET" ] },1, 0]},
                                                    "post":{
                                                        "$cond":[ { "$eq": ["$Dim_Request.Method", "POST" ] },1, 0]}
                                                    }},
                                                    {"$group": {'_id':'$Dim_Request.URL',
                                                                "total_requests_get":{"$sum":"$get"},
                                                                "total_requests_post":{"$sum":"$post"}}},
                                                    {"$group": {'_id':'',
                                                                'url_list':{'$push':'$_id'},
                                                                'request_list_get':{'$push':'$total_requests_get'},
                                                                'request_list_post':{'$push':'$total_requests_post'},
                                                                }}
                                                ])
    except:
        print("Can't get requests number from db")
    return list(requestsGet)

def getLongAndLat(mongoDW):
    users_list = []
    try:
        users_list = mongoDW.db.dm_logs.aggregate([{"$group": {'_id':'$Dim_User.City',
                                                            'users':{'$addToSet':'$Dim_User'}}}])
    except:
        print("Can't get users cities from db")
    return users_list

def general_dm_system(mongoDW):
    lista=[]
    try:
        startD = datetime.now()

        total = mongoDW.db.dm_logs.aggregate([{'$project':{"Dim_Request":1,"_id":0,"Dim_User":1,"Dim_Calendar.Date":1,
                                                "users":{
                                                        "$cond":[{"$and": [ { "$eq": ["$Dim_Request.URL", "/users/"]} ,
                                                                            {"$eq":["$Dim_Request.Code", "200"] }]},1, 0]},
                                                "quizz":{
                                                        "$cond":[ { "$eq": ["$Dim_Request.URL", "/evaluation/quizz" ] },1, 0]},
                                                "opiniao":{
                                                        "$cond":[ { "$eq": ["$Dim_Request.URL", "/evaluation/inquiry" ] },1, 0]}
                                                    }},
                                    {'$group':{'_id':"",
                                                "users":{'$sum':'$users'},
                                                "quizz":{"$sum":"$quizz"},
                                                "opiniao":{"$sum":"$opiniao"},
                                    }},
                                    ])
        
        target_time = datetime.now() - timedelta(days=7)

        semana = mongoDW.db.dm_logs.aggregate([
                                    { '$match': {"Dim_Calendar.Date":{"$gte":( target_time), "$lte": (datetime.now())}}},
                                    {'$project':{"Dim_Request":1,"_id":0,"Dim_User":1,"Dim_Calendar.Date":1,
                                                "users":{
                                                        "$cond":[{"$and": [ { "$eq": ["$Dim_Request.URL", "/users/"]} ,
                                                                            {"$eq":["$Dim_Request.Code", "200"] }]},1, 0]},
                                                "quizz":{
                                                        "$cond":[ { "$eq": ["$Dim_Request.URL", "/evaluation/quizz" ] },1, 0]},
                                                "opiniao":{
                                                        "$cond":[ { "$eq": ["$Dim_Request.URL", "/evaluation/inquiry" ] },1, 0]}
                                                    }},
                                    {'$group':{'_id':"",
                                                "users":{'$sum':'$users'},
                                                "quizz":{"$sum":"$quizz"},
                                                "opiniao":{"$sum":"$opiniao"},
                                    }},
                                    ])
        total_json = {
            'total':{
                'users':0,
                'quizz':0,
                'opiniao':0,
        }}
        for t in total:
            total_json = {
            'total':{
                'users':t['users'],
                'quizz':t['quizz'],
                'opiniao':t['opiniao'],
                }}
        semana_json = {
            'semana':{
                'users':0,
                'quizz':0,
                'opiniao':0,
        }}
        for t in semana:
            quizz=0
            users=0
            opinion=0
            
            if(total_json['total']['users']!=0):
                users=round((t['users']/total_json['total']['users'])*100,2)
            if(total_json['total']['quizz']!=0):
                quizz=round((t['quizz']/total_json['total']['quizz'])*100,2)
            if(total_json['total']['opiniao']!=0):
                opinion=round((t['opiniao']/total_json['total']['opiniao'])*100,2)
            semana_json = {
            'semana':{
                'users':users,
                'quizz':quizz,
                'opiniao':opinion,
                }}
            
        lista=[]  
        lista.append(total_json)
        lista.append(semana_json)

    except:
        print("Can't get system general information from db")

    return lista

def get_last_sevenDays_logins(begin_date,end_date,mongoDW):
    records=[]
    try:
        records = mongoDW.db.dm_logs.aggregate([
                                    { '$match': {"Dim_Calendar.Date":{"$gte":(begin_date), "$lte": (end_date)},
                                                "Dim_Request.URL":"/", "Dim_Request.Method":"POST"}},
                                    {'$project':{"Dim_Request":1,"_id":0,"Dim_User":1,"Dim_Calendar.Date":1,
                                                "auth":{
                                                        "$cond":[{"$or":[ { "$eq": ["$Dim_Request.Code", "200" ]},
                                                                        { "$eq": ["$Dim_Request.Code", "302" ]}]},1, 0]},
                                                "unauth":{
                                                        "$cond":[ { "$eq": ["$Dim_Request.Code", "403" ] },1, 0]}
                                                }},
                                    {'$group':{'_id':"$Dim_Calendar.Date",
                                                "totalLoginsAuth":{'$sum':"$auth"},
                                                "totalLoginsUnauth":{'$sum':"$unauth"}
                                    }},
                                    {"$group": {'_id':'',
                                                'date_list':{'$push':'$_id'},
                                                'authorized_logins':{'$push':'$totalLoginsAuth'},
                                                'unauthorized_logins':{'$push':'$totalLoginsUnauth'},
                                                }}
                                    ])
        for r in records:
            return r
    except:
        print("Can't get last seven days logins from db")