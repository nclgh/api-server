# coding: utf-8

import json
from common import const
from datetime import datetime
from models import db, db_commit
import logging


def param_error(errors):
    return {
        'success': False,
        'message': '参数错误:%s。' % json.dumps(errors)
    }


def add_by_data(table, data, do_commit=True):
    record = table(**data)
    db.session.add(record)
    resp = [True, '', const.success]
    if do_commit:
        resp = db_commit()
    return resp


def update_by_data(records, update_data, do_commit=True):
    update_data['update_time'] = datetime.now()
    records.update(update_data)
    resp = [True, '', const.success]
    if do_commit:
        resp = db_commit()
    return resp


delete_info = {
    'record_status': const.Deleted,
    'update_time': datetime.now()
}


def delete_by_id(table, id, do_commit=True):
    res = is_id_exist(table, id)
    if res[0]:
        delete_info['update_time'] = datetime.now()
        res[1].update(delete_info)
        resp = [True, '', const.success]
        if do_commit:
            resp = db_commit()
        return resp
    return False, '记录不存在', const.param_illegal


def is_code_exist(table, data):
    ext = table.query.filter_by(
        code=data,
        record_status=const.Normal
    )
    if not ext.first():
        return False, None
    return True, ext


def is_id_exist(table, data):
    ext = table.query.filter_by(
        id=data,
        record_status=const.Normal
    )
    if not ext.first():
        return False, None
    return True, ext


def is_name_exist(table, data):
    ext = table.query.filter_by(
        name=data,
        record_status=const.Normal
    )
    if not ext.first():
        return False, None
    return True, ext


def get_page_info(request):
    current_page = request.args.get('page')
    if not current_page:
        current_page = const.current_page_default
    page_size = request.args.get('limit')
    if not page_size:
        page_size = const.page_size_default
    return int(current_page), int(page_size)
