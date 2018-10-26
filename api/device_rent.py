from common.views import login_required_api
from flask import request
from common import const, utils
from common.response import reply
from models import *
from pydash import pick
from api.form import parsing_form
import logging


@login_required_api
@ensure_session_removed
def rent_device():
    valid, form = parsing_form('rentDeviceForm')
    if not valid:
        return reply(success=False, message='参数错误', error_code=const.param_err)
    res_device = utils.is_code_exist(Device, form['device_code'])
    if not res_device[0]:
        return reply(success=False, message='该设备不存在', error_code=const.param_illegal)
    device = res_device[1].first()
    if device.status != const.Returned:
        return reply(success=False, message='该设备已被借出', error_code=const.param_illegal)

    res_member = utils.is_code_exist(Member, form['borrower_member_code'])
    if not res_member[0]:
        return reply(success=False, message='该成员不存在', error_code=const.param_illegal)
    member = res_member[1].first()
    update_info = {
        'status': const.Rented,
    }
    if not utils.update_by_data(res_device[1], update_info, False)[0]:
        return reply(success=False, message='设备状态修改失败', error_code=const.unknown_err)

    device_rent_data = {
        'device_code': form['device_code'],
        'device_department_id': device.department_id,
        'status': const.Rented,
        'borrower_member_code': form['borrower_member_code'],
        'borrower_department_id': member.department_id,
        'borrow_date': form['borrow_date'],
        'borrow_remark': form['borrow_remark'],
        'expect_return_date': form['expect_return_date'],
        # default
        'returner_member_code': '',
        'returner_department_id': 0,
        'real_return_date': form['expect_return_date'],
        'return_remark': '',
        'record_status': const.Normal,
    }
    res = utils.add_by_data(DeviceRent, device_rent_data)
    return reply(success=res[0], message=res[1], error_code=res[2])


@login_required_api
@ensure_session_removed
def return_device():
    valid, form = parsing_form('returnDeviceForm')
    if not valid:
        return reply(success=False, message='参数错误', error_code=const.param_err)

    res_device = utils.is_code_exist(Device, form['device_code'])
    if not res_device[0]:
        return reply(success=False, message='该设备不存在', error_code=const.param_illegal)
    device = res_device[1].first()
    if device.status != const.Rented:
        return reply(success=False, message='该设备未被借出', error_code=const.param_illegal)

    device_rented = DeviceRent.query.filter_by(
        device_code=form['device_code'],
        status=const.Rented,
        record_status=const.Normal
    )
    cnt = device_rented.count()
    if cnt < 1:
        return reply(success=False, message='无此设备正在外借记录', error_code=const.unknown_err)
    if cnt > 1:
        return reply(success=False, message='内部数据错误，请联系管理员', error_code=const.unknown_err)

    res_member = utils.is_code_exist(Member, form['returner_member_code'])
    if not res_member[0]:
        return reply(success=False, message='该归还成员不存在', error_code=const.param_illegal)
    member = res_member[1].first()
    update_info = {
        'status': const.Returned,
    }
    if not utils.update_by_data(res_device[1], update_info, False)[0]:
        return reply(success=False, message='设备状态修改失败', error_code=const.unknown_err)

    device_return_data = {
        'status': const.Returned,
        'returner_member_code': form['returner_member_code'],
        'returner_department_id': member.department_id,
        'real_return_date': form['return_date'],
        'return_remark': form['return_remark'],
    }
    res = utils.update_by_data(device_rented, device_return_data, True)

    return reply(success=res[0], message=res[1], error_code=res[2])
    # return reply(success=True)


@login_required_api
@ensure_session_removed
def delete_device_rent():
    valid, form = parsing_form('deleteByIdForm')
    if not valid:
        return reply(success=False, message='参数错误', error_code=const.param_err)
    res = utils.delete_by_id(DeviceRent, form['id'])
    return reply(success=res[0], message=res[1], error_code=res[2])


# id
# device_code
# status
# borrower_member_code
# borrower_department_id
# borrow_date
# borrow_remark
# returner_member_code
# return_remark
# expect_return_date
# real_return_date

# device_id
# device_name
# model
# brand
# tag_code
# description
# manufacturer_date
# manufacturer
# department_id
# department_code
# department_name

