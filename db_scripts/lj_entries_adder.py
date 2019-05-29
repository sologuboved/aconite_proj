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

    def add_to_db(self):
        self.create_core()
        self.add_author()
        self.add_genre()
        self.add_location()
        self.add_genre()
        self.add_content()
        if self._is_translation:
            self.add_original()
        if self._poem[IS_DERIVATIVE]:
            self.add_canon()
        self._work.save()

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
        print(title)
        return title

    def create_core(self):
        simple_fields = dict(zip([ORIGINAL_TITLE, YEAR, YEAR_DEMO, MONTH, DAY],
                                 [nonefy(self._poem[fieldname]) for fieldname in [TITLE, YEAR, YEAR, MONTH, DAY]]))
        simple_fields.update({TITLE: self.get_title(), IS_TRANSLATION: self._is_translation})
        self._work = Work(**simple_fields)
        self._work.save()

    def add_original(self):
        language = self._poem[TRANSL_FROM_LANG]
        author = self._poem[TRANSL_FROM_AUTH]
        if author == "Ольга Куминова":
            ru_name = author
            en_name = "Olga Kuminova"
        else:
            ru_name, en_name = get_author_name(language, author)
        source_work = create_entry(Inspiration, {TITLE: self._poem[TRANSL_FROM_TITLE]})
        source_work.authors.add(create_entry(Person, {RU_NAME: ru_name, EN_NAME: en_name}))
        source_work.languages.add(create_entry(Language, {NAME: language}))
        source_work.save()
        self._work.inspirations.add(source_work)

    def add_canon(self):
        ru_name, en_name = get_author_name(self._poem[LANG], self._poem[INSPIRED_BY_AUTH])
        source_work = create_entry(Inspiration, {TITLE: self._poem[INSPIRED_BY_TITLE]})
        source_work.authors.add(create_entry(Person, {RU_NAME: ru_name, EN_NAME: en_name}))
        source_work.save()
        self._work.inspirations.add(source_work)

    def add_author(self):
        self._work.authors.add(create_entry(Person, {RU_NAME: "Ольга Куминова", EN_NAME: "Olga Kuminova"}))

    def add_language(self):
        self._work.languages.add(create_entry(Language, {NAME: self._poem[LANG]}))

    def add_location(self):
        loc = self._poem[WHERE]
        if loc:
            ru_name, en_name = get_location(loc)
            self._work.locations.add(create_entry(Location, {RU_NAME: ru_name, EN_NAME: en_name}))

    def add_genre(self):
        ru_name, en_name = {(True, False): ('танка', 'tanka'),
                            (False, True): ('песня', 'song'),
                            (False, False): ('стихотворение', 'poem')}[(self._poem[IS_TANKA], self._poem[IS_SONG])]
        self._work.genre = create_entry(Genre, {IS_PROSE: False, RU_NAME: ru_name, EN_NAME: en_name})

    def add_content(self):
        Content(title=None, num_part=1, text=self._poem[TEXT], work=self._work).save()


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


@which_watch
def add_lj_entries(json_fname):
    poems = load_utf_json(json_fname)
    total = len(poems)
    count = 0
    for poem in poems:
        count += 1
        print("Uploading {} / {}:".format(count, total), end=" ")
        Poem(poem).add_to_db()


if __name__ == '__main__':
    # add_lj_entries('lj_poems.json')
    pass