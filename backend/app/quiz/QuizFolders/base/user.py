from flask_login import UserMixin
from app         import mongo, login_manager

class User(UserMixin):
    def __init__(self, user):
        self.id        = user['id']
        self.username  = user['username']
        self.password  = user['password']
        self.name      = user['name']
        self.gender = user['gender']
        self.degree = user['degree']
        self.user_type = int(user['user_type'])
        self.email     = user['email']
        self.avatar    = user.get('avatar') # return None if key doesn't exist

    def __repr__(self):
        return str(self.username + ' logged in')

    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    user = mongo.db.users.find_one({'id': user_id})

    return User(user) if user else None

@login_manager.request_loader
def load_user_from_request(request):
    username = request.form.get('username')
    user     = mongo.db.users.find_one({'username': username})

    return User(user) if user else None
