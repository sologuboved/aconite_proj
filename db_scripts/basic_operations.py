import json
import os
import re
import sys
import time


def load_utf_json(json_file):
    with open(json_file, encoding='utf8') as data:
        return json.load(data)


def dump_utf_json(entries, json_file):
    with open(json_file, 'w', encoding='utf-8') as handler:
        json.dump(entries, handler, ensure_ascii=False, indent=2)


def which_watch(func):

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(func.__name__, 'took', time.strftime("%H:%M:%S", time.gmtime(time.time() - start)))
        print()
        return result

    return wrapper


def write_pid():
    prefix = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    previous_pid = find_previous_pid(prefix)
    if previous_pid:
        print("\nRemoving {}...".format(previous_pid))
        os.remove(previous_pid)
    pid_fname = '{}_{}.pid'.format(prefix, str(os.getpid()))
    print("Writing {}\n".format(pid_fname))
    with open(pid_fname, 'w') as handler:
        handler.write(str())
    return pid_fname


def delete_pid(pid_fname):
    try:
        os.remove(pid_fname)
    except FileNotFoundError as e:
        print(str(e))


def find_previous_pid(prefix):
    for fname in os.listdir('.'):
        if re.fullmatch(r'{}_\d+\.pid'.format(prefix), fname):
            return fname


def sweep_out(*fnames):
    print("Sweeping out {}...".format(", ".join(fnames)))
    for fname in fnames:
        os.remove(fname)
