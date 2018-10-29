# coding: utf-8


def reply(success=True, data={}, message='', error_code=0):
    return dict(
        success=success,
        data=data,
        message=message,
        error_code=error_code
    )


def query_reply(success=True, data={}, paging={}, message='', error_code=0):
    return dict(
        success=success,
        data=data,
        message=message,
        paging=paging,
        error_code=error_code
    )
