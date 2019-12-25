
## Overview

Assembly provides support for writing external scripts. This includes running a development server, a customised Python shell, scripts to set up your database, cronjobs, and other command-line tasks that belong outside the web application itself.

Assembly provides a CLI tool and framework based on **Click** library

Extension: **<a href="https://click.palletsprojects.com/" target="_blank">Click</a>**

---

## Usage

Upon installing Assembly via `pip install assembly`, Assembly will setup a command line tool for you to interface with some scripts via the `asm` command.

There are the Generator commands start with `asm gen:*` and your custom commands

---

## Commands

### gen:init

To initialize Assembly for the first time in the current directory

```sh
cd my-dir
asm gen:init
```

### gen:serve

To run the development server.

```sh
asm gen:serve
```

or changing environment

```sh
export ASSEMBLY_ENV=Staging 
asm gen:serve
```

or changing environment and app

```sh
export ASSEMBLY_ENV=Testing
export ASSEMBLY_APP=api
asm gen:serve
```


### gen:sync-models

To sync database models to create new tables. Models that extended `db.Model` will be created.

```sh
asm gen:sync-models
```

### gen:view

To generate to generate a view file with its associated templates. The view file will be created in `/views`, and the templates will be in `/templates`

```sh
asm gen:view $view-name
```

ie:

```sh
asm gen:view admin
```

#### Restful

This command can also create a view without templates, by appending `--resftul` or `-x` 

```sh
asm gen:view api --resful
```

It will create a new module structure in the `/modules` directory.  

### gen:upload-assets-s3

If you are serving your assets via CDN or S3, you need to upload them before deploying the application.

When `config.ASSETS_DELIVERY_METHOD` is `S3`, this util will allow you to upload
your assets to S3, and the application will automatically point all your assets
to S3.

```sh
asm gen:upload-assets-s3
```

### gen:version

Return the version of Assembly

```sh
asm gen:version
```

---


## Custom Scripts

Assembly also allows you to create your own CLI scripts, to use with your application. 

It's recommended to place your scripts at `run/scripts.py`.

You probably need CLI to run some routines and setup outside of the web environment, ie: setup database, run worker/task, cronjob, scheduler, etc...


### 1. Create CLI Functions

Assembly CLI is based on **<a href="https://click.palletsprojects.com/" target="_blank">Click</a>** library.

Inside of your view, create `scripts.py` (named so for discoverability). 

NOTE: `@command` is the alias to the custom command. Use it, otherwise your CLI scripts won't be available.

Learn more about **<a href="https://click.palletsprojects.com/" target="_blank">Click</a>**

```python
# run/scripts.py

from assembly.scripts import (command, option, argument, click)

@command
def hello():
  print("Hello world!")

@command('do-something')
@argument(name)
def do_something(name):
  print("Hello %s" % name)

```

### 2. Import in wsgi.py
```python
# wsgi.py

from assembly import Assembly

#->>> Import scripts wsgi.py
import run.scripts

APPS = {
    "default": [
        "views.main"
    ]
}

app = Assembly.init(__name__, APPS)

```


### 3. Execute Commands

Commands can easily be executed by invoking `asm` followed by the name of the function that had `@command`

Example:

```python
# run/scripts.py

from assembly.scripts import (command, option, argument, click)

@command
def hello():
  print("Hello world!")

>> asm hello

@command('do-something')
@argument(name)
def do_something(name):
  print("Hello %s" % name)

>> asm do-something Assembly

it will print out: `Hello Assembly`
```



