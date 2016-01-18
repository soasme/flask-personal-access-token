# -*- coding: utf-8 -*-

from flask import Blueprint

bp = Blueprint('personal_access_token.web', __name__)

@bp.before_request
def before_request():
    bp.app.call_before_request_funcs()

@bp.route('/')
def index():
    return render_template('personal_access_token/index.html')
