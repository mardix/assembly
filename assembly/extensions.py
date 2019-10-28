# -*- coding: utf-8 -*-
"""
Assembly: extensions
"""

import re
import six
import copy
import logging
import flask_s3
import flask_mail
import ses_mailer
import itsdangerous
import flask_kvsession
from passlib.hash import bcrypt
from . import (get_config, ext, extends)
from flask import (request, current_app, send_file, session)

# mail, 
# assets_delivery, 
# crypt

#------------------------------------------------------------------------------
# Set CORS

@extends
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

#------------------------------------------------------------------------------
# Session

@extends
def session(app):
    """
    Sessions
    It uses KV session to allow multiple backend for the session
    """
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
            raise Error("Invalid Session Store. '%s' provided" % scheme)
    if store:
        flask_kvsession.KVSessionExtension(store, app)

#------------------------------------------------------------------------------
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
            raise Error("Mail configuration error")

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
            raise Error("Invalid mail provider. Must be 'SES' or 'SMTP'")

ext.mail = _Mailer()
extends(ext.mail.init_app)

#------------------------------------------------------------------------------
# Assets Delivery

class _AssetsDelivery(flask_s3.FlaskS3):
    def init_app(self, app):
        delivery_method = app.config.get("ASSETS_DELIVERY_METHOD")
        if delivery_method and delivery_method.upper() in ["S3", "CDN"]:
            # with app.app_context():
            is_secure = False  # request.is_secure

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

ext.assets_delivery = _AssetsDelivery()
extends(ext.assets_delivery.init_app)

#------------------------------------------------------------------------------
# Crypt

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

class Crypt(object):
    def __init__(self, secret_key=None, salt=None, rounds=12):
        pass
        
    def init_app(self, app):
        self.secret_key = get_config("SECRET_KEY")
        self.salt = "assembly.security.salt.0"
        self.rounds = 12

    """
    https://passlib.readthedocs.io/en/stable/lib/passlib.hash.bcrypt.html
    CONFIG 
        BCRYPT_ROUNDS = 12  # salt string
        BCRYPT_SALT= None #
        BCRYPT_IDENT = '2b'
    """
    def hash_string(self, string):
        """
        To hash a non versible hashed string. Can be used to hash password
        :returns: string
        """
        config = {
            "rounds": self.rounds
        }
        return bcrypt.using(**config).hash(string)

    def verify_hashed_string(self, string, hash):
        """
        check if string match its hashed. ie: To compare password
        :returns: bool
        """
        return bcrypt.verify(string, hash)

    def jwt_encode(self, data, expires_in=1, **kw):
        """
        To encode JWT data
        :param data:
        :param expires_in: in minutes
        :param kw:
        :return: string
        """
        expires_in *= 60
        s = itsdangerous.TimedJSONWebSignatureSerializer(secret_key=self.secret_key,
                                                         expires_in=expires_in,
                                                         salt=self.salt,
                                                         **kw)
        return s.dumps(data)

    def jwt_decode(self, token, **kw):
        """
        To decode a JWT token
        :param token:
        :param kw:
        :return: mixed data
        """
        s = itsdangerous.TimedJSONWebSignatureSerializer(self.secret_key, salt=self.salt, **kw)
        return s.loads(token)

    def url_safe_encode(self, data, expires_in=None, **kw):
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
            s = URLSafeTimedSerializer2(secret_key=self.secret_key,
                                        expires_in=expires_in,
                                        salt=self.salt,
                                        **kw)
        else:
            s = itsdangerous.URLSafeSerializer(secret_key=self.secret_key,
                                               salt=self.salt,
                                               **kw)
        return s.dumps(data)

    def url_safe_decode(self, token,  **kw):
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
            s = URLSafeTimedSerializer2(secret_key=self.secret_key, salt=self.salt, **kw)
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
            s = itsdangerous.URLSafeSerializer(secret_key=self.secret_key, salt=self.salt, **kw)
            return s.loads(token)

    def data_encode(self, data, **kw):
        s = itsdangerous.Serializer(secret_key=self.secret_key, salt=self.salt, **kw)
        return s.dumps(data)

    def data_ecode(self, data, **kw):
        s = itsdangerous.Serializer(secret_key=self.secret_key, salt=self.salt, **kw)
        return s.loads(data)


ext.crypto = Crypt()
extends(ext.crypto.init_app)



