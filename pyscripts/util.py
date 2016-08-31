import io
import json
import os
import shutil
import sys

SAVE_DIR = os.path.join(os.getcwd(), "__save")
PYSCRIPTS = os.path.join(os.getcwd(), "pyscripts")
PSSCRIPTS = os.path.join(os.getcwd(), "psscripts")
CMDSCRIPTS = os.path.join(os.getcwd(), "cmdscripts")
VMPATH = os.path.join(SAVE_DIR, "vms")

DEBUG = True


def debug(*args, **kwargs):
    if DEBUG:
        print("[!]", *args, **kwargs)


def load_xml(location):
    import xml.etree.ElementTree
    root = xml.etree.ElementTree.parse(location).getroot()
    return root


def parse_input(defaults=None):
    if defaults is None: defaults = {}
    for item in sys.argv[1:]:
        if item.startswith('-') and '=' in item:
            key, value = item[1:].split('=', 1)
            if value.isdigit(): value = int(value)
            elif value.replace('.', '').isdigit(): value = float(value)
            elif value.lower() == "true": value = True
            elif value.lower() == "false": value = False
            defaults[key] = value
    return defaults


def test_path(path, mode="any"):
    isdir = os.path.isdir(path)
    isfile = os.path.isfile(path)
    if mode[0] == "a":
        return isdir or isfile
    elif mode[0] == "f":
        return isfile
    elif mode[0] == "d":
        return isdir
    else:
        raise ValueError("Invalid mode {}".format(mode))


def pyscript(file, silent=True):
    path = os.path.join(PYSCRIPTS, file)
    assert test_path(path, "f") or silent
    return path


def psscript(file, silent=True):
    path = os.path.join(PSSCRIPTS, file)
    assert test_path(path, "f") or silent
    return path


def cmdscript(file, silent=True):
    path = os.path.join(CMDSCRIPTS, file)
    assert test_path(path, "f") or silent
    return path

def savefile(file, silent=True):
    path = os.path.join(SAVE_DIR, file)
    assert test_path(path, "a") or silent
    return path


def rmtree(path, silent=False):
    exists = test_path(path)
    if exists:
        try:
            shutil.rmtree(path)
        except OSError:
            os.popen("rmdir /S /Q \"{}\"".format(path))
    elif not silent:
        raise FileNotFoundError("{} not found".format(path))


def clean():
    for directory in os.listdir(SAVE_DIR):
        path = os.path.join(SAVE_DIR, directory)
        if (directory != "vms"):
            rmtree(path)


def list_vms():
    return [(dir_name, os.path.join(VMPATH, dir_name)) for dir_name in os.listdir(VMPATH) if test_path(os.path.join(VMPATH, dir_name), 'd')]


def save_json(python_object, path, filename=None):
    if filename: path = os.path.join(path, filename)
    with io.open(os.path.join(path), 'w') as context:
        context.write(json.dumps(python_object, indent=2, sort_keys=True))

def mkdir(path, dir_name, silent=True):
    try:
        os.mkdir(os.path.join(path, dir_name))
    except FileExistsError as e:
        if silent:
            raise FileExistsError(e)