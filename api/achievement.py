from common.views import login_required_api
from common import const, utils
from common.response import reply
from models import *
from api.form import parsing_form
from flask import request
from pydash import pick


@login_required_api
@ensure_session_removed
def add_achievement():
    valid, form = parsing_form('addAchievementForm')
    if not valid:
        return reply(success=False, message='参数错误', error_code=const.param_err)
    res_device = utils.is_code_exist(Device, form['device_code'])
    if not res_device[0]:
        return reply(success=False, message='设备不存在', error_code=const.param_illegal)
    if not utils.is_code_exist(Member, form['member_code'])[0]:
        return reply(success=False, message='成员不存在', error_code=const.param_illegal)
    device = res_device[1].first()
    device_achievement_data = {
        'device_code': form['device_code'],
        'member_code': form['member_code'],
        'department_id': device.department_id,
        'manufacturer_date': form['manufacturer_date'],
        'achievement_description': form['achievement_description'],
        'patent_description': form['patent_description'],
        'paper_description': form['paper_description'],
        'competition_description': form['competition_description'],
        'achievement_remark': form['achievement_remark'],
        'record_status': const.Normal,
    }
    res = utils.add_by_data(Achievement, device_achievement_data)
    return reply(success=res[0], message=res[1], error_code=res[2])


@login_required_api
@ensure_session_removed
def delete_achievement():
    valid, form = parsing_form('deleteByIdForm')
    if not valid:
        return reply(success=False, message='参数错误', error_code=const.param_err)

    res = utils.delete_by_id(Achievement, form['id'])
    return reply(success=res[0], message=res[1], error_code=res[2])


def transform(achievement):
    item = pick(achievement,
                'id',
                'device_code',
                'member_code',
                'department_id',
                'manufacturer_date',
                )
    device = Device.query.filter_by(
        code=achievement.device_code,
        record_status=const.Normal
    ).first()
    item['device_id'] = device.id
    item['device_name'] = device.name
    item['model'] = device.model
    item['brand'] = device.brand
    item['tag_code'] = device.tag_code
    item['manufacturer_date'] = device.manufacturer_date
    item['department_id'] = device.department_id
    device_department = Department.query.filter_by(
        id=device.department_id,
        record_status=const.Normal
    ).first()
    item['department_code'] = device_department.code
    item['department_name'] = device_department.name
    achievement_department = Department.query.filter_by(
        id=achievement.department_id,
        record_status=const.Normal
    ).first()
    item['achievement_department_id'] = achievement_department.id
    item['achievement_department_code'] = achievement_department.code
    item['achievement_department_name'] = achievement_department.name
    return item


@login_required_api
@ensure_session_removed
def query_achievement():
    page_info = utils.get_page_info(request)
    current_page = page_info[0]
    page_size = page_info[1]
    valid, form = parsing_form('queryAchievementForm')
    if not valid:
        return reply(success=False, message='参数错误', error_code=const.param_err)
    achievement_query = dict()
    if form['device_code']:
        achievement_query['device_code'] = form['device_code']
    if form['member_code']:
        achievement_query['member_code'] = form['member_code']
    if form['department_id']:
        achievement_query['department_id'] = form['department_id']
    achievements = Achievement.query.filter_by()
    if achievement_query:
        achievements = achievements.filter_by(
            **achievement_query
        )
    device_query = dict()
    if form['device_code']:
        device_query['code'] = form['device_code']
    if form['device_name']:
        device_query['name'] = form['device_name']
    if form['model']:
        device_query['model'] = form['model']
    if form['brand']:
        device_query['brand'] = form['brand']
    if form['tag_code']:
        device_query['tag_code'] = form['tag_code']
    devices = Device.query.filter_by()
    if device_query:
        devices = devices.filter_by(
            **device_query
        )
        achievements = achievements.filter(
            Achievement.device_code.in_(
                map(lambda x: x.code, devices)
            )
        )
    if form['manufacturer_date']:
        achievements = achievements.filter(
            db.cast(Achievement.manufacturer_date, db.DATE) == form['manufacturer_date'])
    total_count = achievements.count()
    achievements = achievements.paginate(current_page, page_size, False).items
    data = map(lambda x: transform(x), achievements)
    data = list(data)
    return reply(success=True,
                 data={
                     'items': data,
                     'total_count': total_count,
                 },
                 message='done', error_code=const.success)


@login_required_api
@ensure_session_removed
def query_achievement_description_by_id():
    achievement_id = request.args.get('id')
    if not achievement_id:
        return reply(success=False, message='参数错误', error_code=const.param_err)
    achievement = Achievement.query.filter_by(
        id=achievement_id
    ).first()
    if not achievement:
        return reply(success=False, message='该设备成果不存在', error_code=const.param_illegal)
    return reply(success=True,
                 data={
                     'achievement_description': achievement.achievement_description,
                     'patent_description': achievement.patent_description,
                     'paper_description': achievement.paper_description,
                     'competition_description': achievement.competition_description,
                     'achievement_remark': achievement.achievement_remark,

                 },
                 message='done', error_code=const.success)
