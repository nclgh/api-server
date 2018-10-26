from common.views import login_required_api
from flask import request
from common import const, utils
from common.response import reply
from models import Member, Department, ensure_session_removed
from pydash import pick
from api.form import parsing_form
import logging


@login_required_api
@ensure_session_removed
def add_member():
    valid, form = parsing_form('addMemberForm')
    if not valid:
        return reply(success=False, message='参数错误', error_code=const.param_err)

    if utils.is_code_exist(Member, form['code'])[0]:
        return reply(success=False, message='该成员编码已存在', error_code=const.param_illegal)

    if not utils.is_id_exist(Department, form['department_id'])[0]:
        return reply(success=False, message='该部门不存在', error_code=const.param_illegal)

    member_data = {
        'code': form['code'],
        'name': form['name'],
        'department_id': form['department_id'],
        'record_status': const.Normal,
    }
    res = utils.add_by_data(Member, member_data)
    return reply(success=res[0], message=res[1], error_code=res[2])


fileds = ['id', 'code', 'name']


def tran_to_json(record):
    item = pick(record, fileds)
    return item


@login_required_api
def query_member():
    page_info = utils.get_page_info(request)
    current_page = page_info[0]
    page_size = page_info[1]
    valid, form = parsing_form('queryMemberForm')
    if not valid:
        return reply(success=False, message='参数错误', error_code=const.param_err)
    members = Member.query.filter_by()
    query_dict = dict()
    if form['id']:
        query_dict['id'] = form['id']
    if form['code']:
        query_dict['code'] = form.code.data
    if form['name']:
        query_dict['name'] = form.name.data
    if query_dict:
        members = members.filter_by(**query_dict)
    members = members.filter_by(
        record_status=const.Normal
    )

    total_count = members.count()
    members = members.paginate(current_page, page_size, False).items
    data = []
    for member in members:
        data.append(member.to_json())
    return reply(success=True,
                 data={
                     'items': data,
                     'total_count': total_count,
                 },
                 message='done', error_code=const.success)

    # data = map(lambda x: tran_to_json(x), members)
    # data = list(data)
    # return reply(success=True,
    #              data={
    #                  'items': data,
    #                  'total_count': total_count,
    #              },
    #              message='done', error_code=const.success)


@login_required_api
@ensure_session_removed
def delete_member():
    valid, form = parsing_form('deleteByIdForm')
    if not valid:
        return reply(success=False, message='参数错误', error_code=const.param_err)

    res = utils.delete_by_id(Member, form['id'])
    return reply(success=res[0], message=res[1], error_code=res[2])
