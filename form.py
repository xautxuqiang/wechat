# -*- coding:utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class KuaiDi(Form):
	kuaidi_type = StringField(u"快递名称", validators=[Required()])
	kuaidi_post = StringField(u"快读单号", validators=[Required()])
	submit = SubmitField(u"确认")
