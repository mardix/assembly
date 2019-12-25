# -*- coding: utf-8 -*-
"""
Assembly: core

This is the Assembly core
"""

import re
import os
import sys
import six
import jinja2
import inspect
import logging
import werkzeug
import functools
import arrow as date
import pkg_resources
import logging.config
from . import utils, _db, about
from flask_assets import Environment
import werkzeug.exceptions as HTTPError
from werkzeug.wrappers import BaseResponse
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.routing import (BaseConverter, parse_rule)
from flask import (Flask,
                   g,
                   render_template,
                   flash,
                   session,
                   make_response,
                   Response,
                   request,
                   abort,
                   url_for as f_url_for,
                   redirect as f_redirect)

# ------------------------------------------------------------------------------

__all__ = [
    "Assembly",
    "db",
    "env",
    "ext",
    "date",
    "views",
    "config",
    "models",
    "url_for",
    "decorate",
    "redirect",
    "HTTPError",
    "get_cookie",
    "set_cookie",
    "app_context",
    "delete_cookie",

]

"""
env
Alias to os.environ, to retrieve environment variable
"""
env = os.environ

"""
config
Alias to access the config.py properties
It behaves the same way you would access the config from flask app.config
ie: config.get("SECRET_KEY") 
can also access via dot notiation
ie: config.get("DATE_FORMAT.datetime")
"""
config = utils.DotDict()

"""
views
Will hold all active class views
It can be used for redirection etc
ie: redirect(views.ContactPage.index)
"""
views = type('', (), {})

"""
models
Will hold models from apps, or to be shared
ie, set new model property -> models.MyNewModel = MyModel
ie: use property -> models.MyNewModel.all()
For convenience, use `_register_models(**kw)` to register the models
By default Assembly will load all the application/__models__.py models
"""
models = type('', (), {})

"""
ext
Extensions objects
Can be used to store extension objects
"""
ext = type('', (), {})

"""
db
Setup the DB
upon initialization will use the right URL for it
also, it exposes the db object to all modules
"""
db = _db.ActiveAlchemyProxy()


def app_context(kls):
    """
    To bind middlewares, plugins that needs the 'app' context to initialize
    Bound middlewares will be assigned on cls.init()
    Usage:

    # As a function
    def myfn(app):
        pass

    app_context(myfn)

    # As a decorator
    @app_context
    def myfn(app):
        pass

    """
    if not hasattr(kls, "__call__"):
        raise AssemblyError("app_context: '%s' is not callable" % kls)
    Assembly._init_apps.add(kls)
    return kls


def url_for(endpoint, **kw):
    """
    NB: Altered flask functions
    Assembly url_for is an alias to the flask url_for, with the ability of
    passing the function signature to build the url, without knowing the endpoint
    :param endpoint:
    :param kw:
    :return:
    """

    _endpoint = None
    if isinstance(endpoint, six.string_types):
        return f_url_for(endpoint, **kw)
    else:
        # self, will refer the caller method, by getting the method name
        if isinstance(endpoint, Assembly):
            fn = sys._getframe().f_back.f_code.co_name
            endpoint = getattr(endpoint, fn)

        if inspect.ismethod(endpoint) or inspect.isfunction(endpoint):
            _endpoint = _get_action_endpoint(endpoint)
            if not _endpoint:
                _endpoint = _make_routename_from_endpoint(endpoint)
    if _endpoint:
        return f_url_for(_endpoint, **kw)
    else:
        raise AssemblyError('Assembly `url_for` received an invalid endpoint')


def redirect(endpoint, **kw):
    """
    NB: Altered flask functions
    Redirect allow to redirect dynamically using the classes methods without
    knowing the right endpoint.
    Expecting all endpoint have GET as method, it will try to pick the first
    match, based on the endpoint provided or the based on the Rule map_url

    An endpoint can also be passed along with **kw

    An http: or https: can also be passed, and will redirect to that site.

    example:
        redirect(self.hello_world)
        redirect(self.other_page, name="x", value="v")
        redirect("https://google.com")
        redirect(views.main.ContactPage.index)
    :param endpoint:
    :return: redirect url
    """

    if isinstance(endpoint, six.string_types):
        # valid for https:// or /path/
        # Endpoint should not have slashes. Use : (colon) to build endpoint
        if "/" in endpoint:
            return f_redirect(endpoint)
        else:
            for r in Assembly._app.url_map.iter_rules():
                # Can't redirect to POST
                if 'GET' in r.methods and endpoint in r.endpoint:
                    endpoint = r.endpoint

    return f_redirect(url_for(endpoint, **kw))


