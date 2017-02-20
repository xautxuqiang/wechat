#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, request, make_response, redirect, render_template
import hashlib, time
import xml.etree.ElementTree as ET
from imagetest import imgtest
from form import KuaiDi
from talk_api import talk
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()

app = Flask(__name__)
app.config['SECRET_KEY'] = "hello"
bootstrap.init_app(app)

@app.route('/', methods=['GET','POST'])
def wechat_auth():
	if request.method == 'GET':
		print 'Coming GET'
		data = request.args
		token = 'xautxuqiang'
		signature = data.get('signature', '')
		timestamp = data.get('timestamp', '')
		nonce = data.get('nonce', '')
		echostr = data.get('echostr', '')
		s = [token, timestamp, nonce]
		s.sort()
		s = ''.join(s)
		if hashlib.sha1(s).hexdigest() == signature:
			return make_response(echostr)
	
	if request.method == 'POST':
		xml_str = request.stream.read()
		xml = ET.fromstring(xml_str)
		toUserName = xml.find('ToUserName').text
		fromUserName = xml.find('FromUserName').text
		createTime = xml.find('CreateTime').text
		msgType = xml.find('MsgType').text
		userid = ''.join(fromUserName.split("_"))
		if msgType == 'text':
			content = xml.find('Content').text
			msgId = xml.find('MsgId').text
			#encode to utf-8
			if type(content).__name__ == "unicode":
				#content = content[::-1]
				content = content.encode('utf-8')
			elif type(content).__name__ == "str":
				print type(content).__name__
				content = content.decode('utf-8')
				#content = content[::-1]
			msg = talk(content, userid)
			reply = '''
				<xml>
				<ToUserName><![CDATA[%s]]></ToUserName>
				<FromUserName><![CDATA[%s]]></FromUserName>
				<CreateTime>%d</CreateTime>
				<MsgType><![CDATA[%s]]></MsgType>
				<Content><![CDATA[%s]]></Content>
				</xml>
			''' % (fromUserName, toUserName, int(time.time()), msgType, msg)
			return reply
		elif msgType == 'voice':
			content = xml.find('Recognition').text
			msgId = xml.find('MsgId').text
                        msg = talk(content, userid)
                        reply = '''
                                <xml>
                                <ToUserName><![CDATA[%s]]></ToUserName>
                                <FromUserName><![CDATA[%s]]></FromUserName>
                                <CreateTime>%d</CreateTime>
                                <MsgType><![CDATA[%s]]></MsgType>
                                <Content><![CDATA[%s]]></Content>
                                </xml>
                        ''' % (fromUserName, toUserName, int(time.time()), 'text', msg)
                        return reply
		elif msgType == 'image':
			picurl = xml.find('PicUrl').text
			datas = imgtest(picurl)
			content = "图中人物性别为"+datas[0]+"\n"+"年龄为"+datas[1]
			reply = '''
                                        <xml>
                                        <ToUserName><![CDATA[%s]]></ToUserName>
                                        <FromUserName><![CDATA[%s]]></FromUserName>
                                        <CreateTime>%d</CreateTime>
                                        <MsgType><![CDATA[%s]]></MsgType>
                                        <Content><![CDATA[%s]]></Content>
                                        </xml>
                                ''' % (fromUserName, toUserName, int(time.time()), 'text', content)
			return reply

		else:
			reply = '''
                                <xml>
                                <ToUserName><![CDATA[%s]]></ToUserName>
                                <FromUserName><![CDATA[%s]]></FromUserName>
                                <CreateTime>%d</CreateTime>
                                <MsgType><![CDATA[%s]]></MsgType>
                                <Content><![CDATA[%s]]></Content>
                                </xml>
                        ''' % (fromUserName, toUserName, int(time.time()), 'text', 'Unknown Format, Please Check Out')
			return reply


@app.route('/kuaidi', methods=['GET','POST'])
def make():
	form = KuaiDi()
	kuaidi = {u"中通":"zhongtong", u"韵达":"yunda", u"圆通":"yuantong",u"顺风":"shunfeng", u"申通":"shentong"}
	if form.validate_on_submit():
		kuaidi_type = form.kuaidi_type.data
		kuaidi_typenum = kuaidi.get(kuaidi_type,'')
		kuaidi_post = form.kuaidi_post.data
		url = u'https://m.kuaidi100.com/index_all.html?type=%s&postid=%s&callbackurl=[点击"返回"跳转的地址]' % (kuaidi_typenum, kuaidi_post)
		return redirect(url)
	return render_template("index.html", form=form)

if __name__ == '__main__':
	app.run('0.0.0.0',8080)
