# -*- coding: utf-8 -*-

from flask import request
from .core import db
from .model import PersonalAccessToken

class PersonalAccessTokenManager(object):

    def __init__(self, app=None):
        self.app = app
        self.before_request_funcs = []
        self.current_user_id = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        db.app = app
        db.init_app(app)

        app.config.setdefault('PERSONAL_ACCESS_TOKEN_ADMIN_API_PREFIX', '/personal_access_token/api')
        app.config.setdefault('PERSONAL_ACCESS_TOKEN_ADMIN_PREFIX', '/personal_access_token')

        from .api import bp as api_bp
        api_bp.app = self
        app.register_blueprint(api_bp, url_prefix='/personal_access_token/api')

        from .admin import bp as admin_bp
        admin_bp.app = self
        app.register_blueprint(admin_bp, url_prefix='/personal_access_token/')

    def create_all(self):
        db.create_all()

    def call_before_request_funcs(self):
        for func in self.before_request_funcs:
            func()

    def before_request(self, f):
        self.before_request_funcs.append(f)
        return f

    def user_loader(self, f):
        self.user_loader_callback = f
        return f

    def load_user(self, user_id):
        if not self.user_loader_callback:
            raise NotImplementedError('You must implement `user_loader`.')
        return self.user_loader_callback(user_id)

    def load_user_by_token(self, token):
        token = PersonalAccessToken.query.filter_by(token=token).first()
        if not token:
            return
        token.use()
        return self.load_user(token.user_id)

    def load_user_from_request(self):
        headers = request.headers
        authorization = headers.get('Authorization')
        if not authorization or not authorization.startswith('Bearer '):
            return
        token = authorization[len('Bearer '):]
        return self.load_user_by_token(token)