def decorate(fn):
    """
    A decorator to apply decorators to all view methods of a class.
    usually when the decorator was meant for a single function. 

    @decorate(login_required)
    class Index(Assembly):
        ...

    """
    def decorator(kls):
        if inspect.isclass(kls):
            apply_function_to_members(kls, fn)
        return kls
    return decorator


"""
Cookies
set_cookie, caches set_cookie *args **kwargs in the g object
because response is not available at the time of invoke
When we receive the response for rendering, we actually set_cookie
set_cookie is a method of the response object.
"""
__ASM_SET_COOKIES__ = "__ASM_SET_COOKIES__"


def set_cookie(*a, **kw):
    """
    Proxy to response.set_cookie()
    It caches the cookies to be set in the g object
    """
    cookies = []
    if __ASM_SET_COOKIES__ in g:
        cookies = getattr(g, __ASM_SET_COOKIES__)
    cookies.append((a, kw))
    setattr(g, __ASM_SET_COOKIES__, cookies)


def delete_cookie(key, path="/", domain=None):
    """
    To delete a cookie
    """
    set_cookie(key, expires=0, max_age=0, path=path, domain=domain)


def get_cookie(key):
    """
    Get a cookie. Alias to request.cookies
    """
    return request.cookies.get(key)

# ------------------------------------------------------------------------------
# Assembly core class


