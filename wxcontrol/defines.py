# -*- coding: utf-8 -*-
"""
@Author: lamborghini1993
@Date: 2017-11-17 00:06:29
@Last Modified by:   lamborghini1993
@Last Modified time: 2017-11-17 00:06:29
@Desc:
    公共定义
"""


OPEN_AUTO_REPLY = 101
CLOSE_AUTO_REPLY = 102

SHOW_MY_ALL_FUND = 201
ADD_FUND = 202
DELET_FUND = 203
SHOW_CUR_FUND_ROSE = 204

MEUN_INFO = {
    OPEN_AUTO_REPLY: "开启微信自动聊天",
    CLOSE_AUTO_REPLY: "关闭微信自动聊天",

    SHOW_MY_ALL_FUND: "显示我所有关注的定投基金",
    ADD_FUND: "添加关注定投基金-{} 基金代号".format(ADD_FUND),
    DELET_FUND: "取消关注定投基金-{} 基金代号".format(DELET_FUND),
    SHOW_CUR_FUND_ROSE: "获取当前定投基金的涨幅",
}


STATE_CLOSE_AUTO_REPLY = 0
STATE_OPEN_AUTO_REPLY = 1
