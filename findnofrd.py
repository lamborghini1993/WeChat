# -*- coding:utf-8 -*-
# 肖豪
# 查找微信被那些好友删除

"""
外部库:itchat
"""

import itchat

# 为了让修改程序不用多次扫码,使用热启动
itchat.auto_login(hotReload=True)

sChatRoomName = "好友删除检测临时群"
iMaxNum = 10

lstFrd = itchat.get_friends(update=True)[1:33]
lstTmp = lstFrd[:iMaxNum]
lstFrd = lstFrd[iMaxNum:]
dResult = itchat.create_chatroom(lstTmp, sChatRoomName)
chatroomUserName = dResult["ChatRoomName"]
itchat.delete_member_from_chatroom(chatroomUserName, lstTmp)

while lstFrd:
	lstTmp = lstFrd[:iMaxNum]
	lstFrd = lstFrd[iMaxNum:]
	r = itchat.add_member_into_chatroom(chatroomUserName, lstTmp)
	# print(r)	
	itchat.delete_member_from_chatroom(chatroomUserName, lstTmp)


