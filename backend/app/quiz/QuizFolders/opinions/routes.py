from flask import Blueprint, render_template
from flask_login   import current_user
from flask_login import login_required
from . import opinion_dash_app

blueprint = Blueprint(
    'opinions_blueprint',
    __name__,
    url_prefix='/opinions',
    template_folder='templates',
    static_folder='static'
)

@blueprint.route('/dashboard')
@login_required
def dashboard():
    return render_template('opinion_dashboard.html', dash_url = opinion_dash_app.url_base)