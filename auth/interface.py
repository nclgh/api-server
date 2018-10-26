# coding: utf-8


class AuthInterface(object):
    def __init__(self, app, login_user, logout_user):
        self.app = app
        self.login_user = login_user
        self.logout_user = logout_user

    def auth(self, *args, **kwargs):
        raise NotImplementedError()
