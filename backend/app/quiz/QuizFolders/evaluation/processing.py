from flask.globals import current_app
from app            import mongo
from .profiler      import Profiler
from .evaluator     import Evaluator
from datetime       import datetime
import random

class Processing:
    '''
        Initialization of the most relevant variables for the reasoning process, specifically the working memory
    '''
    def __init__(self, current_user, domain):
        data = mongo.db.profiles.find_one({ 'username': current_user['username'] })

        self.working_memory = {
            'user_profile_info': data,
            'current_user': current_user,
            'domain': domain['_id'],
            'rules_under_domain': [],
            'conflict_set': [],
            'rule_to_fire': {},
            'fired_rules_id': []
        }

        self.update_properties()

    '''
        Getting rules to support the entire subsequent reasoning process
    '''
    def get_rules(self):
        data = mongo.db.rules.find({ "domain" : self.working_memory['domain']
                                   })

        self.working_memory['rules_under_domain'] = []
        for rule in data:
            self.working_memory['rules_under_domain'].append(rule)

    '''
        Check whether the post-conditions of the rules keep the values ​​of the variables within the limits established for them
    '''
    def control_properties_ranges(self, rule):
        then_clause = rule['then_clauses'][0]

        between_one_and_five            = [ "user_level", "user_performance", "user_skill" ]
        between_zero_and_hundred        = [ "total_right_questions", "total_wrong_questions", "hit_rate", "error_rate" ]
        between_zero_and_ten            = [ "total_right_followed_questions", "total_wrong_followed_questions" ]
        between_zero_and_ninety         = [ "answering_time" ]
        between_zero_and_hundred_eighty = [ "usage_time" ]
        between_zero_and_two_hundred    = [ "total_questions" ]

        if(then_clause['action'] == "decrementar"):
            if( ( then_clause['property'] == "total_wrong_questions" or then_clause['property'] == "hit_rate" or then_clause['property'] == "error_rate" ) ):
                if( ( self.working_memory[then_clause['property']]['before_rule_execution'] > 0 ) ):
                    return 1
                else:
                    return 0
            else:
                value = self.working_memory[then_clause['property']]

                if(
                    ( ( then_clause['property'] in between_one_and_five ) and ( value > 1) ) or 
                    ( ( then_clause['property'] in between_zero_and_hundred ) and ( value > 0) ) or 
                    ( ( then_clause['property'] in between_zero_and_ten ) and ( value > 0) ) or 
                    ( ( then_clause['property'] in between_zero_and_ninety ) and ( value > 0) ) or 
                    ( ( then_clause['property'] in between_zero_and_hundred_eighty ) and ( value > 0) ) or 
                    ( ( then_clause['property'] in between_zero_and_two_hundred ) and ( value > 0) )
                ):
                    return 1
                else:
                    return 0
        else:
            if( ( then_clause['property'] == "total_wrong_questions" or then_clause['property'] == "hit_rate" or then_clause['property'] == "error_rate" ) ):
                if( ( self.working_memory[then_clause['property']]['before_rule_execution'] < 100 ) ):
                    return 1
                else:
                    return 0
            else:
                value = self.working_memory[then_clause['property']]

                if(
                    ( ( then_clause['property'] in between_one_and_five ) and ( value < 5) ) or 
                    ( ( then_clause['property'] in between_zero_and_hundred ) and ( value < 100) ) or 
                    ( ( then_clause['property'] in between_zero_and_ten ) and ( value < 10) ) or 
                    ( ( then_clause['property'] in between_zero_and_ninety ) and ( value < 90) ) or 
                    ( ( then_clause['property'] in between_zero_and_hundred_eighty ) and ( value < 180) ) or 
                    ( ( then_clause['property'] in between_zero_and_two_hundred ) and ( value < 200) )
                ):
                    return 1
                else:
                    return 0

    '''
        Calculates the logic value of a pre-condition (if clause)
    '''
    def calculate_logic_value(self, pre_condition):
        value_to_compare = ''

        if( 
            ( pre_condition['property'] == 'total_wrong_questions' ) or
            ( pre_condition['property'] == 'hit_rate' ) or
            ( pre_condition['property'] == 'error_rate' )
        ):
            value_to_compare = self.working_memory[pre_condition['property']]['before_rule_execution']
        else:
            value_to_compare = self.working_memory[pre_condition['property']]

        if (
            ( ( pre_condition['operator'] == '=' ) and ( value_to_compare == float( pre_condition['value'] ) ) ) or
            ( ( pre_condition['operator'] == '>' ) and ( value_to_compare > float( pre_condition['value'] ) ) ) or
            ( ( pre_condition['operator'] == '<' ) and ( value_to_compare < float( pre_condition['value'] ) ) ) or
            ( ( pre_condition['operator'] == '<>' ) and ( value_to_compare != float( pre_condition['value'] ) ) ) or
            ( ( pre_condition['operator'] == '>=' ) and ( value_to_compare >= float( pre_condition['value'] ) ) ) or
            ( ( pre_condition['operator'] == '<=' ) and ( value_to_compare <= float( pre_condition['value'] ) ) )
        ):
            return 1
        else:
            return 0

    '''
        Decides if a rule should be added to the conflict set
            - return 0 if a rule shouldn't go to conflit set (it means that the logical value of the left side of the rule was not satisfied)
            - return 1 if a rule should go to conflit set (it means that the logical value of the left side of the rule was satisfied)
    '''
    def rule_into_conflit_set(self, rule):
        flag = self.control_properties_ranges(rule)

        if flag == 0:
            return 0
        else:
            rule_if_clauses = rule['if_clauses']

            i = 0
            logic_value = 0
            for r in rule_if_clauses:
                if( (i + 1) >= len(rule_if_clauses) ):
                    break
                elif(i == 0):
                    if(r['condition'] == 'e'):
                        if( ( self.calculate_logic_value(r) == 0 ) or ( self.calculate_logic_value(rule_if_clauses[i+1]) == 0 ) ):
                            logic_value = 0
                        else:
                            logic_value = 1
                    elif(r['condition'] == 'ou'):
                        if( ( self.calculate_logic_value(r) == 1 ) or ( self.calculate_logic_value(rule_if_clauses[i+1]) == 1 ) ):
                            logic_value = 1
                        else:
                            logic_value = 0
                else:
                    if(r['condition'] == 'e'):
                        if( (logic_value == 0) or ( self.calculate_logic_value(rule_if_clauses[i+1]) == 0 ) ):
                            logic_value = 0
                        else:
                            logic_value = 1
                    elif(r['condition'] == 'ou'):
                        if( (logic_value == 1) or ( self.calculate_logic_value(rule_if_clauses[i+1]) == 1 ) ):
                            logic_value = 1
                        else:
                            logic_value = 0
                
                i += 1

            return logic_value

    '''
        Choose the most suitable rule to execute
    '''
    def choose_rule_to_fire(self):
        self.working_memory['rule_to_fire'] = {}

        # >number_of_preconditions => more specific rule => more probability of that rule to be selected
        number_of_preconditions = 0

        keep_most_interesting_rules = []

        for c in self.working_memory['conflict_set']:
            #checks if rules were not fired yet
            if( not c['id'] in self.working_memory['fired_rules_id'] ):
                if( (len(c['if_clauses']) > number_of_preconditions) and (number_of_preconditions >= 0) ):
                    self.working_memory['rule_to_fire'] = c
                    number_of_preconditions = len(c['if_clauses'])
                    keep_most_interesting_rules = []
                elif( (len(c['if_clauses']) == number_of_preconditions) and (number_of_preconditions > 0) ):
                    if( (len(self.working_memory['rule_to_fire']) > 0 ) ):
                        keep_most_interesting_rules.append(self.working_memory['rule_to_fire'])
                        self.working_memory['rule_to_fire'] = {}
                    keep_most_interesting_rules.append(c)

        if( len(self.working_memory['rule_to_fire']) > 0 ):
            self.working_memory['fired_rules_id'].append(self.working_memory['rule_to_fire']['id'])
        elif( len(keep_most_interesting_rules) > 0 ):
            choosen_rule = random.choice(keep_most_interesting_rules)

            self.working_memory['fired_rules_id'].append(choosen_rule['id'])
        else:
            self.working_memory['rule_to_fire'] = {}

    '''
        'Transformation' of the user profile to a pattern
    '''
    def get_user_profile(self, domain, current_user):
        domain_profile = Profiler.get_pattern(current_user, domain, edited_user_profile=self.working_memory['user_profile_info'])

        if domain_profile:
            subdomains_profile = Profiler.get_decision_pattern(current_user, domain, edited_user_profile=self.working_memory['user_profile_info'])

            return { 'domain': domain_profile, 'subdomains': subdomains_profile }

    '''
        Updates working memory properties in one of two situations:
            - at the beginning of the reasoning process, where the user's working memory profile comes from Leonardo's database;
            - after the user's working memory profile is properly updated with the execution of a rule
    '''
    def update_properties(self):
        for element in self.working_memory['user_profile_info']['profile']:
            
            if(  element['domain']== self.working_memory['domain'] ):
                self.working_memory['user_level'] = element['user_level']
                #ALTERAR O VALOR DA PERFORMANCE
                self.working_memory['user_performance'] = round( self.working_memory['user_profile_info']['performance'] )
                self.working_memory['user_skill'] = round( element['skill'] )
                self.working_memory['total_questions'] = element['total']
                self.working_memory['total_right_questions'] = element['hitted']
                self.working_memory['total_wrong_questions'] = {
                    'before_rule_execution': element['total'] - element['hitted'],
                    'after_rule_execution': -1
                }
                self.working_memory['hit_rate'] = {
                    'before_rule_execution': round( ( element['hitted'] / element['total'] ) * 100 ),
                    'after_rule_execution': -1
                }
                self.working_memory['error_rate'] = {
                    'before_rule_execution': round( ( ( element['total'] - element['hitted'] ) / element['total'] ) * 100 ),
                    'after_rule_execution': -1
                }
                #ALTERAR O VALOR DO USAGE_TIME
                self.working_memory['usage_time'] = round( element['answers_time'] )
                self.working_memory['answering_time'] = round( element['answers_time'] )
                self.working_memory['total_right_followed_questions'] = element['rbacklog']
                self.working_memory['total_wrong_followed_questions'] = element['wbacklog']

                break

    '''
        Updates the user's working memory profile after a rule is executed
    '''
    def update_user_profile(self):
        for element in self.working_memory['user_profile_info']['profile']:
            if( element['domain'] == self.working_memory['domain'] ):
                element['user_level'] = self.working_memory['user_level']
                element['user_skill'] = self.working_memory['user_skill']
                element['_total'] = self.working_memory['total_questions']
                element['total'] = self.working_memory['total_questions']
                element['_hitted'] = self.working_memory['total_right_questions']
                element['hitted'] = self.working_memory['total_right_questions']
                element['rbacklog'] = self.working_memory['total_right_followed_questions']
                element['wbacklog'] = self.working_memory['total_wrong_followed_questions']
                element['answers_time'] = self.working_memory['answering_time']

                #VER O QUE FAZER QUANDO EXISTE UM NOVO VALOR PARA A 'PERFORMANCE'
                #VER O QUE FAZER QUANDO EXISTE UM NOVO VALOR PARA O 'USAGE_TIME'
                
                hit_rate_bef_exec = self.working_memory['hit_rate']['before_rule_execution']
                aux_value1 = self.working_memory['hit_rate']['after_rule_execution']
                hit_rate_aft_exec = aux_value1 if ( aux_value1 > 0 ) else hit_rate_bef_exec

                tot_rig_quest = self.working_memory['total_right_questions']

                tot_wro_quest_bef_exec = self.working_memory['total_wrong_questions']['before_rule_execution']
                aux_value2 = self.working_memory['total_wrong_questions']['after_rule_execution']
                tot_wro_quest_aft_exec = aux_value2 if ( aux_value2 > 0 ) else tot_wro_quest_bef_exec

                err_rate_bef_exec = self.working_memory['error_rate']['before_rule_execution']
                aux_value3 = self.working_memory['error_rate']['after_rule_execution']
                err_rate_aft_exec = aux_value3 if ( aux_value3 > 0 ) else err_rate_bef_exec

                if( ( hit_rate_bef_exec < hit_rate_aft_exec ) or ( err_rate_bef_exec > err_rate_aft_exec ) or ( tot_wro_quest_bef_exec > tot_wro_quest_aft_exec ) ):
                    element['_hitted'] = tot_rig_quest + 1
                    element['hitted'] = tot_rig_quest + 1
                if( ( hit_rate_bef_exec > hit_rate_aft_exec ) or ( err_rate_bef_exec < err_rate_aft_exec ) or ( tot_wro_quest_bef_exec < tot_wro_quest_aft_exec ) ):
                    element['_hitted'] = tot_rig_quest - 1
                    element['hitted'] = tot_rig_quest - 1
                
                break

    '''
        Execute a rule, i.e, update the values in working memory and insert a log document in the rules_logs collection
    '''
    def execute_rule(self):
        rule_to_fire = self.working_memory['rule_to_fire']
        if( len(rule_to_fire) > 0 ):
            then_clause = rule_to_fire['then_clauses'][0]

            if( then_clause['action'] == "decrementar" ):
                if( 
                    then_clause['property'] == "total_wrong_questions" or
                    then_clause['property'] == "hit_rate" or
                    then_clause['property'] == "error_rate"
                ):
                    self.working_memory[then_clause['property']]['after_rule_execution'] = self.working_memory[then_clause['property']]['before_rule_execution'] - 1
                else:
                    self.working_memory[then_clause['property']] = self.working_memory[then_clause['property']] - 1
            else:
                if( 
                    then_clause['property'] == "total_wrong_questions" or
                    then_clause['property'] == "hit_rate" or
                    then_clause['property'] == "error_rate"
                ):
                    self.working_memory[then_clause['property']]['after_rule_execution'] = self.working_memory[then_clause['property']]['before_rule_execution'] + 1
                else:
                    self.working_memory[then_clause['property']] = self.working_memory[then_clause['property']] + 1

            mongo.db.rules_logs.insert({
                "rule_id": self.working_memory['rule_to_fire']['id'],
                "domain": self.working_memory['domain'],
                "username": self.working_memory['current_user']['username'],
                "date": str( datetime.now() )
            })

            self.update_user_profile()

    '''
        This method analyzes whether the initially launched question is valid, that is, it corresponds to the new 
        working memory parameters
    '''
    def validate_question(self, current_user, domain, sub_domain, thrown_question_info):
        new_user_profile_as_patterns = self.get_user_profile(domain, current_user)
        questions_related_to_new_user_profile = Evaluator.throw_question(new_user_profile_as_patterns, domain, sub_domain, block_question_generation="block_question_generation", username=current_user['username'])

        #IN THIS CASE, QUESTION IS VALID
        print(eval( questions_related_to_new_user_profile ))
        if (
            ( eval( questions_related_to_new_user_profile )['content']['_id'] == eval( thrown_question_info )['content']['_id'] ) or
            ( ( any( q['_id'] == eval( thrown_question_info )['content']['_id'] for q in eval( questions_related_to_new_user_profile )['choosable_questions'] ) ) == True )
        ):
            return { 'status': 'validated' }
        #GET ANOTHER QUESTION
        else:
            new_question = {}
            
            choosen_question = eval( thrown_question_info )['content']

            list_of_choosable_questions = eval( thrown_question_info )['choosable_questions']

            for q in list_of_choosable_questions:
                if any( ( quest['_id'] == q['_id'] ) and ( q['_id'] != choosen_question['_id'] ) for quest in eval( questions_related_to_new_user_profile )['choosable_questions'] ) == True:
                    new_question = q
            if( new_question != {} ):
                return new_question
            else:
                return {}

    '''
        Main method, following the 'execute_rule_based_system' method of 'rule_based_system.py'.
        After the first filtering of rules, this method covers all steps related to:
            - selection of a rule to fire
            - execution of a rule
            - update of working memory properties
    '''
    def control_center(self):
        self.working_memory['rule_to_fire'] = {}

        i = 0
        while( not ( ( len ( self.working_memory['rule_to_fire'] ) == 0 ) and ( i > 0 ) ) ):
            self.working_memory['conflict_set'] = []

            for b in self.working_memory['rules_under_domain']:
                logic_value = self.rule_into_conflit_set(b)

                if(logic_value == 1):
                    self.working_memory['conflict_set'].append(b)

            self.choose_rule_to_fire()
            self.execute_rule()
            self.update_properties()

            i += 1