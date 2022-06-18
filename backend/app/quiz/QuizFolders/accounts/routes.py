from flask                 import Blueprint, render_template, redirect, request, url_for, session, request
from flask_login           import current_user, login_required, login_user, logout_user
from werkzeug.security    import check_password_hash, generate_password_hash
from app                   import mongo, login_manager
from .forms                import LoginForm, CreateAccountForm
from datetime              import datetime
from string                import digits, ascii_uppercase, ascii_lowercase
from random                import randint, choice
from smtplib               import SMTP_SSL

blueprint = Blueprint(
    'accounts_blueprint',
    __name__,
    url_prefix='',
    template_folder='templates',
    static_folder='static'
)

@blueprint.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    login_form = LoginForm(request.form)
    error_code = -1

    if request.method == 'POST' and login_form.validate_on_submit():
        if current_user.is_anonymous:
            error_code = 0
        elif check_password_hash(current_user.password, login_form.password.data):
            login_user(current_user, remember=login_form.remember_me.data)
            session.permanent = True
        else:
            error_code = 1

    return dict(form=login_form, error=error_code)

@blueprint.route('/sign_out')
@login_required
def sign_out():
    logout_user()
    return redirect(url_for('base_blueprint.route_default'))

@blueprint.route('/sign_up', methods=['GET', 'POST'])
@login_required
def sign_up():
    create_account_form = CreateAccountForm(request.form)
    error_code          = -1

    if request.method == 'POST':
        error_code = 2

        if create_account_form.validate_on_submit():
            username      = create_account_form.username.data
            username_used = mongo.db.users.find_one({'username': username})

            if username_used is None:
                if mongo.db.users.find_one() is None:
                    user_id = 1
                else:
                    last_user = mongo.db.users.find_one(sort = [('id', -1)])
                    user_id   = str(int(last_user['id']) + 1)

                error_code = 0
                email      = create_account_form.email.data
                name       = create_account_form.name.data
                gender     = create_account_form.gender.data
                degree     = create_account_form.degree.data
                user_type  = create_account_form.user_type.data
                password   = generate_password_hash(random_password(8, 10))
                user       = {
                    'id'         : user_id,
                    'username'   : username,
                    'password'   : password,
                    'name'       : name,
                    'email'      : email,
                    'inserted_at': datetime.now().isoformat(timespec='seconds')+'Z',
                    'inserted_by': current_user.username,
                    'user_type'  : user_type,
                    'gender'     : gender,
                    'degree'     : degree
                }
                mongo.db.users.insert(user)
                #send_email(email, username, password)
            else:
                error_code = 1

    return dict(form=create_account_form, error=error_code)

@blueprint.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html')

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('errors/page_403.html'), 403

def random_password(size_min, size_max):
    chars = ascii_uppercase + ascii_lowercase + digits
    size  = randint(size_min, size_max)

    return ''.join(choice(chars) for x in range(size))

def send_email(receiver, username, password):
    sender  = "leo.di.teste@gmail.com"
    server  = SMTP_SSL('smtp.gmail.com', 465)
    subject = 'Welcome to LEONARDO!'
    body    = "Hey, what\'s up?\n\nWelcome to Leonardo!\n\nYour username is: " + username + "\nAnd your password is: " + password + " (You can change it at any time!)\n\n- LEONARDO"
    message = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sender, receiver, subject, body)

    server.login(sender, "leozinho")
    server.sendmail("leo.di.teste@gmail.com", receiver, message)
