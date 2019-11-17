# -*- coding: utf-8 -*-
"""
Assembly: request
"""

import inspect
import flask_cors
import flask_seasurf
from flask import request as f_request
from .assembly import app_context
from . import utils


# CSRF
# :decorator
#   - csrf.exempt
# @request.csrf_exempt
# https://flask-seasurf.readthedocs.io/en/latest/
csrf = flask_seasurf.SeaSurf()
app_context(csrf.init_app)


class RequestProxy(object):
    """
    A request proxy, that attaches some special attributes to the Flask request object
    """

    # CSRF
    csrf = csrf

    @property
    def IS_GET(self):
        return f_request.method == "GET"

    @property
    def IS_POST(cls):
        return f_request.method == "POST"

    @property
    def IS_PUT(self):
        return f_request.method == "PUT"

    @property
    def IS_DELETE(self):
        return f_request.method == "DELETE"

    @classmethod
    def _accept_method(cls, methods, f):
        kw = {
            "append_method": True,
            "methods": methods
        }
        _bind_route_rule_cache(f, rule=None, **kw)
        return f

    @classmethod
    def cors(cls, fn):
        """
        CORS decorator, to make the endpoint available for CORS

        Make sure @cors decorator is placed at the top position.
        All response decorators must be placed below. 
        It's because it requires a response to be available

        class Index(Assembly):
            def index(self):
                return self.render()

            @request.cors
            @response.json
            def json(self):
                return {}

        :return:
        """
        if inspect.isclass(fn):
            raise Error("@cors can only be applied on Assembly methods")
        else:
            cors_fn = flask_cors.cross_origin(automatic_options=True)
            return cors_fn(fn)

    @classmethod
    def get(cls, f):
        """ decorator to accept GET method """
        return cls._accept_method(["GET"], f)

    @classmethod
    def post(cls, f):
        """ decorator to accept POST method """
        return cls._accept_method(["POST"], f)

    @classmethod
    def post_get(cls, f):
        """ decorator to accept POST & GET method """
        return cls._accept_method(["POST", "GET"], f)

    @classmethod
    def delete(cls, f):
        """ decorator to accept DELETE method """
        return cls._accept_method(["DELETE"], f)

    @classmethod
    def put(cls, f):
        """ decorator to accept PUT method """
        return cls._accept_method(["PUT"], f)

    @classmethod
    def all(cls, f):
        """ decorator to accept ALL methods """
        return cls._accept_method(["GET", "POST", "DELETE", "PUT", "OPTIONS", "UPDATE"], f)

    @classmethod
    def options(cls, f):
        """ decorator to accept OPTIONS methods """
        return cls._accept_method(["OPTIONS"], f)

    @classmethod
    def route(cls, rule=None, **kwargs):
        """
        This decorator defines custom route for both class and methods in the view.
        It behaves the same way as Flask's @app.route
        on class:
            It takes the following args
                - rule: the root route of the endpoint
                - decorators: a list of decorators to run on each method
        on methods:
            along with the rule, it takes kwargs
                - endpoint
                - defaults
                - ...
        :param rule:
        :param kwargs:
        :return:
        """

        _restricted_keys = ["route", "decorators"]

        def decorator(f):
            if inspect.isclass(f):
                kwargs.setdefault("route", rule)
                kwargs["decorators"] = kwargs.get("decorators", []) + f.decorators
                setattr(f, "_route_extends__", kwargs)
                setattr(f, "base_route", kwargs.get("route"))
                setattr(f, "decorators", kwargs.get("decorators", []))
            else:
                if not rule:
                    raise ValueError("'rule' is missing in @route ")

                for k in _restricted_keys:
                    if k in kwargs:
                        del kwargs[k]

                _bind_route_rule_cache(f, rule=rule, **kwargs)
            return f

        return decorator

    def __getattr__(self, item):
        # Fall back to flask request
        return getattr(f_request, item)


    @classmethod
    def get_auth_bearer(cls):
        """
        Return the authorization bearer
        :return: string
        """
        if 'Authorization' not in f_request.headers:
            raise ValueError("Missing Authorization Bearer in headers")
        data = f_request.headers['Authorization'].encode('ascii', 'ignore')
        return str.replace(str(data), 'Bearer ', '').strip()

request = RequestProxy()


def _bind_route_rule_cache(f, rule, append_method=False, **kwargs):
    """
    Put the rule cache on the method itself instead of globally
    :param f:
    :param rule:
    :param append_method:

    """
    if rule is None:
        rule = utils.dasherize(f.__name__) + "/"
    if not hasattr(f, '_rule_cache') or f._rule_cache is None:
        f._rule_cache = {f.__name__: [(rule, kwargs)]}
    elif not f.__name__ in f._rule_cache:
        f._rule_cache[f.__name__] = [(rule, kwargs)]
    else:
        # when an endpoint accepts multiple METHODS, ie: post(), get()
        if append_method:
            for r in f._rule_cache[f.__name__]:
                if r[0] == rule and "methods" in r[1] and "methods" in kwargs:
                    r[1]["methods"] = list(set(r[1]["methods"] + kwargs["methods"]))
        else:
            f._rule_cache[f.__name__].append((rule, kwargs))
    return f