class Assembly(object):
    decorators = []
    base_route = None
    route_prefix = None
    trailing_slash = True
    assets = None
    _ext = set()
    __special_methods = ["get", "put", "patch", "post", "delete", "index"]
    _app = None
    _init_apps = set()
    _template_fsl = {}
    _static_paths = set()

    @classmethod
    def init(cls,
             import_name,
             views_list,
             app_name="default",
             app_env="Development"
             ):
        """
        Initialize Assembly
        :param import_name: Flask instance or import name -> __name__
        :param views_list: dict of applications/views to load. ie:
                {
                    "default": [
                        "application",
                        "another.app.path"
                    ]
                }
        :param app_name: name of the application. Can be set via env var ASSEMBLY_APP 
        :param app_env: name of the config to use. Can be set via env var ASSEMBLY_ENV
        :return:
        """

        # initialize flask
        app = import_name if isinstance(import_name, Flask) else Flask(import_name)

        # set app_name
        if env.get("ASSEMBLY_APP"):
            app_name = env.get("ASSEMBLY_APP")

        # set app_env
        if env.get("ASSEMBLY_ENV"):
            app_env = env.get("ASSEMBLY_ENV")
        app_env = app_env.lower().capitalize()

        # load the config file
        app.config.from_object("lib.config.%s" % app_env)

        # update config object. Return a DotDict object
        if not config:
            config.update(app.config.items())

        # Proxyfix
        # By default it will use PROXY FIX
        # To by pass it, or to use your own, set config
        # USE_PROXY_FIX = False
        if app.config.get("USE_PROXY_FIX", True):
            app.wsgi_app = ProxyFix(app.wsgi_app)

        app.url_map.converters['regex'] = _RegexConverter

        cls._app = app
        cls.assets = Environment(app)
        cls._setup_db__(app)

        # Load models implicitely from lib.models
        werkzeug.import_string("lib.models", True)

        # Load views
        try:           
            if app_name not in views_list:
                raise AssemblyError("Missing project: %s" % app_name)
            for view in views_list[app_name]:
                cls._load_view_from_string__(view)
        except ImportError as ie1:
            logging.critical(ie1)

        # register models
        cls._register_models__()

        # register templates
        if cls._template_fsl:
            loader = [app.jinja_loader, _JinjaPrefixLoader(cls._template_fsl)]
            app.jinja_loader = jinja2.ChoiceLoader(loader)

        # register static, load assets.yml
        cls.assets.load_path = [app.static_folder] + list(cls._static_paths)
        for p in cls.assets.load_path:
            f = "%s/assets.yml" % p
            if os.path.isfile(f):
                cls.assets.from_yaml(f)

        # Extensions
        # instanciate all functions that may need the flask.app object
        # Usually for flask extension to be setup
        [init_app(app) for init_app in cls._init_apps]

        # register views
        for subcls in cls.__subclasses__():
            base_route = subcls.base_route
            if not base_route:
                base_route = utils.dasherize(utils.underscore(subcls.__name__))
                if subcls.__name__.lower() == "index":
                    base_route = "/"
            subcls._register__(app, base_route=base_route)
        return app

    @classmethod
    def _load_view_from_string__(cls, view):
        werkzeug.import_string(view)
        _register_application_template(view, view)

    @classmethod
    def render(cls, data={}, __template__=None, **kwargs):
        """
        Render the view template based on the class and the method being invoked
        :param data: The context data to pass to the template
        :param __template__: The file template to use. By default it will map the view/classname/action.html
        """

        # Add some global Assembly data in g, along with APPLICATION DATA
        vars = dict(
            __NAME__=about.__title__,
            __VERSION__=about.__version__,
            __YEAR__=date.utcnow().year
        )
        for k, v in vars.items():
            setattr(g, k, v)

        # Build the template using the method name being called
        if not __template__:
            stack = inspect.stack()[1]
            action_name = stack[3]
            __template__ = _make_template_path(cls, action_name)

        data = data or {}
        data.update(kwargs)

        return render_template(__template__, **data)


    @classmethod
    def _setup_db__(cls, app):
        """
        Setup the DB connection if DB_URL is set
        """
        uri = config.get("DB_URL")
        if uri:
            db.connect__(uri, app)

    @classmethod
    def _register_models__(cls):
        """
        Register the models and assign them to `models`
        :return:
        """
        if db._IS_OK_:
            _register_models(**{m.__name__: m
                                  for m in db.Model.__subclasses__()
                                  if not hasattr(models, m.__name__)})

    @classmethod
    def _register__(cls,
                    app,
                    base_route=None,
                    subdomain=None,
                    route_prefix=None,
                    trailing_slash=True):
        """Registers a Assembly class for use with a specific instance of a
        Flask app. Any methods not prefixes with an underscore are candidates
        to be routed and will have routes registered when this method is
        called.

        :param app: an instance of a Flask application

        :param base_route: The base path to use for all routes registered for
                           this class. Overrides the base_route attribute if
                           it has been set.

        :param subdomain:  A subdomain that this registration should use when
                           configuring routes.

        :param route_prefix: A prefix to be applied to all routes registered
                             for this class. Precedes base_route. Overrides
                             the class' route_prefix if it has been set.
        """

        if cls is Assembly:
            raise TypeError("cls must be a subclass of Assembly, not Assembly itself")

        # Register the view
        _register_view(cls)

        if base_route:
            cls.orig_base_route = cls.base_route
            cls.base_route = base_route

        if route_prefix:
            cls.orig_route_prefix = cls.route_prefix
            cls.route_prefix = route_prefix

        if not subdomain:
            if hasattr(app, "subdomain") and app.subdomain is not None:
                subdomain = app.subdomain
            elif hasattr(cls, "subdomain"):
                subdomain = cls.subdomain

        if trailing_slash is not None:
            cls.orig_trailing_slash = cls.trailing_slash
            cls.trailing_slash = trailing_slash

        for name, value in _get_interesting_members(Assembly, cls):
            proxy = cls._make_proxy_method__(name)
            route_name = _make_routename_from_cls(cls, name)
            try:
                if hasattr(value, "_rule_cache") and name in value._rule_cache:
                    for idx, cached_rule in enumerate(value._rule_cache[name]):
                        rule, options = cached_rule
                        rule = cls._build_rule__(rule)
                        sub, ep, options = cls._parse_options__(options)

                        if not subdomain and sub:
                            subdomain = sub

                        if ep:
                            endpoint = ep
                        elif len(value._rule_cache[name]) == 1:
                            endpoint = route_name
                        else:
                            endpoint = "%s_%d" % (route_name, idx,)

                        app.add_url_rule(rule, endpoint, proxy,
                                         subdomain=subdomain,
                                         **options)
                elif name in cls.__special_methods:
                    if name in ["get", "index"]:
                        methods = ["GET"]
                        if name == "index":
                            if hasattr(value, "_methods_cache"):
                                methods = value._methods_cache
                    else:
                        methods = [name.upper()]

                    rule = cls._build_rule__("/", value)
                    if not cls.trailing_slash:
                        rule = rule.rstrip("/")
                    app.add_url_rule(rule, route_name, proxy,
                                     methods=methods,
                                     subdomain=subdomain)

                else:
                    methods = value._methods_cache \
                        if hasattr(value, "_methods_cache") \
                        else ["GET"]

                    name = utils.dasherize(name)
                    route_str = '/%s/' % name
                    if not cls.trailing_slash:
                        route_str = route_str.rstrip('/')
                    rule = cls._build_rule__(route_str, value)
                    app.add_url_rule(rule, route_name, proxy,
                                     subdomain=subdomain,
                                     methods=methods)
            except DecoratorCompatibilityError:
                raise DecoratorCompatibilityError(
                    "Incompatible decorator detected on %s in class %s" % (name, cls.__name__))

        # Error Handler
        # To handle error
        # error code: _error_$code, ie: _error_400(), _error_500()
        # or catch-all, _error_handler()
        for name, fn in _get_interesting_members_http_error(Assembly, cls):
            match = _match_http_error(name)
            if match:
                try:
                    mname = match.groups()[0]
                    exc = int(mname) if mname.isdigit() else HTTPException
                    app.register_error_handler(exc, lambda e: cls._error_handler__(fn, e))
                except KeyError as kE:
                    raise AssemblyError(str(kE) + " - module: '%s'" % _get_full_method_name(fn))

        if hasattr(cls, "orig_base_route"):
            cls.base_route = cls.orig_base_route
            del cls.orig_base_route

        if hasattr(cls, "orig_route_prefix"):
            cls.route_prefix = cls.orig_route_prefix
            del cls.orig_route_prefix

        if hasattr(cls, "orig_trailing_slash"):
            cls.trailing_slash = cls.orig_trailing_slash
            del cls.orig_trailing_slash

    @classmethod
    def _parse_options__(cls, options):
        """Extracts subdomain and endpoint values from the options dict and returns
           them along with a new dict without those values.
        """
        options = options.copy()
        subdomain = options.pop('subdomain', None)
        endpoint = options.pop('endpoint', None)
        return subdomain, endpoint, options,

    @classmethod
    def _make_proxy_method__(cls, name):
        """Creates a proxy function that can be used by Flasks routing. The
        proxy instantiates the Assembly subclass and calls the appropriate
        method.
        :param name: the name of the method to create a proxy for
        """

        i = cls()
        view = getattr(i, name)

        for decorator in cls.decorators:
            view = decorator(view)

        @functools.wraps(view)
        def proxy(**forgettable_view_args):
            # Always use the global request object's view_args, because they
            # can be modified by intervening function before an endpoint or
            # wrapper gets called. This matches Flask's behavior.
            del forgettable_view_args

            if hasattr(i, "_before_request"):
                response = i._before_request(name, **request.view_args)
                if response is not None:
                    return response

            before_view_name = "_before_" + name
            if hasattr(i, before_view_name):
                before_view = getattr(i, before_view_name)
                response = before_view(**request.view_args)
                if response is not None:
                    return response

            response = view(**request.view_args)

            # You can also return a dict or None, it will pass it to render
            if isinstance(response, dict) or response is None:
                response = response or {}
                if hasattr(i, "_renderer"):
                    response = i._renderer(response)
                else:
                    template = _make_template_path(cls, view.__name__)
                    response.setdefault("__template__", template)
                    response = i.render(**response)

            if not isinstance(response, Response):
                response = make_response(response)

            for ext in cls._ext:
                response = ext(response)

            after_view_name = "_after_" + name
            if hasattr(i, after_view_name):
                after_view = getattr(i, after_view_name)
                response = after_view(response)

            if hasattr(i, "_after_request"):
                response = i._after_request(name, response)

            #  set_cookie on the response, which was cached in the g object
            if __ASM_SET_COOKIES__ in g:
                cookies = g.pop(__ASM_SET_COOKIES__)
                for cookie in cookies:
                    response.set_cookie(*cookie[0], **cookie[1])
            return response

        return proxy

    @classmethod
    def _build_rule__(cls, rule, method=None):
        """Creates a routing rule based on either the class name (minus the
        'View' suffix) or the defined `base_route` attribute of the class

        :param rule: the path portion that should be appended to the
                     route base

        :param method: if a method's arguments should be considered when
                       constructing the rule, provide a reference to the
                       method here. arguments named "self" will be ignored
        """

        rule_parts = []

        if cls.route_prefix:
            rule_parts.append(cls.route_prefix)

        base_route = cls._get_base_route__()
        if base_route:
            rule_parts.append(base_route)

        rule_parts.append(rule)
        ignored_rule_args = ['self']
        if hasattr(cls, 'base_args'):
            ignored_rule_args += cls.base_args

        if method:
            args = _get_true_argspec(method)[0]
            for arg in args:
                if arg not in ignored_rule_args:
                    rule_parts.append("<%s>" % arg)

        result = "/%s" % "/".join(rule_parts)
        return re.sub(r'(/)\1+', r'\1', result)

    @classmethod
    def _get_base_route__(cls):
        """Returns the route base to use for the current class."""
        base_route = cls.__name__.lower()
        if cls.base_route is not None:
            base_route = cls.base_route
            base_rule = parse_rule(base_route)
            cls.base_args = [r[2] for r in base_rule]
        return base_route.strip("/")

    @classmethod
    def _error_handler__(cls, fn, e):
        """
        Error handler callback.
        adding _error_handler() or _error_$code()/_error_404(), 
        will trigger this method to return the response
        The method must accept one arg, which is the error object 
        'self' can still be used in your class
        :param fn: the method invoked
        :param e: the error object
        """
        resp = fn(cls, e)
        if isinstance(resp, Response) or isinstance(resp, BaseResponse):
            return resp
        if isinstance(resp, dict) or isinstance(resp, tuple) or resp is None:
            data, status, headers = utils.prepare_view_response(resp)
            # create template from the error name, without the leading _,
            # ie: _error_handler -> error_handler.html, _error_404 -> error_404.html
            # template can be changed using @respone.template('app/class/action.html')
            if "__template__" not in data:
                data["__template__"] = _make_template_path(cls, fn.__name__.lstrip("_"))
            return cls.render(**resp), e.code, headers
        return resp

