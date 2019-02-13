'''
功能
	微信红包助手
作者:
	Ahab
公众号:
	Ahab杂货铺

	如果你是小白你应该关注的公众号，如果你是大牛你更应该关注。
	坚持每天原创输出，免费分享Python基础&进阶，数据分析挖掘和机器学习相关知识，
	所有技术文章层层递进，带你循序渐进的学习。
	为了巩固数据结构知识，定期打卡刷LeetCode，分享面试经验，锻炼编程能力化身Offer收割机，
	另外公众号会不定期给粉丝送福利，总之我是强烈推荐关注【Ahab杂货铺】的！
'''
import itchat
import pygame

'''声音提示'''
def voice ():
	pygame.mixer.init()
	pygame.mixer.music.load('voice .mp3')
	pygame.mixer.music.play()

'''监控是否有红包-群聊(Note参数: 通知消息类型)'''
@itchat.msg_register('Note', isGroupChat=True)
def getNoteGroup(msg):
	if u'收到红包' in msg['Text']:
		print('[INFO]: %s' % msg['Text'])
		voice()


'''监控是否有红包-个人(Note参数: 通知消息类型)'''
@itchat.msg_register('Note', isGroupChat=False)
def getNote(msg):
	if u'收到红包' in msg['Text']:
		print('[INFO]: %s' % msg['Text'])
		voice()

if __name__ == '__main__':
	itchat.auto_login(hotReload=True)
	itchat.run()
	itchat.logout()