# -*- coding:utf-8 -*-
# 肖豪
# 自动检查微信被那些好友拉黑/删除 (优化)

import ssl
import requests
import time
import re
import sys
import os
import subprocess
import xml.dom.minidom
import json
import threading


def GetCurTime():
	iTime=time.time()
	iTime=int(iTime)
	return iTime


DEBUG=True	#调试
MAX_GROUP_NUM=10


class CWeiXin(object):

	m_DevideID="e000000000000000"
	m_Header={"content-type":"application/json; charset=UTF-8"}

	def __init__(self):
		self.m_MyRequests=None
		self.m_Uuid=None
		self.m_Tip=0
		self.m_RedirectUri=None
		self.m_BaseUri=None
		self.m_PushUri=None
		self.m_Key=None
		self.m_WXsid=None
		self.m_WXuin=None
		self.m_PassTicket=None
		self.m_BaseRequest=None
		self.m_My=[]
		self.m_SyncKey=None
		self.m_MemberList=None
		self.m_MemberInfo={}	#基本信息
		self.m_DeletedList=[]	# 被对方删除了
		self.m_BlockedList=[]	# 被加入黑名单


	def Fuck(self):
		self.m_MyRequests=myRequests
		self.m_Uuid=uuid
		self.m_Tip=tip
		self.m_QRImagePath=QRImagePath
		self.m_RedirectUri=redirect_uri
		self.m_BaseUri=base_uri
		self.m_PushUri=push_uri
		self.m_Key=skey
		self.m_WXsid=wxsid
		self.m_WXuin=wxuin
		self.m_PassTicket=pass_ticket
		self.m_BaseRequest=BaseRequest
		#ContactList没用
		self.m_SyncKey=SyncKey


	def Start(self):
		self.InitConfige()
		self.InitRequest()
		if not self.GetUuid():
			print "获取uuid失败"
			return
		self.GetQRImage()
		while self.WaitForLogin()!="200":
			pass
		if not self.Login():
			print "登陆失败……"
			return
		if not self.WebWXInit():
			print "初始化失败……"
			return

		self.WebWXGetContact()
		print "总共有%s位微信好友"%len(self.m_MemberList)
		# threading.Thread(target=self.HeartBeatLoop)

		# self.FilterBlacklist()
		# self.ShowBlackList()


	def InitConfige(self):
		if hasattr(ssl,'_create_unverified_context'):
			ssl._create_default_https_context=ssl._create_unverified_context
		self.m_QRImagePath=os.path.join(os.getcwd(),'xiaohao.jpg')


	def InitRequest(self):
		# 浏览器UA设置
		dHearder={
			"User-agent"	:"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36",
		}
		self.m_MyRequests=requests.Session()
		self.m_MyRequests.headers.update(dHearder)


	def GetUuid(self):
		sUrl="https://login.weixin.qq.com/jslogin"
		dParams={
			"appid"	:"wx782c26e4c19acffb",
			"fun"	:"new",
			"lang"	:"zh_CN",
			"_"		:GetCurTime(),
		}
		oRequest=self.m_MyRequests.get(url=sUrl,params=dParams)
		oRequest.encoding="utf-8"
		sData=oRequest.text
		#获取的data为:window.QRLogin.code = 200; window.QRLogin.uuid = "oZwt_bFfRg==";
		sRegx=r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)"'
		oPm=re.search(sRegx,sData)
		sCode=oPm.group(1)
		self.m_Uuid=oPm.group(2)
		if sCode=="200":
			return True
		return False


	def GetQRImage(self):
		print "正在获取二维码图片..."
		sUrl="https://login.weixin.qq.com/qrcode/"+self.m_Uuid
		dParams={
			"t"	:"webwx",
			"_"	:GetCurTime(),
		}
		oRequest=self.m_MyRequests.get(url=sUrl,params=dParams)
		self.m_Tip=1
		
		f=open(self.m_QRImagePath,"wb")
		f.write(oRequest.content)
		f.close()

		sPlatform=sys.platform
		if sPlatform.find("darwin")>=0:		#mac OSX
			subprocess.call(["open",self.m_QRImagePath])
		elif sPlatform.find("linux")>=0:		#linux
			subprocess.call(["xdg-open",self.m_QRImagePath])
		else:					#win32--windows
			os.startfile(self.m_QRImagePath)

		print "请使用微信扫描二维码以登录..."


	def WaitForLogin(self):
		sUrl="https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?tip=%s&uuid=%s&_=%s"%(self.m_Tip,self.m_Uuid,GetCurTime())
		oRequest=self.m_MyRequests.get(url=sUrl)
		oRequest.encoding="utf-8"
		sData=oRequest.text
		#window.code=500;
		sRegx=r"window.code=(\d+);"
		oPm=re.search(sRegx,sData)
		sCode=oPm.group(1)

		if sCode=="201":	#已扫描
			print "成功扫描,请在手机上点击确认以登录"
			self.m_Tip=0
			return sCode

		if sCode=="200":	#已登录
			print "正在登陆"
			sRegx=r'window.redirect_uri="(\S+?)";'
			oPm=re.search(sRegx,sData)
			self.m_RedirectUri=oPm.group(1)+"&fun=new"
			self.m_BaseUri=self.m_RedirectUri[:self.m_RedirectUri.rfind("/")]

			lstServices=[
				("wx2.qq.com","webpush2.weixin.qq.com"),
				("qq.com","webpush.weixin.qq.com"),
				("web1.wechat.com","webpush1.wechat.com"),
				("web2.wechat.com","webpush2.wechat.com"),
				("wechat.com","webpush.wechat.com"),
				("web1.wechatapp.com","webpush1.wechatapp.com"),
			]
			self.m_PushUri=self.m_BaseUri
			for sSearchUrl,sPushUrl in lstServices:
				if self.m_BaseUri.find(sSearchUrl)>=0:
					self.m_PushUri="https://%s/cgi-bin/mmwebwx-bin"%sPushUrl
					break;

			# closeQRImage for OSX with Preview
			if sys.platform=="darwin":
				os.system("osascript -e 'quit app \"Preview\"'")
			#删除二维码
			os.remove(self.m_QRImagePath)
		return sCode


	def Login(self):
		oRequest=self.m_MyRequests.get(url=self.m_RedirectUri)
		oRequest.encoding="utf-8"
		sData=oRequest.text

		sDoc=xml.dom.minidom.parseString(sData)
		xRoot=sDoc.documentElement

		for node in xRoot.childNodes:
			if node.nodeName=="skey":
				self.m_Key=node.childNodes[0].data
			elif node.nodeName=="wxsid":
				self.m_WXsid=node.childNodes[0].data
			elif node.nodeName=="wxuin":
				self.m_WXuin=node.childNodes[0].data
			elif node.nodeName=="pass_ticket":
				self.m_PassTicket=node.childNodes[0].data

		if not all((self.m_Key,self.m_WXsid,self.m_WXuin,self.m_PassTicket)):
			return False

		self.m_BaseRequest={
			"Uin"		:int(self.m_WXuin),
			"Sid"		:self.m_WXsid,
			"Skey"		:self.m_Key,
			"DeviceID"	:self.m_DevideID,
		}
		return True


	def ResponseState(self,func,BaseResponse):
		sErrMsg=BaseResponse["ErrMsg"]
		iRet=BaseResponse["Ret"]
		if DEBUG or iRet!=0:
			print "func:%s Ret:%s ErrMsg:%s"%(func,iRet,sErrMsg)

		if iRet:
			return False
		return True


	def WebWXInit(self):
		sUrl="%s/webwxinit?pass_ticket=%s&skey=%s&r=%s"%(self.m_BaseUri,self.m_PassTicket,self.m_Key,GetCurTime())
		dParams={"BaseRequest":self.m_BaseRequest}
		dHeader={"content-type":"application/json; charset=UTF-8"}

		dData=self.GetRequestPost(sUrl,json.dumps(dParams),self.m_Header)
		print dData

		

		self.m_My=dData["User"]
		self.m_SyncKey=dData["SyncKey"]

		bState=self.ResponseState("webwxsync",dData["BaseResponse"])
		return bState


	def WebWXGetContact(self):
		sUrl="%s/webwxgetcontact?pass_ticket=%s&skey=%s&r=%s"%(self.m_BaseUri,self.m_PassTicket,self.m_Key,GetCurTime())
		dHeader={"content-type":"application/json; charset=UTF-8"}

		oRequest=self.m_MyRequests.post(url=sUrl,headers=dHeader)
		oRequest.encoding="utf-8"
		dData=oRequest.json()

		if DEBUG:
			f=open(os.path.join(os.getcwd(),"webwx.json"),"wb")
			f.write("%s"%dData)
			f.write(oRequest.content)
			f.close()

		self.m_MemberList=dData["MemberList"]
		##去掉一些没用的
		# lstSpecialUser=["newsapp", "fmessage", "filehelper", "weibo", "qqmail", "tmessage", "qmessage", "qqsync", "floatbottle", "lbsapp", "shakeapp", "medianote", "qqfriend", "readerapp", "blogapp", "facebookapp", "masssendapp","meishiapp", "feedsapp", "voip", "blogappweixin", "weixin", "brandsessionholder", "weixinreminder", "wxid_novlwrv3lqwv11", "gh_22b87fa7cb3c", "officialaccounts", "notification_messages", "wxitil", "userexperience_alarm"]
		# for i in xrange(len(self.m_MemberList)-1,-1,-1):
		# 	dMember=self.m_MemberList[i]
		# 	if Member['VerifyFlag'] & 8 != 0:	# 公众号/服务号
		# 		self.m_MemberList.remove(dMember)
		# 	if Member['UserName'] in lstSpecialUser:	# 特殊账号
		# 		self.m_MemberList.remove(dMember)
		# 	if Member['UserName'].find("@@") != -1:		#群聊
		# 		self.m_MemberList.remove(dMember)
		# 	if Member['UserName']==self.m_My["UserName"]:	# 自己
		# 		self.m_MemberList.remove(dMember)


	def HeartBeatLoop(self):
		while True:
			sSyncKey=self.SyncCheck()
			if sSyncKey!="0":
				self.WebWXSync()
			time.sleep(1)


	def SyncCheck(self):
		sUrl=self.m_PushUri+"/synccheck?"
		dParams={
			"skey"		:self.m_BaseRequest["Skey"],
			"sid"		:self.m_BaseRequest["Sid"],
			"uin"		:self.m_BaseRequest["Uin"],
			"deviceId"	:self.m_BaseRequest["DeviceID"],
			"synckey"	:self.Synckey(),
			"r"			:GetCurTime(),
		}

		oRequest=self.m_MyRequests.get(url=sUrl,params=dParams)
		oRequest.encoding="utf-8"
		sData=oRequest.text

		# window.synccheck={retcode:"0",selector:"2"}
		sRegx=r'window.synccheck={retcode:"(\d+)",selector:"(\d+)"}'
		oPm=re.search(sRegx,sData)

		selector=oPm.group(2)
		return selector


	def Synckey(self):
		lstSyncKey=[]
		for item in self.m_SyncKey["List"]:
			sTmp="%s_%s"%(item["Key"],item["Val"])
			lstSyncKey.append(sTmp)
		sSyncKey="|".join(lstSyncKey)
		return sSyncKey


	def WebWXSync(self):
		sUrl="%s/webwxsync?lang=zh_CN&skey=%s&sid=%s&pass_ticket=%s"\
			%(self.m_BaseUri,self.m_BaseRequest["Skey"],self.m_BaseRequest["Sid"],quote_plus(self.m_PassTicket))
		dParams={
			"BaseRequest"	:self.m_BaseRequest,
			"SyncKey"		:self.m_SyncKey,
			"rr"			:~GetCurTime(),
		}
		dHeader={"content-type":"application/json; charset=UTF-8"}
		oRequest=self.m_MyRequests.post(url=sUrl,data=json.dumps(dParams))
		oRequest.encoding="utf-8"
		dData=oRequest.json()

		self.m_SyncKey=dData["SyncKey"]

		state=self.ResponseState('webwxsync',dData['BaseResponse'])
		return state


	def FilterBlacklist(self):
		for dMember in self.m_MemberList:
			self.m_MemberInfo[dMember["UserName"]]=(dMember["NickName"],dMember["RemarkName"])
			sChatRoomName=""
		iMemberNum=len(self.m_MemberList)
		iGroupNum=iMemberNum/MAX_GROUP_NUM+(iMemberNum%MAX_GROUP_NUM!=0)
		for i in xrange(iGroupNum):
			lstUserName=[]
			for j in xrange(MAX_GROUP_NUM):
				iTmp=i*MAX_GROUP_NUM+j
				if iTmp>=iMemberNum:
					break
				dMember=self.m_MemberList[iTmp]
				lstUserName.append(dMember["UserName"])

			# 新建群组/添加成员
			if sChatRoomName=="":
				sChatRoomName=self.CreateChatRoom(lstUserName)
			else:
				self.AddMemberToChatRoom(sChatRoomName,lstUserName)

			self.DeleteMenber(sChatRoomName,lstUserName)



	def CreateChatRoom(self,lstUserName):
		lstMember=[]
		for sUserName in lstUserName:
			lstMember.append({"UserName":sUserName})

		sUrl="%s/webwxcreatechatroom?pass_ticket=%s&r=%s"\
			%(self.m_BaseUri,self.m_PassTicket,GetCurTime())
		dParams={
			"BaseRequest"	:self.m_BaseRequest,
			"MemberCount"	:len(lstMember),
			"MemberList"	:lstMember,
			"Topic"			:"",
		}


		dData=self.GetRequestPost(sUrl,json.dumps(dParams),self.m_Header)
		self.ChoiceBlacklist(dData)

		sChatRoomName=dData["ChatRoomName"]
		state=self.ResponseState("createChatroom",dData["BaseResponse"])
		return sChatRoomName


	def AddMemberToChatRoom(self,sChatRoomName,lstUserName):
		"""加到讨论组中"""
		sUrl="%s/webwxupdatechatroom?fun=addmember&pass_ticket=%s"\
			%(self.m_BaseUri,self.m_PassTicket)
		dParams={
			"BaseRequest"	:self.m_BaseRequest,
			"ChatRoomName"	:sChatRoomName,
			"AddMemberList"	:",".join(lstUserName),
		}
		dData=self.GetRequestPost(sUrl,json.dumps(dParams),self.m_Header)
		self.ChoiceBlacklist(dData)
		iState=self.ResponseState("addMember",dData["BaseResponse"])


	def GetRequestPost(self,sUrl,sParams,dHeader):
		oRequest=self.m_MyRequests.post(url=sUrl,data=sParams,headers=dHeader)
		oRequest.encoding="utf-8"
		dData=oRequest.json()

		# if DEBUG:
		# 	f=open(os.path.join(os.getcwd(),"web.json"),"wb")
		# 	f.write(oRequest.content)
		# 	f.close()

		return dData


	def ChoiceBlacklist(self,dData):
		"""筛选被对方删除或者拉黑的名单"""
		lstMember=dData["MemberList"]
		for dMember in lstMember:
			if dMember["MemberStatus"]==4:		# 被对方删除了
				self.m_DeletedList.append(dMember["UserName"])
			elif dMember["MemberStatus"]==3:	# 被加入黑名单
				self.m_BlockedList.append(dMember["UserName"])


	def DeleteMenber(self,sChatRoomName,lstUserName):
		sUrl="%s/webwxupdatechatroom?fun=delmember&pass_ticket=%s"\
			%(self.m_BaseUri,self.m_PassTicket)
		dParams={
			"BaseRequest"	:self.m_BaseRequest,
			"ChatRoomName"	:sChatRoomName,
			"DelMemberList"	:",".join(lstUserName),
		}
		dData=self.GetRequestPost(sUrl,json.dumps(dParams),self.m_Header)
		iState=self.ResponseState("deleteMember",dData["BaseResponse"])
		return iState


	def ShowBlackList(self):
		print "--------------------------------"
		print "被对方删除的人数%d:%s"%(len(self.m_DeletedList),self.m_DeletedList)
		print "被对方拉黑的人数%d:%s"%(len(self.m_BlockedList),self.m_BlockedList)
		print "--------------------------------"

obj=CWeiXin()
obj.Start()
