
'''
功能
	表情包制作
作者:
	Ahab
公众号:
	Ahab杂货铺
'''
import pygame
import random

# 初始化pygame
pygame.init()

# 根据背景图片的大小，设置屏幕长宽
SIZE = (1000, 500)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("下雪了")
background = pygame.image.load('snow.jpg')

# 雪花列表
snow = []

# 初始化雪花：[x坐标, y坐标, x轴速度, y轴速度]
for i in range(300):
    x = random.randrange(0, SIZE[0])
    y = random.randrange(0, SIZE[1])
    speedx = random.randint(-1, 2)
    speedy = random.randint(2, 7)
    snow.append([x, y, speedx, speedy])

clock = pygame.time.Clock()

# 游戏主循环
done = False
while not done:
    # 消息事件循环，判断退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # 黑背景/图片背景
    # screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # 雪花列表循环
    for i in range(len(snow)):
    # 绘制雪花，颜色、位置、大小


        pygame.draw.circle(screen, (255, 255, 255), snow[i][:2], snow[i][3])

        # 移动雪花位置（下一次循环起效）
        snow[i][0] += snow[i][2]
        snow[i][1] += snow[i][3]

        # 如果雪花落出屏幕，重设位置
        if snow[i][1] > SIZE[1]:
            snow[i][1] = random.randrange(-50, -10)
            snow[i][0] = random.randrange(0, SIZE[0])

    # 刷新屏幕
    pygame.display.flip()
    clock.tick(20)

# 退出
pygame.quit()