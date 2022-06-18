from .processing    import Processing

class RuleBasedSystem:
    '''
        'Main' of rule based mechanism
    '''
    @classmethod
    def execute_rule_based_system(cls, current_user, domain, sub_domain, thrown_question_info):
        val = Processing(current_user, domain)
        val.get_rules()
        val.control_center()

        result = val.validate_question(current_user, domain, sub_domain, thrown_question_info)

        return result