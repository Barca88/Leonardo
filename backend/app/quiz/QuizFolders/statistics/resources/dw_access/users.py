from bson.json_util import dumps, loads
from datetime import datetime, date, timedelta

def get_info_user(name,mongoDW):
    result=[]
    try:
        result = mongoDW.db.dm_answers.distinct("Dim_User",{"Dim_User.Name":name})
    except:
        print("Can't get user information from db")

def get_general_right_wrong(student,mongoDW):
    answers=[]
    try:
        answers = mongoDW.db.dm_answers.aggregate([
                                { '$match': {"Dim_User.Name":student}},
                                {'$project':{"Dim_Question":1,"_id":0,"Answer":1,
                                            "pointsEq1":{
                                                "$cond":[ { "$eq": ["$Answer.Correction", "1" ] },1, 0]},
                                            "pointsEq0":{
                                                "$cond":[ { "$eq": ["$Answer.Correction", "0" ] },1, 0]}
                                            }},
                                {'$group':{'_id':"$Dim_Question.Difficulty_Level",
                                            "right_answers_subdomain":{"$sum":"$pointsEq1"},
                                            "wrong_answers_subdomain":{"$sum":"$pointsEq0"},
                                }}])
    except:
        print("Can't get number of right and wrong answers from db")
    return list(answers)

def getOldRecord(student,mongoDW):
    recent=[]
    try:
        recent = mongoDW.db.dm_answers.aggregate([
                                    { '$match': {"Dim_User.Name":student}},
                                    { '$project': { "Dim_Calendar.Date": 1, "_id":0 }
                                    },
                                    {'$sort':{'Dim_Calendar.Date':-1}},
            ])
    except:
        print("Can't get oldest record for user from db")

    return list(recent)

def getCorrections(domain, subdomain, begin_date, end_date,student,mongoDW):
    corrections=[]
    try:
        corrections = mongoDW.db.dm_answers.aggregate([
                                { '$match': {
                                                "Dim_User.Name":student,
                                                "Dim_Question.Domain":domain,
                                                "Dim_Question.Subdomain":subdomain,
                                                "Dim_Calendar.Date":{"$gte":( begin_date), "$lte": (end_date)}}},
                                { '$project': { "Dim_Question": 1,"Dim_Calendar.Date": 1, "Answer.Correction":1, "_id":0,
                                                "pointsEq1":{
                                                        "$cond":[ { "$eq": ["$Answer.Correction", "1" ] },1, 0]
                                                },
                                                "pointsEq0":{
                                                        "$cond":[ { "$eq": ["$Answer.Correction", "0" ] },1, 0]
                                                },
                                }},
                                { '$group': {'_id':'$Dim_Calendar.Date',"right_answers_subdomain":{"$sum":"$pointsEq1"},
                                                                    "wrong_answers_subdomain":{"$sum":"$pointsEq0"}
                                            }
                                },
                                {'$sort':{'_id':1}},
                                { '$group': {'_id':"",
                                            "dates":{
                                                "$push":"$_id"
                                            },
                                            "total_right_answers":{
                                                "$push":"$right_answers_subdomain"
                                            },
                                            "total_wrong_answers":{
                                                "$push":"$wrong_answers_subdomain"
                                            }

                                            }
                                }
                                ])
    except:
        print("Can't get corrections per user from db")
    return loads(dumps(corrections))[0]

