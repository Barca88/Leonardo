import json

from flask import request, Blueprint

from app.voice.action_manager.action_manager import ActionManager
from app.voice.speech.speech_recognizer import parse_file_input

action_manager: ActionManager = ActionManager()

blueprint = Blueprint(
    'voice_blueprint',
    __name__,
    url_prefix='/voice'
)


def build_response(value: dict, status: int):
    return json.dumps(value), status, {'ContentType': 'application/json'}


@blueprint.errorhandler(Exception)
def all_exception_handler(error: Exception):
    return build_response({"error": str(error)}, 400)

'''@blueprint.route("/", methods=["GET"])
def receive_audio_blob():
    print("\n\n\n\nRecebi o pedido\n\n\n\n")
    language = request.form.get("language", "pt-PT")
    file = request.files["audio"]

    transcript = parse_file_input(file, language)
    callback = action_manager.select_action(transcript, language)

    #return build_response(callback, 200)

    return "Done"'''

@blueprint.route("/", methods=["POST"])
def receive_audio_blob():
    print("\n\n\n\nRecebi o pedido\n\n\n\n")
    language = request.form.get("language", "pt-PT")
    file = request.files["audio"]

    transcript = parse_file_input(file, language)
    callback = action_manager.select_action(transcript, language)

    return build_response(callback, 200)
