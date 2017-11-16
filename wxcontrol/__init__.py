# -*- coding: utf-8 -*-
"""
@Author: lamborghini1993
@Date: 2017-11-16 09:10:26
@Last Modified by:   lamborghini1993
@Last Modified time: 2017-11-16 09:10:26
@Desc:
    微信总控制
"""

from wxcontrol import meun

if "MENU_MGR" not in globals():
    MENU_MGR = meun.MeunMgr()


def get_replay_msg(who):
    global MENU_MGR
    reply = MENU_MGR.deal_menu(who)
    return reply
