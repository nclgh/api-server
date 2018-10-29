from common.views import login_required_api
from common import const, utils
from common.response import *
from models import Department, ensure_session_removed
from pydash import pick
from api.form import parsing_form
import logging


@login_required_api
@ensure_session_removed
def add_department():
    valid, form = parsing_form('addDepartmentForm')
    if not valid:
        return reply(success=False, message='参数错误', error_code=const.PARAM_ERR)

    if utils.is_code_exist(Department, form['code'])[0]:
        return reply(success=False, message='该部门已存在', error_code=const.PARAM_ILLEGAL)
    department_data = {
        'code': form['code'],
        'name': form['name'],
        'record_status': const.RECORD_NORMAL,
    }
    res = utils.add_by_data(Department, department_data)
    return reply(success=res[0], message=res[1], error_code=res[2])


@login_required_api
@ensure_session_removed
def delete_department():
    valid, form = parsing_form('deleteByIdForm')
    if not valid:
        return reply(success=False, message='参数错误', error_code=const.PARAM_ERR)

    res = utils.delete_by_id(Department, form['id'])
    return reply(success=res[0], message=res[1], error_code=res[2])


@login_required_api
def query_department():
    logging.warning('111')
    departments = Department.query.order_by(
        Department.name
    ).filter_by(
        record_status=const.RECORD_NORMAL
    )
    total_count = departments.count()
    data = []
    for department in departments:
        data.append(department.to_json())
    return query_reply(success=True,
                       data=data,
                       paging={
                           'records': total_count,
                       },
                       message='done', error_code=const.CODE_SUCCESS)