def getSubdomainsInfo(domain,begin_date,end_date,student,mongoDW):
    subdoms=[]
    try:
        subdoms = mongoDW.db.dm_answers.aggregate([{"$match":{"Dim_User.Name":student,"Dim_Question.Domain":domain,
                                                    "Dim_Calendar.Date":{"$gte":( begin_date), "$lte": (end_date)}}},
                                                            {"$project":{"Dim_Question":1, "Answer":1,
                                                                        "genderF":{
                                                                            "$cond":[ { "$eq": ["$Dim_User.Gender", "F" ] },"$Answer.Answer_Points", 0]},
                                                                        "genderM":{
                                                                            "$cond":[ { "$eq": ["$Dim_User.Gender", "M" ] },"$Answer.Answer_Points", 0]}}},
                                                            {"$group": {'_id':'$Dim_Question.Subdomain',
                                                                        "total_questions":{"$sum":1},
                                                                        "points_f_sub":{"$sum": {"$toInt":"$genderF"}},
                                                                        "points_m_sub":{"$sum":{"$toInt":"$genderM"}},
                                                                        "answertime_avg_sub":{"$avg":{ "$toDouble": "$Answer.Answer_Time" }}}},
                                                            {"$group": {'_id':'',
                                                                        'subs_list':{'$push':'$_id'},
                                                                        'questions_list':{'$push':'$total_questions'},
                                                                        'points_f_list':{'$push':'$points_f_sub'},
                                                                        'points_m_list':{'$push':'$points_m_sub'},
                                                                        'answertime_avg_list':{'$push':'$answertime_avg_sub'}}}])
    except:
        print("Can't get subdomains information from db")
    return list(subdoms)

def answers_by_level(year,semester,quarter,month,student,mongoDW):
    answers_count=[]
    try:
        if semester is not None:
            match_option = {'$match':{"Dim_User.Name":student,'Dim_Calendar.Year':year,'Dim_Calendar.Semester':semester}}
        else:
            if quarter is not None:
                match_option = {'$match':{"Dim_User.Name":student,'Dim_Calendar.Year':year,'Dim_Calendar.Quarter':quarter}}
            else:
                match_option = {'$match':{"Dim_User.Name":student,'Dim_Calendar.Year':year,'Dim_Calendar.Month':month}}

        answers_count = mongoDW.db.dm_answers.aggregate([
                                match_option,
                                {'$project':{"Dim_Question":1,"_id":0,"Answer":1,
                                            "pointsEq1":{
                                                "$cond":[ { "$eq": ["$Answer.Correction", "1" ] },1, 0]},
                                            "pointsEq0":{
                                                "$cond":[ { "$eq": ["$Answer.Correction", "0" ] },1, 0]}
                                            }},
                                {'$group':{'_id':"$Dim_Question.Difficulty_Level",
                                            "right_answers_subdomain":{"$sum":"$pointsEq1"},
                                            "wrong_answers_subdomain":{"$sum":"$pointsEq0"},
                                            "answertime_avg_level":{"$avg":{ "$toDouble": "$Answer.Answer_Time" }}
                                }},
                                {'$sort':{'_id':1}},
                                {"$group": {'_id':'',
                                    'levels_list':{'$push':'$_id'},
                                    'right_list':{'$push':'$right_answers_subdomain'},
                                    'wrong_list':{'$push':'$wrong_answers_subdomain'},
                                    'answertime_avg_list':{'$push':'$answertime_avg_level'}}}])
    except:
        print("Can't get answers by level from db")

    return list(answers_count)

def getLevelsByDates(begin_date, end_date,student,mongoDW):
    levels=[]
    try:
        levels = mongoDW.db.dm_answers.aggregate([
                                { '$match': {"Dim_User.Name":student,
                                    "Dim_Calendar.Date":{"$gte":( begin_date), "$lte": (end_date)}}},
                                { '$group': {'_id':{
                                                'date':'$Dim_Calendar.Date',
                                                'level':'$Dim_Question.Difficulty_Level'}}},
                                {'$sort':{'_id':1}},
                                { '$group': {'_id':"",
                                            "dates":{
                                                "$push":"$_id.date"
                                            },
                                            "levels":{
                                                "$push":"$_id.level"
                                            }
                                            }
                                }
                                ])
    except:
        print("Can't get recent and old record for logins from db")
    return levels

