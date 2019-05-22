
'''
功能
	微信自动回复祝福语
作者:
	Ahab
公众号:
	程序员小王
'''


import itchat
import requests
import time
import random
from itchat.content import *


# 用于记录回复过的好友
replied = []


# 获取新年祝福语
def GetRandomGreeting():
	res = requests.get("http://www.xjihe.com/api/life/greetings?festival=新年&page=10", headers = {'apiKey':'sQS2ylErlfm9Ao2oNPqw6TqMYbJjbs4g'})
	results = res.json()['result']
	return results[random.randrange(len(results))]['words']


# 发送新年祝福语
def SendGreeting(msg):
	global replied
	friend = itchat.search_friends(userName=msg['FromUserName'])
	if friend['RemarkName']:
		itchat.send((friend['RemarkName']+','+GetRandomGreeting()), msg['FromUserName'])
	else:
		itchat.send((friend['NickName']+','+GetRandomGreeting()), msg['FromUserName'])
	replied.append(msg['FromUserName'])


# 文本消息
@itchat.msg_register([TEXT])
def text_reply(msg):
	if '年' in msg['Text'] and msg['FromUserName'] not in replied:
		SendGreeting(msg)


# 其他消息
@itchat.msg_register([PICTURE, RECORDING, VIDEO, SHARING])
def others_reply(msg):
	if msg['FromUserName'] not in replied:
		SendGreeting(msg)



if __name__ == '__main__':

	itchat.auto_login()
	itchat.run()



