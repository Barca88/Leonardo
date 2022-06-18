from flask                  import Blueprint, render_template
from flask_login            import login_required, current_user
from flask_restful          import reqparse
from flask                  import request
import requests
import json
from app                    import mongo
from ..base.enums.user_type import UserType

blueprint = Blueprint(
    'evaluation_blueprint',
    __name__,
    url_prefix='/evaluation',
    template_folder='templates',
    static_folder='static'
)

@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def index():
    pipeline     = [
        { '$match': { 'id': current_user.id } },
        { '$project': { 'domains': 1, '_id': 0 } },
        { '$unwind': '$domains' },
        { '$group': {
            '_id': {
                'study_cycle': '$domains.study_cycle',
                'scholarity' : '$domains.scholarity'
            },
            'domains': { '$push': '$domains' }
        } }
    ]
    user_domains = mongo.db.users.aggregate(pipeline)

    if current_user.user_type is UserType.STUDENT.value:
        return render_template('studying.html', domains=user_domains)
    else:
        user_tests = mongo.db.tests.find({ 'user_id': current_user.id })

        return render_template(
            'tests.html',
            tests=user_tests,
            domains=user_domains)

@blueprint.route('/<template>')
@login_required
def route_template(template):
    return render_template(template + '.html')