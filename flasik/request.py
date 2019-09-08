import inspect
from flask import  request
from .core import _bind_route_rule_cache, extends
import flask_seasurf


def is_get():
    return request.method == "GET"

def is_post():
    return request.method == "POST"

def is_put():
    return request.method == "PUT"

def is_delete(self):
    return request.method == "DELETE"

def _accept_method(methods, f):
    kw = {
        "append_method": True,
        "methods": methods
    }
    _bind_route_rule_cache(f, rule=None, **kw)
    return f


def get(f):
    """ decorator to accept GET method """
    return _accept_method(["GET"], f)


def post(f):
    """ decorator to accept POST method """
    return _accept_method(["POST"], f)


def post_get(f):
    """ decorator to accept POST & GET method """
    return _accept_method(["POST", "GET"], f)


def delete(f):
    """ decorator to accept DELETE method """
    return _accept_method(["DELETE"], f)


def put(f):
    """ decorator to accept PUT method """
    return _accept_method(["PUT"], f)


def all(f):
    """ decorator to accept ALL methods """
    return _accept_method(["GET", "POST", "DELETE", "PUT", "OPTIONS", "UPDATE"], f)


def options(f):
    """ decorator to accept OPTIONS methods """
    return _accept_method(["OPTIONS"], f)


def route(rule=None, **kwargs):
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



def get_auth_bearer():
    """
    Return the authorization bearer
    :return: string
    """
    if 'Authorization' not in request.headers:
        raise ValueError("Missing Authorization Bearer in headers")
    data = request.headers['Authorization'].encode('ascii', 'ignore')
    return str.replace(str(data), 'Bearer ', '').strip()

# CSRF
# :decorator
#   - csrf.exempt
# @request.csrf_exempt
# https://flask-seasurf.readthedocs.io/en/latest/
csrf = flask_seasurf.SeaSurf()
extends(csrf.init_app)
csrf_exempt = csrf.exempt