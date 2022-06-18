from flask_wtf          import FlaskForm, validators
from wtforms            import StringField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, AnyOf
from flask_babel        import lazy_gettext as _l

class LoginForm(FlaskForm):
    usr_msg     = _l('Nome de utilizador obrigatório')
    pwd_msg     = _l('Palavra-passe obrigatória')
    username    = StringField(_l('Nome de utilizador'), validators=[DataRequired(usr_msg)], id='username_login')
    password    = PasswordField(_l('Palavra-passe'), validators=[DataRequired(pwd_msg)], id='pwd_login')
    remember_me = BooleanField(id='remember_me_login')

class CreateAccountForm(FlaskForm):
    email_msg     = _l('Endereço de email do novo utilizador necessário')
    usr_msg       = _l('Defina o nome de utilizador da conta a ser criada')
    name_msg      = _l('Indique o nome do novo utilizador')
    user_type_msg = _l('Selecione um grau de acesso')
    gender_msg    = _l('Selecione um género')
    degree_msg    = _l('Indique um curso')
    email         = StringField(_l('Endereço de email'), validators=[DataRequired(email_msg), Email(email_msg)], id='email_create') # Institutional email
    username      = StringField(_l('Nome de utilizador'), validators=[DataRequired(usr_msg)], id='username_create') # Institution's number id
    name          = StringField(_l('Nome (primeiro e último)'), validators=[DataRequired(name_msg)], id='name_create') # User's name
    degree        = StringField(_l('Curso do utilizador'), validators=[DataRequired(degree_msg)], id='degree_create')
    genderValues  = ['F','M']
    gender        = SelectField(
        choices=[('G', _l('-- Género --')), ('F', _l('Feminino')), ('M', _l('Masculino'))],
        coerce=str,
        validators=[AnyOf(genderValues, gender_msg)],
        id='gender_create',
        description=_l('Género do utilizador.')
    )
    values        = [1, 2, 3, 4]
    user_type     = SelectField(
        choices=[(0, _l('-- Escolha um grau de acesso --')), (4, _l('Estudante')), (3, _l('Operador')), (2, _l('Responsável')), (1, _l('Administrador'))],
        coerce=int,
        validators=[AnyOf(values, user_type_msg)],
        id='user_type_create',
        description=_l('O grau de acesso define os privilégios do utilizador.')
    )