# ------------------------------------------------------------------------------

def apply_function_to_members(cls, fn):
    """
    Apply a function to all the members of a class.
    Used for decorators that is applied in a class and want all the members
    to use it
    :param cls: class
    :param fn: function
    :return: 
    """
    for name, method in _get_interesting_members(Assembly, cls):
        setattr(cls, name, fn(method))

# ------------------------------------------------------------------------------
# Utility functions

def _sanitize_module_name(module_name):
    return module_name.replace(".views", "")

def _get_full_method_name(mtd):
    return "%s.%s" % (mtd.__module__, mtd.__name__)


def _register_models(**kwargs):
    """
    Alias to register model
    :param kwargs:
    :return:
    """
    [setattr(models, k, v) for k, v in kwargs.items()]

def _register_view(cls):
    """
    To register a view that will be accessed in the `views` object
    so view path can be reached like: redirect(views.modules.main.Index.index)
    :param cls: the view class
    """
    mod = views
    module_name = _sanitize_module_name(cls.__module__)
    if "." in module_name:
        for k in module_name.split("."):
            if not hasattr(mod, k):
                setattr(mod, k, type('', (), {}))
            mod = getattr(mod, k)
    setattr(mod, cls.__name__, cls)

def _get_action_endpoint(action):
    """
    Return the endpoint base on the view's action
    :param action:
    :return:
    """
    _endpoint = None
    if inspect.ismethod(action) and hasattr(action, "_rule_cache"):
        rc = action._rule_cache
        if rc:
            k = list(rc.keys())[0]
            rules = rc[k]
            len_rules = len(rules)
            if len_rules == 1:
                rc_kw = rules[0][1]
                _endpoint = rc_kw.get("endpoint", None)
                if not _endpoint:
                    _endpoint = _make_routename_from_endpoint(action)
            elif len_rules > 1:
                _prefix = _make_routename_from_endpoint(action)
                for r in Assembly._app.url_map.iter_rules():
                    if ('GET' in r.methods or 'POST' in r.methods) and _prefix in r.endpoint:
                        _endpoint = r.endpoint
                        break
    return _endpoint


