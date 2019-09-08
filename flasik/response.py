# -*- coding: utf-8 -*-

import copy
import inspect
import arrow
import blinker
import functools
import flask_cors
from jinja2 import Markup
from dicttoxml import dicttoxml
from werkzeug.wrappers import BaseResponse
import flask_cors
from .core import (Flasik,
                   apply_function_to_members,
                   build_endpoint_route_name
                   )
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


def _normalize_response_tuple(tuple_):
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
    if isinstance(data, dict) or data is None:
        data = {} if data is None else data
        for _ in __view_parsers:
            data = _(data)
        return make_response(renderer(data), 200, None)
    elif isinstance(data, tuple):
        data, status, headers = _normalize_response_tuple(data)
        for _ in __view_parsers:
            data = _(data)
        return make_response(renderer(data or {}), status, headers)
    return data

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
    http://flask.pocoo.org/snippets/79/
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
            raise Error("@template can only be applied on Flasik methods")
            return f
        else:
            @functools.wraps(f)
            def wrap(*args2, **kwargs2):
                response = f(*args2, **kwargs2)
                if isinstance(response, dict) or response is None:
                    response = response or {}
                    if page:
                        response.setdefault("template", page)
                    for k, v in kwargs.items():
                        response.setdefault(k, v)
                return response
            return wrap
    return decorator


def cors(*args, **kwargs):
    """
    Decorator
    A wrapper around flask-cors cross_origin, to also act on classes

    **An extra note about cors, a response must be available before the
    cors is applied. Dynamic return is applied after the fact, so use the
    decorators, json, xml, or return self.render() for txt/html
    ie:

    class Index(Flasik):
        def index(self):
            return self.render()

        @cors()
        @json
        def json(self):
            return {}

    class Index2(Flasik):
        def index(self):
            return self.render()

        @cors()
        @json
        def json(self):
            return {}


    :return:
    """
    def decorator(fn):
        cors_fn = flask_cors.cross_origin(automatic_options=True, *args, **kwargs)
        if inspect.isclass(fn):
            raise Error("@cors can only be applied on Flasik methods")
            return fn
        else:
            return cors_fn(fn)
    return decorator

def headers(params={}):
    """This decorator adds the headers passed in to the response
    http://flask.pocoo.org/snippets/100/
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
    """This decorator passes X-Robots-Tag: noindex
    http://flask.pocoo.org/snippets/100/
    """
    return headers({'X-Robots-Tag': 'noindex'})(f)
