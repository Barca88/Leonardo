
from flask                                                  import Blueprint
from flask_restful                                          import Api
from ..evaluation.resources.create_test                     import CreateTest
from ..evaluation.resources.preview_test                    import PreviewTest
from ..evaluation.resources.get_domains                     import GetDomains
from ..evaluation.resources.get_statistics                  import GetStatistics
from ..evaluation.resources.new_evaluation                  import NewEvaluation
from ..evaluation.resources.next_question                   import NextQuestion
from ..evaluation.resources.get_gamification_users          import GetUsers
from ..evaluation.resources.post_gamification_users         import PostUsers
from ..evaluation.resources.get_gamification_domains        import GetDoms
from ..evaluation.resources.get_quizz_monitor_parameters    import GetQuizzParameters
from ..evaluation.resources.get_button_info                 import GetButtonInfo
from ..evaluation.resources.rules                           import Rules
from ..evaluation.resources.rule                            import Rule
from ..accounts.resources.upload_avatar                     import UploadAvatar
from ..accounts.resources.change_password                   import ChangePassword
from ..students.resources.list                              import List
from ..questions.resources.domains_map                      import DomainsMap
from ..questions.resources.get_domains_by_charge            import GetDomainsByCharge
from ..questions.resources.get_subdomains_by_charge         import GetSubdomainsByCharge
from ..inquiries.resources.answers                          import Answers
from ..inquiries.resources.inquiry                          import Inquiry

blueprint    = Blueprint(
    'api_blueprint',
    __name__,
    url_prefix='/api/v0'
)
internal_api = Api(blueprint)

# ========== EVALUATION ==========
internal_api.add_resource(CreateTest         , '/evaluation/create_test')
internal_api.add_resource(PreviewTest        , '/evaluation/preview_test/<int:test_id>')
internal_api.add_resource(GetDomains         , '/evaluation/getDomains')
internal_api.add_resource(GetStatistics      , '/evaluation/getStatistics')
internal_api.add_resource(NewEvaluation      , '/evaluation/new')
internal_api.add_resource(NextQuestion       , '/evaluation/next')
internal_api.add_resource(GetQuizzParameters , '/evaluation/quizzParameters')
internal_api.add_resource(GetButtonInfo      , '/evaluation/getButtonInfo')
internal_api.add_resource(Rules              , '/evaluation/rules')
internal_api.add_resource(Rule               , '/evaluation/rules/<int:rule_id>')

# =========== ACCOUNTS ===========
internal_api.add_resource(UploadAvatar  , '/accounts/avatar/upload')
internal_api.add_resource(ChangePassword, '/accounts/password/change')

# =========== STUDENTS ===========
internal_api.add_resource(List, '/students/list')

# =========== QUESTIONS ==========
internal_api.add_resource(DomainsMap, '/questions/domains_map')
internal_api.add_resource(GetDomainsByCharge, '/questions/getDomainsByCharge')
internal_api.add_resource(GetSubdomainsByCharge, '/questions/getSubdomainsByCharge')

# =========== INQUIRIES =========
internal_api.add_resource(Answers,'/inquiries/inquiry_answers')
internal_api.add_resource(Inquiry,'/inquiries/inquiry')

# =========== GAMIFICATION =========
internal_api.add_resource(GetUsers,'/gamification/get_users')
internal_api.add_resource(GetDoms,'/gamification/get_doms')
internal_api.add_resource(PostUsers,'/gamification/post_users')

