# -*- coding: utf-8 -*-
"""
@Author: lamborghini1993
@Date: 2017-11-16 09:10:26
@Last Modified by:   lamborghini1993
@Last Modified time: 2017-11-16 09:10:26
@Desc:
    微信总控制
"""

from wxcontrol.defines import *


class MeunMgr(object):

    def __init__(self):
        self.fouc_fund = {}
        self.func = {
            # OPEN_AUTO_REPLY: self.open_auto_reply,
            # CLOSE_AUTO_REPLY: self.close_auto_reply,
            SHOW_MY_ALL_FUND: self.show_my_all_fund,
            ADD_FUND: self.add_fund,
            DELET_FUND: self.delet_fund,
        }

    def get_func(self, funnum):
        try:
            funnum = int(funnum)
        except:
            return None
        func = self.func.get(funnum, None)
        return func

    def get_menu(self):
        msg = "请输入以下代号进行操作:"
        for num, tip in MEUN_INFO.items():
            msg += "\n  {}: {}".format(num, tip)
        return msg

    def deal_menu(self, who):
        reply = None
        content = who["Content"]
        if content == "showmenu":
            return self.get_menu()
        funnum = content.split(" ")[0]
        func = self.get_func(funnum)
        if not func:
            return None
        reply = func(who)
        return reply

    def show_my_all_fund(self, who):
        """显示我所有关注的定投基金"""
        userid = who["FromUserName"]
        if userid not in self.fouc_fund:
            return "你还没有关注的定投基金,使用({}, id)添加关注".format(ADD_FUND)
        myfundinfo = self.fouc_fund[userid]
        reply = ""
        for fundid, desc in myfundinfo.items():
            reply += "{} {}\n".format(fundid, desc)
        return reply

    def add_fund(self, who):
        """添加关注的定投基金"""
        content = who["Content"]
        userid = who["FromUserName"]
        try:
            _, fundid = content.split(" ")
        except:
            return None
        if userid not in self.fouc_fund:
            self.fouc_fund[userid] = {}
        myfundinfo = self.fouc_fund[userid]
        if fundid in myfundinfo:
            return "该定投基金已经关注，请勿重复关注"
        fundname = "xx"  # TODO
        myfundinfo[fundid] = fundname
        return "已关注({} {})定投基金".format(fundid, fundname)

    def delet_fund(self, who):
        """删除已关注的定投基金"""
        content = who["Content"]
        userid = who["FromUserName"]
        try:
            _, fundid = content.split(" ")
        except:
            return None
        if userid not in self.fouc_fund:
            return "你还没有关注任何定投基金"
        myfundinfo = self.fouc_fund[userid]
        if fundid not in myfundinfo:
            return "你还没有关注{}定投基金".format(fundid)
        fundname = myfundinfo[fundid]
        del myfundinfo[fundid]
        return "已取消关注({} {})定投基金".format(fundid, fundname)
