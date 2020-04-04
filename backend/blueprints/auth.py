from flask import Blueprint, jsonify, request
from flask_login import current_user, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import ValidationError, Length

from backend.models import db

import backend.config as config
from backend.models import User
from backend.database import Userdb,Tododb

bp = Blueprint('auth', __name__)


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[Length(max=64)])
    password = PasswordField('Password', validators=[Length(8, 16)])
    confirm = PasswordField('Confirm Password')

    def validate_username(self, field):
        # check request
        if User.query.filter_by(username=field.data).count() > 0:
            raise ValidationError('Username %s already exists!' % field.data)


# service + sql execution
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Length(max=64)])
    password = PasswordField('Password', validators=[Length(8, 16)])
    remember = BooleanField('Remember Me')

    def validate_username(self, field):
        if not self.get_user():
            raise ValidationError('Invalid username!')

    def validate_password(self, field):
        if not self.get_user():
            return
        if not self.get_user().check_password(field.data):
            raise ValidationError('Incorrect password!')

    def get_user(self):
        if Userdb.getUserByUsername(self.data['username']) is not None:
            return Userdb.getUserByUsername(self.data['username'])
        print('after select by username is none')
        return None


@bp.route('/register', methods=['POST'])
def register():
    user_data = request.get_json()
    form = RegisterForm(data=user_data)
    if form.validate():
        user = User(username=user_data['username'], password=user_data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': form.errors}), 400


# controller
@bp.route('/login', methods=['POST'])
def login():
    user_data = request.get_json()
    form = LoginForm(data=user_data)
    if form.validate():
        user = form.get_user()
        print('check ~~~~~~~~~')
        user.todos = Tododb.getTodoListByUserId(user_data['id'])
        login_user(user, remember=form.remember.data)
        config.cur_user = user
        print(current_user)
        print(user.to_json())
        # return json file {status,json_info_of_user }
        return jsonify({'status': 'success', 'user': user.to_json()})
    return jsonify({'status': 'error', 'message': form.errors}), 403


@bp.route('/session')
def get_session():
    print("is getting session ")
    if config.cur_user is None:
        print('   current is not verify')
        return jsonify({'status': 'error'}), 401
    print('    is verify')
    print(config.cur_user.to_json())
    return jsonify({'status': 'success', 'user': config.cur_user.to_json()})


@bp.route('/logout')
def logout():
    logout_user()
    return jsonify({'status': 'success'})
