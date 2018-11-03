from common.views import login_required_api
from common import const, utils
from common.response import *
from models import *
from api.form import parsing_form
from flask import request
from pydash import pick, assign


@login_required_api
@ensure_session_removed
def add_device():
    valid, form = parsing_form('addDeviceForm')
    if not valid:
        return reply(success=False, message='参数错误', error_code=const.PARAM_ERR)

    if utils.is_code_exist(Device, form['code'])[0]:
        return reply(success=False, message='该设备编码已存在', error_code=const.PARAM_ILLEGAL)

    if not utils.is_id_exist(Department, form['department_id'])[0]:
        return reply(success=False, message='该部门不存在', error_code=const.PARAM_ILLEGAL)

    if not utils.is_id_exist(Manufacturer, form['manufacturer_id'])[0]:
        return reply(success=False, message='该生产厂家不存在', error_code=const.PARAM_ILLEGAL)

    device_data = {
        'code': form['code'],
        'name': form['name'],
        'model': form['model'],
        'brand': form['brand'],
        'tag_code': form['tag_code'],
        'description': form['description'],
        'status': const.DEVICE_RETURNED,
        'manufacturer_date': form['manufacturer_date'],
        'manufacturer_id': form['manufacturer_id'],
        'department_id': form['department_id'],
        'record_status': const.RECORD_NORMAL,
    }
    res = utils.add_by_data(Device, device_data)
    return reply(success=res[0], message=res[1], error_code=res[2])


@login_required_api
@ensure_session_removed
def delete_device():
    valid, form = parsing_form('deleteByIdForm')
    if not valid:
        return reply(success=False, message='参数错误', error_code=const.PARAM_ERR)

    res = utils.delete_by_id(Device, form['id'])
    return reply(success=res[0], message=res[1], error_code=res[2])


# manufacturer_name
# department_code
# department_name

def transform(device, with_description=False):
    item = pick(device,
                'id',
                'code',
                'name',
                'model',
                'brand',
                'tag_code',
                'status',
                'manufacturer_id',
                'manufacturer_date',
                'department_id',
                )
    if with_description:
        item['description'] = device.description
    manufacturer = Manufacturer.query.filter_by(
        id=device.manufacturer_id,
        record_status=const.RECORD_NORMAL
    ).first()
    item['manufacturer_name'] = manufacturer.name

    department = Department.query.filter_by(
        id=device.department_id,
        record_status=const.RECORD_NORMAL
    ).first()
    item['department_code'] = department.code
    item['department_name'] = department.name
    return item


@login_required_api
@ensure_session_removed
def query_device():
    page_info = utils.get_page_info(request)
    current_page = page_info[0]
    page_size = page_info[1]
    valid, form = parsing_form('queryDeviceForm')
    if not valid:
        return reply(success=False, message='参数错误', error_code=const.PARAM_ERR)
    device_query = dict()
    if form['code']:
        device_query['code'] = form['code']
    if form['name']:
        device_query['name'] = form['name']
    if form['model']:
        device_query['model'] = form['model']
    if form['brand']:
        device_query['brand'] = form['brand']
    if form['tag_code']:
        device_query['tag_code'] = form['tag_code']
    if form['status']:
        device_query['status'] = form['status']
    if form['manufacturer_id']:
        device_query['manufacturer_id'] = form['manufacturer_id']
    if form['department_id']:
        device_query['department_id'] = form['department_id']

    devices = Device.query.filter_by()
    if device_query:
        devices = devices.filter_by(
            **device_query
        )
    if form['manufacturer_date']:
        devices = devices.filter(
            db.cast(Device.manufacturer_date, db.DATE) == form['manufacturer_date'])

    total_count = devices.count()
    devices = devices.paginate(current_page, page_size, False).items
    data = map(lambda x: transform(x), devices)
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
def query_device_description_by_id():
    device_id = request.args.get('id')
    if not device_id:
        return reply(success=False, message='参数错误', error_code=const.PARAM_ERR)
    device = Device.query.filter_by(
        id=device_id
    ).first()
    if not device:
        return reply(success=False, message='该设备不存在', error_code=const.PARAM_ILLEGAL)
    return reply(success=True,
                 data={
                     'description': device.description,
                 },
                 message='done', error_code=const.CODE_SUCCESS)


@login_required_api
@ensure_session_removed
def query_device_with_description():
    page_info = utils.get_page_info(request)
    current_page = page_info[0]
    page_size = page_info[1]
    valid, form = parsing_form('queryDeviceForm')
    if not valid:
        return reply(success=False, message='参数错误', error_code=const.PARAM_ERR)
    device_query = dict()
    if form['code']:
        device_query['code'] = form['code']
    if form['name']:
        device_query['name'] = form['name']
    if form['model']:
        device_query['model'] = form['model']
    if form['brand']:
        device_query['brand'] = form['brand']
    if form['tag_code']:
        device_query['tag_code'] = form['tag_code']
    if form['status']:
        device_query['status'] = form['status']
    if form['manufacturer_id']:
        device_query['manufacturer_id'] = form['manufacturer_id']
    if form['department_id']:
        device_query['department_id'] = form['department_id']

    devices = Device.query.filter_by()
    if device_query:
        devices = devices.filter_by(
            **device_query
        )
    if form['manufacturer_date']:
        devices = devices.filter(
            db.cast(Device.manufacturer_date, db.DATE) == form['manufacturer_date'])

    total_count = devices.count()
    devices = devices.paginate(current_page, page_size, False).items
    data = map(lambda x: transform(x, True), devices)
    data = list(data)
    return query_reply(success=True,
                       data=data,
                       paging={
                           'current': current_page,
                           'pages': int(total_count / page_size + 1),
                           'records': total_count,
                       },
                       message='done', error_code=const.CODE_SUCCESS)
