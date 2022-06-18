
from bson.json_util import dumps, loads

from datetime import datetime, date, timedelta

def getSubdomains(domain,mongoDW):
    subdomains_json=[]

    try:
        subdomains = mongoDW.db.dm_answers.distinct("Dim_Question.Subdomain",
                                            {"Dim_Question.Domain":domain} )
        for d in subdomains:
            json={
                'label':d,
                'value':d
            }
            subdomains_json.append(json)
    except:
        print("Can't get subdomains from db")
    return subdomains_json

def getSubdomainsInfo(domain,begin_date,end_date,mongoDW):
    subdoms = []
    try:
        subdoms = mongoDW.db.dm_answers.aggregate([{"$match":{"Dim_Question.Domain":domain,
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
        print("Can't get subdomains info from db")

    return list(subdoms)

def getCorrections(domain, subdomain, begin_date, end_date,mongoDW):
    corrections = []
    try:
        corrections = mongoDW.db.dm_answers.aggregate([
                                { '$match': {"Dim_Question.Domain":domain,
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
        print("Can't get corrections from db")

    return loads(dumps(corrections))[0]

def getOldRecord(domain, subdomain,mongoDW):
    recent = []
    try:
        recent = mongoDW.db.dm_answers.aggregate([
                                    { '$match': {"Dim_Question.Domain":domain,
                                                "Dim_Question.Subdomain":subdomain }},
                                    { '$project': { "Dim_Calendar.Date": 1, "_id":0 }
                                    },
                                    {'$sort':{'Dim_Calendar.Date':-1}},
            ])
    except:
        print("Can't get old record from db")

    return list(recent)

def getOldRecord_Domain(domain,mongoDW):
    recent = []
    try:
        recent = mongoDW.db.dm_answers.find({"Dim_Question.Domain":domain}).sort('Dim_Calendar.Date',1)
    except:
        print("Can't getting top students from db")

    return list(recent)


def getYears_Domain(domain,subdom,mongoDW):
    recent = []
    try:
        recent = mongoDW.db.dm_answers.distinct("Dim_Calendar.Year",{"Dim_Question.Domain":domain, "Dim_Question.Subdomain":subdom})
    except:
        print("Can't get years domains from db")
    return recent

def answers_by_level(year,semester,quarter,month,mongoDW):
    answers_count = []

    try:
        if semester is not None:
            match_option = {'$match':{'Dim_Calendar.Year':year,'Dim_Calendar.Semester':semester}}
        else:
            if quarter is not None:
                match_option = {'$match':{'Dim_Calendar.Year':year,'Dim_Calendar.Quarter':quarter}}
            else:
                match_option = {'$match':{'Dim_Calendar.Year':year,'Dim_Calendar.Month':month}}

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

def score_by_level_gender(year,semester,quarter,month,mongoDW):
    answers_count = []

    try:
        if semester is not None:
            match_option = {'$match':{'Dim_Calendar.Year':year,'Dim_Calendar.Semester':semester}}
        else:
            if quarter is not None:
                match_option = {'$match':{'Dim_Calendar.Year':year,'Dim_Calendar.Quarter':quarter}}
            else:
                match_option = {'$match':{'Dim_Calendar.Year':year,'Dim_Calendar.Month':month}}

        answers_count = mongoDW.db.dm_answers.aggregate([
                                        match_option,
                                        {'$project':{"Dim_Question":1,"_id":0,"Dim_User":1,
                                            "Answer":1,
                                            "genderF":{
                                                "$cond":[ { "$eq": ["$Dim_User.Gender", "F" ] },"$Answer.Answer_Points", 0]},
                                            "genderM":{
                                                "$cond":[ { "$eq": ["$Dim_User.Gender", "M" ] },"$Answer.Answer_Points", 0]}
                                            }},
                                {'$group':{'_id':"$Dim_Question.Difficulty_Level",
                                            "points_f_level":{"$sum": {"$toInt":"$genderF"}},
                                            "points_m_level":{"$sum":{"$toInt":"$genderM"}},
                                }},
                                {'$sort':{'_id':1}},
                                {"$group": {'_id':'',
                                    'levels_list':{'$push':'$_id'},
                                    'points_f_list':{'$push':'$points_f_level'},
                                    'points_m_list':{'$push':'$points_m_level'}}}])
    except:
        print("Can't get score by level and gender from db")
    
    return list(answers_count)

def get_answers_degree(dom,subdom,start,end,mongoDW):
    res=[]
    try:
        points = mongoDW.db.dm_answers.aggregate([
                                { '$match': {"Dim_Question.Domain":dom,
                                                    "Dim_Question.Subdomain":subdom,
                                                    "Dim_Calendar.Date":{"$gte":( start), "$lte": (end)}}},
                                {'$project':{"_id":0,"Dim_User":1,
                                            "Answer":1, "Dim_Calendar":1}},
                                {'$group':{'_id':{
                                                "Date":"$Dim_Calendar.Date",
                                                "Degree":"$Dim_User.Degree"},   
                                            "points_degree":{"$push": {"$toInt":"$Answer.Answer_Points"}}         
                                }},
                                {'$sort':{'_id':1}},
                                {'$project':
                                    {'list_points':{'$reduce':{
                                        'input':'$points_degree',
                                        'initialValue':{'sum':0},
                                        'in':{
                                            'sum':{'$add':['$$value.sum','$$this']}
                                        }
                                    }}}
                                },
                                {'$group':{'_id':'$_id.Degree',
                                            'dates':{'$push':'$_id.Date'},
                                            'list_p':{'$push':'$list_points.sum'}}}])

        res=loads(dumps(points))    
    except:
        print("Can't get answers per degree from db")

    return res

def get_top_students(dom,subdom,start,end,mongoDW):
    res=[]
    points=[]
    try:
        points = mongoDW.db.dm_answers.aggregate([
                                { '$match': {"Dim_Question.Domain":dom,
                                                "Dim_Question.Subdomain":subdom,
                                                "Dim_Calendar.Date":{"$gte":( start), "$lte": (end)}}},
                                {'$project':{"_id":0,"Dim_User":1,"Answer":1}},
                                {'$group':{'_id':{
                                                "id":"$Dim_User.UserId",
                                                "name":"$Dim_User.Name",
                                                "degree":"$Dim_User.Degree"},   
                                                "points_user":{"$sum": {"$toInt":"$Answer.Answer_Points"}}         
                                }},
                                {'$sort':{'points_user':-1}},
                                { '$limit' : 3 }])
        for p in points:
            res.append(p)
        
        return res
    except:
        print("Can't getting top students from db")

def get_answers_domain(dom,start,end,mongoDW):
    answers = []
    try:
        answers = mongoDW.db.dm_answers.aggregate([
                                { '$match': {"Dim_Question.Domain":dom,
                                                    "Dim_Calendar.Date":{"$gte":( start), "$lte": (end)}}},
                                {'$project':{"_id":0,"Dim_Question":1,
                                            "Answer":1, "Dim_Calendar":1}},
                                {'$group':{'_id':{
                                                "Date":"$Dim_Calendar.Date",
                                                "Subdomain":"$Dim_Question.Subdomain"},   
                                                "answers_subdomain":{"$sum": 1}         
                                }},
                                {'$sort':{'_id':1}},
                                {'$group':{'_id':'$_id.Subdomain',
                                            'dates':{'$push':'$_id.Date'},
                                            'list_a':{'$push':'$answers_subdomain'}}}])
    except:
        print("Can't get anwers domains from db")

    return list(answers)

def get_questions_domain(dom,mongoDW):
    questions = []
    try:    
        questions = mongoDW.db.dm_answers.aggregate([
                                { '$match': {"Dim_Question.Domain":dom}},
                                {'$project':{"_id":0,"Dim_Question":1,
                                            "Answer":1, "Dim_Calendar":1}},
                                {'$group':{'_id':"$Dim_Question.Subdomain",   
                                                "questions_subdomain":{"$addToSet": "$Dim_Question.QuestionId"}         
                                }}])
    except:
        print("Can't get questions domains from db")
    
    return questions

def general_dm_answers(mongoDW):
    lista = []
    try:
        startD = datetime.now()

        total = mongoDW.db.dm_answers.aggregate([{'$project':{"Dim_Question":1,"_id":0,"Dim_User":1,
                                                "Answer":1,"Dim_Calendar.Date":1,
                                                "pointsEq1":{
                                                    "$cond":[ { "$eq": ["$Answer.Correction", "1" ] },1, 0]},
                                                "pointsEq0":{
                                                    "$cond":[ { "$eq": ["$Answer.Correction", "0" ] },1, 0]}}},
                                    {'$group':{'_id':"",
                                                "domains":{'$addToSet':'$Dim_Question.Domain'},
                                                "right_answers_total":{"$sum":"$pointsEq1"},
                                                "wrong_answers_total":{"$sum":"$pointsEq0"},
                                                "avg_time_total":{'$avg':{'$toDouble':'$Answer.Answer_Time'}}
                                    }},
                                    ])
        
        target_time = datetime.now() - timedelta(days=7)

        semana = mongoDW.db.dm_answers.aggregate([
                                    { '$match': {"Dim_Calendar.Date":{"$gte":( target_time), "$lte": (datetime.now())}}},
                                    {'$project':{"Dim_Question":1,"_id":0,"Dim_User":1,
                                                "Answer":1,"Dim_Calendar.Date":1,
                                                "pointsEq1":{
                                                    "$cond":[ { "$eq": ["$Answer.Correction", "1" ] },1, 0]},
                                                "pointsEq0":{
                                                    "$cond":[ { "$eq": ["$Answer.Correction", "0" ] },1, 0]}}},
                                    {'$group':{'_id':"",
                                                "domains":{'$addToSet':'$Dim_Question.Domain'},
                                                "right_answers_total":{"$sum":"$pointsEq1"},
                                                "wrong_answers_total":{"$sum":"$pointsEq0"},
                                                "avg_time_total":{'$avg':{'$toDouble':'$Answer.Answer_Time'}}
                                    }},
                                    ])
        total_json = {
            'total':{
                'domains':0,
                'right':0,
                'wrong':0,
                'avg':0
        }}
        for t in total:
            total_json = {
            'total':{
                'domains':len(t['domains']),
                'right':t['right_answers_total'],
                'wrong':t['wrong_answers_total'],
                'avg':round(t['avg_time_total'],2)
                }}
        semana_json = {
            'semana':{
                'domains':0,
                'right':0,
                'wrong':0,
                'avg':0
        }}
        for t in semana:
            domains=0
            right=0
            wrong=0
            avg=0
            if(total_json['total']['domains']!=0):
                domains=round((t['right_answers_total']/total_json['total']['right'])*100,2)
            if(total_json['total']['right']!=0):
                right=round((t['right_answers_total']/total_json['total']['right'])*100,2)
            if(total_json['total']['wrong']!=0):
                wrong=round((t['wrong_answers_total']/total_json['total']['wrong'])*100,2)
            if(total_json['total']['avg']!=0):
                avg=round((t['avg_time_total']/total_json['total']['avg'])*100,2)
            semana_json = {
            'semana':{
                'domains':domains,
                'right':right,
                'wrong':wrong,
                'avg':avg
                }}
            
        lista=[]  
        lista.append(total_json)
        lista.append(semana_json)

    except:
        print("Can't get general_dm_answers from db")

    return lista

def get_evaluation_history(month,subdom,year,dom,mongoDW):
    evaluation = []
    try:
        evaluation = mongoDW.db.dm_answers.aggregate([{"$match":{"Dim_Question.Domain":dom, "Dim_Question.Subdomain":subdom,
                                                                'Dim_Calendar.Year':year,'Dim_Calendar.Month':month}},
                                                            {"$project":{"Dim_Question":1, "Answer":1, "Dim_Calendar":1,
                                                            }},
                                                            {"$group": {'_id':{"Subdomain":'$Dim_Question.Subdomain',
                                                                                "Week":'$Dim_Calendar.Week'},
                                                                        "answerpoints_avg_sub":{"$avg":{ "$toDouble": "$Answer.Answer_Points" }}}},
                                                            {'$sort':{'_id.Week':1}},
                                                            {"$group": {'_id':'',
                                                                        'week_list':{'$push':{'$concat':['Semana: ',{'$toString':'$_id.Week'},' ']}},
                                                                        'answerpoints_avg_list':{'$push':'$answerpoints_avg_sub'}}}])
    except:
        print("Can't get evaluation history from db")
    
    return list(evaluation)
