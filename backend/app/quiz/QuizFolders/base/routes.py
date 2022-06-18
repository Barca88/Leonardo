from flask             import Blueprint, render_template, redirect, request, url_for
from flask_api         import status
from flask_login       import current_user, login_required
from ..accounts.routes import sign_in
from .enums.user_type  import UserType
from .user             import User

blueprint = Blueprint(
    'base_blueprint',
    __name__,
    url_prefix='',
    template_folder='templates',
    static_folder='static'
)

@blueprint.route('/', methods=['GET', 'POST'])
def route_default():
    if request.method == 'GET' and current_user.is_authenticated:
        # TODO: check user's homepage and redirect to it
        return redirect(url_for('base_blueprint.home'))

    sign_in_data = sign_in()
    error_code   = sign_in_data['error']

    if request.method == 'POST' and error_code == -1:
        return redirect(url_for('base_blueprint.home'))

    if request.method == 'POST' and error_code == 0:
        return render_template(
        'login.html',
        login_form=sign_in_data['form'],
        error=error_code), status.HTTP_403_FORBIDDEN

    return render_template(
        'login.html',
        login_form=sign_in_data['form'],
        error=error_code)

@blueprint.route('/home', methods=['GET'])
@login_required
def home():
    if current_user.user_type is UserType.STUDENT.value:
        return redirect(url_for('evaluation_blueprint.index'))
    else:
        return redirect(url_for('statistics_blueprint.analitics'))

@blueprint.route('/<template>')
@login_required
def route_template(template):
    return render_template(template + '.html')

@blueprint.route('/fixed_<template>')
@login_required
def route_fixed_template(template):
    return render_template('fixed/fixed_{}.html'.format(template))

@blueprint.route('/page_<error>')
def route_errors(error):
    return render_template('errors/page_{}.html'.format(error))

@blueprint.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

## Errors

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/page_403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errors/page_404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errors/page_500.html'), 500
