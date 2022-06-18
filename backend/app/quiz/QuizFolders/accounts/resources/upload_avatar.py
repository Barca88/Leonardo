from flask_login             import current_user
from flask_restful           import reqparse, Resource
from os                      import path, remove
from glob                    import glob
from werkzeug.datastructures import FileStorage
from flask                   import current_app
from app                     import mongo

class UploadAvatar(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('avatar', type=FileStorage, location='files')

        params      = parser.parse_args()
        name_prefix = 'user_%s' % current_user.id
        avatar_name = '%s_%s' % (name_prefix, params.avatar.filename)
        assets_path = path.join(current_app.root_path, current_app.config['ASSETS_PATH'])
        new_avatar  = path.join(assets_path, 'images/avatars/%s' % avatar_name)
        old_avatars = glob(path.join(assets_path, 'images/avatars/%s*' % name_prefix))

        if old_avatars:
            [ remove(avatar) for avatar in old_avatars ]

        params.avatar.save(new_avatar)
        mongo.db.users.update({ 'id': current_user.id }, { '$set': { 'avatar': avatar_name } })
