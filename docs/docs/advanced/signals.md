

## Overview

Signals help you decouple applications by sending notifications when actions occur elsewhere in the appliation. In short, signals allow certain senders to notify subscribers that something happened.



Assembly uses **Blinker** to provide a fast dispatching system that allows any number of
interested parties to subscribe to events, or “signals”.

Extension: <a href="https://pythonhosted.org/blinker/" target="_blank">Blinker</a>

---

## Usage

### Import

```python
from assembly import signal
```


### Create a signal

Import and use the `@signal` decorator on the function to send signal from. It will add a `@pre` and `@post` decorators on that function to be used by other function that will listens it.

Whenever the function with the `@signal` get executed, all functions with `@pre` and `@post` will be executed before and after the `@signal` function is executed repectively.

```python
from assembly import signal

@signal
def hello_world(name):
    return "Hello World %s" %s

```

### Listens to a signal


Now `hello_world` has `@hello_world.pre` and `@hello_world.post`. These decorators can attached to functions.

```python

@hello_world.pre
def before_hello_world(*a, **kw):
    """This will be executed before"""

@hello_world.post
def after_hello_world(result, *kw):
    """This will be executed after"""
    if result:
        print(result)

@hello_world.post
def after_another_hello_world(result, *kw):
    """This will be executed after"""
    if result:
        print(result)

```

### Full Example

Now we can run the functions and our signals will be executed


```python
from assembly import signal

# Emit the signal

@signal
def hello_world(name):
    return "Hello World %s" %s

# Listeners

@hello_world.pre
def before_hello_world(*a, **kw):
    """This will be executed before"""

@hello_world.post
def after_hello_world(result, *kw):
    """This will be executed after"""
    if result:
        print(result)

@hello_world.post
def after_another_hello_world(result, *kw):
    """This will be executed after"""
    if result:
        print(result)


hello_world('Assembly')
hello_world('Mardix')

```


## API

### @signal

---

### @pre

Functions with `@pre` will be executed before the signaled functions is executed.

The function receiving the signal, must have 1 args:

```
- *a
- **kwargs: 
    args: *a,
    kwargs: **kw,
    name: the name of the signal,
    signal: the signal's instance
```

Example

```python
@myfn.pre
def post_action(*a, **kw):
    pass

```

---

### @post

Functions with `@post` will be executed after the signaled functions is finished.

The function receiving the signal, must have 2 args:
```
- result: that's the result sent from the signal
- **kwargs: 
    args: *a,
    kwargs: **kw,
    name: the name of the signal,
    signal: the signal's instance
```

Example

```python
@myfn.post
def post_action(result, **kw):
    if result: 
        print("Done!")

```

### @pre_ and @post_

To fully utilize Blinker functionalities, use `post_` and `pre_`, for example
`@do_something.post_.connect`, `@do_something.pre_.connect`

