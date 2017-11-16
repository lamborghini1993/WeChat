# -*- coding:utf-8 -*-
# 肖豪
# 使用了图灵机器人api接入微信自动回复

"""
外部库:itchat
"""

import urllib
import itchat  # 这是一个用于微信回复的库
from mytool import pubdefines

KEY = 'ca098ebe818b49df98af997bef29b3b3'  # 这个key可以直接拿来用
# KEY = '63eb9f95bd2945e79bcceca31dc09935' #我的key

# 向api发送请求


def get_response(content, userid):
    url = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': KEY,
        'info': content,
        'userid': 'pth-robot',
    }
    try:
        postdata = urllib.parse.urlencode(data)
        postdata = postdata.encode("utf-8")
        res = urllib.request.urlopen(url, postdata)
        sInfo = res.read()
        dInfo = eval(sInfo)
        return dInfo["text"]
    except:
        return "肖豪真帅"

# def get_response3(msg):
# 	resp=urllib.request.Request("http://api.qingyunke.com/api.php",{
# 		'key':'free',
# 		'appid':0,
# 		'msg':msg,
# 	})
# 	resp.encoding='utf-8'
# 	resp=resp.json()
# 	return resp['content']

# 注册方法


@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    content = msg["Content"]
    userid = msg["FromUserName"]
    # pubdefines.trace_msg()
    # for key, value in msg.items():
    #     print("{}:  {}".format(key, value))
    # 如果图灵Key出现问题，那么reply将会是None
    reply = get_response(content, userid)
    return reply


# 为了让修改程序不用多次扫码,使用热启动
itchat.auto_login(hotReload=True)
itchat.run()
