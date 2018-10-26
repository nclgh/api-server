# SQLAlchemy
SQLALCHEMY_ECHO = False
SQLALCHEMY_POOL_RECYCLE = 30
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_COMMIT_ON_TEARDOWN = False
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:ci@127.0.0.1:3306/server?charset=utf8mb4'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:ci@server_mysql:3306/server?charset=utf8mb4'

# Flask
SESSION_COOKIE_NAME = 'server-session'
SECRET_KEY = '712c6541448b331d5215d3abd0f22925'

# Babel
BABEL_DEFAULT_LOCALE = 'zh_CN'
BABEL_DEFAULT_TIMEZONE = 'Asia/Shanghai'

# Auth
# AUTH = "auth.noauth:NoAuth"
AUTH = "auth.oauth2:Oauth2"
OAUTH_AUTHORIZE_URL = "/server/login/"
