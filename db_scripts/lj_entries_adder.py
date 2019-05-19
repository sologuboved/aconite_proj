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
from db_scripts.global_vars import *


class Poem:

    def __init__(self, poem):
        self._poem = poem
        self._is_translation = self.is_translation()
        self._work = None
        self._content = None

    def is_translation(self):
        if self._poem[TRANSL_FROM_AUTH]:
            return True
        else:
            return False

    def get_title(self):
        if self._poem[TITLE]:
            title = self._poem[TITLE]
        else:
            title = self._poem[TEXT].split('\n')[0]
            title = title[0].upper() + title[1:]
            indx = len(title)
            while indx > 0:
                indx -= 1
                if title[indx].isalpha():
                    break
            if indx >= 0:
                title = title[: indx + 1]
            title += '...'
        return title

    def add_poem(self):
        self.create_core()
        author = create_entry(Person, {RU_NAME: "Ольга Куминова", EN_NAME: "Olga Kuminova"})
        self._work.authors.add(author)


    def create_core(self):
        simple_fields = {fieldname: nonefy(self._poem[fieldname]) for fieldname in(DAY, MONTH, YEAR)}
        simple_fields.update({TITLE: self.get_title(),
                              ORIGINAL_TITLE: self._poem[TITLE],
                              IS_TRANSLATION: self._is_translation})
        self._work = Work(**simple_fields)
        self._work.save()


def create_entry(relation, fields):
    return relation.objects.get_or_create(**fields)

def get_title(poem):
    if poem[TITLE]:
        title = poem[TITLE]
    else:
        title = poem[TEXT].split('\n')[0]
        title = title[0].upper() + title[1:]
        indx = len(title)
        while indx > 0:
            indx -= 1
            if title[indx].isalpha():
                break
        if indx >= 0:
            title = title[: indx + 1]
        title += '...'
    return title


def get_author_name(lang, name):
    if lang == 'en':
        return None, nonefy(name)
    else:
        return nonefy(name), None


def get_location(location):
    return map(lambda x: x.strip(), location.split('/'))


def add_lj_entries(json_fname):
    for poem in load_utf_json(json_fname):
        if poem[TRANSL_FROM_AUTH]:
            is_translation = True
        else:
            is_translation = False
        simple_fields = {fieldname: nonefy(poem[fieldname]) for fieldname in(DAY, MONTH, YEAR)}
        simple_fields.update({TITLE: get_title(poem),
                              ORIGINAL_TITLE: poem[TITLE],
                              IS_TRANSLATION: is_translation})
        work = Work(**simple_fields)
        work.save()
        author = Person.objects.get_or_create(ru_name="Ольга Куминова", en_name="Olga Kuminova")
        work.authors.add(author)
        if is_translation:
            transl_from_lang = poem[TRANSL_FROM_LANG]
            transl_from_author = poem[TRANSL_FROM_AUTH]
            if transl_from_author == "Ольга Куминова":
                ru_name = transl_from_author
                en_name = "Olga Kuminova"
            else:
                ru_name, en_name = get_author_name(transl_from_lang, transl_from_author)
            original_author = Person.objects.get_or_create(ru_name=ru_name, en_name=en_name)
            original_language = Language.objects.get_or_create(name=transl_from_lang)
            original_work = Inspiration.objects.get_or_create(title=poem[TRANSL_FROM_TITLE])
            original_work.authors.add(original_author)
            original_work.languages.add(original_language)
            original_work.save()
            work.inspirations.add(original_work)
        if poem[IS_DERIVATIVE]:
            ru_name, en_name = get_author_name(poem[LANG], poem[INSPIRED_BY_AUTH])
            original_author = Person.objects.get_or_create(ru_name=ru_name, en_name=en_name)
            original_work = Inspiration.objects.get_or_create(title=poem[INSPIRED_BY_TITLE])
            original_work.authors.add(original_author)
            original_work.save()
            work.inspirations.add(original_work)
        language = Language.objects.get_or_create(name=poem[LANG])
        work.languages.add(language)
        loc = poem[WHERE]
        if loc:
            ru_name, en_name = get_location(loc)
            location = Location.objects.get_or_create(ru_name=ru_name, en_name=en_name)
            work.locations.add(location)
        ru_name, en_name = {True: ('танка', 'tanka'), False: ('стихотворение', 'poem')}[poem[IS_TANKA]]
        work.genre = Genre.objects.get_or_create(is_prose=False, ru_name=ru_name, en_name=en_name)
        work.save()
        content = Content(title=None, num_part=1, text=poem[TEXT], work=work)
        content.save()


if __name__ == '__main__':
    # add_lj_entries('lj_poems.json')
    pass
