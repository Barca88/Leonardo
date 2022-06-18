from flask import Blueprint, render_template
from flask_login import login_required
from .resources import Dash_App2, OpinionsDate

blueprint = Blueprint(
    'inquiries_blueprint',
    __name__,
    url_prefix='/inquiries',
    template_folder='templates',
    static_folder='static'
)

@blueprint.route('/analitics/opinions')
@login_required
def analitics_opinions():
    return render_template('opinions.html',dash_url = Dash_App2.url_base)

@blueprint.route('/analitics/opinionsDate')
@login_required
def analitics_opinions_data():
    return render_template('opinionsDate.html',dash_url = OpinionsDate.url_base)
