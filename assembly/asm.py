# -*- coding: utf-8 -*-
"""
Assembly: asm
Set of helpers and functions. These functions are dependents of some config and setup
"""

import re
import six
import copy
import blinker
import logging
import inspect
import datetime
import functools
import itsdangerous
import flask_cloudy
from passlib.hash import bcrypt
from . import (app_context, ext, config, utils)
from flask import (send_file, session, g)

__all__ = [
    "signal",
    "flash_data",
    "get_flashed_data",
    "send_mail",
    "get_file",
    "upload_file",
    "delete_file",
    "download_file",
    "hash_string",
    "verify_hashed_string",
    "encode_jwt",
    "decode_jwt",
    "sign_data",
    "unsign_data"
]

# ------------------------------------------------------------------------------
# signal

__signals_namespace = blinker.Namespace()


def signal(fn):
    """
    @signal
    A decorator to mark a function as a signal emitter
    It will turn the function into a decorator that can be used to
    receive signal with: $fn_name.pre, $fn_name.post
    *pre will execute before running the function
    *post will run after running the function

    # What are signals
    Signals help you decouple applications by sending notifications 
    when actions occur elsewhere in the application. 
    In short, signals allow certain senders to notify subscribers that 
    something happened.

    # Example:

    #1. Create a function, and add the @signal

    @signal
    def hello():
      return 42

    #2. Create the listener decorators, using the function that has the signal
    - @pre to capture before the execution
      accepts args: (*a, **kw)
      - **kw: properties
    - @post to capture after the execution
      accepts args: (result, **kw)
      - result: the value that was return from the function
      - **kw: propeties


    @hello.pre
    def i_run_before(**kw):
      print("I Run before", kw)

    @hello.post 
    def i_run_after(result, **kw):
      print("I run after", result, kw)

    #3. Whenever the hello() function is run, i_run_before and i_run_after will be executed
    hello()
    hello()   
    """
    ns = __signals_namespace

    fnargs = inspect.getfullargspec(fn).args
    fname = fn.__module__
    if 'self' in fnargs or 'cls' in fnargs:
        caller = inspect.currentframe().f_back
        fname += "_" + caller.f_code.co_name
    fname += "__" + fn.__name__

    # pre and post
    fn.pre_ = ns.signal('pre_%s' % fname)
    fn.post_ = ns.signal('post_%s' % fname)

    # alias
    fn.pre = fn.pre_.connect
    fn.post = fn.post_.connect

    def send(action, *a, **kw):
        sig_name = "%s_%s" % (action, fname)
        result = kw.pop("result", None)
        resp = {
            "args": a,
            "kwargs": kw,
            "name": fn.__name__,
            "signal": kw.get('self', kw.get('cls', fn))
        }
        if action == 'post':
            ns.signal(sig_name).send(result, **resp)
        else:
            ns.signal(sig_name).send(**resp)

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        send('pre', *args, **kwargs)
        result = fn(*args, **kwargs)
        kwargs["result"] = result
        send('post', *args, **kwargs)
        return result

    return wrapper


# ------------------------------------------------------------------------------

def flash_data(data):
    """
    Set temporary data in the session.
    It will replace the previous one
    :param data:
    :return:
    """
    session["_flash_data"] = data


def get_flashed_data():
    """
    Retrieve and pop data from the session
    :return: mixed
    """
    return session.pop("_flash_data", None)


# ------------------------------------------------------------------------------
# mail

@signal
def send_mail(to, **kwargs):
    """
    Alias to mail.send()
    ie: 
    - send_mail("user@email.com", subject="", body="")
    - send_mail("user@email.com", template="welcome.mail.tpl")

    # This function emits a signal
    @asm.send_email.post
    def email_sent(result, **kw):
        if result:
            print("Email sent")

    :param template:
    :param to:
    :param kwargs:
    :return:
    """
    return ext.mail.send(to=to, **kwargs)


# ------------------------------------------------------------------------------
# Storage
storage = flask_cloudy.Storage()
@app_context
def init_storage(app):
    utils.flatten_config_property("STORAGE", app.config)
    storage.init_app(app)


def get_file(filename):
    """
    Get file from storage
    :param filename:
    :return: Storage object
    """
    return storage.get(filename)


@signal
def upload_file(file, props=None,  **kw):
    """
    Wrapper around storage.upload to upload a file conveniently.

    A preset key can be used to upload image type alike. 
    config file must have STORAGE_UPLOAD_FILE_PROPS where it contains k/v, ie:

    STORAGE_UPLOAD_FILE_PROPS = {
        "profile-image": {
            "extensions": ["jpg", "jpeg", "gif", "png"],
            "prefix": "/profile-image/",
            "public": True
        },
        ...
    }
    and 'props' must be the key of the value to use

    # using props key name
    upload_file(my_file, props="profile-image")

    # passing the props directly
    or upload_file(my_file, props={
        "extensions": ["jpg", "jpeg", "gif", "png"],
        "prefix": "/profile-image/",
        "public": True
    })

    # or simply
    upload_file(my_file, extensions=["jpg"], "prefix="/", public=True)

    # This function emits a signal
    @asm.upload_file.post
    def file_uploaded(result, **kw):
        if result:
            print("File uploaded")


    :param file: File object or string location
    :param props: (str) a key available in config.STORAGE_UPLOAD_FILE_PROPS, or dict
    :param kw: extra **kw for upload
    :return: Storage object
    """
    kwargs = {}
    if isinstance(props, str):
        conf = config.get("STORAGE_UPLOAD_FILE_PROPS")
        if not conf:
            raise ValueError("Missing STORAGE_UPLOAD_FILE_PROPS in config")
        if props not in conf:
            raise ValueError("Missing '%s' properties in config STORAGE_UPLOAD_FILE_PROPS" % props)
        kwargs.update(conf.get(props))
    elif isinstance(props, dict):
        kwargs.update(props)
    kwargs.update(kw)

    return storage.upload(file, **kwargs)


