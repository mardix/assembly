# -*- coding: utf-8 -*-
"""
decorators.py

Misc decorators

"""

import copy
import inspect
import blinker
import functools
import flask_cors
from .core import (init_app as h_init_app,
                   apply_function_to_members)
from flask import make_response


# ------------------------------------------------------------------------------

def init_app(f):
    """
    Decorator for init_app
    As a convenience
    ie:
    def fn(app):
        pass
        
    before you would do: init_app(fn)
    
    with this decorator
    
    @init_app
    def fn(app):
        pass
        
    """
    return h_init_app(f)

# ------------------------------------------------------------------------------

def cors(*args, **kwargs):
    """
    A wrapper around flask-cors cross_origin, to also act on classes

    **An extra note about cors, a response must be available before the
    cors is applied. Dynamic return is applied after the fact, so use the
    decorators, json, xml, or return self.render() for txt/html
    ie:
    @cors()
    class Index(Mocha):
        def index(self):
            return self.render()

        @json
        def json(self):
            return {}

    class Index2(Mocha):
        def index(self):
            return self.render()

        @cors()
        @json
        def json(self):
            return {}


    :return:
    """
    def decorator(fn):
        cors_fn = flask_cors.cross_origin(automatic_options=False, *args, **kwargs)
        if inspect.isclass(fn):
            apply_function_to_members(fn, cors_fn)
        else:
            return cors_fn(fn)
        return fn
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



# ------------------------------------------------------------------------------
"""
Signals

Signals allow you to connect to a function and re

Usage

1.  Emitter.
    Decorate your function with @emit_signal.
    That function itself will turn into a decorator that you can use to
    receivers to be dispatched pre and post execution of the function

    @emit_signal()
    def login(*a, **kw):
        # Run the function
        return

    @emit_signal()
    def logout(your_fn_args)
        # run function
        return

2.  Receivers/Observer.
    The function that was emitted now become signal decorator to use on function
    that will dispatch pre and post action. The pre and post function will
    be executed before and after the signal function runs respectively.

    @login.pre.connect
    def my_pre_login(*a, **kw):
        # *a, **kw are the same arguments passed to the function
        print("This will run before the signal is executed")

    @login.post.connect
    def my_post_login(result, **kw):
        result: the result back
        **kw
            params: params passed 
            sender: the name of the funciton
            emitter: the function that emits this signal
            name: the name of the signal
        print("This will run after the signal is executed")

    # or for convenience, same as `post.connect`, but using `observe`
    @login.observe
    def my_other_post_login(result, **kw):
        pass
    
3.  Send Signal
    Now sending a signal is a matter of running the function.

    ie:
    login(username, password)

That's it!

"""
__signals_namespace = blinker.Namespace()


def emit_signal(sender=None, namespace=None):
    """
    @emit_signal
    A decorator to mark a method or function as a signal emitter
    It will turn the function into a decorator that can be used to 
    receive signal with: $fn_name.pre.connect, $fn_name.post.connect 
    *pre will execute before running the function
    *post will run after running the function
    
    **observe is an alias to post.connect
    
    :param sender: string  to be the sender.
    If empty, it will use the function __module__+__fn_name,
    or method __module__+__class_name__+__fn_name__
    :param namespace: The namespace. If None, it will use the global namespace
    :return:

    """
    if not namespace:
        namespace = __signals_namespace

    def decorator(fn):
        fname = sender
        if not fname:
            fnargs = inspect.getargspec(fn).args
            fname = fn.__module__
            if 'self' in fnargs or 'cls' in fnargs:
                caller = inspect.currentframe().f_back
                fname += "_" + caller.f_code.co_name
            fname += "__" + fn.__name__

        # pre and post
        fn.pre = namespace.signal('pre_%s' % fname)
        fn.post = namespace.signal('post_%s' % fname)
        # alias to post.connect
        fn.observe = fn.post.connect

        def send(action, *a, **kw):
            sig_name = "%s_%s" % (action, fname)
            result = kw.pop("result", None)
            kw.update(inspect.getcallargs(fn, *a, **kw))
            sendkw = {
                "kwargs": {k: v for k, v in kw.items() if k in kw.keys()},
                "sender": fn.__name__,
                "emitter": kw.get('self', kw.get('cls', fn))
            }
            if action == 'post':
                namespace.signal(sig_name).send(result, **sendkw)
            else:
                namespace.signal(sig_name).send(**sendkw)

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            send('pre', *args, **kwargs)
            result = fn(*args, **kwargs)
            kwargs["result"] = result
            send('post', *args, **kwargs)
            return result
        return wrapper
    return decorator

