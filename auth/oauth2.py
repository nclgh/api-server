# coding: utf-8

from urllib import parse

from flask import Flask, redirect, url_for, request, abort

from models import User, db, ensure_session_removed
from auth.interface import AuthInterface


class Oauth2(AuthInterface):
    def __init__(self, app: Flask, login_user, logout_user):
        super().__init__(app, login_user, logout_user)
        try:
            self.app.add_url_rule('/oauth2/callback', 'oauth2.callback')
        except AssertionError:
            pass

    def login(self, user):
        self.login_user(user)

    def login_out(self):
        self.logout_user()
