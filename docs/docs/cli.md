
## Overview

Assembly provides a CLI tool and framework based on **Click** library

Extension: **<a href="https://click.palletsprojects.com/" target="_blank">Click</a>**

---

## Usage

Upon installing Assembly via `pip install assembly`, two commands will be available for the command line:

- `asm`: for custom command list
- `asm-admin`: for Assembly specific commands

---

## Admin CLI: asm-admin

This command allows you to access Assembly specific commands

### init

To initialize Assembly for the first time in the current directory

```sh
cd my-dir
asm-admin init
```

### serve

To run the development server.

```sh
asm-admin serve
```

or changing environment

```sh
export ASSEMBLY_ENV=Staging 
asm-admin serve
```

or changing environment and app

```sh
export ASSEMBLY_ENV=Testing
export ASSEMBLY_APP=api
asm-admin serve
```


### sync-models

To sync database models to create new tables. Models that extended `db.Model` will be created.

```sh
asm-admin sync-models
```

### gen-api-view

To create a view that can be used as API endpoint

```sh
asm-admin gen-api-view $view-name
```

ie:

```sh
asm-admin gen-api-view api
```

It will create a new view at the root. 


### gen-template-view

To create a view that contains template

```sh
asm-admin gen-template-view $view-name
```

ie:

```sh
asm-admin gen-api-view admin
```

It will create a new view `admin` at the root. 

### upload-assets-s3

If you are serving your assets via CDN or S3, you need to upload them before deploying the application.

When `config.ASSETS_DELIVERY_METHOD` is `S3`, this util will allow you to upload
your assets to S3, and the application will automatically point all your assets
to S3.

```sh
asm-admin upload-assets-s3
```

### version

Return the version of Assembly

```sh
asm-admin version
```

---


## Custom CLI: asm

Assembly also allows you to create your own CLI scripts, to use with your application. 

You probably need CLI to run some routines and setup outside of the web environment, ie: setup database, run worker/task, cronjob, scheduler, etc...


### 1. Create CLI Functions

Assembly CLI is based on **<a href="https://click.palletsprojects.com/" target="_blank">Click</a>** library.

Inside of your view, create `cli.py` (named so for discoverability). 

NOTE: `@command` is the alias to the custom command. Use it, otherwise your CLI scripts won't be available.

Learn more about **<a href="https://click.palletsprojects.com/" target="_blank">Click</a>**

```python
# main/cli.py

from assembly.cli import (command, option, argument, click)

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

#->>> Import your CLI in the wsgi.py
import admin.cli

APPS = {
    "default": [
        "main"
    ]
}

app = Assembly.init(__name__, APPS)

```


### 3. Execute Commands

Commands can easily be executed by invoking `asm` followed by the name of the function that had `@command`

Example:

```python
# main/cli.py

from assembly.cli import (command, option, argument, click)

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



