# -*- coding: utf-8 -*-
"""
@Author: lamborghini1993
@Date: 2017-11-18 00:14:57
@Last Modified by:   lamborghini1993
@Last Modified time: 2017-11-18 00:14:57
@Desc:使用了图灵机器人api接入微信自动回复
    @db24b43420b00f4d651ec4906c43f13c
"""


import urllib.parse
import urllib.request


def get_response(who):
    # for a, b in who.items():
    #     print("{}:\t{}".format(a, b))
    content = who["Content"]
    content = content.replace("小豪", "小歪")
    tulinkey = 'ca098ebe818b49df98af997bef29b3b3'  # 这个key可以直接拿来用
    # tulinkey = '63eb9f95bd2945e79bcceca31dc09935' #我的key
    url = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': tulinkey,
        'info': content,
        'userid': 'pth-robot',
    }
    try:
        postdata = urllib.parse.urlencode(data)
        postdata = postdata.encode("utf-8")
        res = urllib.request.urlopen(url, postdata)
        data = res.read()
        myinfo = eval(data)
        reply = myinfo["text"].replace("小歪", "小豪")
        return reply
    except:
        return "你真好，我好像爱上你了~"

