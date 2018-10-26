import wtforms

from wtforms.validators import *

from flask import request

loginForm = {
    'username': True,
    'password': True,
}

deleteByIdForm = {
    'id': True,
}

addDeviceForm = {
    'code': True,
    'name': True,
    'model': True,
    'brand': True,
    'tag_code': True,
    'description': True,
    'manufacturer_date': True,
    'manufacturer_id': True,
    'department_id': True,
}

addAchievementForm = {
    'device_code': True,
    'member_code': True,
    'manufacturer_date': True,
    'achievement_description': True,
    'patent_description': True,
    'paper_description': True,
    'competition_description': True,
    'achievement_remark': True,
}

addDepartmentForm = {
    'code': True,
    'name': True,
}

addMemberForm = {
    'code': True,
    'name': True,
    'department_id': True,
}

addManufacturerForm = {
    'name': True,
}

rentDeviceForm = {
    'device_code': True,
    'borrower_member_code': True,
    'borrow_date': True,
    'borrow_remark': True,
    'expect_return_date': True,
}

returnDeviceForm = {
    'device_code': True,
    'returner_member_code': True,
    'return_date': True,
    'return_remark': True,
}

queryMemberForm = {
    'id': False,
    'code': False,
    'name': False,
}

queryDeviceForm = {
    'code': False,
    'name': False,
    'model': False,
    'brand': False,
    'tag_code': False,
    'status': False,
    'department_id': False,
    'manufacturer_date': False,
    'manufacturer_id': False,
}

queryDeviceLendForm = {
    'device_code': False,
    'device_name': False,
    'model': False,
    'brand': False,
    'tag_code': False,
    'status': False,
    'department_id': False,
    'borrower_member_code': False,
    'borrower_department_id': False,
    'borrow_date': False,
    'returner_member_code': False,
    'returner_department_id': False,
    'expect_return_date': False,
    'real_return_date': False,
}

queryAchievementForm = {
    'device_code': False,
    'device_name': False,
    'model': False,
    'brand': False,
    'tag_code': False,
    'member_code': False,
    'manufacturer_date': False,
    'department_id': False,
}

form_dict = {
    'loginForm': loginForm,
    'deleteByIdForm': deleteByIdForm,
    'addDeviceForm': addDeviceForm,
    'addAchievementForm': addAchievementForm,
    'addDepartmentForm': addDepartmentForm,
    'addMemberForm': addMemberForm,
    'addManufacturerForm': addManufacturerForm,
    'rentDeviceForm': rentDeviceForm,
    'returnDeviceForm': returnDeviceForm,
    'queryMemberForm': queryMemberForm,
    'queryDeviceForm': queryDeviceForm,
    'queryDeviceLendForm': queryDeviceLendForm,
    'queryAchievementForm': queryAchievementForm,
}


def get_form(key):
    return request.form.get(key, None)


def parsing_form(form_key):
    pattern = form_dict[form_key]
    form = {}
    for key in pattern:
        val = get_form(key)
        if pattern[key] and not val:
            return False, None
        form[key] = val
    return True, form


class DeleteByIdForm(wtforms.Form):
    id = wtforms.StringField(validators=[DataRequired()])


class AddDeviceForm(wtforms.Form):
    code = wtforms.StringField(validators=[DataRequired()])
    name = wtforms.StringField(validators=[DataRequired()])
    model = wtforms.StringField(validators=[DataRequired()])
    brand = wtforms.StringField(validators=[DataRequired()])
    tag_code = wtforms.StringField(validators=[DataRequired()])
    description = wtforms.StringField(validators=[DataRequired()])
    manufacturer_date = wtforms.DateTimeField(validators=[DataRequired()])
    manufacturer_id = wtforms.StringField(validators=[DataRequired()])
    department_id = wtforms.StringField(validators=[DataRequired()])


class AddAchievementForm(wtforms.Form):
    device_code = wtforms.StringField(validators=[DataRequired()])
    member_code = wtforms.StringField(validators=[DataRequired()])
    manufacturer_date = wtforms.DateTimeField(validators=[DataRequired()])
    achievement_description = wtforms.StringField(validators=[DataRequired()])
    patent_description = wtforms.StringField(validators=[DataRequired()])
    paper_description = wtforms.StringField(validators=[DataRequired()])
    competition_description = wtforms.StringField(validators=[DataRequired()])
    achievement_remark = wtforms.StringField(validators=[DataRequired()])


class AddDepartmentForm(wtforms.Form):
    code = wtforms.StringField(validators=[DataRequired()])
    name = wtforms.StringField(validators=[DataRequired()])


class AddMemberForm(wtforms.Form):
    code = wtforms.StringField(validators=[DataRequired()])
    name = wtforms.StringField(validators=[DataRequired()])
    department_id = wtforms.StringField(validators=[DataRequired()])


class AddManufacturerForm(wtforms.Form):
    name = wtforms.StringField(validators=[DataRequired()])


class RentDeviceForm(wtforms.Form):
    device_code = wtforms.StringField(validators=[DataRequired()])
    borrower_member_code = wtforms.StringField(validators=[DataRequired()])
    borrow_date = wtforms.DateTimeField(validators=[DataRequired()])
    borrow_remark = wtforms.StringField(validators=[DataRequired()])
    expect_return_date = wtforms.DateTimeField(validators=[DataRequired()])


class ReturnDeviceForm(wtforms.Form):
    device_code = wtforms.StringField(validators=[DataRequired()])
    returner_member_code = wtforms.StringField(validators=[DataRequired()])
    return_date = wtforms.DateTimeField(validators=[DataRequired()])
    return_remark = wtforms.StringField(validators=[DataRequired()])


class QueryMemberForm(wtforms.Form):
    id = wtforms.StringField()
    code = wtforms.StringField()
    name = wtforms.StringField()


class QueryDefaultForm(wtforms.Form):
    page = wtforms.IntegerField()
    limit = wtforms.IntegerField()


class QueryDeviceLendForm(wtforms.Form):
    device_code = wtforms.StringField()
    device_name = wtforms.StringField()
    model = wtforms.StringField()
    brand = wtforms.StringField()
    tag_code = wtforms.StringField()
    status = wtforms.StringField()
    department_id = wtforms.StringField()
    borrower_member_code = wtforms.StringField()
    borrower_department_id = wtforms.StringField()
    borrow_date = wtforms.StringField()
    returner_code = wtforms.StringField()
    returner_department_id = wtforms.StringField()
    return_date = wtforms.StringField()
    expect_return_date = wtforms.StringField()
    real_return_date = wtforms.StringField()
