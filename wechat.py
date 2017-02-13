#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, request, make_response
import hashlib, time
import xml.etree.ElementTree as ET
from imagetest import imgtest

app = Flask(__name__)

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
		if msgType == 'text':
			content = xml.find('Content').text
			msgId = xml.find('MsgId').text
			kuaidi = {u"zhongtong":"zhongtong", u"yunda":"yunda", u"yuantong":"yuantong",u"shunfeng":"shunfeng", u"shentong":"shentong"}
			if u"xiaohua" in content:
				pass
			elif content[0:2] in kuaidi.keys():
				kuaidi_type = kuaidi.get(content[0:2], '')
				kuaidi_post = str(content[2:])
				url = 'https://m.kuaidi100.com/index_all.html?type=%s&postid=%s&callbackurl=[点击"返回"跳转的地址]' % (kuaidi_type, kuaidi_post)
				return redirect(url)
			else:
				#encode to utf-8
				if type(content).__name__ == "unicode":
					#content = content[::-1]
					content = content.encode('utf-8')
				elif type(content).__name__ == "str":
					print type(content).__name__
					content = content.decode('utf-8')
					#content = content[::-1]
				reply = '''
					<xml>
					<ToUserName><![CDATA[%s]]></ToUserName>
					<FromUserName><![CDATA[%s]]></FromUserName>
					<CreateTime>%d</CreateTime>
					<MsgType><![CDATA[%s]]></MsgType>
					<Content><![CDATA[%s]]></Content>
					</xml>
				''' % (fromUserName, toUserName, int(time.time()), msgType, content)
				return reply
		elif msgType == 'image':
			picurl = xml.find('PicUrl').text
			datas = imgtest(picurl)
			content = "tu zhong ren wu xing bie"+datas[0]+"\n"+"nian ling wei"+datas[1]
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


@app.route('/make')
def make():
	echostr = "hello"
	return make_response(echostr)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)
