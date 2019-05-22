import os
import itchat
import math
from PIL import Image
# 获取数据

def get_image():
    itchat.auto_login()
    friends = itchat.get_friends(update=True)
    #  在当前位置创建一个用于存储头像的目录headImages
    base_path = 'headImages'
    if not os.path.exists(base_path):
        os.mkdir(base_path)
     # 获取所有好友头像
    for friend in friends:
        img_data = itchat.get_head_img(userName=friend['UserName'])
        # 获取头像数据
        img_name = friend['RemarkName']if friend['RemarkName'] != '' else friend['NickName']
        print(img_name)
get_image()

'''
        img_file = os.path.join(base_path, img_name + '.jpg')
        print(img_file)
        with open(img_file, 'wb') as file:
            file.write(img_data)


# 拼接头像
def join_image():
    base_path = 'headImages'
    files = os.listdir(base_path)
    each_size = int(math.sqrt(float(640 * 640) / len(files)))
    lines = int(640 / each_size)
    image = Image.new('RGB', (640, 640))
    x = 0
    y = 0
    for file_name in files:
        img = Image.open(os.path.join(base_path, file_name))
        img = img.resize((each_size, each_size), Image.ANTIALIAS)
        image.paste(img, (x * each_size, y * each_size))
        x += 1
        if x == lines:
            x = 0
            y += 1
    image.save('all.jpg')
if __name__ == '__main__':
    #get_image()
    join_image()
'''
