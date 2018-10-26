# coding: utf-8

import functools
from flask_login import login_user, current_user, logout_user
from werkzeug.utils import import_string

from app import app
from config import config

auth_cls = import_string(config['AUTH'])
auth = auth_cls(app, login_user, logout_user)


def login_required(func):
    @functools.wraps(func)
    def _func(*args, **kwargs):
        if not current_user.is_authenticated:
            resp = auth.auth()
            if resp:
                return resp
        return func(*args, **kwargs)

    return _func


def login_required_api(func):
    @functools.wraps(func)
    def _func(*args, **kwargs):
        if not current_user.is_authenticated:
            return {
                'success': False,
                'message': 'Login Required'
            }
        return func(*args, **kwargs)

    return _func
