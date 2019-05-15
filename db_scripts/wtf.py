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


def add_languages(*args):
    for language in args:
        Language(name=language).save()
    print(Language.objects.all())


if __name__ == '__main__':
    add_languages('Ru', 'En')
