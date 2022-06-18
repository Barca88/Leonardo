from app           import mongo
from flask_restful import reqparse, Resource
from werkzeug.security     import check_password_hash, generate_password_hash
from flask_login   import current_user
from flask         import jsonify

class ChangePassword(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('old')
        parser.add_argument('new')

        params         = parser.parse_args()
        password_error = False
        old_password   = params.old
        new_password   = params.new

        if check_password_hash(current_user.password, old_password):
            mongo.db.users.update(
                { 'username': current_user.username },
                { '$set': { 'password' : generate_password_hash(new_password) } }
            )
        else:
            password_error = True

        return jsonify(error=password_error)
