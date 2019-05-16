from db_scripts.basic_operations import load_utf_json, dump_utf_json
from db_scripts.global_vars import *


def add_fields(json_fname, default, *fieldnames):
    poems = list()
    for poem in load_utf_json(json_fname):
        poem.update({fieldname: default for fieldname in fieldnames})
        poems.append(poem)
    dump_utf_json(poems, json_fname)


if __name__ == '__main__':
    # add_fields(LJ_POEMS_JSON, str(), INSPIRED_BY_AUTH, INSPIRED_BY_TITLE)
    pass
