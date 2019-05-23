from db_scripts.basic_operations import load_utf_json
from db_scripts.global_vars import *
from db_scripts.lj_entries_adder import get_location


class SomeClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b


def check():
    # locs = set()
    years = set()
    for poem in load_utf_json(LJ_POEMS_JSON):
        # if (poem[INSPIRED_BY_AUTH] or poem[INSPIRED_BY_TITLE]) and not poem[IS_DERIVATIVE]:
        #     print(poem)
        # if (poem[TRANSL_FROM_AUTH] or poem[TRANSL_FROM_TITLE]) and poem[IS_DERIVATIVE]:
        #     print(poem)
        # if sum(True if poem[fieldname] else False for fieldname in (TRANSL_FROM_AUTH, TRANSL_FROM_TITLE)) == 0:
        #     print(poem)
        # if poem[TRANSL_FROM_AUTH]:
        #     print(poem[TRANSL_FROM_LANG], '-', poem[TRANSL_FROM_TITLE])
        # if poem[IS_DERIVATIVE]:
        #     print(poem[LANG], poem[INSPIRED_BY_AUTH], poem[INSPIRED_BY_TITLE])
        # if poem[ORIGINAL_BY]:
        #     print(poem[ORIGINAL_TITLE])
        # print(get_title(poem))
        # if poem[WHERE]:
        #     ru_name, en_name = get_location(poem[WHERE])
        #     locs.add(" | ".join([ru_name, en_name]))
        years.add(poem[YEAR])

    # for loc in locs:
    #     print(loc)
    for year in years:
        print(year)


if __name__ == '__main__':
    # dictionary = {'a': 0, 'b': 1}
    # some_class = SomeClass(**dictionary)
    # print(some_class.a, some_class.b)
    check()
