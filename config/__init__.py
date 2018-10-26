from six import string_types
from werkzeug.utils import import_string


class Config(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def from_object(self, obj):
        if isinstance(obj, string_types):
            obj = import_string(obj)
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)


config = Config()
config.from_object('config.conf')

if __name__ == '__main__':
    print(config['SQLALCHEMY_TRACK_MODIFICATIONS'])