def general_dm_users(student,mongoDW):
    lista=[]
    try:
        startD = datetime.now()

        total = mongoDW.db.dm_answers.aggregate([{'$match': {"Dim_User.Name":student}},
                                                {'$project':{"Dim_Question":1,"_id":0,"Dim_User":1,
                                                "Answer":1,"Dim_Calendar.Date":1,
                                                "pointsEq1":{
                                                    "$cond":[ { "$eq": ["$Answer.Correction", "1" ] },1, 0]},
                                                "pointsEq0":{
                                                    "$cond":[ { "$eq": ["$Answer.Correction", "0" ] },1, 0]}}},
                                    {'$group':{'_id':"",
                                                "right_answers_total":{"$sum":"$pointsEq1"},
                                                "wrong_answers_total":{"$sum":"$pointsEq0"},
                                                "avg_time_total":{'$avg':{'$toDouble':'$Answer.Answer_Time'}}
                                    }},
                                    ])
        
        target_time = datetime.now() - timedelta(days=7)

        semana = mongoDW.db.dm_answers.aggregate([
                                    { '$match': {"Dim_User.Name":student,"Dim_Calendar.Date":{"$gte":( target_time), "$lte": (datetime.now())}}},
                                    {'$project':{"Dim_Question":1,"_id":0,"Dim_User":1,
                                                "Answer":1,"Dim_Calendar.Date":1,
                                                "pointsEq1":{
                                                    "$cond":[ { "$eq": ["$Answer.Correction", "1" ] },1, 0]},
                                                "pointsEq0":{
                                                    "$cond":[ { "$eq": ["$Answer.Correction", "0" ] },1, 0]}}},
                                    {'$group':{'_id':"",
                                                "right_answers_total":{"$sum":"$pointsEq1"},
                                                "wrong_answers_total":{"$sum":"$pointsEq0"},
                                                "avg_time_total":{'$avg':{'$toDouble':'$Answer.Answer_Time'}}
                                    }},
                                    ])
        total_json = {
            'total':{
                'right':0,
                'wrong':0,
                'avg':0
        }}
        for t in total:
            total_json = {
            'total':{
                'right':t['right_answers_total'],
                'wrong':t['wrong_answers_total'],
                'avg':round(t['avg_time_total'],2)
                }}
        semana_json = {
            'semana':{
                'right':0,
                'wrong':0,
                'avg':0
        }}
        for t in semana:
            right=0
            wrong=0
            avg=0
            if(total_json['total']['right']!=0):
                right=round((t['right_answers_total']/total_json['total']['right'])*100,2)
            if(total_json['total']['wrong']!=0):
                wrong=round((t['wrong_answers_total']/total_json['total']['wrong'])*100,2)
            if(total_json['total']['avg']!=0):
                avg=round((t['avg_time_total']/total_json['total']['avg'])*100,2)
            semana_json = {
            'semana':{
                'right':right,
                'wrong':wrong,
                'avg':avg
                }}
            
        lista=[]  
        lista.append(total_json)
        lista.append(semana_json)

    except:
        print("Can't get general user information from db")

    return lista

def get_answers_domain_user(domain,student,start,end,mongoDW):
    res=[]
    try:
        points = mongoDW.db.dm_answers.aggregate([
                                { '$match': {"Dim_Question.Domain":domain,"Dim_User.Name":student,"Dim_Calendar.Date":{"$gte":start, "$lte":end}}},
                                {'$project':{"_id":0,"Dim_User":1,
                                            "Answer":1, "Dim_Calendar":1, "Dim_Question":1,
                                            "pointsEq1":{
                                                    "$cond":[ { "$eq": ["$Answer.Correction", "1" ] },1, 0]},
                                                "pointsEq0":{
                                                    "$cond":[ { "$eq": ["$Answer.Correction", "0" ] },1, 0]}}},
                                {'$group':{'_id':"$Dim_Question.Subdomain",   
                                            "answers_right":{"$sum": "$pointsEq1"},
                                            "answers_wrong":{"$sum": "$pointsEq0"}         
                                }},
                                 {"$group": {'_id':'',
                                    'subdomains_list':{'$push':'$_id'},
                                    'right_list':{'$push':'$answers_right'},
                                    'wrong_list':{'$push':'$answers_wrong'}}}])

        res=loads(dumps(points))
    except:
        print("Can't get answers per domain for user "+student+" from db")

    return res