# -*- coding: utf-8 -*-
"""
@Author: lamborghini1993
@Date: 2017-11-17 00:22:35
@Last Modified by:   lamborghini1993
@Last Modified time: 2017-11-17 00:22:35
@Desc:
    微信处理各种业务
"""

import itchat
import wxcontrol


@itchat.msg_register(itchat.content.TEXT)
def itchat_menu(who):
    # content = msg["Content"]
    # userid = msg["FromUserName"]
    # pubdefines.trace_msg()
    # for key, value in msg.items():
    #     print("{}:  {}".format(key, value))
    reply = wxcontrol.get_replay_msg(who)
    return reply


# 为了让修改程序不用多次扫码,使用热启动
itchat.auto_login(hotReload=True)
itchat.run()
