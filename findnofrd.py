# -*- coding:utf-8 -*-
# 肖豪
# 查找微信被那些好友删除

"""
外部库:itchat
"""

import itchat
import chardet
# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') 

# 为了让修改程序不用多次扫码,使用热启动
itchat.auto_login(hotReload=True)

sChatRoomName = "好友删除检测临时群"
iMaxNum = 10

def MyPrint(dInfo):
	dTmp = dInfo["BaseResponse"]
	# print(dTmp)
	sMsg = dTmp["RawMsg"]
	sMsg = bytes(sMsg)
	print(type(sMsg))
	print(sMsg.encode("gbk"))
	# for sKey, xValue in dInfo.items():
	# 	print("{}:\t{}".format(sKey, xValue))

lstFrd = itchat.get_friends(update=True)[1:25]
lstTmp = lstFrd[:5]
lstFrd = lstFrd[5:]
dResult = itchat.create_chatroom(lstTmp, sChatRoomName)
MyPrint(dResult)
chatroomUserName = dResult["ChatRoomName"]

itchat.delete_member_from_chatroom(dResult, lstTmp)

# while lstFrd:
# 	print(len(lstFrd))
# 	lstTmp = lstFrd[:iMaxNum]
# 	lstFrd = lstFrd[iMaxNum:]
# 	r = itchat.add_member_into_chatroom(dResult, lstTmp)
# 	print(r)	
# 	itchat.delete_member_from_chatroom(dResult, lstTmp)


