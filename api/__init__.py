from api.db_test import db_add
from api.login import login, login_out
from api.device import add_device, delete_device, query_device, query_device_description_by_id
from api.achievement import add_achievement, delete_achievement, query_achievement, query_achievement_description_by_id
from api.department import add_department, delete_department, query_department
from api.member import add_member, delete_member, query_member
from api.manufacturer import add_manufacturer, delete_manufacturer, query_manufacturer
from api.device_rent import rent_device, delete_device_rent, return_device, query_rent_device

__all__ = [
    'db_add',
    'login',
    'login_out',
    'add_device',
    'delete_device',
    'add_achievement',
    'delete_achievement',
    'add_department',
    'delete_department',
    'add_member',
    'delete_member',
    'add_manufacturer',
    'delete_manufacturer',
    'rent_device',
    'return_device',
    'delete_device_rent',
    'query_department',
    'query_member',
    'query_manufacturer',
    'query_device',
    'query_device_description_by_id',
    'query_rent_device',
    'query_achievement',
    'query_achievement_description_by_id',
]
