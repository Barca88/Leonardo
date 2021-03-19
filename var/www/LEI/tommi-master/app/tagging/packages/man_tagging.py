#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import os
import subprocess
import json
from app.tagging.packages import extra

def getClassificationList(classifier_words):
    classification_list = []
    for word in classifier_words:
        classi = word['classification']
        if classi != 'NP':
            if classi not in classification_list:
                classification_list.append(classi) 
    return classification_list

def canStop(next_verify, classifier_words,classification_list):
    op = 0
    dict_to_verify = classifier_words[next_verify]
    classification = dict_to_verify['classification']
    if classification in classification_list:
        if classification.startswith('P') or classification.startswith('S'):
            op = 2
        else:
            op = 1
    return op

def getPotentialWordLength(verify,word,classifier_words,classification_list):
    stop = False
    verify = verify + 1
    while(stop == False):
        dic_to_verify = classifier_words[verify]
        word = dic_to_verify['word']
        classification = dic_to_verify['classification']
        last = dic_to_verify['position']
        option = canStop(verify+1, classifier_words,classification_list)
        if option == 0:
            verify = verify + 1
        elif option == 1:
            stop = True
        else:
            option = canStop(verify+2, classifier_words,classification_list) 
            if option == 0:
                first = classifier_words[verify+1]['word']
                second = classifier_words[verify+2]['word']
                verify = verify + 2
            else:
                stop = True
    last = last
    return last

        


def getPotentialWords(start_words,classifier_words,classification_list):
    potential_words = []
    tamanho = len(classifier_words)
    verify = 0
    while verify < tamanho:
        word = classifier_words[verify]
        if(word['anotated'] == False):
            word_to_compare = word['word']
            new = {}
            if word_to_compare in start_words:
                last = getPotentialWordLength(verify,word_to_compare,classifier_words,classification_list)
                new['start'] = verify
                new['stop'] = last
                potential_words.append(new)
                verify = last + 1
            else:
                verify = verify + 1
        else:
            verify = verify + 1 
    return potential_words


############### Names #####################

def getNomesProprios(words):
    potential_nomes = []
    tamanho = len(words)
    verify = 0
    while verify < tamanho:
        word = words[verify]
        if(word['anotated'] == False):
            new = {}
            if (word['classification'] == 'NP'):
                new['start'] = verify
                last = verify
                nextTest = last +1
                if (nextTest < tamanho):
                    word = words[nextTest]
                    stop = False
                    while(stop == False):
                        if(word['classification'] == 'NP'):
                            last = nextTest
                            nextTest  = nextTest + 1
                            if(nextTest < tamanho):
                                word = words[nextTest]
                            else: 
                                stop = True
                        elif(word['classification'] == 'SP'):
                            nextTest  = nextTest + 1
                            if(nextTest < tamanho):
                                word = words[nextTest]
                                if(word['classification'] == 'NP'):
                                    last = nextTest
                                    nextTest  = nextTest + 1
                                    if(nextTest < tamanho):
                                        word = words[nextTest]
                                    else: 
                                        stop = True
                                else:
                                    stop = True
                            else: 
                                stop = True
                        else:
                            stop = True                
                new['stop'] = last
                potential_nomes.append(new)
                verify = last + 1
            else:
                verify = verify + 1
        else:
            verify = verify + 1 
    return potential_nomes
