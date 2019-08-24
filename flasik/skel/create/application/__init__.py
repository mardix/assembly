# -*- coding: utf-8 -*-
# Mocha

import os

# ------------------------------------------------------------------------------
# A convenient utility to access data path from your application and config files

# The application directory
# /apps
APP_DIR = os.path.dirname(__file__)

# The root dir
# /
ROOT_DIR = os.path.dirname(APP_DIR)

# Data directory
# apps/var
VAR_DIR = os.path.join(APP_DIR, "var")


def get_var_path(path):
    """
    get the path stored in the 'app/data' directory
    :param path: string
    :return: string
    """
    return os.path.join(VAR_DIR, path)
