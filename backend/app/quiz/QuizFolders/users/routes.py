from flask             import Blueprint, render_template
from flask_login       import login_required, current_user
from app               import mongo, mongoDW
from ..accounts.routes import sign_up
from flask_api         import status

blueprint = Blueprint(
    'users_blueprint',
    __name__,
    url_prefix='/users',
    template_folder='templates',
    static_folder='static'
)

@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def list():
    users_sorted        = mongo.db.users.find(sort = [('user_type', 1)])
    users_grouped       = {}
    current_user_type   = ''
    create_account_form = None
    error_code          = -1

    for user in users_sorted:
        if user['user_type'] != current_user_type:
            current_user_type                = user['user_type']
            users_grouped[current_user_type] = []

        users_grouped[current_user_type].append(user)

    if current_user.user_type == 1:
        sign_up_data        = sign_up()
        create_account_form = sign_up_data['form']
        error_code          = sign_up_data['error']

    if(error_code!=0):
        return render_template(
        'users_list.html',
        dict=users_grouped,
        create_form=create_account_form,
        error=error_code), status.HTTP_400_BAD_REQUEST
    print(users_grouped)
    return render_template(
        'users_list.html',
        dict=users_grouped,
        create_form=create_account_form,
        error=error_code)

@blueprint.route('/<template>')
@login_required
def route_template(template):
    return render_template(template + '.html')
