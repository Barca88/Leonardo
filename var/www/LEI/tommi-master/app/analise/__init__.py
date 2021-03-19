from flask import Blueprint

blueprint = Blueprint(
    'api_blueprint',
    __name__,
    url_prefix='/analise',
    template_folder='templates',
    static_folder='static'
)
