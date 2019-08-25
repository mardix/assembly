
def init_app(kls):
    """
    To bind middlewares, plugins that needs the 'app' object to init
    Bound middlewares will be assigned on cls.init()
    """
    if not hasattr(kls, "__call__"):
        raise Error("init_app: '%s' is not callable" % kls)
    #Flasik._init_apps.add(kls)
    print('registered 1')
    return kls

def deco(f):
  print('register deco')
  init_app(f)

@init_app
def hello():
  pass

init_app(hello)