# -*- coding: utf-8 -*-
"""
Assembly: response
"""

import copy
import arrow
import inspect
import functools
from . import utils
import flask_caching
from jinja2 import Markup
from dicttoxml import dicttoxml
from werkzeug.wrappers import BaseResponse
from .assembly import (Assembly, app_context, apply_function_to_members)
from flask import (Response,
                   jsonify,
                   request,
                   current_app,
                   url_for,
                   make_response,
                   g)

# ----------------------------------------------------------------------------------------------------------------------
# ----  Monkey patch jsonify, to convert other data type: ie: Arrow
import flask.json
from flask.json import dumps as flask_dumps


class _JSONEnc(flask.json.JSONEncoder):
    def default(self, o):
        if isinstance(o, arrow.Arrow):
            return o.for_json()
        else:
            return super(self.__class__, self).default(o)


def dumps(o, **kw):
    kw["cls"] = _JSONEnc
    return flask_dumps(o, **kw)
flask.json.dumps = dumps

# ----------------------------------------------------------------------------------------------------------------------


__view_parsers = set()


def view_parser(f):
    """
    A simple decorator to to parse the data that will be rendered
    :param func:
    :return:
    """
    __view_parsers.add(f)
    return f

def _build_response(data, renderer=None):
    """
    Build a response using the renderer from the data
    :return:
    """
    if isinstance(data, Response) or isinstance(data, BaseResponse):
        return data
    if not renderer:
        raise AttributeError(" Renderer is required")

    data, status, headers = utils.prepare_view_response(data)
    for _ in __view_parsers:
        data = _(data) 
    return make_response(renderer(data), status, headers)

json_renderer = lambda i, data: _build_response(data, jsonify)
xml_renderer = lambda i, data: _build_response(data, dicttoxml)

def json(func):
    """
    Decorator to render as JSON
    :param func:
    :return:
    """
    if inspect.isclass(func):
        apply_function_to_members(func, json)
        return func
    else:
        @functools.wraps(func)
        def decorated_view(*args, **kwargs):
            data = func(*args, **kwargs)
            return _build_response(data, jsonify)
        return decorated_view

def xml(func):
    """
    Decorator to render as XML
    :param func:
    :return:
    """
    if inspect.isclass(func):
        apply_function_to_members(func, xml)
        return func
    else:
        @functools.wraps(func)
        def decorated_view(*args, **kwargs):
            data = func(*args, **kwargs)
            return _build_response(data, dicttoxml)
        return decorated_view

def jsonp(func):
    """Wraps JSONified output for JSONP requests.
    """

    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        callback = request.args.get('callback', None)
        if callback:
            data = str(func(*args, **kwargs))
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)
    return decorated_view

def template(page=None, **kwargs):
    """
    Decorator to change the view template.

    It works only on view methods

    ** on method that return a dict
        page or layout are optional

        :param page: The html page
        :param layout: The layout to use for that view

        :param kwargs:
            get pass to the view as k/V

    ** on other methods that return other type, it doesn't apply

    :return:
    """
    pkey = "_template_extends__"

    def decorator(f):
        if inspect.isclass(f):
            raise Error("@template can only be applied on Assembly methods")
            return f
        else:
            @functools.wraps(f)
            def wrap(*args2, **kwargs2):
                response = f(*args2, **kwargs2)
                if isinstance(response, dict) or response is None:
                    response = response or {}
                    if page:
                        response.setdefault("__template__", page)
                    for k, v in kwargs.items():
                        response.setdefault(k, v)
                return response
            return wrap
    return decorator

def headers(params={}):
    """This decorator adds the headers passed in to the response
    """
    def decorator(f):

        if inspect.isclass(f):
            h = headers(params)
            apply_function_to_members(f, h)
            return f

        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            resp = make_response(f(*args, **kwargs))
            h = resp.headers
            for header, value in params.items():
                h[header] = value
            return resp
        return decorated_function
    return decorator

def noindex(f):
    """This decorator passes X-Robots-Tag: noindex"""
    return headers({'X-Robots-Tag': 'noindex'})(f)

# ------------------------------------------------------------------------------
"""
Caching
Allow caching in the response
@cache

@reponse.cache(timeout=10)
def cached(self):
    ...

"""
caching = flask_caching.Cache()

@app_context
def _init_caching(app):
    utils.flatten_config_property("CACHE", app.config)
    caching.init_app(app)

cache = caching.cached

