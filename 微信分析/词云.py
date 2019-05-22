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
               stopwords=stopwords,
               max_font_size=400, random_state=50)

# 将分词后数据传入云图
wc.generate_from_text(words)
plt.imshow(wc)  # 绘制图像
plt.axis('off')  # 不显示坐标轴
# 保存结果到本地
wc.to_file('个性签名词云图1.jpg')
