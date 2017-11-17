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
from wxcontrol import fund
from wxcontrol import autoreply


class MeunMgr(object):

    def __init__(self):
        self.fouc_fund = {}
        self.cur_state = {}
        self.func = {
            OPEN_AUTO_REPLY: self.open_auto_reply,
            CLOSE_AUTO_REPLY: self.close_auto_reply,
            SHOW_MY_ALL_FUND: self.show_my_all_fund,
            ADD_FUND: self.add_fund,
            DELET_FUND: self.delet_fund,
            SHOW_CUR_FUND_ROSE: self.show_cur_fund_rose,
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

    def open_auto_reply(self, who):
        """开启自动回复"""
        userid = who["FromUserName"]
        self.cur_state[userid] = STATE_OPEN_AUTO_REPLY
        return "已开启自动回复"

    def close_auto_reply(self, who):
        """关闭自动回复"""
        userid = who["FromUserName"]
        self.cur_state[userid] = STATE_CLOSE_AUTO_REPLY
        return "已关闭自动回复"

    def deal_menu(self, who):
        reply = None
        content = who["Content"]
        if content in ("showmenu", "显示菜单"):
            return self.get_menu()
        funnum = content.split(" ")[0]
        func = self.get_func(funnum)
        if func:
            reply = func(who)
            return reply
        userid = who["FromUserName"]
        curstate = self.cur_state.get(userid, 0)
        if curstate == STATE_OPEN_AUTO_REPLY:
            reply = autoreply.get_response(content)
            return reply
        return None

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
        fundname = fund.FUND_OBJ.get_fund_name(fundid)
        if not fundname:
            return "你输入的\"{}\"定投基金代号有误".format(fundid)
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

    def show_cur_fund_rose(self, who):
        userid = who["FromUserName"]
        myfundinfo = self.fouc_fund.get(userid, {})
        if not myfundinfo:
            return "你还没有关注任何定投基金"
        fundidlist = []
        for fundid, _ in myfundinfo.items():
            fundidlist.append(fundid)
        result = fund.FUND_OBJ.get_fund_info(fundidlist)
        return result
