from bs4 import BeautifulSoup
import re
import string
import sys, getopt
from spellchecker import SpellChecker
from googletrans import Translator
import enchant


#Remove tags html of the text
def remove_html(text):
	soup = BeautifulSoup(text,'lxml')
	ntext = soup.get_text()
	return ntext  


#Converts the string to the automata alphabet
def convert_automata_alphabet(c):
    ax = ''
    if(c.isalpha() or c.isnumeric()):
        if(c in string.ascii_lowercase):
            ax = 'x'
        else: 
            ax = 'X'
    else:
        ax = '.'
    return ax

def word_breaker(transitions,initial,accepting,s):
    state = initial
    state_b = initial
    ns = ''
    for c in s:
        ax = convert_automata_alphabet(c)
        state_b = state
        state = transitions[state][ax]
        #print(state)
        if( (state_b == 3 and state == 2) or (state_b == 3 and state == 1)
         or (state_b == 2 and state == 1) or (state_b == 4 and state == 1) or
         (state_b == 4 and state == 2)):
            c = ' '+c
        ns = ns+c

    #return ns, state in accepting
    return ns

def phrase_breaker(t):
	#automata definition
	dfa = {0:{'X':1, 'x':2, '.':4},
       1:{'X':1,'x':2, '.':3},
       2:{'x':2, 'X':1, '.':3},
       3:{'X':1, 'x':2, '.':5},
       4:{'X':1, 'x':2, '.':5},
       5:{'.':5, 'x':5, 'X': 5}}
    #split the phrase in words 
	l = t.split()
	li =[]
	s = " "
	#apply the word breaker 
	for i in range(len(l)):
		li.append(word_breaker(dfa,0,{1,2,3,4},l[i]))
		s=" ".join(li)
	return s

def convert_lower_case(s):
	return s.lower()

def only_punctuation(word):
	for i in word:
		if not (i in string.punctuation):
			return False
	return True

def check_word_has_punctuation(word):
    flag = False
    w=''
    for p in string.punctuation:
        #print(p,word)
        if(word.find(p)!= -1 and only_punctuation(word) == False):
            flag = True
            w = re.sub('['+string.punctuation+']', '', word).split()
            break
    if(flag):
        return flag, w[0], p
    else: 
        return flag, p


def opinion_spell_checker(opinion):
	#words = re.sub('['+string.punctuation+']', '', opinion).split()
	words = opinion.split()
	li =[]
	s = " "
	spell = SpellChecker(language='en')
	# find those words that may be misspelled
	# misspelled = spell.unknown(['Olá mund.'])
	for word in words:
		cwhp = check_word_has_punctuation(word)
		if(cwhp[0]):
			li.append(spell.correction(cwhp[1]))
			li.append(cwhp[2])		
		else: 
			li.append(spell.correction(word))
		s=" ".join(li)
	return s 

def opinion_translate(opinion):
	translator = Translator()
	# origin = translator.translate(opinion, src='pt').origin
	translate = translator.translate(opinion, src='pt', dest='en').text
	return translate 

def pre_processing(opinion_text):
	# ap = argparse.ArgumentParser()
	# ap.add_argument("-t", "--t", required=True,
	# help="opinion text")
	# args = vars(ap.parse_args())
	# opinion_text = args["t"]
	if(opinion_text == ""):
		return opinion_text 

	opinion_text = remove_html(opinion_text)
	opinion_text = phrase_breaker(opinion_text)
	opinion_text = convert_lower_case(opinion_text)
	opinion_text = opinion_spell_checker(opinion_text)
	opinion_text = opinion_translate(opinion_text)
	return opinion_text




