

Mocha uses [Blinker](https://pythonhosted.org/blinker/)
to provide a fast dispatching system that allows any number of
interested parties to subscribe to events, or “signals”.

As it will be described below, a best way to use signal is to dispatch data/message
between modules.

For example, when a user register using the built-in AUTH, you may want to do
something with that new user. So the create_user emit a signal containing
the new user data, and each function observing the create_user, will be executed


** Import **

    from mocha.decorators import emit_signal


## Emit Signal



### @emit_signal

A decorator that will turn a function into a signal emitter, which will contain
a `pre` and `post` signal.


    # signals.py
    from mocha import decorators as deco

    @deco.emit_signal
    def do_something(data):
        return data

The example above creates a signal `do_something`, each time this function
is invoked it will emit two signals `do_something.pre`
and `do_something.post`. These objects (pre, post) were created when `@emit_signal`
decorated the `do_something` function.

`pre` will be invoked before running accepting the signal, and `post` after the
signal is executed.

For every `@emit_signal` use, the function will have two blinker signal objects:
`pre` and `post`

    @emit_signal
    def hello():
        pass

will now have the following decorators:

    @hello.post
    @hello.pre


## Receive Signal

### @observe

`@observe` allows you to connect a function to an emitter. `@observe` is a shortcut
for `@post.connect`.


    import my_signals

    @signals.do_something.observe
    def my_thing(result, **kw):
        if result:
            pass




To fully utilize Blinker functionalities, use `post` and `pre`, for example
`@do_something.post.connect`, `@do_something.pre.connect`

### @post.connect

    @signals.do_something.post.connect
    def receive_create_user(user, **kw):
        if user:
            # do something with user

The function receiving the signal, must have 2 args:

- result: that's the result sent from the signal
- **kwargs: some
    - kwargs: kwargs that were passed in the signal function
    - sender: The name of the function
    - emitter: The instance of the

### @pre.connect

    @signals.do_something.pre.connect
    def receive_create_user_pre(**kw):
        # do something
