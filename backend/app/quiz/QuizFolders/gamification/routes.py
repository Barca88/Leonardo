from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound

blueprint = Blueprint(
    'gamification_blueprint',
    __name__,
    url_prefix='/gamification',
    template_folder='templates',
    static_folder='static'
)


@blueprint.route('/index')
@login_required
def get_sample():
    return render_template('index.html')

@blueprint.route('/<template>')
def route_template(template):
    return render_template(template + '.html')

