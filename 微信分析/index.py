import itchat
# 导入Pie组件，用于生成饼图
from pyecharts import Pie
# 获取数据


import sys



def get_data():
# 扫描二维码登陆微信，实际上就是通过网页版微信登陆
     itchat.auto_login()
# 获取所有好友信息
     friends = itchat.get_friends(update=True,encoding='utf-8')
# 返回一个包含用户信息字典的列表
     return friends

# 处理数据
def parse_data(data):
    friends = []
    for item in data[1:]:#第一个元素是自己，排除掉
        friend = {
            'NickName': item['NickName'],# 昵称
            'RemarkName': item['RemarkName'], # 备注名
            'Sex': item['Sex'],# 性别：1男，2女，0未设置
            'Province': item['Province'],  # 省份
            'City': item['City'],  # 城市
            'Signature':
            item['Signature'].replace('\n', ' ').replace(',', ' '),# 个性签名（处理签名内容换行的情况）
            'StarFriend': item['StarFriend'], # 星标好友：1是，0否
            'ContactFlag': item['ContactFlag']  # 好友类型及权限：1和3好友，259和33027不让他看我的朋友圈，65539不看他的朋友圈，65795两项设置全禁止
        }
        print(friend)
        friends.append(friend)
    return friends

# 存储数据，存储到文本文件
def save_to_txt():
    friends = parse_data(get_data())
    for item in friends:
        with open('friends.txt', mode='a', encoding='utf-8') as f:
            f.write('%s,%s,%d,%s,%s,%s,%d,%d\n' % (
            item['NickName'],
            item['RemarkName'],
            item['Sex'],
            item['Province'],
            item['City'],
            item['Signature'],
            item['StarFriend'],
            item['ContactFlag']))

#性别分析


# 获取所有性别
sex = []
with open('friends.txt', mode='r',
          encoding='utf-8') as f:
    rows = f.readlines()
    for row in rows:
        sex.append(row.split(',')[2])
# 统计每个性别的数量
attr = ['帅哥', '美女', '未知']
value = [sex.count('1'),
         sex.count('2'), sex.count('0')]
pie = Pie('好友性别比例', '好友总人数：%d' % len(sex),
          title_pos='center')
pie.add('', attr, value, radius=[30, 75],
        rosetype='area', is_label_show=True,
        is_legend_show=True, legend_top='bottom')

pie.render('好友性别比例.html')



#好友位置分析

# 导入Counter类，用于统计值出现的次数
from collections import Counter
# 导入Geo组件，用于生成地理坐标类图
from pyecharts import Geo
import json
# 导入Bar组件，用于生成柱状图
from pyecharts import Bar

# 数据可视化
def render():
    # 获取所有城市
    cities = []
    with open('friends.txt', mode='r', encoding='utf-8') as f:
        rows = f.readlines()
        for row in rows:
            city = row.split(',')[4]
            if city != '':  # 去掉城市名为空的值
                cities.append(city)

# 对城市数据和坐标文件中的地名进行处理
    handle(cities)

# 统计每个城市出现的次数
    data = Counter(cities).most_common()  # 使用Counter类统计出现的次数，并转换为元组列表
    print(data)

# 根据城市数据生成地理坐标图
    geo = Geo('好友位置分布', '', title_color='#fff', title_pos='center', width=1200, height=600,background_color='#404a59')
    attr, value = geo.cast(data)
    geo.add('', attr, value, visual_range=[0, 500], visual_text_color='#fff', symbol_size=15, is_visualmap=True,
            is_piecewise=True)
    geo.render('好友位置分布.html')

    # 根据城市数据生成柱状图
    data_top20 = Counter(cities).most_common(20)  # 返回出现次数最多的20条
    bar = Bar('好友所在城市TOP20', '', title_pos='center', width=1200, height=600)
    attr, value = bar.cast(data_top20)
    bar.add('', attr, value, is_visualmap=True, visual_text_color='#fff', is_more_utils=True,
            is_label_show=True)
    bar.render('好友所在城市TOP20.html')


# 处理地名数据，解决坐标文件中找不到地名的问题
def handle(cities):
    # print(len(cities), len(set(cities)))
    # 获取坐标文件中所有地名
    data = None
    with open('C:/Users/Administrator/AppData/Roaming/Python/Python36/site-packages/pyecharts/datasets/city_coordinates.json',
              mode='r', encoding='utf-8') as f:
         data = json.loads(f.read())  # 将str转换为json

    # 循环判断处理
    data_new = data.copy()  # 拷贝所有地名数据
    for city in set(cities):  # 使用set去重

        # 处理地名为空的数据
        if city == '':
            while city in cities:
                cities.remove(city)
        count = 0
        for k in data.keys():
            count += 1
            if k == city:
                break
            if k.startswith(city):  # 处理简写的地名，如 达州市 简写为 达州
                    # print(k, city)
                data_new[city] = data[k]
                break
            if k.startswith(city[0:-1]) and len(city) >= 3:  # 处理行政变更的地名，如县改区 或 县改市等
                data_new[city] = data[k]
                break
            # 处理不存在的地名
        if count == len(data):
            while city in cities:
                cities.remove(city)

# 写入覆盖坐标文件
    with open('C:/Users/Administrator/AppData/Roaming/Python/Python36/site-packages/pyecharts/datasets/city_coordinates.json',
    mode='w', encoding='utf-8') as f:
         f.write(json.dumps(data_new, ensure_ascii=False))
#个性签名词云

# 导入jieba模块，用于中文分词
import jieba
# 导入matplotlib，用于生成2D图形
import matplotlib.pyplot as plt
# 导入wordcount，用于制作词云图
from wordcloud import WordCloud, STOPWORDS

# 获取所有个性签名
signatures = []
with open('friends.txt', mode='r', encoding='utf-8') as f:
    rows = f.readlines()
    for row in rows:
        signature = row.split(',')[5]
        if signature != '':
            signatures.append(signature)

# 设置分词
split = jieba.cut(str(signatures), cut_all=False)  # False精准模式分词、True全模式分词
words = ' '.join(split)  # 以空格进行拼接

# 设置屏蔽词，去除个性签名中的表情、特殊符号等
stopwords = STOPWORDS.copy()
stopwords.add('span')
stopwords.add('class')
stopwords.add('emoji')
stopwords.add('emoji1f334')
stopwords.add('emoji1f388')
stopwords.add('emoji1f33a')
stopwords.add('emoji1f33c')
stopwords.add('emoji1f633')

# 导入背景图
bg_image = plt.imread('5.jpg')
# 设置词云参数，参数分别表示：画布宽高、背景颜色、背景图形状、字体、屏蔽词、最大词的字体大小
wc = WordCloud(width=1024, height=768, background_color='white', mask=bg_image,
               font_path='D:\PycharmProjects\music\SIMYOU.TTF',
               max_font_size=400, random_state=50)

# 将分词后数据传入云图
wc.generate_from_text(words)
plt.imshow(wc)  # 绘制图像
plt.axis('off')  # 不显示坐标轴
# 保存结果到本地
wc.to_file('个性签名词云图.jpg')


if __name__ == '__main__':
    print(get_data())
   # print(parse_data(get_data()))
    #save_to_txt()
    #render()