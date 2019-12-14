# -*- coding: utf-8 -*-
"""
Assembly: extensions
"""

import os
import re
import six
import copy
import logging
import markdown
import flask_s3
import flask_mail
import ses_mailer
import flask_login
import flask_kvsession
from jinja2 import Markup
from jinja2.ext import Extension
from urllib.parse import urlparse
from jinja2.nodes import CallBlock
from jinja2 import TemplateSyntaxError
from . import (ext, config, app_context, utils)
from jinja2.lexer import Token, describe_token
from flask import (request, current_app, send_file, session)

# ------------------------------------------------------------------------------
@app_context
def setup(app):
    check_config_keys = ["SECRET_KEY"]
    for k in check_config_keys:
        if k not in app.config \
                or not app.config.get(k):
            msg = "Missing config key value: %s " % k
            logging.warning(msg)
            exit()

    # 
    """
    Flatten properties that were set in dict in the config
    MAIL = {
        "sender": "me@email.com",
        "a_key": "some-value
    }
    MAIL_SENDER
    MAIL_A_KEY
    """
    for k in ["CORS"]:
        utils.flatten_config_property(k, app.config)


# ------------------------------------------------------------------------------
# Session

@app_context
def session(app):
    """
    Sessions
    It uses KV session to allow multiple backend for the session
    """
    store = None
    uri = app.config.get("SESSION_URL")
    if uri:
        parse_uri = urlparse(uri)
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

        utils.flatten_config_property("MAIL", app.config)
        self.config = app.config
        scheme = None

        mailer_uri = self.config.get("MAIL_URL")
        if mailer_uri:
            templates_sources = app.config.get("MAIL_TEMPLATE")
            if not templates_sources:
                templates_sources = app.config.get("MAIL_TEMPLATES_DIR") or app.config.get("MAIL_TEMPLATES_DICT")

            mailer_uri = urlparse(mailer_uri)
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
                                            template=templates_sources,
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

                _ses_mailer = ses_mailer.Mail(template=templates_sources,
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
app_context(ext.mail.init_app)

# ------------------------------------------------------------------------------
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
                    domain_parsed = urlparse(domain)
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
app_context(ext.assets_delivery.init_app)

# ------------------------------------------------------------------------------
# Flask-Login

ext.login_manager = flask_login.LoginManager()
@ext.login_manager.user_loader
def _login_manager_user_loader(user_id):
    """ 
    setup None user loader. 
    Without this, it will throw an error if it doesn't exist 
    """
    return None

@app_context
def login_manager_init(app):
    """ set the config for the login manager """
    lm = app.config.get("LOGIN_MANAGER")
    ext.login_manager.init_app(app)
    if lm:
        for k, v in lm.items():
            setattr(ext.login_manager, k, v)


# ------------------------------------------------------------------------------
# Markdown

class JinjaMDTagExt(Extension):
    """
    A simple extension for adding a {% markdown %}{% endmarkdown %} tag to Jinja

    <div> 
    {% markdown %}
        ## Hi
    {% endmarkdown %}
    </div>
    """
    tags = set(['markdown'])

    def __init__(self, environment):
        super(JinjaMDTagExt, self).__init__(environment)
        environment.extend(
            markdowner=markdown.Markdown(extensions=['extra'])
        )

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        body = parser.parse_statements(
            ['name:endmarkdown'],
            drop_needle=True
        )
        return CallBlock(
            self.call_method('_markdown_support'),
            [],
            [],
            body
        ).set_lineno(lineno)

    def _markdown_support(self, caller):
        block = caller()
        block = self._strip_whitespace(block)
        return self._render_markdown(block)

    def _strip_whitespace(self, block):
        lines = block.split('\n')
        whitespace = ''
        output = ''

        if (len(lines) > 1):
            for char in lines[1]:
                if (char == ' ' or char == '\t'):
                    whitespace += char
                else:
                    break

        for line in lines:
            output += line.replace(whitespace, '', 1) + '\r\n'

        return output.strip()

    def _render_markdown(self, block):
        block = self.environment.markdowner.convert(block)
        return block


class JinjaMDExt(Extension):
    """
    JINJA Convert Markdown file to HTML
    """
    options = {}
    file_extensions = '.md'

    def preprocess(self, source, name, filename=None):
        if (not name or
                (name and not os.path.splitext(name)[1] in self.file_extensions)):
            return source
        return md_to_html(source)


# Markdown
mkd = markdown.Markdown(extensions=[
    'markdown.extensions.extra',
    'markdown.extensions.nl2br',
    'markdown.extensions.sane_lists',
    'markdown.extensions.toc'
])


def md_to_html(text):
    '''
    Convert MD text to HTML
    :param text:
    :return:
    '''
    mkd.reset()
    return mkd.convert(text)


@app_context
def setup_markdown(app):
    """
    Load markdown extension
    """
    app.jinja_env.add_extension(JinjaMDTagExt)
    app.jinja_env.add_extension(JinjaMDExt)


# The extension
ext.markdown = md_to_html

# --------


"""
  -- jinja2-htmlcompress

    a Jinja2 extension that removes whitespace between HTML tags.

    Example usage:

      env = Environment(extensions=['htmlcompress_ext.HTMLCompress'])

    How does it work?  It throws away all whitespace between HTML tags
    it can find at runtime.  It will however preserve pre, textarea, style
    and script tags because this kinda makes sense.  In order to force
    whitespace you can use ``{{ " " }}``.

    Unlike filters that work at template runtime, this remotes whitespace
    at compile time and does not add an overhead in template execution.

    What if you only want to selective strip stuff?

      env = Environment(extensions=['htmlcompress_ext.SelectiveHTMLCompress'])

    And then mark blocks with ``{% strip %}``:

      {% strip %} ... {% endstrip %}

"""

gl_tag_re = re.compile(r'(?:<(/?)([a-zA-Z0-9_-]+)\s*|(>\s*))(?s)')
gl_ws_normalize_re = re.compile(r'[ \t\r\n]+')


class StreamProcessContext(object):
    def __init__(self, stream):
        self.stream = stream
        self.token = None
        self.stack = []

    def fail(self, message):
        raise TemplateSyntaxError(message, self.token.lineno, self.stream.name,
                                  self.stream.filename)


def _make_dict_from_listing(listing):
    rv = {}
    for keys, value in listing:
        for key in keys:
            rv[key] = value
    return rv


class HTMLCompress(Extension):
    isolated_elements = set(['script', 'style', 'noscript', 'textarea', 'pre'])
    void_elements = set(['br', 'img', 'area', 'hr', 'param', 'input',
                         'embed', 'col'])
    block_elements = set(['div', 'p', 'form', 'ul', 'ol', 'li', 'table', 'tr',
                          'tbody', 'thead', 'tfoot', 'tr', 'td', 'th', 'dl',
                          'dt', 'dd', 'blockquote', 'h1', 'h2', 'h3', 'h4',
                          'h5', 'h6'])
    breaking_rules = _make_dict_from_listing([
        (['p'], set(['#block'])),
        (['li'], set(['li'])),
        (['td', 'th'], set(['td', 'th', 'tr', 'tbody', 'thead', 'tfoot'])),
        (['tr'], set(['tr', 'tbody', 'thead', 'tfoot'])),
        (['thead', 'tbody', 'tfoot'], set(['thead', 'tbody', 'tfoot'])),
        (['dd', 'dt'], set(['dl', 'dt', 'dd']))
    ])

    def is_isolated(self, stack):
        for tag in reversed(stack):
            if tag in self.isolated_elements:
                return True
        return False

    def is_breaking(self, tag, other_tag):
        breaking = self.breaking_rules.get(other_tag)
        return breaking and (tag in breaking or (
            '#block' in breaking and tag in self.block_elements))

    def enter_tag(self, tag, ctx):
        while ctx.stack and self.is_breaking(tag, ctx.stack[-1]):
            self.leave_tag(ctx.stack[-1], ctx)
        if tag not in self.void_elements:
            ctx.stack.append(tag)

    def leave_tag(self, tag, ctx):
        if not ctx.stack:
            ctx.fail(
                'Tried to leave "%s" but something closed it already' % tag)
        if tag == ctx.stack[-1]:
            ctx.stack.pop()
            return
        for idx, other_tag in enumerate(reversed(ctx.stack)):
            if other_tag == tag:
                for num in range(idx + 1):
                    ctx.stack.pop()
            elif not self.breaking_rules.get(other_tag):
                break

    def normalize(self, ctx):
        pos = 0
        buffer = []

        def write_data(value):
            if not self.is_isolated(ctx.stack):
                value = gl_ws_normalize_re.sub(' ', value)
            buffer.append(value)

        for match in gl_tag_re.finditer(ctx.token.value):
            closes, tag, sole = match.groups()
            preamble = ctx.token.value[pos:match.start()]
            write_data(preamble)
            if sole:
                write_data(sole)
            else:
                buffer.append(match.group())
                (closes and self.leave_tag or self.enter_tag)(tag, ctx)
            pos = match.end()

        write_data(ctx.token.value[pos:])
        return ''.join(buffer)

    def filter_stream(self, stream):
        ctx = StreamProcessContext(stream)
        for token in stream:
            if token.type != 'data':
                yield token
                continue
            ctx.token = token
            value = self.normalize(ctx)
            yield Token(token.lineno, 'data', value)


class SelectiveHTMLCompress(HTMLCompress):
    def filter_stream(self, stream):
        ctx = StreamProcessContext(stream)
        strip_depth = 0
        while True:
            if stream.current.type == 'block_begin':
                if stream.look().test('name:strip') or stream.look().test(
                        'name:endstrip'):
                    stream.skip()
                    if stream.current.value == 'strip':
                        strip_depth += 1
                    else:
                        strip_depth -= 1
                        if strip_depth < 0:
                            ctx.fail('Unexpected tag endstrip')
                    stream.skip()
                    if stream.current.type != 'block_end':
                        ctx.fail(
                            'expected end of block, got %s' % describe_token(
                                stream.current))
                    stream.skip()
            if strip_depth > 0 and stream.current.type == 'data':
                ctx.token = stream.current
                value = self.normalize(ctx)
                yield Token(stream.current.lineno, 'data', value)
            else:
                yield stream.current
            next(stream)


@app_context
def setup_compress_html(app):
    if app.config.get("COMPRESS_HTML"):
        app.jinja_env.add_extension(HTMLCompress)

# ------------------------------------------------------------------------------

"""
PLACEHOLDER

With this extension you can define placeholders where your blocks get rendered 
and at different places in your templates append to those blocks. 
This is especially useful for css and javascript. 
Your sub-templates can now define css and Javascript files 
to be included, and the css will be nicely put at the top and 
the Javascript to the bottom, just like you should. 
It will also ignore any duplicate content in a single block.

<html>
    <head>
        {% placeholder "css" %}
    </head>
    <body>
        Your content comes here.
        Maybe you want to throw in some css:

        {% addto "css" %}
            <link href="/media/css/stylesheet.css" media="screen" rel="[stylesheet](stylesheet)" type="text/css" />
        {% endaddto %}

        Some more content here.

        {% addto "js" %}
            <script type="text/javascript">
                alert("Hello flask");
            </script>
        {% endaddto %}

        And even more content.
        {% placeholder "js" %}
    </body>
</html>
"""


@app_context
def init_app(app):
    app.jinja_env.add_extension(PlaceholderAddTo)
    app.jinja_env.add_extension(PlaceholderRender)
    app.jinja_env.placeholder_tags = {}


class PlaceholderAddTo(Extension):
    tags = set(['addtoblock'])
    def _render_tag(self, name, caller):
        context = self.environment.placeholder_tags
        blocks = context.get(name)
        if blocks is None:
            blocks = set()
        blocks.add(caller().strip())
        context[name] = blocks
        return Markup("")

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        name = parser.parse_expression()
        body = parser.parse_statements(['name:endaddtoblock'], drop_needle=True)
        args = [name]
        return CallBlock(self.call_method('_render_tag', args),
                         [], [], body).set_lineno(lineno)


class PlaceholderRender(Extension):
    tags = set(['renderblock'])

    def _render_tag(self, name: str, caller):
        context = self.environment.placeholder_tags
        return Markup('\n'.join(context.get(name, [])))

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        name = parser.parse_expression()
        args = [name]
        return CallBlock(self.call_method('_render_tag', args),
                         [], [], []).set_lineno(lineno)
