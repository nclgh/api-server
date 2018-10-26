from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import (
    BIGINT, VARCHAR, DATETIME, BOOLEAN, TINYINT
)
from flask_login import UserMixin
import functools
from datetime import datetime
from common import const

db = SQLAlchemy()


def ensure_session_removed(func):
    @functools.wraps(func)
    def _func(*args, **kws):
        try:
            return func(*args, **kws)
        finally:
            db.session.remove()

    return _func


def db_commit():
    try:
        db.session.commit()
        return True, '', const.success
    except:
        return False, '数据库操作失败', const.db_err


class MySQLMixin(object):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }


class User(db.Model, MySQLMixin, UserMixin):
    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    name = db.Column(VARCHAR(255), nullable=False)
    username = db.Column(VARCHAR(255), nullable=False)
    password = db.Column(VARCHAR(255), nullable=False)
    record_status = db.Column(TINYINT(unsigned=True), default=0)  # 0---success 1---delete
    create_time = db.Column(DATETIME, default=datetime.now)
    update_time = db.Column(DATETIME, default=datetime.now)


class Device(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    code = db.Column(VARCHAR(255), nullable=False)
    name = db.Column(VARCHAR(255), nullable=False)
    model = db.Column(VARCHAR(255), nullable=False)
    brand = db.Column(VARCHAR(255), nullable=False)
    tag_code = db.Column(VARCHAR(255), nullable=False)
    status = db.Column(TINYINT(unsigned=True), default=0)
    manufacturer_id = db.Column(VARCHAR(255), nullable=False)
    manufacturer_date = db.Column(DATETIME, default='')
    department_id = db.Column(BIGINT(unsigned=True), nullable=False)
    record_status = db.Column(TINYINT(unsigned=True), default=0)
    create_time = db.Column(DATETIME, default=datetime.now)
    update_time = db.Column(DATETIME, default=datetime.now)
    description = db.Column(VARCHAR(1020), nullable=False)

    def to_json(self):
        _dict = self.__dict__
        if "_sa_instance_state" in _dict:
            del _dict["_sa_instance_state"]
        return _dict


class Manufacturer(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    name = db.Column(VARCHAR(255), nullable=False)
    record_status = db.Column(TINYINT(unsigned=True), default=0)  # 0---success 1---delete
    create_time = db.Column(DATETIME, default=datetime.now)
    update_time = db.Column(DATETIME, default=datetime.now)

    def to_json(self):
        _dict = self.__dict__
        if "_sa_instance_state" in _dict:
            del _dict["_sa_instance_state"]
        return _dict


class Department(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    code = db.Column(VARCHAR(255), nullable=False)
    name = db.Column(VARCHAR(255), nullable=False)
    record_status = db.Column(TINYINT(unsigned=True), default=0)
    create_time = db.Column(DATETIME, default=datetime.now)
    update_time = db.Column(DATETIME, default=datetime.now)

    def to_json(self):
        _dict = self.__dict__
        if "_sa_instance_state" in _dict:
            del _dict["_sa_instance_state"]
        return _dict


class Member(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    code = db.Column(VARCHAR(255), nullable=False)
    name = db.Column(VARCHAR(255), nullable=False)
    department_id = db.Column(BIGINT(unsigned=True), nullable=False)
    record_status = db.Column(TINYINT(unsigned=True), default=0)
    create_time = db.Column(DATETIME, default=datetime.now)
    update_time = db.Column(DATETIME, default=datetime.now)

    def to_json(self):
        _dict = self.__dict__
        if "_sa_instance_state" in _dict:
            del _dict["_sa_instance_state"]
        return _dict


class DeviceRent(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    device_code = db.Column(VARCHAR(255), nullable=False)
    device_department_id = db.Column(BIGINT(unsigned=True), nullable=False)
    status = db.Column(TINYINT(unsigned=True), default=0)
    borrower_member_code = db.Column(VARCHAR(255), nullable=False)
    borrower_department_id = db.Column(BIGINT(unsigned=True), nullable=False)
    borrow_date = db.Column(DATETIME, default=datetime.now)
    expect_return_date = db.Column(DATETIME, default=datetime.now)
    borrow_remark = db.Column(VARCHAR(1020), nullable=False)
    returner_member_code = db.Column(VARCHAR(255), nullable=False)
    returner_department_id = db.Column(BIGINT(unsigned=True), nullable=False)
    real_return_date = db.Column(DATETIME, default=datetime.now)
    return_remark = db.Column(VARCHAR(1020), nullable=False)
    record_status = db.Column(TINYINT(unsigned=True), default=0)
    create_time = db.Column(DATETIME, default=datetime.now)
    update_time = db.Column(DATETIME, default=datetime.now)

    def to_json(self):
        _dict = self.__dict__
        if "_sa_instance_state" in _dict:
            del _dict["_sa_instance_state"]
        return _dict


class Achievement(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    device_code = db.Column(VARCHAR(255), nullable=False)
    member_code = db.Column(VARCHAR(255), nullable=False)
    department_id = db.Column(BIGINT(unsigned=True), nullable=False)
    manufacturer_date = db.Column(DATETIME, default=datetime.now)
    achievement_description = db.Column(VARCHAR(1020), nullable=False)
    patent_description = db.Column(VARCHAR(1020), nullable=False)
    paper_description = db.Column(VARCHAR(1020), nullable=False)
    competition_description = db.Column(VARCHAR(1020), nullable=False)
    achievement_remark = db.Column(VARCHAR(1020), nullable=False)
    record_status = db.Column(TINYINT(unsigned=True), default=0)
    create_time = db.Column(DATETIME, default=datetime.now)
    update_time = db.Column(DATETIME, default=datetime.now)

    def to_json(self):
        _dict = self.__dict__
        if "_sa_instance_state" in _dict:
            del _dict["_sa_instance_state"]
        return _dict
