# -*- coding: utf-8 -*-
from . import decorators as deco

@deco.emit_signal()
def upload_file(change):
    return change()

@deco.emit_signal()
def delete_file(change):
    return change()

@deco.emit_signal()
def send_mail(change, **kwargs):
    return change()


