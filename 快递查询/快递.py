
import pickle
import requests

def Check():
        kd_num = input("请输入快递单号:")
        getExpressInfo(number=kd_num)


companies = pickle.load(open('companies.pkl', 'rb'))
'''将快递公司的拼音变为汉字'''
def py2hz(py):
	return companies.get(py)


'''利用快递100查询快递'''
def getExpressInfo(number):
	url = 'http://www.kuaidi100.com/autonumber/autoComNum?resultv2=1&text=%s' % number
	infos = []
	for each in requests.get(url).json()['auto']:
		company_name = each['comCode']
		url = 'http://www.kuaidi100.com/query?type=%s&postid=%s' % (company_name, number)
		temps = requests.get(url).json()['data']
		info = '公司: %s\n' % py2hz(company_name)
		for idx, each in enumerate(temps):
			if idx == 0:
				info += '-' * 60 + '\n时间:\n' + each['time'] + '\n进度:\n' + each['context'] + '\n' + '-' * 60 + '\n'
			else:
				info += '时间:\n' + each['time'] + '\n进度:\n' + each['context'] + '\n' + '-' * 60 + '\n'
		if not temps:
			info += '-' * 60 + '\n' + '单号不存在或已过期\n' + '-' * 60 + '\n'
		infos.append(info)
	return infos


if __name__ == '__main__':
        Check()

