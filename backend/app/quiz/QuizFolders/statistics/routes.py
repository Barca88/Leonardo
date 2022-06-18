from flask import Blueprint, render_template
from flask_login import login_required
from app import mongoDW
from .resources import Dash_answers, Dash_users, Dash_home, Dash_system

blueprint = Blueprint(
    'statistics_blueprint',
    __name__,
    url_prefix='/statistics',
    template_folder='templates',
    static_folder='static'
)

@blueprint.route('/analitics/users_old')
@login_required
def analitics_select_users():
    user_list = mongoDW.db.dm_answers.distinct("Dim_User.Name")
    return render_template('select_user.html',users=user_list)

@blueprint.route('/analitics/users_old/<id>')
@login_required
def analitics_users(id):
    domains_list = mongoDW.db.dm_answers.distinct("Dim_Question.Domain")
    user = mongoDW.db.dm_answers.find_one({"Dim_User.Name":id})
    return render_template('dm_user.html',user=user, domains=domains_list)

@blueprint.route('/analitics')
@login_required
def analitics():
    return render_template('dash.html', dash_url = Dash_home.url_base, styleF='width: 100%; height: 1700px;')


@blueprint.route('/analitics/answers')
@login_required
def analitics_dm_answers():
    return render_template('dash.html', dash_url = Dash_answers.url_base, styleF='width: 100%; height: 2300px;')

@blueprint.route('/analitics/users')
@login_required
def analitics_user(): 
    return render_template('dash.html', dash_url = Dash_users.url_base, styleF='width: 100%; height: 2750px;')

@blueprint.route('/analitics/system')
@login_required
def analitics_system(): 
    return render_template('dash.html', dash_url = Dash_system.url_base, styleF='width: 100%; height: 2400px;')

@blueprint.route('/analitics/old') 
@login_required
def analitics_answers():
    domains_list = mongoDW.db.dm_answers.distinct("Dim_Question.Domain")
    #return render_template('dm_answers.html',domains=domains_list,dash_url = Dash_answers.url_base)
    return render_template('charts.html')

@blueprint.route('/<template>')
@login_required
def route_template(template):
    return render_template(template + '.html')
