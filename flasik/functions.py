# -*- coding: utf-8 -*-
"""
Extensions
"""

import re
import six
import logging
from flask import request, current_app, send_file
import flask_cloudy
import flask_recaptcha
import flask_seasurf
import flask_kvsession
import flask_caching
import ses_mailer
import flask_mail
import flask_s3
import flask_babel
from flask_babel import lazy_gettext as _
from passlib.hash import bcrypt as passhash
from . import (Flasik,
               init_app,
               utils,
               exceptions,
               g,
               config,
               signals)

from .ext import jinja_helpers, flasik_db
from paginator import Paginator

__all__ = ["cache",
           "storage",
           "upload_file",
           "delete_file",
           "download_file",
           "get_file",
           "recaptcha",
           "csrf",
           "bcrypt",
           "send_mail",
           "paginate",
           "_",
           ]


def _setup(app):

    check_config_keys = [
        "SECRET_KEY",
        "ADMIN_EMAIL",
        "CONTACT_EMAIL",
        "MAIL_URL",
        "MAIL_SENDER",
        "DB_URL",
        "DATETIME_TIMEZONE",
        "DATETIME_FORMAT",
        "RECAPTCHA_SITE_KEY",
        "RECAPTCHA_SECRET_KEY"
    ]
    for k in check_config_keys:
        if k not in app.config \
                or not app.config.get(k):
            msg = "Missing config key value: %s " % k
            logging.warning(msg)

init_app(_setup)

# ------------------------------------------------------------------------------

# Session
#
# It uses KV session to allow multiple backend for the session
def _session(app):
    store = None
    uri = app.config.get("SESSION_URL")
    if uri:
        parse_uri = utils.urlparse(uri)
        scheme = parse_uri.scheme
        username = parse_uri.username
        password = parse_uri.password
        hostname = parse_uri.hostname
        port = parse_uri.port
        bucket = parse_uri.path.strip("/")

        if "redis" in scheme:
            import redis
            from simplekv.memory.redisstore import RedisStore
            conn = redis.StrictRedis.from_url(url=uri)
            store = RedisStore(conn)
        elif "s3" in scheme or "google_storage" in scheme:
            from simplekv.net.botostore import BotoStore
            import boto
            if "s3" in scheme:
                _con_fn = boto.connect_s3
            else:
                _con_fn = boto.connect_gs
            conn = _con_fn(username, password)
            _bucket = conn.create_bucket(bucket)
            store = BotoStore(_bucket)
        elif "memcache" in scheme:
            import memcache
            from simplekv.memory.memcachestore import MemcacheStore
            host_port = "%s:%s" % (hostname, port)
            conn = memcache.Client(servers=[host_port])
            store = MemcacheStore(conn)
        elif "sql" in scheme:
            from simplekv.db.sql import SQLAlchemyStore
            from sqlalchemy import create_engine, MetaData
            engine = create_engine(uri)
            metadata = MetaData(bind=engine)
            store = SQLAlchemyStore(engine, metadata, 'kvstore')
            metadata.create_all()
        else:
            raise exceptions.FlasikError("Invalid Session Store. '%s' provided" % scheme)
    if store:
        flask_kvsession.KVSessionExtension(store, app)

