from django.shortcuts import render
# Create your views here.
# -*- coding: utf-8 -*-
import hashlib
import json
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import time
import xml.etree.ElementTree as ET
from weixin.models import ResourceMessage
from django.db.models import Q

# django默认开启csrf防护，这里使用@csrf_exempt去掉防护
@csrf_exempt
def weixin_main(request):
    print('method:', request.method)
    if request.method == "GET":
        # 接收微信服务器get请求发过来的参数
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        # 服务器配置中的token,请按照公众平台官网\基本配置中信息填写
        token = 'hello'
        # 把参数放到list中排序后合成一个字符串，再用sha1加密得到新的字符串与微信发来的signature对比，如果相同就返回echostr给服务器，校验通过
        list = [token, timestamp, nonce]
        print('list:', list)
        list.sort()
        sha1 = hashlib.sha1()
        sha1.update(list[0].encode('utf-8'))
        sha1.update(list[1].encode('utf-8'))
        sha1.update(list[2].encode('utf-8'))
        hashcode = sha1.hexdigest()
        print("handle/GET func: hashcode, signature: ", hashcode, signature)
        if hashcode == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("验证失败")
    else:
        other_content = auto_reply(request)
        return HttpResponse(other_content)


# 微信服务器推送消息是xml的，根据利用ElementTree来解析出的不同xml内容返回不同的回复信息，就实现了基本的自动回复功能了，也可以按照需求用其他的XML解析方法
def auto_reply(request):
    try:
        web_data = request.body
        xml_data = ET.fromstring(web_data)
        print('web_data:', web_data)
        msg_type = xml_data.find('MsgType').text
        to_user_name = xml_data.find('ToUserName').text
        from_user_name = xml_data.find('FromUserName').text
        to_user = from_user_name
        from_user = to_user_name
        if msg_type == 'text':
            req_content = xml_data.find('Content').text
            resource_messages = None
            print('req_content:', req_content)
            if req_content.isdigit():
                resource_messages = ResourceMessage.objects.filter(resource_code=req_content)
            content = '无效资源，请联系博主处理'
            if resource_messages and len(resource_messages)>0:
                content = resource_messages[0].resource_name+' '+resource_messages[0].resource_message;
            print(content)
            reply_msg = TextMsg(to_user, from_user, content)
            return reply_msg.send()
        # 关注和取关的类型是envent
        elif msg_type == 'event':
                envent = xml_data.find('Event').text
                # 关注事件（取消关注的类型是'unsubscribe',这里没有写）
                if envent == 'subscribe':
                    content = '''感谢关注"我的Python世界"，在我的Python世界中，从Python基础，Diango，爬虫，在到机器学习...我们一起学习，一起进步。
                        本公众号正在建设中，后续会逐步完善。
                    '''
                    reply_msg = TextMsg(to_user, from_user, content)
                    return reply_msg.send()
        elif msg_type == 'image':
            content = "图片已收到,谢谢"
            reply_msg = TextMsg(to_user, from_user, content)
            return reply_msg.send()
        elif msg_type == 'voice':
            content = "语音已收到,谢谢"
            replyMsg = TextMsg(to_user, from_user, content)
            return replyMsg.send()
        elif msg_type == 'video':
            content = "视频已收到,谢谢"
            replyMsg = TextMsg(to_user, from_user, content)
            return replyMsg.send()
        elif msg_type == 'shortvideo':
            content = "小视频已收到,谢谢"
            replyMsg = TextMsg(to_user, from_user, content)
            return replyMsg.send()
        elif msg_type == 'location':
            content = "位置已收到,谢谢"
            replyMsg = TextMsg(to_user, from_user, content)
            return replyMsg.send()
        else:
            msg_type == 'link'
            content = "链接已收到,谢谢"
            replyMsg = TextMsg(to_user, from_user, content)
            return replyMsg.send()
    except Exception as Argment:
        return Argment


class Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text


class TextMsg(Msg):
    def __init__(self, to_user, from_user, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = to_user
        self.__dict['FromUserName'] = from_user
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**self.__dict)
