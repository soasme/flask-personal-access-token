# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, current_app, url_for, redirect, request, flash

bp = Blueprint(
    'personal-access-token-admin',
    __name__,
    template_folder='templates',
    static_folder='static'
)

@bp.before_request
def before_request():
    return bp.app.call_before_request_funcs()

@bp.route('/')
def index():
    render_data = {
        'base_api_url': current_app.config.get('PERSONAL_ACCESS_TOKEN_ADMIN_API_PREFIX'),
        'base_web_url': current_app.config.get('PERSONAL_ACCESS_TOKEN_ADMIN_PREFIX'),
        'debug': current_app.config.get('DEBUG'),
    }
    return render_template('/personal_access_token/index.html', **render_data)
