from flask import Flask, json
from flasgger import Swagger
import settings
from routes.index import index_api
from routes.tests import tests_api
from routes.generator import generator_api
from routes.config import config_api
from routes.evaluation import evaluation_api
from routes.stats import stats_api
from werkzeug.exceptions import HTTPException
from flask_cors import CORS


def create_app():

    app = Flask(
        __name__,
        static_url_path='',
        static_folder='static'
    )
    app.config['SWAGGER'] = {
        'title': settings.SWAGGER_DOCS_TITLE
    }
    app.config["CACHE_TYPE"] = "null"
    swagger = Swagger(app)
    return app, swagger


app, swagger = create_app()
CORS(app)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.after_request
def after_request(response):
    if settings.FLASK_DEBUG:
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Expires"] = '0'
        response.headers["Pragma"] = "no-cache"
    return response


app.register_blueprint(index_api, url_prefix='/')
app.register_blueprint(tests_api, url_prefix='/tests')
app.register_blueprint(generator_api, url_prefix='/generator')
app.register_blueprint(config_api, url_prefix='/config')
app.register_blueprint(evaluation_api, url_prefix="/evaluation")
app.register_blueprint(stats_api, url_prefix="/stats")

app.run(debug=settings.FLASK_DEBUG, port=settings.FLASK_PORT)
