# -*- coding: utf-8 -*-

from flask_personal_access_token import PersonalAccessTokenManager
from flask import Flask, g
from collections import namedtuple

class User(namedtuple('User', 'id')):pass

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/token.db'

manager = PersonalAccessTokenManager()
manager.app = app
manager.init_app(app)
manager.create_all()
manager.user_loader(User)

@manager.before_request
def bf():
    manager.current_user_id = 2

@app.before_request
def bff():
    g.user = manager.load_user_from_request()
    pass

@app.route('/')
def index():
    return 'hello %s' % g.user

if __name__ == '__main__':
    app.run()
