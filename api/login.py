from common.views import auth
from models import User
from common import const
from flask_login import login_user, current_user
from common.response import reply
from api.form import parsing_form
import logging


def login():
    valid, form = parsing_form('loginForm')
    if not valid:
        return reply(success=False, message='参数缺失', error_code=const.param_err)
    user = User.query.filter_by(
        username=form['username'],
        record_status=const.Normal
    ).first()
    if not user:
        return reply(success=False, message='用户不存在', error_code=const.login_err)
    if user.password != form['password']:
        return reply(success=False, message='密码错误', error_code=const.login_err)

    auth.login(user)
    return reply(success=True)


def login_out():
    if current_user.is_authenticated:
        auth.login_out()
    return dict(
        success=True
    )
