# -*- coding:utf-8 -*-
# 肖豪
# 微信群发

"""
外部库:itchat
"""

import itchat
import time
import chardet

# 为了让修改程序不用多次扫码,使用热启动
itchat.auto_login(hotReload=True)

def Trans(sMsg):
	# try:
	# print(type(sMsg))
	# print(chardet.detect(sMsg.encode()))
	# print(sMsg)
	# sMsg = sMsg.encode("gbk").decode("utf8")
	# except:
		# print("err..")
	return sMsg

def GetFrd():
	sDefault = "xxxx"
	lstFrd = itchat.get_friends(update=True)[1:]
	for dFrd in lstFrd:
		sNick = Trans(dFrd["NickName"])
		sRemark = Trans(dFrd["RemarkName"])
		try:
			print("NickName:{:<50}".format(sNick), end=' ')
		except:
			print("NickName:{:<50}".format(sDefault), end=' ')
			
		try:
			print("RemarkName:{:<24}".format(sRemark))
		except:
			print("RemarkName:{:<24}".format(sDefault))
		# print("NickName:{:<24}RemarkName:{}".format(sNick, sRemark))

def AllSendMsg():
	SINCERE_WISH = "祝%s新年快乐！"
	lstFrd = itchat.get_friends(update=True)
	for friend in lstFrd:
		print("=" * 50)
		for sKey, xValue in friend.items():
			print("{}\t{}".format(sKey, xValue))
		# print(SINCERE_WISH % (friend['DisplayName'] or friend['NickName']), friend['UserName'])
		# itchat.send(SINCERE_WISH % (friend['DisplayName'] or friend['NickName']), friend['UserName'])
		# time.sleep(.5)

AllSendMsg()
