from flask import Flask
import blinker
import inspect
import functools


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


@signal
def do_something(data, **kw):
    print("MY OWN KW", kw)
    return data


@do_something.post
def my_thing(result, **kw):
    print("LISTENER", result, kw)


@do_something.post
def my_thing2(result, **kw):
    print("I just pull up to this party-----", result, kw)


@do_something.pre
def before_thing(*a, **kw):

    print("BEFORE THING", kw["kwargs"])
    kw["kwargs"]["genre"] = "Rap"
    print("BEFORE THING", kw["kwargs"])


#do_something("hello MM", location="CLT", music="TUPAC", genre="Hip-Hop")
# do_something("Gettho Gospel!")
# do_something("Costa Rica!")

class Conf(object):

    CORS = {
        "NAME": "A",
        "B": "C",
        "D": "E"
    }

    # The AWS Access KEY
    AWS_ACCESS_KEY_ID = ""

    # Secret Key
    AWS_SECRET_ACCESS_KEY = ""

    # The bucket name for S3
    AWS_S3_BUCKET_NAME = ""

    # The default region name
    AWS_REGION_NAME = "us-east-1"

    AWS = {
        "ACCESS_KEY_ID": "",
        "SECRET_ACCESS_KEY": "",
        "S3_BUCKET_NAME": "",
        "REGION_NAME": "",
        "LOCATION": "TOU_WOUJ"
    }


def config_flatten_property(key, config):
    """
    To flatten a config property
    This method is mutable
    Having a config:
    class Conf(object):
      AWS = {
        "ACCESS_KEY_ID": "",
        "SECRET_ACCESS_KEY": ""
      }

    config_flatten_property("AWS", app.config)

    it will flatten the config to be:
      AWS_ACCESS_KEY_ID
      AWS_SECRET_ACCESS_KEY

    If the key exists already, it will not modify it

    :param key: string - the key to flatten
    :param dict: app.config - the flask app.config or dict
    """
    if key in config:
        for k, v in config[key].items():
            _ = "%s_%s" % (key, k.upper())
            if _ not in config:
                config[_] = v


app = Flask(__name__)
app.testing = True
app.config.from_object(Conf())

config_flatten_property("AWS", app.config)
config_flatten_property("CORS", app.config)

print(app.config)


send_mail(to="", subject="", body="")
send_mail(to="", template="", )