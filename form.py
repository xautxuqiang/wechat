#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class KuaiDi(Form):
	kuaidi_type = StringField(u"kuaidi_type",validators=[Required()])
	kuaidi_post = StringField(u"kuaidi_post",validators=[Required()])
	submit = SubmitField(u"queren")
