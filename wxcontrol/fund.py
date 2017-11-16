# -*- coding: utf-8 -*-
"""
@Author: lamborghini1993
@Date: 2017-11-16 09:18:29
@Last Modified by:   lamborghini1993
@Last Modified time: 2017-11-16 09:18:29
@Desc:
    查看基金相关
    http://fund.10jqka.com.cn/
"""

import re
from selenium import webdriver


class Fund(object):
    url = "http://fund.10jqka.com.cn/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) \
            Gecko/20100101 Firefox/57.0"
    }
    re_time = r'<span class="time">\[(.*?)\]</span>'
    re_zf = r'<span class="zf(.*?)">(.*?)</span>'
    re_title = r'<title>(.*?)</title>'

    def __init__(self):
        self.fundlist = {
            "xiaohao": ["000311", "001542", "110029"]
        }

    def start(self):
        info = self.get_fund_info()
        print(info)

    def get_fund_info(self):
        result = []
        onelist = self.fundlist.get("xiaohao", [])
        for fundnum in onelist:
            url = self.url + fundnum
            oneresult = self.get_one_info(url)
            result.append(oneresult)
        return "\n".join(result)

    def get_one_info(self, url):
        fundinfo = self.get_phantomjs_by_url(url)
        return fundinfo

    def get_re_info(self, recomplie, source, num=1):
        pattern = re.compile(recomplie)
        match = pattern.search(source)
        if not match:
            return ""
        return match.group(num)

    def valid_get_correct(self, *args):
        for tmp in args:
            if tmp in ("", "--"):
                return False
        return True

    def get_phantomjs_by_url(self, url):
        for tmp in range(10):
            try:
                driver = webdriver.PhantomJS(
                    executable_path="./lib/phantomjs.exe")
                driver.get(url)
                page_source = driver.page_source.encode('utf8')
                page_source = page_source.decode("utf8")
                title = self.get_re_info(self.re_title, page_source)
                zf = self.get_re_info(self.re_zf, page_source, 2)
                zftime = self.get_re_info(self.re_time, page_source)
                if not self.valid_get_correct(title, zf, zftime):
                    continue
                return "{} [{}] 估值涨幅:{}".format(title, zftime, zf)
            except:
                pass


obj = Fund()
obj.start()