init_app(_session)
# ------------------------------------------------------------------------------
# Mailer
class _Mailer(object):
    """
    config key: MAIL_*
    A simple wrapper to switch between SES-Mailer and Flask-Mail based on config
    """
    mail = None
    provider = None
    config = None
    _template = None

    @property
    def validated(self):
        return bool(self.mail)

    def init_app(self, app):
        self.config = app.config
        scheme = None

        mailer_uri = self.config.get("MAIL_URL")
        if mailer_uri:
            mailer_uri = utils.urlparse(mailer_uri)
            scheme = mailer_uri.scheme
            hostname = mailer_uri.hostname

            # Using ses-mailer
            if "ses" in scheme.lower():
                self.provider = "SES"

                access_key = mailer_uri.username or app.config.get("AWS_ACCESS_KEY_ID")
                secret_key = mailer_uri.password or app.config.get("AWS_SECRET_ACCESS_KEY")
                region = hostname or self.config.get("AWS_REGION", "us-east-1")
                
                self.mail = ses_mailer.Mail(aws_access_key_id=access_key,
                                            aws_secret_access_key=secret_key,
                                            region=region,
                                            sender=self.config.get("MAIL_SENDER"),
                                            reply_to=self.config.get("MAIL_REPLY_TO"),
                                            template=self.config.get("MAIL_TEMPLATE"),
                                            template_context=self.config.get("MAIL_TEMPLATE_CONTEXT"))

            # SMTP will use flask-mail
            elif "smtp" in scheme.lower():
                self.provider = "SMTP"

                class _App(object):
                    config = {
                        "MAIL_SERVER": mailer_uri.hostname,
                        "MAIL_USERNAME": mailer_uri.username,
                        "MAIL_PASSWORD": mailer_uri.password,
                        "MAIL_PORT": mailer_uri.port,
                        "MAIL_USE_TLS": True if "tls" in mailer_uri.scheme else False,
                        "MAIL_USE_SSL": True if "ssl" in mailer_uri.scheme else False,
                        "MAIL_DEFAULT_SENDER": app.config.get("MAIL_SENDER"),
                        "TESTING": app.config.get("TESTING"),
                        "DEBUG": app.config.get("DEBUG")
                    }
                    debug = app.config.get("DEBUG")
                    testing = app.config.get("TESTING")

                _app = _App()
                self.mail = flask_mail.Mail(app=_app)

                _ses_mailer = ses_mailer.Mail(template=self.config.get("MAIL_TEMPLATE"),
                                              template_context=self.config.get("MAIL_TEMPLATE_CONTEXT"))
                self._template = _ses_mailer.parse_template
            else:
                logging.warning("Mailer Error. Invalid scheme '%s'" % scheme)

    def send(self, to, subject=None, body=None, reply_to=None, template=None, **kwargs):
        """
        To send email
        :param to: the recipients, list or string
        :param subject: the subject
        :param body: the body
        :param reply_to: reply_to
        :param template: template, will use the templates instead
        :param kwargs: context args
        :return: bool - True if everything is ok
        """
        sender = self.config.get("MAIL_SENDER")
        recipients = [to] if not isinstance(to, list) else to
        kwargs.update({
            "subject": subject,
            "body": body,
            "reply_to": reply_to
        })

        if not self.validated:
            raise exceptions.FlasikError("Mail configuration error")

        if self.provider == "SES":
            kwargs["to"] = recipients
            if template:
                self.mail.send_template(template=template, **kwargs)
            else:
               self.mail.send(**kwargs)

        elif self.provider == "SMTP":
            if template:
                data = self._template(template=template, **kwargs)
                kwargs["subject"] = data["subject"]
                kwargs["body"] = data["body"]
            kwargs["recipients"] = recipients
            kwargs["sender"] = sender

            # Remove invalid Messages keys
            _safe_keys = ["recipients", "subject", "body", "html", "alts",
                          "cc", "bcc", "attachments", "reply_to", "sender",
                           "date", "charset", "extra_headers", "mail_options",
                           "rcpt_options"]
            for k in kwargs.copy():
                if k not in _safe_keys:
                    del kwargs[k]

            message = flask_mail.Message(**kwargs)
            self.mail.send(message)
        else:
            raise exceptions.FlasikError("Invalid mail provider. Must be 'SES' or 'SMTP'")

mail = _Mailer()
init_app(mail.init_app)

def send_mail(template, to, **kwargs):
    """
    Alias to mail.send(), but makes template required
    ie: send_mail("welcome-to-the-site.txt", "user@email.com")
    :param template: 
    :param to:
    :param kwargs:
    :return:
    """

    def cb():
        return mail.send(to=to, template=template, **kwargs)

    return signals.send_mail(cb, data={"to": to, "template": template, "kwargs": kwargs})


# ------------------------------------------------------------------------------

# Assets Delivery
class _AssetsDelivery(flask_s3.FlaskS3):
    def init_app(self, app):
        delivery_method = app.config.get("ASSETS_DELIVERY_METHOD")
        if delivery_method and delivery_method.upper() in ["S3", "CDN"]:
            #with app.app_context():
            is_secure = False #request.is_secure

            if delivery_method.upper() == "CDN":
                domain = app.config.get("ASSETS_DELIVERY_DOMAIN")
                if "://" in domain:
                    domain_parsed = utils.urlparse(domain)
                    is_secure = domain_parsed.scheme == "https"
                    domain = domain_parsed.netloc
                app.config.setdefault("S3_CDN_DOMAIN", domain)

            app.config["FLASK_ASSETS_USE_S3"] = True
            app.config["FLASKS3_ACTIVE"] = True
            app.config["FLASKS3_URL_STYLE"] = "path"
            app.config.setdefault("FLASKS3_USE_HTTPS", is_secure)
            app.config.setdefault("FLASKS3_ONLY_MODIFIED", True)
            app.config.setdefault("FLASKS3_GZIP", True)
            app.config.setdefault("FLASKS3_BUCKET_NAME", app.config.get("AWS_S3_BUCKET_NAME"))

            super(self.__class__, self).init_app(app)

assets_delivery = _AssetsDelivery()
init_app(assets_delivery.init_app)

# ------------------------------------------------------------------------------

# Set CORS
def set_cors_config(app):
    """
    Flask-Cors (3.x.x) extension set the config as CORS_*,
     But we'll hold the config in CORS key.
     This function will convert them to CORS_* values
    :param app:
    :return:
    """
    if "CORS" in app.config:
        for k, v in app.config["CORS"].items():
            _ = "CORS_" + k.upper()
            if _ not in app.config:
                app.config[_] = v

