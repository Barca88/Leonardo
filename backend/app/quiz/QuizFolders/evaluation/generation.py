from app                             import mongo
from datetime                        import datetime
from random                          import choice
from concurrent.futures              import ThreadPoolExecutor
import spacy
from spacy_wordnet.wordnet_annotator import WordnetAnnotator
import random

class Generation:
    print('generation')
    '''
        Initialization of the most relevant variables for the reasoning process, specifically the working memory
    '''
    def __init__(self, username, difficulty_level, domain, subdomain):
        self.working_memory = {}
        
        nlp = spacy.load("pt_core_news_md")
        nlp.add_pipe("spacy_wordnet", config={'lang': 'pt'})
        
        self.working_memory = {
            'username': username,
            'domain': domain['_id'],
            #'study_cycle': domain['study_cycle'],
            #'scholarity': domain['scholarity'],
            'subdomain': subdomain,
            'difficulty_level': difficulty_level,
            'retrieved_questions': [],
            'most_interesting_question': {},
            'correct_answers': [],
            'nlp': "",
            'new_question': {}
        }

        self.working_memory['nlp'] = nlp

    '''
        Replacement of tokens (belonging to answer options) with synonyms
    '''
    def parse_synonyms(self, element, tokens_to_be_replaced_by_synonyms):
        print('-GENERATION PARSE')
        valid_synonyms = []

        for lemma in element['lemmas']:
            lemma_name = lemma.name()

            if(lemma.synset().pos() == element['pos']):
                if(lemma_name != element['description']):
                    doc_lemma = self.working_memory['nlp'](lemma_name)
                    token_info = doc_lemma[0]

                    same_number = False
                    same_gender = False

                    if(len(token_info.morph.get("Number")) > 0):
                        if(token_info.morph.get("Number")[0] == element['number']):
                            same_number = True
                    else:
                        same_number = False
                    if(len(token_info.morph.get("Gender")) > 0):                    
                        if(token_info.morph.get("Gender")[0] == element['gender']):
                            same_gender = True
                    else:
                        same_number = False

                    if( ( same_number == True ) and ( same_gender == True ) ):
                        valid_synonyms.append(lemma_name)

        synonym_description = ""
        if(len(valid_synonyms) > 0):
            synonym_description = choice(valid_synonyms)

        if(synonym_description != ""):
            next((x for x in tokens_to_be_replaced_by_synonyms if x['position_on_list'] == element['position_on_list']), None)['description'] = synonym_description

        #print("\nTokens_to_be_replaced_by_synonyms no parse_synonyms:", tokens_to_be_replaced_by_synonyms, "\n")

        return ""

    '''
        Modification of the most interesting question header
    '''
    #ter em atenção se a palavra original é ou nao portuguesa
    def edit_question_header(self):
        print('-GENERATION EDIT')
        sentence = self.working_memory['nlp'](self.working_memory['most_interesting_question']['header'])

        new_tokens = []
        counter = 0
        tokens_to_be_replaced_by_synonyms = []
        for token in sentence:
            if( 
                ( ( token.pos_ == "NOUN" ) or ( token.pos_ == "ADJ" ) ) and
                ( ( counter > 0 ) and ( counter < (len(sentence) - 1) ) ) and
                ( ( sentence[counter - 1].text != '\'' ) and ( sentence[counter + 1].text != '\'' ) )
            ):

                tokens_to_be_replaced_by_synonyms.append({
                    'pos': 'n' if token.pos_ == "NOUN" else "a",
                    'position_on_list': counter,
                    'description': token.text,
                    'gender': token.morph.get("Gender")[0] if len(token.morph.get("Gender")) > 0 else "",
                    'number': token.morph.get("Number")[0] if len(token.morph.get("Number")) > 0 else "",
                    'lemmas': token._.wordnet.lemmas()
                })

            new_tokens.append(token.text)

            counter += 1

        #print("\nTokens_to_be_replaced_by_synonyms no edit_question_header antes do with:", tokens_to_be_replaced_by_synonyms, "\n")

        number_of_tokens = len(tokens_to_be_replaced_by_synonyms)

        #futures = []

        with ThreadPoolExecutor(max_workers=number_of_tokens) as executor:
            for i in range(number_of_tokens):
                #print("\nUma iteração\n")
                future = executor.submit(self.parse_synonyms, tokens_to_be_replaced_by_synonyms[i], tokens_to_be_replaced_by_synonyms)
                print("\nFuture:", future, "\n")

                #futures.append(future)

        #print("\nFutures:", futures, "\n")
        #print("\nTokens_to_be_replaced_by_synonyms no edit_question_header depois do with:", tokens_to_be_replaced_by_synonyms, "\n")

        #for t in tokens_to_be_replaced_by_synonyms:
            #self.

        for n in tokens_to_be_replaced_by_synonyms:
            new_tokens[n['position_on_list']] = n['description']

        #Joining the various constituents of the new header in a single expression
        self.working_memory['most_interesting_question']['header'] = ' '.join(new_tokens)

        return

    '''
        Calculating and sorting incorrect answer options by their degree of similarity, on average, with the correct 
        answer options for the most interesting question
    '''
    def get_similarities(self, answers):
        print('-GENERATION GETSIMS')
        nlp_correct_answers_without_stop_words = []

        list1 = list(self.working_memory['nlp'].pipe(self.working_memory['correct_answers']))

        list2 = [' '.join([str(t) for t in l if not t.is_stop]) for l in list1]

        nlp_correct_answers_without_stop_words = list(self.working_memory['nlp'].pipe(list2))

        average_similarity_by_answer = []
        counter = 0

        for a in answers:
            doc = self.working_memory['nlp'](a)
            doc_without_stop_words = self.working_memory['nlp'](' '.join([str(t) for t in doc if not t.is_stop]))

            total_similarity = 0
            for ans in nlp_correct_answers_without_stop_words:
                sim = doc_without_stop_words.similarity(ans)
                if(sim < 1):
                    total_similarity += sim

            avg_similarity = total_similarity / len( self.working_memory['correct_answers'] )
            average_similarity_by_answer.append({ 'text': a, 'similarity': avg_similarity })

            counter += 1

        sorted_average_similarity_by_answer = sorted(average_similarity_by_answer, key=lambda k: k.get('similarity'), reverse=True)
        
        sorted_answers = [ a for a in sorted_average_similarity_by_answer ]

        return sorted_answers

    '''
        Selecting the most interesting question from the retrieved_questions set
    '''
    def question_selection(self):
        print('-GENERATION SELECT')
        questions_by_number_of_appearances = {}
        for q in self.working_memory['retrieved_questions']:
            number_of_appearances = mongo.db.profiles.find( { "session_questions_ids": { "$all": [ q['_id'] ] } } ).count()
            

            questions_by_number_of_appearances[q['_id']] = ( 0.6 * number_of_appearances )

            question_info = mongo.db.question.find_one({ "_id": q['_id'] })

            questions_by_number_of_appearances[q['_id']] += ( 0.3 * len( question_info['body'] ) )

            number_of_right_option_answers = 0
            for a in question_info['body']:
                if( a['correction'] == '1' ):
                    number_of_right_option_answers += 1

            questions_by_number_of_appearances[q['_id']] += ( 0.1 * number_of_right_option_answers )

        sorted_dict = {}
        sorted_keys = sorted(questions_by_number_of_appearances, key=questions_by_number_of_appearances.get, reverse=True)

        for w in sorted_keys:
            sorted_dict[w] = questions_by_number_of_appearances[w]

        try:
            greatest_value = int( sorted_dict[list(sorted_dict.keys())[0]] )
        except:
            greatest_value=0

        greatest_values = {}
        for w in sorted_dict:
            if sorted_dict[w] >= greatest_value:
                greatest_values[w] = sorted_dict[w]

        random_id_from_greatest_values = random.choice(list(greatest_values))

        self.working_memory['most_interesting_question'] = mongo.db.question.find_one({"_id": random_id_from_greatest_values})

        print("\nMost_interesting_question:", self.working_memory['most_interesting_question'], "\n")

    '''
        Represents the formation of the new JSON object, relative to the new multiple choice question
    '''
    def form_question(self, sorted_answers):
        print('-GENERATION FORMQUESTION')
        new_body = []

        for c in self.working_memory['correct_answers']:
            new_body.append({
                "answer" : c,
                "correction" : "1",
                "mandatory" : "1",
                "eliminative" : "0",
                "points" : "0"
            })

        c = 0
        answers_controller = []
        for d in sorted_answers:
            if(c <= 4 and (not d['text'] in answers_controller)):
                new_body.append({
                    "answer" : d['text'],
                    "correction" : "0",
                    "mandatory" : "1",
                    "eliminative" : "0",
                    "points" : "0"
                })
                answers_controller.append(d['text'])
                c += 1

        most_inter_quest = self.working_memory['most_interesting_question']

        id_from_most_inter_quest = self.working_memory['most_interesting_question']['_id']
        fst_part = id_from_most_inter_quest[ : len( id_from_most_inter_quest ) - 3]

        regex = fst_part + ".*"

        query = mongo.db.question.count_documents( { "_id" : { "$regex" : regex } } )

        snd_part = "0" + str(query + 1) if(query < 100) else str(query + 1)
        
        self.working_memory['new_question'] = {
            "_id" : fst_part + snd_part,
            "language" : most_inter_quest['language'],
            "study_cycle" : most_inter_quest['study_cycle'],
            "scholarity" : most_inter_quest['scholarity'],
            "domain" : most_inter_quest['domain'],
            "subdomain" : most_inter_quest['subdomain'],
            "difficulty_level" : most_inter_quest['difficulty_level'],
            "display_mode" : most_inter_quest['display_mode'],
            "answering_time" : most_inter_quest['answering_time'],
            "type_" : most_inter_quest['type_'],
            "precedence" : most_inter_quest['precedence'],
            "repetitions" : most_inter_quest['repetitions'],
            "header" : most_inter_quest['header'],
            "body" : new_body,
            #"solution" : most_inter_quest['solution'],
            "source" : most_inter_quest['source'],
            "notes" : most_inter_quest['notes'],
            "status" : most_inter_quest['status'],
            "inserted_by" : '',
            "inserted_at" : '',
            "validated_by" : '',
            "validated_at" : '',
        }

    '''
        Represents the beginning of the system's reasoning based on cases and is represented by two large processes: an 
        initial collection of cases (multiple choice questions) and the selection, among these, of the most “suitable” to 
        support the formation of a new multiple choice question
    '''
    def retrieve(self):
        print('retrieveGEN')
        filter_object = {
            #"study_cycle": self.working_memory['study_cycle'],
           # "scholarity": self.working_memory['scholarity'],
            "domain": self.working_memory['domain'],
            "subdomain": self.working_memory['subdomain'],
            "difficulty_level": self.working_memory['difficulty_level']
        }
        print('filter_object')
        print(filter_object)
        q1 = mongo.db.question.find(filter_object)
        q2 = mongo.db.profiles.find_one( { "username" : self.working_memory['username'] }, { "_id": 0, "session_questions_ids": 1 } )

        answered_questions = [ qid for qid in q2['session_questions_ids'] ]

        self.working_memory['retrieved_questions'] = []
        for q in q1:
            if q['_id'] in answered_questions:
                self.working_memory['retrieved_questions'].append(q)

        self.question_selection()

    '''
        It represents the formation of the new question, which consists of modifying some of the attributes of the most 
        interesting question (represented by the most_interesting_question attribute of working memory), of which the header 
        and body stand out
    '''
    def reuse(self):
        print('REUSE')
        self.edit_question_header()

        self.working_memory['correct_answers'] = []

        for opt in self.working_memory['most_interesting_question']['body']:
            if(opt['correction'] == '1'):
                self.working_memory['correct_answers'].append(opt['answer'])

        all_answers = []
        for q in self.working_memory['retrieved_questions']:
            for ans in q['body']:
                if( ans['correction'] == '0' ):
                    all_answers.append(ans['answer'])

        sorted_answers = self.get_similarities(all_answers)

        self.form_question(sorted_answers)

    '''
        The elements of the new question are analyzed, mainly the ones that can introduce information redundancy
        in Leonardo's database or inconsistencies in the presentation of the question in the system interface. These elements are the id and the body
    '''
    def revise(self):
        data = mongo.db.question.find({}, { "_id": 1 })

        for q in data:
            if( q['_id'] == self.working_memory['new_question']['_id'] ):
                id_from_most_inter_quest = self.working_memory['most_interesting_question']['_id']
                fst_part = id_from_most_inter_quest[ : len( id_from_most_inter_quest ) - 3]

                regex = fst_part + ".*"

                query = mongo.db.question.count_documents( { "_id" : { "$regex" : regex } } )

                snd_part = "0" + str(query + 1) if(query < 100) else str(query + 1)
                
                self.working_memory['new_question']['_id'] = fst_part + snd_part

        body = self.working_memory['new_question']['body']
        for a in body:
            a['correction']  = '0' if ( ( a['correction'] != '0' ) and ( a['correction'] != '1' ) ) else a['correction']
            a['mandatory']   = '0' if ( ( a['mandatory'] != '0' ) and ( a['mandatory'] != '1' ) ) else a['mandatory']
            a['eliminative'] = '0' if ( ( a['eliminative'] != '0' ) and ( a['eliminative'] != '1' ) ) else a['eliminative']
            a['points']      = '0' if ( ( a['points'] != '0' ) and ( a['points'] != '1' ) ) else a['points']

            if( ( a['answer'] in self.working_memory['correct_answers'] ) and ( a['correction'] != '1') ):
                self.working_memory['new_question']['body'].remove(a)

            found_element = next((a for a in body if a['answer'] == "Nenhuma das anteriores."), None)

            if( found_element != None ):
                body.remove(found_element)
                body.insert(len(body), found_element)

        self.working_memory['new_question']['body'] = body

    '''
        It represents the persistence of the new question in Leonardo's database. The new question, which is represented by 
        the 'new_question' attribute of the working memory, is placed along with the other questions in the questions 
        collection. This action is performed by executing a MongoDB query
    '''
    def retain(self):
        insertion_data = str( datetime.now() )
        self.working_memory['new_question']['inserted_at'] = insertion_data.split(' ')[0]
        #Alterado
        #Faz sentido?
        print('A inserir nova questao')
        print(self.working_memory['new_question'] )
        #mongo.db.question.insert( self.working_memory['new_question'] )

        print("\nWorking_memory:", self.working_memory, "\n")

        mongo.db.generated_questions.insert({
            'id': self.working_memory['new_question']['_id'],
            'date': insertion_data
        })