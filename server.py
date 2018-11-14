from flask import render_template
from werkzeug.wsgi import DispatcherMiddleware
from app import app
from werkzeug.routing import Rule
import api
from models import db
from flask_login import LoginManager
from models import User
from common.views import login_required_api


class IndexRule(Rule):
    def match(self, path, method=None):
        if path.startswith('|/api/'):
            return
        if path.startswith('|/static/'):
            return
        return super().match(path='|/', method=method)


def init():
    db.init_app(app)

    def __(_, resp):
        resp('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'Not Found']

    @login_required_api
    def index():
        return render_template('index.html')

    app.wsgi_app = DispatcherMiddleware(__, {'/api': app.wsgi_app})
    login_manager = LoginManager(app)
    login_manager.user_callback = lambda user_id: User.query.filter(User.id == user_id).first()

    app.add_url_rule(IndexRule('/', endpoint='index'), view_func=index)

    # test
    app.add_url_rule('/db_test/', 'api_db_test', view_func=api.db_add, methods=['GET'])
    # login
    app.add_url_rule('/user/login/', 'user_login', view_func=api.login, methods=['POST'])
    app.add_url_rule('/user/login_out/', 'user_login_out', view_func=api.login_out, methods=['POST'])
    # department
    app.add_url_rule('/department/add/', 'department_add', view_func=api.add_department, methods=['POST'])
    app.add_url_rule('/department/delete/', 'department_delete', view_func=api.delete_department, methods=['POST'])
    app.add_url_rule('/department/query/', 'department_query', view_func=api.query_department, methods=['GET'])

    # member
    app.add_url_rule('/department/member/add/', 'member_add', view_func=api.add_member, methods=['POST'])
    app.add_url_rule('/department/member/delete/', 'member_delete', view_func=api.delete_member, methods=['POST'])
    app.add_url_rule('/department/member/query/', 'member_query', view_func=api.query_member, methods=['POST'])

    # device
    app.add_url_rule('/device/document/add/', 'device_add', view_func=api.add_device, methods=['POST'])
    app.add_url_rule('/device/document/delete/', 'device_delete', view_func=api.delete_device, methods=['POST'])
    app.add_url_rule('/device/document/query/', 'device_query', view_func=api.query_device, methods=['POST'])
    app.add_url_rule('/device/document/querywithdescription/', 'device_query_withdescription',
                     view_func=api.query_device_with_description, methods=['POST'])
    app.add_url_rule('/device/document/description/', 'device_query_description',
                     view_func=api.query_device_description_by_id,
                     methods=['GET'])

    # achievement
    app.add_url_rule('/device/achievement/add/', 'achievement_add', view_func=api.add_achievement, methods=['POST'])
    app.add_url_rule('/device/achievement/delete/', 'achievement_delete', view_func=api.delete_achievement,
                     methods=['POST'])
    app.add_url_rule('/device/achievement/query/', 'achievement_query', view_func=api.query_achievement,
                     methods=['POST'])
    app.add_url_rule('/device/achievement/querywithdescription/', 'achievement_query_with_description',
                     view_func=api.query_achievement_with_description,
                     methods=['POST'])
    app.add_url_rule('/device/achievement/description/', 'achievement_query_description',
                     view_func=api.query_achievement_description_by_id,
                     methods=['GET'])

    # manufacturer
    app.add_url_rule('/manufacturer/add/', 'manufacturer_add', view_func=api.add_manufacturer, methods=['POST'])
    app.add_url_rule('/manufacturer/delete/', 'manufacturer_delete', view_func=api.delete_manufacturer,
                     methods=['POST'])
    app.add_url_rule('/manufacturer/query/', 'manufacturer_query', view_func=api.query_manufacturer, methods=['GET'])

    # device rent
    app.add_url_rule('/device/lend/add/', 'device_lend_add', view_func=api.rent_device, methods=['POST'])
    app.add_url_rule('/device/return/add/', 'device_return_add', view_func=api.return_device, methods=['POST'])
    app.add_url_rule('/device/lend/delete/', 'device_lend_delete', view_func=api.delete_device_rent,
                     methods=['POST'])
    app.add_url_rule('/device/lend/query/', 'device_lend_query', view_func=api.query_rent_device, methods=['POST'])


init()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
