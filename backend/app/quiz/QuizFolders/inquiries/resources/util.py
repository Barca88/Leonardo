#/usr/bin/python3
from flask import Flask, jsonify, json
from datetime import date, datetime
import calendar
import os
from app import mongo
from pprint import pprint
from .my_preprocessing.preprocessor import pre_processing
from .my_preprocessing.tokenizer import filtered_comment
from .sentiment_analysis.sentiment_analysis import get_polarity_from_comment, get_important_words
from .sentiment_analysis.utils import get_index_average

'''
    Esta função é responsável por devolver o inquérito pedido.
'''
def findInquiry(id):
    data = mongo.db.templates.find()
    print(data)
    
    for inq in data:
        if(inq['inquiry_id'] == id):
            print('found')
            return inq
        print('next')
    print('Not found!')

'''
    Esta função é responsável por devolver todos os id's dos inqueritos existentes.
'''
def getAllIds():
    data = mongo.db.templates.find()
    ids= []
    for inq in data:
        ids.append(inq["inquiry_id"])
    return ids

'''
    Esta função é responsável por modificar a estrutura JSON correspondente à questão.
'''
def questionDimStructure(data):
    qid = data['id']
    study_cicle= data['study_cycle']
    scholarity= data['scholarity']
    domain = data['domain']
    sdomain = data['subdomain']
    ssdomain=data['subsubdomain']
    difficulty_level= data['difficulty_level']
    anstime = data['answering_time']
    tp = data['type']

    dim_question = {}
    dim_question['QuestionId'] = qid
    dim_question['Study_Cycle'] = study_cicle
    dim_question['Scholarity'] = scholarity
    dim_question['Domain'] = domain
    dim_question['Subdomain'] = sdomain
    dim_question['Subsubdomain'] = ssdomain
    dim_question['Difficulty_Level'] = difficulty_level
    dim_question['Answering_Time'] = anstime
    dim_question['Type'] = tp

    return dim_question

'''
    Esta função é responsável por devolver a linguagem da questão
'''
def getLanguage(data):
    return data['language']

'''
    Esta função é responsável por alterar a estrutura da data recebido da aplicação do cliente.
'''
def changeDateStructure(date):
    return datetime.strptime(date,'%Y-%m-%dT%H:%M:%S.%fZ')

'''
    Esta função é responsável por devolver o ano de uma respetiva data.
'''
def getYear(date):
    return date.year

'''
    Esta função é responsável por devolver o mês, como um inteiro, de uma respetiva data.
'''
def getMonth(date):
    return date.month
'''
    Esta função é responsável por devolver o dia, como um inteiro, de uma respetiva data.
'''
def getDay(date):
    return date.day

'''
    Esta função é responsável por converter o mês, como um inteiro, para o seu respetivo nome.
'''
def convertMonth(month:int):
    return calendar.month_name[int(month)]

'''
    Esta função é responsável por converter o quartil no qual um mês se insere.
'''
def convertQuarter(month:int):
    if(month >= 1 and month <= 3):
        return '01'
    if(month >= 4 and month <= 6):
        return '02'
    if(month >= 7 and month <= 9):
        return '03'
    if(month >= 10 and month <= 12):
        return '04'
    else:
        print('Conversion failed.')
        return None

'''
    Esta função é responsável por converter o semestre no qual um mês se insere.
'''
def convertSemester(month: int):
    if(month >= 1 and month <= 6):
        return '01'
    if(month >= 7 and month <= 12):
        return '02'
    else:
        print('Conversion failed.')
        return None
'''
    Esta função é responsável por devolver o dia da semana a qual a data corresponde.
'''
def convertWeekDay(nd):
    return calendar.day_name[nd.weekday()]

'''
    Esta função é responsável por devolver o número da semana de uma determinada data.
'''
def convertWeek(nd):
    return nd.isocalendar()[1]

'''
    Esta função é responsável por converter uma data no JSON Dim_Calendar.
'''
def convertDimCalendar(dates):
    nd = changeDateStructure(dates)
    dat = nd.date()
    month = getMonth(nd)
    dic = { 
    "Date": str(dat),
    "Month": convertMonth(month),
    "Quarter": convertQuarter(month),
    "Semester": convertSemester(month),
    "Year": str(getYear(nd)),
    "Week": convertWeek(nd),
    "Weekday": convertWeekDay(nd)
    }
    return dic

'''
    Esta função é responsável por converter uma data no atributo JSON 'Dim_Time'.
'''
def convertDimTime(dates):
    nd = changeDateStructure(dates)
    t = nd.time()
    ret = (str(t.hour)) + ":00"
    return ret

'''
    Esta função é responsável por converter uma data no atributo JSON 'Dim_User'.
'''
def getUser(user):
    print(user)
    data = mongo.db.users.find({ 'id': user })
    cursor = list(data)[0]
    dic = {
        "User_id": user,
        "Name": cursor['name'],
		"Gender": cursor['gender'],
		"Degree": cursor['degree']
    }
    return dic

def comment_analysis(comment):
    processed_text = pre_processing(comment)
    tokenized_text = filtered_comment(processed_text)
    polarity = get_polarity_from_comment(tokenized_text)
    important_words = get_important_words(tokenized_text)
    return polarity, important_words

def opinion_analysis(opinion):
    index_average = get_index_average(opinion)
    score, important_words = comment_analysis(opinion['InquiryAnswer']['Comments'])

    if(len(important_words) == 0):
        final_score = index_average
    else:
        final_score = index_average * 0.75 + score * 0.25

    sentiment = 'Positive'

    if (final_score <= 2.5):
        sentiment = 'Negative'

    if (final_score > 2.5 and final_score < 3.5):
        sentiment = 'Neutral'

    opinion['Opinion'] = {}

    opinion['Opinion']['Static_Index_Average'] = index_average
    opinion['Comments'] = {
        'Comment' : opinion['InquiryAnswer']['Comments'],
        'Comment_rating' : score,
            'Sentiment' : sentiment,
            'Important_Words' : important_words
        }
    opinion['Review_Final_Score'] = final_score

    return opinion

def fixAnswersDocument(answers,date,user,question,inquiry_id):
    answers["Inquiry_id"] = inquiry_id
    answers["Dim_Calendar"] = convertDimCalendar(date)
    answers["Dim_Time"] = convertDimTime(date)
    answers["Dim_Period"] = "N"
    answers["Dim_User"] = getUser(user)
    if (question is not None):
        data = mongo.db.question.find({'id': question})
        data = list(data)[0]
        answers["Dim_Question"] = questionDimStructure(data)
        answers["Dim_Language"] = getLanguage(data)

    return opinion_analysis(answers)