init_app(set_cors_config)

# ------------------------------------------------------------------------------
# BCRYPT
class Bcrypt(object):
    """

    https://passlib.readthedocs.io/en/stable/lib/passlib.hash.bcrypt.html

    CONFIG 
        BCRYPT_ROUNDS = 12  # salt string
        BCRYPT_SALT= None #
        BCRYPT_IDENT = '2b'

    """

    def __init__(self, app=None):
        self.config = {
            "rounds": 12
        }
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.config = app.config.get_namespace("BCRYPT_")

    def hash(self, string):
        return passhash.using(**self.config).hash(string)

    def verify(self, string, hash):
        return passhash.verify(string, hash)

bcrypt = Bcrypt()
init_app(bcrypt.init_app)

# ------------------------------------------------------------------------------



# Cache
cache = flask_caching.Cache()
init_app(cache.init_app)

# Storage
storage = flask_cloudy.Storage()
init_app(storage.init_app)


# Upload file
def upload_file(_props_key, file, **kw):
    """
    Wrapper around storage.upload to upload a file conveniently by using set 
    properties, so no need to keep rewriting the same code.
    config file must have STORAGE_UPLOAD_FILE_PROPS where it contains k/v, ie:

    STORAGE_UPLOAD_FILE_PROPS = {
        "profile-image": {
            "extensions": ["jpg", "jpeg", "gif", "png"],
            "prefix": "/profile-image/",
            "public": True
        }, 
        ...
    }

    upload_file("profile-image", my_file)
    :param _props_key: (str) a key available in config.STORAGE_UPLOAD_FILE_PROPS
    :param file: FileStorage object or string location
    :param kw: extra **kw for 
    :return: Storage object
    """
    kwargs = {}
    if _props_key is not None:
        conf = config("STORAGE_UPLOAD_FILE_PROPS")
        if not conf:
            raise ValueError("Missing STORAGE_UPLOAD_FILE_PROPS in config")
        if _props_key not in conf:
            raise ValueError("Missing '%s' in config STORAGE_UPLOAD_FILE_PROPS" % _props_key)
        kwargs.update(conf.get(_props_key))
    kwargs.update(kw)

    return signals.upload_file(lambda: storage.upload(file, **kwargs))


def get_file(object_name):
    """
    Alias to get file from storage 
    :param object_name: 
    :return: Storage object
    """
    return storage.get(object_name)


def delete_file(fileobj):
    """
    Alias to delete a file from storage
    :param fileobj: 
    :return: 
    """
    if not isinstance(fileobj, (flask_cloudy.Object, flasik_db.StorageObject)):
        raise TypeError("Invalid file type. Must be of flask_cloudy.Object")
    return signals.delete_file(lambda: fileobj.delete())


def download_file(filename, object_name=None, content=None, as_attachment=True, timeout=60):
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
    if object_name:
        file = get_file(object_name)
        if not isinstance(file, (flask_cloudy.Object, flasik_db.StorageObject)):
            raise TypeError("Can't download file. It must be of StorageObject type")
        return file.download_url(timeout=timeout, name=filename)
    elif content:
        buff = six.BytesIO()
        buff.write(content)
        buff.seek(0)
        return send_file(buff,
                         attachment_filename=filename,
                         as_attachment=as_attachment)
    raise TypeError("`file` object or `content` text must be provided")


# Recaptcha
recaptcha = flask_recaptcha.ReCaptcha()
init_app(recaptcha.init_app)

# CSRF
csrf = flask_seasurf.SeaSurf()
init_app(csrf.init_app)


def paginate(iter, **kwargs):
    """
     A wrapper around the Paginator that takes config data
    :param iter: Query object or any iterables
    :param kwargs:
        - page: current page
        - per_page: max number of items per page
        - total: Max number of items. If not provided, it will use the query to count
        - padding: Number of elements of the next page to show
        - callback: a function to callback on each item being iterated.
        - static_query: bool - When True it will return the query as is, without slicing/limit. Usally when using the paginator to just create the pagination.
    :return: Paginator
    """
    kwargs.setdefault("page", int(request.args.get('page', 1)))
    kwargs.setdefault("per_page", int(config("PAGINATION_PER_PAGE", 1)))
    kwargs.setdefault("padding", int(config("PAGINATION_PADDING", 0)))
    return Paginator(iter, **kwargs)

# Babel
babel = flask_babel.Babel()


def init_babel(app):
    babel.init_app(app)

    # languages = app.config.get("LANGUAGES", {})
    #
    # @babel.localeselector
    # def get_locale():
    #     lang = request.params.get("lang", "en")
    #     return request.accept_languages.best_match(languages.keys())
init_app(init_babel)


# ------------------------------------------------------------------------------

