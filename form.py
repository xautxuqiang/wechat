#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class KuaiDi(Form):
	kuaidi_type = StringField(u"快递公司",validators=[Required()])
	kuaidi_post = StringField(u"快递单号",validators=[Required()])
	submit = SubmitField(u"查询")