@signal
def delete_file(fileobj, **kw):
    """
    Alias to delete a file from storage

    # This function emits a signal
    @asm.delete_file.post
    def file_delete(result, **kw):
        if result:
            print("File deleted")

    :param fileobj: string or StorageObject type
    :return:
    """
    if isinstance(fileobj, str):
        fileobj = get_file(fileobj)

    if not isinstance(fileobj, (flask_cloudy.Object, assembly_db.StorageObject)):
        raise TypeError("Invalid file type. Must be of flask_cloudy.Object or file doesn't exist")
    return fileobj.delete()

@signal
def download_file(object_name, name=None, timeout=60, **kw):
    """
    Alias to download a file object as attachment, or convert some text as .
    :param object_name: the file storage object name
    :param filename: the filename with extension.
        If the file to download is an StorageOject, filename doesn't need to have an extension. 
        It will automatically put it
    :param timeout: the timeout to download file from the cloud
    :return: string. Use it to redirect for download
    """
    file = get_file(object_name)
    if not isinstance(file, (flask_cloudy.Object, assembly_db.StorageObject)):
        raise TypeError("Can't download file. It must be of StorageObject type or file doesn't exist")
    return file.download_url(timeout=timeout, name=name)


def send_file(filename, content, as_attachment=True):
    """
    Alias to download a file object as attachment, or convert some text as .
    :param filename: the filename with extension.
        If the file to download is an StorageOject, filename doesn't need to have an extension.
            It will automatically put it
        If the file to download is a `content` text, extension is required.
    :param object_name: the file storage object name
    :param content: string/bytes of text
    :param as_attachment: to download as attachment
    :param timeout: the timeout to download file from the cloud
    :return:
    """
    buff = six.BytesIO()
    buff.write(content)
    buff.seek(0)
    return send_file(buff,
                     attachment_filename=filename,
                     as_attachment=as_attachment)

# ------------------------------------------------------------------------------


__CRYPT = {}
@app_context
def __crypt_init(app):
    """
    https://passlib.readthedocs.io/en/stable/lib/passlib.hash.bcrypt.html
    CONFIG
        BCRYPT_ROUNDS = 12  # salt string
        BCRYPT_SALT= None #
        BCRYPT_IDENT = '2b'
    """

    __CRYPT.update({
        "secret_key": config.get("SECRET_KEY"),
        "salt": config.get("BCRYPT_SALT", "assembly.bcrypt.salt.0"),
        "rounds": config.get("BCRYPT_ROUNDS", 12)
    })


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


def hash_string(string):
    """
    To hash a non versible hashed string. Can be used to hash password
    :returns: string
    """
    conf = {
        "rounds": __CRYPT.get("rounds")
    }
    return bcrypt.using(**conf).hash(string)


def verify_hashed_string(string, hash):
    """
    check if string match its hashed. ie: To compare password
    :returns: bool
    """
    return bcrypt.verify(string, hash)


def encode_jwt(data, expires_in=1, **kw):
    """
    To encode JWT data
    :param data:
    :param expires_in: in minutes
    :param kw:
    :return: string
    """
    expires_in *= 60
    s = itsdangerous.TimedJSONWebSignatureSerializer(secret_key=__CRYPT.get("secret_key"),
                                                     expires_in=expires_in,
                                                     salt=__CRYPT.get("salt"),
                                                     **kw)
    return s.dumps(data)


def decode_jwt(token, **kw):
    """
    To decode a JWT token
    :param token:
    :param kw:
    :return: mixed data
    """
    s = itsdangerous.TimedJSONWebSignatureSerializer(__CRYPT.get("secret_key"), salt=__CRYPT.get("salt"), **kw)
    return s.loads(token)


def sign_data(data, expires_in=None, **kw):
    """
    To sign url safe data.
    If expires_in is provided it will Time the signature
    :param data: (mixed) the data to sign
    :param expires_in: (int) in minutes. Time to expire
    :param kw: kwargs for itsdangerous.URLSafeSerializer
    :return:
    """
    if expires_in:
        expires_in *= 60
        s = URLSafeTimedSerializer2(secret_key=__CRYPT.get("secret_key"),
                                    expires_in=expires_in,
                                    salt=__CRYPT.get("salt"),
                                    **kw)
    else:
        s = itsdangerous.URLSafeSerializer(secret_key=__CRYPT.get("secret_key"),
                                           salt=__CRYPT.get("salt"),
                                           **kw)
    return s.dumps(data)


def unsign_data(token,  **kw):
    """
    To unsign url safe data.
    If expires_in is provided it will Time the signature
    :param token:
    :param secret_key:
    :param salt: (string) a namespace key
    :param kw:
    :return:
    """
    if len(token.split(".")) == 3:
        s = URLSafeTimedSerializer2(secret_key=__CRYPT.get("secret_key"), salt=__CRYPT.get("salt"), **kw)
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
        s = itsdangerous.URLSafeSerializer(secret_key=__CRYPT.get("secret_key"), salt=__CRYPT.get("salt"), **kw)
        return s.loads(token)
