from models import db, User
from common.views import login_required


@login_required
def db_add():
    user_data = {
        'id': 10,
        'name': 'test',
        'username': 'test_name',
        'password': 'test'
    }
    user_info = User(**user_data)
    db.session.add(user_info)
    db.session.commit()
    return dict(
        success='CODE_SUCCESS'
    )
