from common.views import login_required_api
from common import const, utils
from common.response import reply
from models import Department, ensure_session_removed
from pydash import pick
from api.form import parsing_form


@login_required_api
@ensure_session_removed
def add_department():
    valid, form = parsing_form('addDepartmentForm')
    if not valid:
        return reply(success=False, message='参数错误', error_code=const.param_err)

    if utils.is_code_exist(Department, form['code'])[0]:
        return reply(success=False, message='该部门已存在', error_code=const.param_illegal)
    department_data = {
        'code': form['code'],
        'name': form['name'],
        'record_status': const.Normal,
    }
    res = utils.add_by_data(Department, department_data)
    return reply(success=res[0], message=res[1], error_code=res[2])


@login_required_api
@ensure_session_removed
def delete_department():
    valid, form = parsing_form('deleteByIdForm')
    if not valid:
        return reply(success=False, message='参数错误', error_code=const.param_err)

    res = utils.delete_by_id(Department, form['id'])
    return reply(success=res[0], message=res[1], error_code=res[2])


@login_required_api
def query_department():
    departments = Department.query.order_by(
        Department.name
    ).filter_by(
        record_status=const.Normal
    )
    total_count = departments.count()
    data = []
    for department in departments:
        data.append(department.to_json())
    return reply(success=True,
                 data={
                     'items': data,
                     'total_count': total_count,
                 },
                 message='done', error_code=const.success)