def _make_routename_from_cls(cls, method_name, class_name=None):
    """
    Build the route endpoint
    It is recommended to place your views in /views directory, so it can build
    the endpoint from it. If not, it will make the endpoint from the module name
    The main reason for having the views directory, it is explicitly easy
    to see the path of the view

    :param cls: The view class
    :param method_name: The name of the method
    :param class_name: To pass the class name.
    :return: string
    """
    m = _sanitize_module_name(cls.__module__)
    return "%s.%s.%s" % (m, class_name or cls.__name__, method_name)


def _make_routename_from_endpoint(endpoint):
    class_name, method_name = endpoint.__qualname__.split(".", 2)
    return _make_routename_from_cls(endpoint, method_name, class_name)


def _register_application_template(pkg, prefix):
    """
    Allow to register an app templates by loading and exposing: templates, static,
    and exceptions for abort()

    Structure of package
        root
            | $package_name
                | __init__.py
                |
                | /templates
                    |
                    |
                |
                | /static
                    |
                    | assets.yml

    :param pkg: str - __package__
                    or __name__
                    or The root dir
                    or the dotted resource package (package.path.path,
                    usually __name__ of templates and static
    :param prefix: str - to prefix the template path
    """
    root_pkg_dir = pkg
    if not os.path.isdir(pkg):
        root_pkg_dir = pkg_resources.resource_filename(pkg, "")

    template_path = os.path.join(root_pkg_dir, "templates")
    static_path = os.path.join(root_pkg_dir, "static")

    if os.path.isdir(template_path):
        loader = jinja2.FileSystemLoader(template_path)
        Assembly._template_fsl.update({prefix: loader})
    if os.path.isdir(static_path):
        Assembly._static_paths.add(static_path)


