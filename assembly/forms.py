
# -*- coding: utf-8 -*-
"""
Forms

WTForms extension
*fields, *validators are exposed
"""
from wtforms import Form
from flask import request
from wtforms.fields import * 
from wtforms.validators import *
from wtforms.meta import DefaultMeta
from werkzeug.datastructures import (CombinedMultiDict, ImmutableMultiDict)

SUBMIT_METHODS = ('POST', 'PUT', 'PATCH', 'DELETE')
OBJ = object()

class Model(Form):
    class Meta:
        def wrap_formdata(self, form, formdata):
            if formdata is OBJ:
                if request.method in SUBMIT_METHODS:
                    if request.files:
                        return CombinedMultiDict((request.files, request.form))
                    elif request.form:
                        return request.form
                    elif request.get_json():
                        return ImmutableMultiDict(request.get_json())
                return None
            return formdata


    def __init__(self, formdata=OBJ, **kwargs):
        super().__init__(formdata=formdata, **kwargs)


    def validate(self):
        """ Validate a form """
        return super().validate()

