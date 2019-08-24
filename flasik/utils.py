# -*- coding: utf-8 -*-
"""
utils.py

This module contains some common functions, and also exposes under the `utils`
namespace some 3rd party functions. ie: 
    utils.slugify 
    utils.dasherize
    
others:
    utils.is_email_valid
    utils.md5(string)

"""

from __future__ import division
import os
import re
import inspect
import time
import datetime
import arrow
import string
import random
import socket
import itsdangerous
import humanize
import pkg_resources
import urllib
import hashlib
import json
import uuid
from six import string_types
from slugify import slugify
from werkzeug.utils import import_string
from distutils.dir_util import (copy_tree as copy_dir,
                                remove_tree as remove_dir,
                                mkpath as make_dirs)
from distutils.file_util import copy_file, move_file
from inflection import (dasherize,
                        underscore,
                        camelize,
                        pluralize,
                        singularize,
                        titleize)
from six.moves.urllib.parse import (urlparse,
                                    urlencode,
                                    unquote_plus as urllib_unquote_plus)


def is_email_valid(email):
    """
    Check if email is valid
    """
    pattern = re.compile(r'[\w\.-]+@[\w\.-]+[.]\w+')
    return bool(pattern.match(email))


def is_password_valid(password):
    """
    Check if a password is valid
    """
    pattern = re.compile(r"^.{4,75}$")
    return bool(pattern.match(password))


def is_username_valid(username):
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


def is_url_valid(url):
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


def urldecode(s):
    return urllib_unquote_plus(s)


def md5(value):
    """
    Create MD5
    :param value:
    :return:
    """
    m = hashlib.md5()
    m.update(value)
    return str(m.hexdigest())


def guid():
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


def in_any_list(items1, items2):
    """
    Check if any items are in list2
    :param items1: list
    :param items2: list
    :return:
    """
    return any(i in items2 for i in items1)


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


class dict_dot(dict):
    """
    A dict extension that allows dot notation to access the data.
    ie: dict.get('key.key2.0.keyx')
    my_dict = {...}
    d = dict_dot(my_dict)
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


def sign_jwt(data, secret_key, expires_in, salt=None, **kw):
    """
    To create a signed JWT
    :param data:
    :param secret_key:
    :param expires_in:
    :param salt:
    :param kw:
    :return: string
    """
    s = itsdangerous.TimedJSONWebSignatureSerializer(secret_key=secret_key,
                                                     expires_in=expires_in,
                                                     salt=salt,
                                                      **kw)
    return s.dumps(data)


def unsign_jwt(token, secret_key, salt=None, **kw):
    """
    To unsign a JWT token
    :param token:
    :param kw:
    :return: mixed data
    """
    s = itsdangerous.TimedJSONWebSignatureSerializer(secret_key, salt=salt, **kw)
    return s.loads(token)


class TimestampSigner2(itsdangerous.TimestampSigner):
    expires_in = 0

    def get_timestamp(self):
        now = datetime.datetime.utcnow()
        expires_in = now + datetime.timedelta(seconds=self.expires_in)
        return int(expires_in.strftime("%s"))

    @staticmethod
    def timestamp_to_datetime(ts):
        return datetime.datetime.fromtimestamp(ts)


class URLSafeTimedSerializer2(itsdangerous.URLSafeTimedSerializer):
    default_signer = TimestampSigner2

    def __init__(self, secret_key, expires_in=3600, salt=None, **kwargs):
        self.default_signer.expires_in = expires_in
        super(self.__class__, self).__init__(secret_key, salt=salt, **kwargs)


def sign_url_safe(data, secret_key, expires_in=None, salt=None, **kw):
    """
    To sign url safe data.
    If expires_in is provided it will Time the signature
    :param data: (mixed) the data to sign
    :param secret_key: (string) the secret key
    :param expires_in: (int) in minutes. Time to expire
    :param salt: (string) a namespace key
    :param kw: kwargs for itsdangerous.URLSafeSerializer
    :return:
    """
    if expires_in:
        expires_in *= 60
        s = URLSafeTimedSerializer2(secret_key=secret_key,
                                    expires_in=expires_in,
                                    salt=salt,
                                    **kw)
    else:
        s = itsdangerous.URLSafeSerializer(secret_key=secret_key,
                                           salt=salt,
                                           **kw)
    return s.dumps(data)


def unsign_url_safe(token, secret_key, salt=None, **kw):
    """
    To sign url safe data.
    If expires_in is provided it will Time the signature
    :param token:
    :param secret_key:
    :param salt: (string) a namespace key
    :param kw:
    :return:
    """
    if len(token.split(".")) == 3:
        s = URLSafeTimedSerializer2(secret_key=secret_key, salt=salt, **kw)
        value, timestamp = s.loads(token, max_age=None, return_timestamp=True)
        now = datetime.datetime.utcnow()
        if timestamp > now:
            return value
        else:
            raise itsdangerous.SignatureExpired(
                'Signature age %s < %s ' % (timestamp, now),
                payload=value,
                date_signed=timestamp)
    else:
        s = itsdangerous.URLSafeSerializer(secret_key=secret_key, salt=salt, **kw)
        return s.loads(token)


def sign_data(data, secret_key, expires_in=None, salt=None, **kw):
    if expires_in:
        pass
    else:
        s = itsdangerous.Serializer(secret_key=secret_key, salt=salt, **kw)
        return s.dumps(data)


def unsign_data(data, secret_key, salt=None, **kw):
    s = itsdangerous.Serializer(secret_key=secret_key, salt=salt, **kw)
    return s.loads(data)

# ------------------------------------------------------------------------------


def to_json(d):
    """
    Convert data to json. It formats datetime/arrow time
    :param d: dict or list
    :return: json data
    """
    return json.dumps(d, cls=_MochaJSONEncoder)


class _MochaJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, arrow.Arrow):
            return obj.for_json()
        elif isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class InspectDecoratorCompatibilityError(Exception):
    pass


class _InspectMethodsDecorators(object):
    """
    This class attempt to retrieve all the decorators in a method
    """
    def __init__(self, method):
        self.method = method
        self.decos = []

    def parse(self):
        """
        Return the list of string of all the decorators found
        """
        self._parse(self.method)
        return list(set([deco for deco in self.decos if deco]))

    @classmethod
    def extract_deco(cls, line):
        line = line.strip()
        if line.startswith("@"):
            if "(" in line:
                line = line.split('(')[0].strip()
            return line.strip("@")

    def _parse(self, method):
        argspec = inspect.getargspec(method)
        args = argspec[0]
        if args and args[0] == 'self':
            return argspec
        if hasattr(method, '__func__'):
            method = method.__func__
        if not hasattr(method, '__closure__') or method.__closure__ is None:
            raise InspectDecoratorCompatibilityError

        closure = method.__closure__
        for cell in closure:
            inner_method = cell.cell_contents
            if inner_method is method:
                continue
            if not inspect.isfunction(inner_method) \
                and not inspect.ismethod(inner_method):
                continue
            src = inspect.getsourcelines(inner_method)[0]
            self.decos += [self.extract_deco(line) for line in src]
            self._parse(inner_method)


def get_decorators_list(method):
    """
    Shortcut to InspectMethodsDecorators
    :param method: object
    :return: List
    """
    kls = _InspectMethodsDecorators(method)
    return kls.parse()
