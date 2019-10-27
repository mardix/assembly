# -*- coding: utf-8 -*-
from .functions import emit_signal

@emit_signal()
def upload_file(change):
    return change()

@emit_signal()
def delete_file(change):
    return change()

@emit_signal()
def send_mail(change, **kwargs):
    return change()


