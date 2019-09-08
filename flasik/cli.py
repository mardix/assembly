# -*- coding: utf-8 -*-
"""
The Flasik CLI 
"""

import os
import re
import sys
import traceback
import logging
import importlib
import pkg_resources
import click
import yaml
import functools
import json
from werkzeug import import_string
from .__about__ import *
from flasik import utils
import flask
import sh
import subprocess
from .core import db


CWD = os.getcwd()
SKELETON_DIR = "scaffold"
ENTRY_PY = "__flasik__.py"

flasik_app = None
app_dir = CWD
_cmds = []

__all__ = [
    "command",
    "argument",
    "options"
]

def get_project_dir_path(project_name):
    return "%s/%s" % (app_dir, project_name)


def copy_resource_dir(src, dest):
    """
    To copy package data directory to destination
    """
    package_name = "flasik"
    dest = (dest + "/" + os.path.basename(src)).rstrip("/")
    if pkg_resources.resource_isdir(package_name, src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        for res in pkg_resources.resource_listdir(__name__, src):
            copy_resource_dir(src + "/" + res, dest)
    else:
        if not os.path.isfile(dest) and os.path.splitext(src)[1] not in [".pyc"]:
            copy_resource_file(src, dest)


def copy_resource_file(src, dest):
    with open(dest, "wb") as f:
        f.write(pkg_resources.resource_string(__name__, src))


# ------------------------------------------------------------------------------

def run_cmd(cmd):
    subprocess.call(cmd.strip(), shell=True)


def get_propel_config(cwd, key):
    with open("%s/%s" % (cwd, "propel.yml")) as f:
        config = yaml.load(f)
    return config.get(key)


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
def catch_exception(func):
    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as ex:
            print("-" * 80)
            print("Exception Uncaught")
            print("-" * 80)
            print(ex)
            print("-" * 80)
    return decorated_view


def cwd_to_sys_path():
    sys.path.append(CWD)


def project_name(name):
    return re.compile('[^a-zA-Z0-9_]').sub("", name)

def bold(str):
    return '\033[1m%s\033[0m' % str

def header(title=None):
    print('*' * 80)
    print("%s v. %s" % (__title__,__version__))
    print("")
    if title:
        print(':: %s ::' % title.upper())


def build_assets(app):
    from webassets.script import CommandLineEnvironment
    assets_env = app.jinja_env.assets_environment
    log = logging.getLogger('webassets')
    log.addHandler(logging.StreamHandler())
    log.setLevel(logging.DEBUG)
    cmdenv = CommandLineEnvironment(assets_env, log)
    cmdenv.build()


@click.group()
def cli():
    """ Flasik

    NOTE: To use the admin commands run 'flask-admin'

    (http://mardix.github.io/flasik) 

    """

@click.group()
def cli_admin():
    """:::FLASIK-ADMIN:::
    
    The admin CLI to manage Flasik

    (http://mardix.github.io/flasik) 
    
    """
    
# Object to expose
command = cli.command 
argument = click.argument
option = click.option


@cli_admin.command("init")
@catch_exception
def init():
    """Init Flasik in the current directory """

    flasikpyfile = os.path.join(os.path.join(CWD, ENTRY_PY))

    header("Setup %s" % __title__)
    if os.path.isfile(flasikpyfile):
        print("Flasik is already setup in ths directory")
        print("Found '%s' in %s" % (ENTRY_PY, CWD))
        print("")
    else:
        copy_resource_dir(SKELETON_DIR + "/init/", CWD)
        print("%s is setup successfully!" % __title__)
        print("")
        print("> To do:")
        print("- Edit application's config [ /__config__.py ] ")
        print("- Run your setup command [ flasik setup ]")
        print("- Create your Models/Database tables [ flasik-admin sync-models ]")
        print("- Launch app on development mode, run [ flasik-admin run ]")
        print("")

def create_views(scaffold, name):
    dest = os.path.join(app_dir, name)
    if os.path.isdir(dest):
        print("ERROR: directory exists already '%s'" % dest)
    else:
        utils.make_dirs(dest)
        copy_resource_dir(SKELETON_DIR + "/%s/" % scaffold, dest)
        viewdest = os.path.join(dest, "__views__.py")
        with open(viewdest, "r+") as f:
            content = f.read().replace("%ROUTE%", name.lower())
            f.seek(0)
            f.write(content)
            f.truncate()

@cli_admin.command("create-template-view")
@click.argument("name")
def add_view(name):
    """ Create Template based views"""

    header("Create Template based views")

    create_views("create-template-views", name)

    print("")
    print("*" * 80)

@cli_admin.command("create-api-view")
@click.argument("name")
def api_view(name):
    """ Create API based views"""

    header("Create API based views")

    create_views("create-api-views", name)
    
    print("")
    print("*" * 80)



@cli_admin.command("run")
@click.option("--port", "-p", default=5000)
@catch_exception
def run(port):
    """ Run the application in development mode """

    header("Run Flasik in Dev mode")
    print("Port: %s" % port)
    print("http://localhost:%s" % port)
    cwd_to_sys_path()
    flasik_app.run(debug=True, host='0.0.0.0', port=port)


@cli_admin.command("sync-models")
def sync_models():
    """ Sync database models to create new tables """

    header("Sync Models")
    cwd_to_sys_path()
    if db and hasattr(db, "Model"):
        db.create_all()
        for m in db.Model.__subclasses__():
            if hasattr(m, "initialize__"):
                print("Sync up model: %s ..." % m.__name__)
                getattr(m, "initialize__")()



@cli_admin.command("assets2s3")
@catch_exception
def assets2s3():
    """ Upload assets files to S3 """
    import flask_s3

    header("Assets2S3")
    print("")
    print("Building assets files..." )
    build_assets(flasik_app)
    print("Uploading assets files to S3 ...")
    flask_s3.create_all(flasik_app)
    print("")


@cli_admin.command("version")
def version():
    print(__version__)





# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def cmd():
    """
    Help to run the command line
    :return:
    """
    global flasik_app, app_dir

    script_name = sys.argv[0].split('/')[-1]
    is_admin = script_name == 'flasik-admin'

    flasikpyfile = os.path.join(os.path.join(CWD, ENTRY_PY))
    if os.path.isfile(flasikpyfile):
        cwd_to_sys_path()
        entry = import_string(ENTRY_PY.replace('.py', ''))
        flasik_app = entry.app
        app_dir = CWD
        cli_admin() if is_admin is True else cli()
        return 
    else:
        header()
        if len(sys.argv) == 1 or (len(sys.argv) > 1 and sys.argv[1] != 'setup'):
            print("Error: %s is  not setup yet" % __title__)
            print("Run %s in the directory you want to create it" % bold("flasik-admin init"))
            print("Missing file '%s' in %s" % (ENTRY_PY, CWD))
            print('_' * 80)
            print("")
    if is_admin is True:
        cli_admin()

    
