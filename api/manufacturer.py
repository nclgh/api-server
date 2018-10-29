from common.views import login_required_api
from flask import request
from common import const, utils
from common.response import *
from models import Manufacturer, ensure_session_removed
from pydash import pick
from api.form import parsing_form


@login_required_api
@ensure_session_removed
def add_manufacturer():
    valid, form = parsing_form('addManufacturerForm')
    if not valid:
        return reply(success=False, message='参数错误', error_code=const.PARAM_ERR)

    if utils.is_name_exist(Manufacturer, form['name'])[0]:
        return reply(success=False, message='该生产厂家已存在', error_code=const.PARAM_ILLEGAL)
    manufacturer_data = {
        'name': form['name'],
        'record_status': const.RECORD_NORMAL,
    }
    res = utils.add_by_data(Manufacturer, manufacturer_data)
    return reply(success=res[0], message=res[1], error_code=res[2])


fileds = ['id', 'name']


def tran_to_json(record):
    item = pick(record, fileds)
    return item


@login_required_api
def query_manufacturer():
    page_info = utils.get_page_info(request)
    current_page = page_info[0]
    page_size = page_info[1]
    manufacturer = Manufacturer.query.order_by(
        Manufacturer.name
    ).filter_by(
        record_status=const.RECORD_NORMAL
    )
    total_count = manufacturer.count()
    members = manufacturer.paginate(current_page, page_size, False).items
    data = map(lambda x: tran_to_json(x), members)
    data = list(data)
    return query_reply(success=True,
                       data=data,
                       paging={
                           'current': current_page,
                           'pages': int(total_count / page_size + 1),
                           'records': total_count,
                       },
                       message='done', error_code=const.CODE_SUCCESS)


@login_required_api
@ensure_session_removed
def delete_manufacturer():
    valid, form = parsing_form('deleteByIdForm')
    if not valid:
        return reply(success=False, message='参数错误', error_code=const.PARAM_ERR)

    res = utils.delete_by_id(Manufacturer, form['id'])
    return reply(success=res[0], message=res[1], error_code=res[2])
