from django.conf import settings
from django.core.wsgi import get_wsgi_application
import secret_data

settings.configure(DATABASES={
                       'default': {
                           'ENGINE': 'django.db.backends.postgresql_psycopg2',
                           'NAME': secret_data.DB_NAME,
                           'USER': secret_data.DB_USERNAME,
                           'PASSWORD': secret_data.DB_PASSWORD,
                           'HOST': '127.0.0.1',
                           'PORT': '',
                       }
                   },
                   SHARD_EPOCH=0,
                   INSTALLED_APPS=('aconite_app',))
get_wsgi_application()

from aconite_app.models import *
from db_scripts.basic_operations import *


def add_lj_entries(json_fname):
    for entry in load_utf_json(json_fname):
        if entry['original_title']:
            print(entry)
            print()


if __name__ == '__main__':
    add_lj_entries('lj_poems.json')

