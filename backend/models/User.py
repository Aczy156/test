import backend.config
from werkzeug.security import generate_password_hash, check_password_hash
from backend.database import Tododb


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.todos = Tododb.getTodoListByUserId(id)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_json(self):
        return {'id': self.id, 'username': self.username}

