# -*- coding: utf-8 -*-
"""
Assembly: utils.py

This module contains some common functions, and also exposes under the `utils`
namespace some 3rd party functions. ie: 
    utils.slugify 
    utils.dasherize
    
others:
    utils.is_email_valid
    utils.md5(string)

functions in here are independents from configs and setup
"""

from __future__ import division
import os
import re
import time
import json
import uuid
import arrow
import string
import random
import hashlib
import datetime
from slugify import slugify
from distutils.file_util import copy_file, move_file
from distutils.dir_util import copy_tree, remove_tree, mkpath
from inflection import (dasherize,
                        underscore,
                        camelize,
                        pluralize,
                        singularize,
                        titleize,
                        ordinalize,
                        ordinal)

"""
--- Reference ---
gen_md5
gen_uuid
gen_uuid_hex
to_json
chunk_list
in_any_list
dict_replace
list_replace
DotDict
is_valid_email
is_valid_password
is_valid_username
is_valid_url

#lib: slugify
slugify 

#lib: inflection
camelize
titleize
dasherize
underscore
plurialize
singularize
ordinalize
ordinal

copy_file, 
move_file,
copy_tree, 
remove_tree, 
mkpath
"""

def is_valid_email(email):
    """
    Check if email is valid
    """
    pattern = re.compile(r'[\w\.-]+@[\w\.-]+[.]\w+')
    return bool(pattern.match(email))


def is_valid_password(password):
    """
    - min length is 6 and max length is 25
    - at least include a digit number,
    - at least a upcase and a lowcase letter
    - at least a special characters
    :return bool:
    """
    pattern = re.compile('^(?=\S{6,25}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')
    return bool(pattern.match(password))


def is_valid_username(username):
    """
    Check if a valid username.
    valid:
        oracle
        bill-gates
        steve.jobs
        micro_soft
    not valid
        Bill Gates - no space allowed
        me@yo.com - @ is not a valid character
    :param username: string
    :return:
    """
    pattern = re.compile(r"^[a-zA-Z0-9_.-]+$")
    return bool(pattern.match(username))


def is_valid_url(url):
    """
    Check if url is valid
    """
    pattern = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            #r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(pattern.match(url))


def gen_md5(value):
    """
    Generates MD5
    :param value: string
    :return: string
    """
    return hashlib.md5(value.encode()).hexdigest()


def gen_uuid():
    """
    Generates and returns a UUID 4 value
    :return: string
    """
    return str(uuid.uuid4())

def gen_uuid_hex():
    """
    Creates and returns a UUID 4 hex value
    :return: string
    """
    return uuid.uuid4().hex


def chunk_list(items, size):
    """
    Return a list of chunks
    :param items: List
    :param size: int The number of items per chunk
    :return: List
    """
    size = max(1, size)
    return [items[i:i + size] for i in range(0, len(items), size)]


def in_any_list(list1, list2):
    """
    Check if any items in list1 are in list2
    :param list1: list
    :param list2: list
    :return:
    """
    list1 = list1.split(" ") if isinstance(list1, str) else list1
    list2 = list2.split(" ") if isinstance(list2, str) else list2
    return any(i in list2 for i in list1)

def generate_random_string(length=8):
    """
    Generate a random string
    """
    char_set = string.ascii_uppercase + string.digits
    return ''.join(random.sample(char_set * (length - 1), length))


def generate_random_hash(size=32):
    """
    Return a random hash key
    :param size: The max size of the hash
    :return: string
    """
    return os.urandom(size//2).encode('hex')


def list_replace(subject_list, replacement, string):
    """
    To replace a list of items by a single replacement
    :param subject_list: list
    :param replacement: string
    :param string: string
    :return: string
    """
    for s in subject_list:
        string = string.replace(s, replacement)
    return string


def dict_replace(subject_dict, string):
    """
    Replace a dict map, key to its value in the stirng
    :param subject_dict: dict
    :param string: string
    :return: string
    """
    for i, j in subject_dict.items():
        string = string.replace(i, j)
    return string


def to_json(d):
    """
    Convert data to json. It formats datetime/arrow time
    :param d: dict or list
    :return: json data
    """
    return json.dumps(d, cls=_JSONEncoder)


class _JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, arrow.Arrow):
            return obj.for_json()
        elif isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

class DotDict(dict):
    """
    A dict extension that allows dot notation to access the data.
    ie: dict.get('key.key2.0.keyx')
    my_dict = {...}
    d = DotDict(my_dict)
    d.get("key1")
    d.get("key1.key2")
    d.get("key3.key4.0.keyX")

    Still have the ability to access it as a normal dict
    d[key1][key2]
    """
    def get(self, key, default=None):
        """
        Access data via
        :param key:
        :param default: the default value
        :return:
        """
        try:
            val = self
            if "." not in key:
                return self[key]
            for k in key.split('.'):
                if k.isdigit():
                    k = int(k)
                val = val[k]
            return val
        except (TypeError, KeyError, IndexError) as e:
            return default


def flatten_config_property(key, config):
    """
    To flatten a config property
    This method is mutable
    Having a flask config or an object:
    class Conf(object):
      AWS = {
        "ACCESS_KEY_ID": "",
        "SECRET_ACCESS_KEY": ""
      }

    app = Flask(__name__)
    app.config.from_object(Conf())

    flatten_config_property("AWS", app.config)

    it will flatten the config to be:
      AWS_ACCESS_KEY_ID
      AWS_SECRET_ACCESS_KEY

    If the key exists already, it will not modify it

    :param key: string - the key to flatten
    :param dict: app.config - the flask app.config or dict
    """
    if key in config:
        for k, v in config[key].items():
            _ = "%s_%s" % (key, k.upper())
            if _ not in config:
                config[_] = v

# ------------
# internal usage

def prepare_view_response(data):
    """
    Prepare a view response from a data returned
    params data (dict, tuple): the data from the view response
    return tuple: data:dict, status:int|None, headers:dict|None
    """
    if isinstance(data, dict) or data is None:
        data = {} if data is None else data
        return data, 200, None
    elif isinstance(data, tuple):
        data, status, headers = prepare_view_response_set_from_tuple(data)
        return data or {}, status, headers
    return data, None, None

def prepare_view_response_set_from_tuple(tuple_):
    """
    Helper function to normalize view return values .
    It always returns (dict, status, headers). Missing values will be None.
    For example in such cases when tuple_ is
      (dict, status), (dict, headers), (dict, status, headers),
      (dict, headers, status)

    It assumes what status is int, so this construction will not work:
    (dict, None, headers) - it doesn't make sense because you just use
    (dict, headers) if you want to skip status.
    """
    v = tuple_ + (None,) * (3 - len(tuple_))
    return v if isinstance(v[1], int) else (v[0], v[2], v[1])
