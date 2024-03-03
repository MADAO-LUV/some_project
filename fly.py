""""
@画布的大小是800 * 600 其中800为x  600为y
@注意：load里面全是自己加入的一些素材，需要把它写在与fly.py里的同一个文件夹中，否则就找不到文件了
"""
import pygame
import random
import math


#初始化游戏界面
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('一起打飞机')
icon = pygame.image.load('屏幕截图 2024-03-02 210131.png')
pygame.display.set_icon(icon) #游戏图标
#加入背景图
bgImg = pygame.image.load('bground.png')

#添加背景音效
pygame.mixer.music.load('1355731144.mp3')
pygame.mixer.music.play(-1) #当曲循环

#添加射中音效
bao_sound = pygame.mixer.Sound('猫叫声_耳聆网_[声音ID：15603].mp3')

#引入驾驶飞机
playerImg = pygame.image.load('final_player.jpg')

#调整图片大小
scaled_width = 50
scaled_height = 60

scaled_playerImg = pygame.transform.scale(playerImg,(scaled_width,scaled_height))


#5.飞机位置
playerX = 400
playerY = 500
playerStep = 0


#添加分数
score = 0
font = pygame.font.Font('freesansbold.ttf',32)

def show_score():
    text = f"Score：{score}"
    score_render = font.render(text,True,(0,255,0))
    screen.blit(score_render,(10,10)) #放到左上角

#游戏结束
is_over = False
over_font = pygame.font.Font('freesansbold.ttf',64)
def check_is_over():
    if is_over:
        text = "Game Over"
        render = over_font.render(text,True,(255,0,0))
        screen.blit(render,(200,250))


#6.添加敌人
number_of_enemies = 6 #敌人的数量

#敌人类
class Enemy():
    def __init__(self):
        self.Img = pygame.image.load('enemy_cat.png')
        self.x = random.randint(200,600)
        self.y = random.randint(50,200)
        self.step = random.randint(2,5)

    #当被射中时，恢复位置
    def reset(self):
        self.x = random.randint(200,600)
        self.y = random.randint(50,200)
#保存所有的敌人
enemies = []
for i in range(number_of_enemies):
    s = Enemy()
    s.Img = pygame.transform.scale(s.Img,(64,64))
    enemies.append(s)


#两个点之间的距离 子弹与敌人之间的距离
def distance(bx,by,ex,ey):
    a = bx - ex #x轴上的直角边
    b = by - ey #y轴上的直角边
    return math.sqrt(a*a + b*b)



#子弹类
class Bullet():
    def __init__(self):
        self.Img = pygame.image.load('bullet.png')
        self.x = playerX
        self.y = playerY + 10
        self.step = 2 #子弹移动的速度

    #击中
    def hit(self):
        global  score
        for e in enemies:
            if(distance(self.x,self.y,e.x,e.y) < 30):
                bao_sound.play()
                bullets.remove(self)
                e.reset() #重置敌人的位置
                score += 1


bullets = [] #保存现有的子弹

#显示子弹
def show_bullets():
    for b in bullets:
        screen.blit(b.Img,(b.x,b.y))
        b.hit()  #尝试是否击中目标
        b.y -= b.step
        if b.y < 0:
            bullets.remove(b)


#显示敌人，并下沉
def show_enemy():
    global enemyX,enemyStep,enemyY,is_over
    for e in enemies:
        screen.blit(e.Img,(e.x,e.y))
        e.x += e.step
        if e.x > 736:
            e.step = - random.randint(1,3)
            e.y += 20
            if e.y > 450:
                is_over = True
                print("游戏结束啦！")
                enemies.clear()
        elif e.x < 0:
            e.step = random.randint(1,3)
            e.y += 20
            if e.y > 450:
                is_over = True
                print("游戏结束啦！")
                enemies.clear()
#处理信息
def process_events():
    global playerStep
    #监听信息
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #如果是键盘按下 通过键盘事件来控制飞机移动
        if event.type == pygame.KEYDOWN: #按下就移动
            if event.key == pygame.K_RIGHT:
                playerStep = 0.5
            elif event.key == pygame.K_LEFT:
                playerStep = -0.5
            elif event.key == pygame.K_SPACE:
                print("发射子弹....")
                #创建一颗子弹
                b = Bullet()
                b.Img = pygame.transform.scale(b.Img,(30,40))
                bullets.append(b)

        #不按键盘的时候就不动
        if event.type == pygame.KEYUP:
            playerStep = 0



#移动玩家
def move_player():
    global playerX
    # 防止飞机出界
    if playerX > 750:
        playerX = 0
    if playerX < 0:
        playerX = 0


#游戏主循环
running = True
while running:
    screen.blit(bgImg,(0,0)) #把背景图整张画入
    process_events()
    show_score()

    #绘制出飞机---我方
    screen.blit(scaled_playerImg,(playerX,playerY))
    playerX += playerStep
    move_player() #显示玩家
    show_enemy() #显示敌人
    show_bullets() #显示子弹
    check_is_over() #检查游戏是否结束 每一帧
    pygame.display.update() #做完事情之后一定要更新一下，一定要放到最后