# borrower_id
# borrower_name
# borrower_department_code
# borrower_department_name
# returner_id
# returner_name

def transform(device_rent):
    item = pick(device_rent,
                'id',
                'device_code',
                'status',
                'borrower_member_code',
                'borrower_department_id',
                'borrow_date',
                'borrow_remark',
                'returner_member_code',
                'return_remark',
                'expect_return_date',
                'real_return_date',
                )
    device = Device.query.filter_by(
        code=device_rent.device_code,
        record_status=const.Normal
    ).first()
    item['device_id'] = device.id
    item['device_name'] = device.name
    item['model'] = device.model
    item['brand'] = device.brand
    item['tag_code'] = device.tag_code
    item['description'] = device.description
    item['manufacturer_date'] = device.manufacturer_date
    item['department_id'] = device.department_id

    manufacturer = Manufacturer.query.filter_by(
        id=device.manufacturer_id,
        record_status=const.Normal
    ).first()
    item['manufacturer'] = manufacturer.name

    device_department = Department.query.filter_by(
        id=device.department_id,
        record_status=const.Normal
    ).first()
    item['department_code'] = device_department.code
    item['department_name'] = device_department.name

    borrower = Member.query.filter_by(
        code=device_rent.borrower_member_code,
        record_status=const.Normal
    ).first()
    item['borrower_id'] = borrower.id
    item['borrower_name'] = borrower.name

    borrower_department = Department.query.filter_by(
        id=borrower.department_id,
        record_status=const.Normal
    ).first()
    item['borrower_department_code'] = borrower_department.code
    item['borrower_department_name'] = borrower_department.name
    returner = Member.query.filter_by(
        code=device_rent.returner_member_code,
        record_status=const.Normal
    ).first()
    item['returner_id'] = returner.id
    item['returner_name'] = returner.name
    return item


@login_required_api
@ensure_session_removed
def query_rent_device():
    page_info = utils.get_page_info(request)
    current_page = page_info[0]
    page_size = page_info[1]
    valid, form = parsing_form('queryDeviceLendForm')
    if not valid:
        return reply(success=False, message='参数错误', error_code=const.param_err)
    rent_query = dict()
    if form['device_code']:
        rent_query['device_code'] = form['device_code']
    if form['status']:
        rent_query['status'] = form['status']
    if form['department_id']:
        rent_query['device_department_id'] = form['department_id']
    if form['borrower_member_code']:
        rent_query['borrower_member_code'] = form['borrower_member_code']
    if form['borrower_department_id']:
        rent_query['borrower_department_id'] = form['borrower_department_id']
    if form['returner_member_code']:
        rent_query['returner_member_code'] = form['returner_member_code']
    if form['returner_department_id']:
        rent_query['returner_department_id'] = form['returner_department_id']

    device_rents = DeviceRent.query.filter_by()
    if rent_query:
        device_rents = device_rents.filter_by(
            **rent_query
        )

    device_query = dict()
    if form['device_name']:
        device_query['device_name'] = form['device_name']
    if form['model']:
        device_query['model'] = form['model']
    if form['brand']:
        device_query['brand'] = form['brand']
    if form['tag_code']:
        device_query['tag_code'] = form['tag_code']
    if device_query:
        devices = Device.filter_by(
            **device_query
        )
        device_rents = device_rents.filter(
            DeviceRent.device_code.in_(
                map(lambda x: x.device_code, devices)
            )
        )
    if form['borrow_date']:
        device_rents = device_rents.filter(
            db.cast(DeviceRent.borrow_date, db.DATE) == form['borrow_date'])
    if form['real_return_date']:
        device_rents = device_rents.filter(
            db.cast(DeviceRent.return_date, db.DATE) == form['real_return_date'])
    if form['expect_return_date']:
        device_rents = device_rents.filter(
            db.cast(DeviceRent.expect_return_date, db.DATE) == form['expect_return_date'])

    total_count = device_rents.count()
    device_rents = device_rents.paginate(current_page, page_size, False).items
    data = map(lambda x: transform(x), device_rents)
    data = list(data)
    return reply(success=True,
                 data={
                     'items': data,
                     'total_count': total_count,
                 },
                 message='done', error_code=const.success)
