
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


do_something("hello MM", location="CLT", music="TUPAC", genre="Hip-Hop")
# do_something("Gettho Gospel!")
# do_something("Costa Rica!")

