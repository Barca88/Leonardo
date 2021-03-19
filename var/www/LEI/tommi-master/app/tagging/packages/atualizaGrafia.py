#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import os
import json
import io
from app.tagging.packages import extra

regras_path = './app/tagging/packages/static/json/regras_atualizagrafia.json'
folios_path = './app/tagging/packages/static/Folios/'

def getRegras(regrasAtualizacao):
    rules = {}
    for regra in regrasAtualizacao:
        old = regra['old']
        new = regra['new']
        if old not in rules:
            rules[old] = new
    return rules


def applyRegra(key, val, word):
    word = word.replace("\n","")
    grupos = key.split('#')
    match = ""
    substituir = ""
    index = 1
    for group in grupos:
        match = match + "(" + group + ")" 
        if ('[' in group) and (']' in group):
            substituir = substituir + "\\" + str(index)
        else:
            substituir = substituir + val
        index = index + 1
    regra_match = r'' + match + '' 
    regra_susbstituir = r'' + substituir + ''
    word = re.sub(regra_match, regra_susbstituir, word)
    return word

def applyRules(folio,rules):
    words = folio.split(' ')
    count = 0
    replacerList = []
    novoFolio = ""
    for word in words:
        replacer = {}
        if word:
            replacer["old"] = word
            for rule_key,rule_val in rules.items():
                word = applyRegra(rule_key, rule_val, word)
            replacer["new"] = word
            replacerList.append(replacer)
    for rule_key,rule_val in rules.items():
        folio = applyRegra(rule_key,rule_val,folio)
    return folio,replacerList


def refresh(rules,folio):
    refresh_folio,replacerList = applyRules(folio,rules)
    return refresh_folio, replacerList
    

def atualizaFolio(folio):
    regrasAtualizacao = extra.getRegrasAtualizacao()
    rules = getRegras(regrasAtualizacao)
    refresh_folio, replacerList = refresh(rules,folio)
    return refresh_folio, replacerList
    