def _make_template_path(cls, method_name):
    _template = _make_routename_from_cls(cls, method_name)
    m = _template.split(".")
    if "views" in m:
        m.remove("views")
    _template = ".".join(list(m))
    _template = utils.list_replace([".", ":"], "/", _template)
    return "%s.html" % _template


def _get_interesting_members(base_class, cls):
    """Returns a generator of methods that can be routed to"""

    base_members = dir(base_class)
    predicate = inspect.ismethod if six.PY2 else inspect.isfunction
    all_members = inspect.getmembers(cls, predicate=predicate)
    return (member for member in all_members
            if not member[0] in base_members
            and (
                (hasattr(member[1], "__self__") and not member[1].__self__ in inspect.getmro(cls)) if six.PY2 else True)
            and not member[0].startswith("_")
            and not member[0].startswith("before_")
            and not member[0].startswith("after_"))


def _get_interesting_members_http_error(base_class, cls):
    """Returns a generator of methods that can be routed to"""

    base_members = dir(base_class)
    predicate = inspect.ismethod if six.PY2 else inspect.isfunction
    all_members = inspect.getmembers(cls, predicate=predicate)
    return (member for member in all_members
            if not member[0] in base_members
            and ((hasattr(member[1], "__self__") and not member[1].__self__ in inspect.getmro(cls)) if six.PY2 else True)
            and member[0].startswith("_")
            and _match_http_error(member[0])
            and not member[0].startswith("before_")
            and not member[0].startswith("after_"))


def _match_http_error(val):
    """
    catches:
    _error_$code, _error_404
    _error_handler
    :param val: string
    :return: object or None
    """
    return re.match(r"^_error_(\d+|handler)$", val)


def _get_true_argspec(method):
    """Drills through layers of decorators attempting to locate the actual argspec for the method."""

    argspec = inspect.getargspec(method)
    args = argspec[0]
    if args and args[0] == 'self':
        return argspec
    if hasattr(method, '__func__'):
        method = method.__func__
    if not hasattr(method, '__closure__') or method.__closure__ is None:
        raise DecoratorCompatibilityError

    closure = method.__closure__
    for cell in closure:
        inner_method = cell.cell_contents
        if inner_method is method:
            continue
        if not inspect.isfunction(inner_method) \
                and not inspect.ismethod(inner_method):
            continue
        true_argspec = _get_true_argspec(inner_method)
        if true_argspec:
            return true_argspec

# ------------------------------------------------------------------------------
# Utility classes

class AssemblyError(Exception):
    """
    This exception is not reserved, but it used for all Assembly exception.
    It helps catch Core problems.
    """

class DecoratorCompatibilityError(Exception):
    pass


class _RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(_RegexConverter, self).__init__(url_map)
        self.regex = items[0]


class _JinjaPrefixLoader(jinja2.PrefixLoader):
    """
    Prefix loader modifier, that will take into account the full path
    """
    def get_loader(self, template):
        try:
            for prefix in self.mapping.keys():
                prek = prefix.replace(".", "/") + "/"
                if template.startswith(prek):
                    name = template.split(prek, 1)[1]
                    break
            else:
                prefix, name = template.split(self.delimiter, 1)
            loader = self.mapping[prefix]
        except (ValueError, KeyError):
            raise jinja2.exceptions.TemplateNotFound(template)
        return loader, name