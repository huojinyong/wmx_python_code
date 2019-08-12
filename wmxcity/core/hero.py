import sys
import pygame
from pygame.locals import *
from constants import *
from  libs.sound_manager import sound_manager
from core.game_board import *
class Hero():

    def __init__(self):
        pygame.init()
        self.fontObj = pygame.font.Font('res/Kaiti_GB2312.ttf', 40)
        self.scoreFont = pygame.font.Font('res/Kaiti_GB2312.ttf', 32)
        self.state = 'stand' #默认状态为站立状态
        self.life = 100 #英雄生命值
        self.energy = 0 #英雄能量值
        self.defend = 0  # 英雄护甲值(只有下蹲防御时才不为0)
        self.life_num = 2 #剩余几条命
        self.pos = [0,0] #英雄坐标
        self.born_site = ''#标志着英雄是在左侧出生还是在右侧出生,取left或right

        #键盘标志位（默认为假）
        self.event_w = False
        self.event_a = False
        self.event_s = False
        self.event_d = False
        self.event_j = False
        self.event_k = False
        self.event_l = False
        self.event_u = False
        self.event_i = False
        self.event_o = False
        self.event_UP = False
        self.event_DOWN = False
        self.event_LEFT = False
        self.event_RIGHT = False
        self.event_1 = False
        self.event_2 = False
        self.event_3 = False
        self.event_4 = False
        self.event_5 = False
        self.event_6 = False
        self.time = 0#用来计算自由落体运动耗时
        self.v0 = -70#英雄跳跃初速度（向下为正方向）
        self.stand_flag = 0#英雄站立时不是一张静止的图片，而是三张循环播放的图片

    #需要手动设置英雄是在左侧出生还是在右侧出生
    def set(self,born_site):
        self.born_site = born_site
        if(born_site == 'left'):
            self.pos[0] = 10
            self.pos[1] = 40
        elif(born_site == 'right'):
            self.pos[0] = 120
            self.pos[1] = 40
    def send_pos(self):
        #把出生坐标汇报给系统：
        if self.born_site == 'left':
            con.hero1_pos[0] = self.pos[0]
            con.hero1_pos[1] = self.pos[1]
        elif self.born_site == 'right':
            con.hero2_pos[0] = self.pos[0]
            con.hero2_pos[1] = self.pos[1]
    def draw_self(self, screen):
        #画人物
        the_size = (20*USIZE, 30*USIZE)
        if self.born_site == 'right' and con.in_shenwei:
            the_size = con.shenwei_size
        man_picture = self.which_picture()
        man = pygame.image.load(man_picture)
        man = pygame.transform.scale(man, the_size)  # 调整图片大小
        screen.blit(man, (self.pos[0]*USIZE,self.pos[1]*USIZE))
        #画血条和怒气值
        if self.born_site == 'left':
            pygame.draw.rect(screen, PURPLE, (2, 2, 6 * USIZE, 6 * USIZE), 3)
            name_xi = self.fontObj.render('熙', True, BLACK)
            screen.blit(name_xi, (10, 10))
            pygame.draw.line(screen, GREEN, (65, 15), (65 + (4 * self.life), 15), 25)
            pygame.draw.line(screen, ORANGE, (65, 45), (65 + (8 * self.energy), 45), 25)
            pygame.draw.line(screen, BLUE, (470, 0), (470, 6 * USIZE), 5)
            if self.life > 0 or con.hero1_life_num != 0:
                pygame.draw.circle(screen, GRAY, (25, 90), 20)
            if con.hero1_life_num == 2:
                pygame.draw.circle(screen,GRAY,(75,90),20)
                pygame.draw.circle(screen,GRAY,(125,90),20)
            if con.hero1_life_num == 1:
                pygame.draw.circle(screen,GRAY,(75,90),20)
        if self.born_site == 'right':
            pygame.draw.rect(screen, PURPLE, ((134 * USIZE) - 2, 2, 6 * USIZE, 6 * USIZE), 3)
            name_kun = self.fontObj.render('坤', True, BLACK)
            screen.blit(name_kun, ((134 * USIZE) + 6, 10))
            pygame.draw.line(screen, GREEN, ((140 * USIZE) - 67, 15), ((140 * USIZE) - 67-4*self.life, 15), 25)
            pygame.draw.line(screen, ORANGE, ((140 * USIZE) - 67, 45), ((140 * USIZE) - 67-8*self.energy, 45), 25)
            pygame.draw.line(screen, BLUE, (928, 0), (928, 6 * USIZE), 5)
            if self.life > 0 or con.hero2_life_num != 0:
                pygame.draw.circle(screen, GRAY, (1375, 90), 20)
            if con.hero2_life_num == 2:
                pygame.draw.circle(screen,GRAY,(1325,90),20)
                pygame.draw.circle(screen,GRAY,(1275,90),20)
            if con.hero2_life_num == 1:
                pygame.draw.circle(screen,GRAY,(1325,90),20)

            #pygame.draw.line(screen, BLUE, (699, 0), (699, 6 * USIZE), 3)
            '''name_vs = self.fontObj.render('VS', True, BLACK)
            screen.blit(name_vs, (680, 10))
            pygame.draw.line(screen, PURPLE, (675, 6*USIZE), (724, 6 * USIZE), 3)'''
    def which_picture(self):
        #根据英雄当前状态判断英雄现在应该使用什么图片
        man_picture = ''
        self.stand_flag = (self.stand_flag + 1) % 3
        if self.born_site == 'left':
            if con.WHO_IS_LEFT == 1:
                #默认站立（三张图片）：
                if self.stand_flag == 0:
                    man_picture = r'res\xi_s_r_1.jpg'
                elif self.stand_flag == 1:
                    man_picture = r'res\xi_s_r_2.jpg'
                elif self.stand_flag == 2:
                    man_picture = r'res\xi_s_r_3.jpg'
                if self.event_j == True :
                    man_picture = r'res\xi_f_r_1.jpg'
                if self.event_k == True :
                    man_picture = r'res\xi_t_r.jpg'
            elif con.WHO_IS_LEFT == 2:
                if self.stand_flag == 0:
                    man_picture = r'res\xi_s_l_1.jpg'
                elif self.stand_flag == 1:
                    man_picture = r'res\xi_s_l_2.jpg'
                elif self.stand_flag == 2:
                    man_picture = r'res\xi_s_l_3.jpg'
                if self.event_j == True :
                    man_picture = r'res\xi_f_l_1.jpg'
                if self.event_k == True :
                    man_picture = r'res\xi_t_l.jpg'

        elif self.born_site == 'right':
            if con.WHO_IS_LEFT == 1:
                #默认站立（三张图片）：
                if self.stand_flag == 0:
                    man_picture = 'res\kun_s_l_1.jpg'
                elif self.stand_flag == 1:
                    man_picture = 'res\kun_s_l_2.jpg'
                elif self.stand_flag == 2:
                    man_picture = 'res\kun_s_l_3.jpg'
                if self.event_1 == True:
                    man_picture = 'res\kun_f_l_1.jpg'
                if self.event_2 == True:
                    man_picture = 'res\kun_t_l.jpg'
            elif con.WHO_IS_LEFT == 2:
                if self.stand_flag == 0:
                    man_picture = 'res\kun_s_r_1.jpg'
                elif self.stand_flag == 1:
                    man_picture = 'res\kun_s_r_2.jpg'
                elif self.stand_flag == 2:
                    man_picture = 'res\kun_s_r_3.jpg'
                if self.event_1 == True:
                    man_picture = 'res\kun_f_r_1.jpg'
                if self.event_2 == True:
                    man_picture = 'res\kun_t_r.jpg'
            if con.in_shenwei:
                man_picture = 'res\shenwei.png'
        return man_picture

    def hero_everytime(self):
        #每次循环都要判断
        #判断是否死亡、计算剩余生命
        # 把本英雄的坐标、生命值、能量值上报给全局变量
        #以及
        # 一个英雄挤走另一个英雄的情况处理(这个貌似被删下去了)
        if self.born_site == 'left':
            if con.flag1_change == 1:
                self.pos[0] = con.hero1_pos[0]
                self.pos[1] = con.hero1_pos[1]
                con.flag1_change = 0
            if con.flag1_life_change == 1:
                self.life = con.hero1_life
                con.flag1_life_change = 0
            if con.flag1_energy_change == 1:
                self.energy = con.hero1_energy
                con.flag1_energy_change = 0
            if con.flag1_life_num_change == 1:
                self.life_num = con.hero1_life_num
                con.flag1_life_num_change = 0
            if self.life <= 1:
                if self.life_num > 0:
                    self.life_num -= 1
                    con.hero1_life_num = self.life_num
                    self.life = 100#复活
                else:
                    # 败北
                    if con.winner == 0:
                        con.winner = 2
                        con.gameover()
            con.hero1_pos[0] = self.pos[0]
            con.hero1_pos[1] = self.pos[1]
            con.hero1_life = self.life
            con.hero1_energy = self.energy
        if self.born_site == 'right':
            if con.flag2_change == 1:
                self.pos[0] = con.hero2_pos[0]
                self.pos[1] = con.hero2_pos[1]
                con.flag2_change = 0
            if con.flag2_life_change == 1:
                self.life = con.hero2_life
                con.flag2_life_change = 0
            if con.flag2_energy_change == 1:
                self.energy = con.hero2_energy
                con.flag2_energy_change = 0
            if con.flag2_life_num_change == 1:
                self.life_num = con.hero2_life_num
                con.flag2_life_num_change = 0
            if self.life <= 1:
                if self.life_num > 0:
                    self.life_num -= 1
                    con.hero2_life_num = self.life_num
                    self.life = 100  # 复活
                else:
                    # 败北
                    if con.winner == 0:
                        con.winner = 1
                        con.gameover()
            con.hero2_pos[0] = self.pos[0]
            con.hero2_pos[1] = self.pos[1]
            con.hero2_life = self.life
            con.hero2_energy = self.energy

    def handle_event_man(self,event):
        if event.type == KEYDOWN:
            if self.born_site == 'left':
                if event.key == K_w:
                    self.event_w = True
                if event.key == K_a:
                    self.event_a = True
                if event.key == K_l:
                    self.event_s = True
                if event.key == K_d:
                    self.event_d = True
                if event.key == K_j and self.event_s == False and con.skill_protect == 0:
                    self.event_j = True
                    self.the_handle_j()
                if event.key == K_k and self.event_s == False and con.skill_protect == 0:
                    self.event_k = True
                    self.the_handle_k()
                #if event.key == K_s and self.event_s == False:
                    #self.event_s = True
                    #self.the_handle_s()
                if event.key == K_u and self.event_s == False and con.skill_protect == 0:
                    if self.energy >= 50:
                        con.skill_protect = 1
                        sound_manager.play_sound_shenwei()
                        self.energy-= 50#消耗能量值
                        con.hero1_energy = self.energy
                        con.flag1_energy_change = 1
                        con.hero2_life -= 70
                        con.flag2_life_change = 1
                        if con.hero2_life <= 0 and con.hero2_life_num == 0:
                            con.hero2_life = 0
                        elif con.hero2_life <= 0 and con.hero2_life_num > 0:
                            con.hero2_life += 100
                            con.hero2_life_num -= 1
                            con.flag2_life_num_change = 1
                        self.event_u = True
                        con.in_shenwei = True
                if event.key == K_i and self.event_s == False and con.skill_protect == 0:
                    if self.energy >= 25:
                        con.skill_protect = 1
                        sound_manager.play_sound_feibiao()
                        self.energy-= 25#消耗能量值
                        con.hero1_energy = self.energy
                        con.flag1_energy_change = 1
                        con.hero2_life -= 30
                        con.flag2_life_change = 1
                        if con.hero2_life <= 0 and con.hero2_life_num == 0:
                            con.hero2_life = 0
                        elif con.hero2_life <= 0 and con.hero2_life_num > 0:
                            con.hero2_life += 100
                            con.hero2_life_num -= 1
                            con.flag2_life_num_change = 1
                        self.event_i = True
                if event.key == K_o and self.event_s == False and con.skill_protect == 0:
                    if self.energy >= 50 and con.flag1_once_attcak == 1:
                        con.skill_protect = 1
                        con.flag1_once_attcak = 0
                        sound_manager.play_jiandi()
                        self.energy -= 50#消耗能量值
                        con.hero1_energy = self.energy
                        con.flag1_energy_change = 1
                        if con.hero2_life_num == 2 or con.hero2_life_num == 1:
                            con.hero2_life_num -= 1
                            con.flag2_life_num_change = 1
                            if con.hero1_life_num == 2 or con.hero1_life_num == 1:
                                con.hero1_life_num -= 1
                                con.flag1_life_num_change = 1
                            elif con.hero1_life_num == 0:
                                con.hero1_life = 0
                                con.flag1_life_change = 1
                        elif con.hero2_life_num == 0:
                            if con.hero1_life_num == 0:
                                if con.hero1_life < con.hero2_life:
                                    con.hero1_life = 0
                                    con.flag1_life_change = 1
                                else:
                                    con.hero2_life = 0
                                    con.flag2_life_change = 1
                            else:
                                con.hero2_life = 0
                                con.flag2_life_change = 1
                                con.hero1_life_num -= 1
                                con.flag1_life_num_change = 1
                        self.event_o = True
            if self.born_site == 'right':
                if event.key == K_UP:
                    self.event_UP = True
                if event.key == K_KP3:
                    self.event_DOWN = True
                if event.key == K_LEFT:
                    self.event_LEFT = True
                if event.key == K_RIGHT:
                    self.event_RIGHT = True
                if event.key == K_KP1 and self.event_DOWN == False and con.skill_protect == 0:
                    self.event_1 = True
                    self.the_handle_1()
                if event.key == K_KP2 and self.event_DOWN == False and con.skill_protect == 0:
                    self.event_2 = True
                    self.the_handle_2()
                if event.key == K_KP4 and self.event_DOWN == False and con.skill_protect == 0:
                    if self.energy >= 50:
                        con.skill_protect = 1
                        sound_manager.play_sound_ikun()
                        self.energy = 0#清空能量值
                        con.hero2_energy = 0
                        con.flag2_energy_change = 1
                        con.hero1_life -= 60
                        con.flag1_life_change = 1
                        if con.hero1_life <= 0 and con.hero1_life_num == 0:
                            con.hero1_life = 0
                        elif con.hero1_life <= 0 and con.hero1_life_num > 0:
                            con.hero1_life += 100
                            con.hero1_life_num -= 1
                            con.flag1_life_num_change = 1
                        self.event_4 = True
                if event.key == K_KP5 and self.event_DOWN == False and con.skill_protect == 0:
                    if self.energy >= 25:
                        con.skill_protect = 1
                        sound_manager.play_tongling()
                        self.energy -= 25 #清空能量值
                        con.hero2_energy = self.energy
                        con.flag2_energy_change = 1
                        self.life += 40
                        if self.life >= 100:
                            if con.hero2_life_num == 2:
                                self.life = 100
                            else:
                                con.hero2_life_num += 1
                                con.flag2_life_num_change = 1
                                self.life -= 100
                        con.hero1_life -= 30
                        con.flag1_life_change = 1
                        if con.hero1_life <= 0 and con.hero1_life_num == 0:
                            con.hero1_life = 0
                        elif con.hero1_life <= 0 and con.hero1_life_num > 0:
                            con.hero1_life += 100
                            con.hero1_life_num -= 1
                            con.flag1_life_num_change = 1
                        self.event_5 = True
                if event.key == K_KP6 and self.event_DOWN == False and con.skill_protect == 0:
                    if self.energy >= 50 and con.flag2_once_attcak == 1:
                        con.skill_protect = 1
                        con.hero2_energy_add = 2
                        con.flag2_once_attcak = 0
                        sound_manager.play_fumo()
                        self.energy = 0 #清空能量值
                        con.hero2_energy = self.energy
                        con.flag2_energy_change = 1
                        self.life += 20
                        if self.life >= 100:
                            if con.hero2_life_num == 2:
                                self.life = 100
                            else:
                                con.hero2_life_num += 1
                                con.flag2_life_num_change = 1
                                self.life -= 100
                        con.hero1_life -= 20
                        con.flag1_life_change = 1
                        if con.hero2_life_num == 0:
                            self.life = 0
                        else:
                            con.hero2_life_num -= 1
                            con.flag2_life_num_change = 1
                        if con.hero1_life <= 0 and con.hero1_life_num == 0:
                            con.hero1_life = 0
                        elif con.hero1_life <= 0 and con.hero1_life_num > 0:
                            con.hero1_life += 100
                            con.hero1_life_num -= 1
                            con.flag1_life_num_change = 1
                        self.event_6 = True
        if event.type == KEYUP:
            if self.born_site == 'left':
                #if event.key == K_w:
                    #self.event_w = False
                if event.key == K_a:
                    self.event_a = False
                if event.key == K_l:
                    self.event_s = False
                    self.defend = 0
                    con.hero1_defend = 0
                if event.key == K_d:
                    self.event_d = False
                if event.key == K_j:
                    self.event_j = False
                if event.key == K_k:
                    self.event_k = False
                #if event.key == K_s:
                    #self.event_s = False
                if event.key == K_u:
                    pass
                if event.key == K_i:
                    pass
                if event.key == K_o:
                    pass
            if self.born_site == 'right':
                #if event.key == K_UP:
                    #self.event_UP = False
                if event.key == K_KP3:
                    self.event_DOWN = False
                    self.defend = 0
                    con.hero2_defend = 0
                if event.key == K_LEFT:
                    self.event_LEFT = False
                if event.key == K_RIGHT:
                    self.event_RIGHT = False
                if event.key == K_KP1:
                    self.event_1 = False
                if event.key == K_KP2:
                    self.event_2 = False
                if event.key == K_KP4:
                    pass
                    #self.event_4 = False
                if event.key == K_KP5:
                    pass
                if event.key == K_KP6:
                    pass
        #self.the_handle_event_man()


    def the_handle_event_man(self):
        if self.born_site == 'left':
            if self.event_w == True:
                self.pos[1] = int(40 + self.v0 * self.time + 26 * self.time * self.time)
                self.time += 0.5
                if self.pos[1] > 40:
                    self.pos[1] = 40
                    self.event_w = False
                    self.time = 0
            if self.event_a == True:
                self.pos[0] -= 6
                #防止走出地图外
                if self.pos[0] <=0:
                    self.pos[0] = 0
                #考虑挤走另一个英雄的情况(跳跃时不考虑)
                #下面减9是为了可以让两个英雄身体间可以有重合部分（长度就是这个9），减小违和感
                if con.WHO_IS_LEFT == 2 and self.pos[0] < 20 + con.hero2_pos[0] - 9 and \
                        self.event_w == False :
                    if self.pos[0] >= 20:
                        con.hero2_pos[0] = self.pos[0] - 20 + 9
                        con.flag2_change = 1
                        self.pos[0] += 1
                        con.hero2_pos[0] += 1
                    else:
                        self.pos[0] += 2.5
            if self.event_s == True:
                self.defend = 3
                con.hero1_defend = 3
            if self.event_d == True:
                self.pos[0] += 6
                # 防止走出地图外
                if self.pos[0] >=120:
                    self.pos[0] = 120
                #考虑挤走另一个英雄的情况(跳跃时不考虑)
                if con.WHO_IS_LEFT == 1 and self.pos[0] + 20 > con.hero2_pos[0] + 9 and \
                        self.event_w == False :
                    if self.pos[0] + 20 <= 120:
                        con.hero2_pos[0] = self.pos[0] + 20 - 9
                        con.flag2_change = 1
                        self.pos[0] -= 1
                        con.hero2_pos[0] -= 1
                    else:
                        self.pos[0] -= 2.5
            if self.event_j == True:
                pass
            if self.event_k == True:
                pass
            if self.event_u == True:
                self.the_handle_u()
            if self.event_i == True:
                self.the_handle_i()
            if self.event_o == True:
                self.the_handle_o()
        if self.born_site == 'right':
            if self.event_UP == True:
                self.pos[1] = int(40 + self.v0 * self.time + 26 * self.time * self.time)
                self.time += 0.5
                if self.pos[1] > 40:
                    self.pos[1] = 40
                    self.event_UP = False
                    self.time = 0
            if self.event_DOWN == True:
                self.defend = 3
                con.hero2_defend = 3
            if self.event_LEFT == True:
                self.pos[0] -= 6
                # 防止走出地图外
                if self.pos[0] <=0:
                    self.pos[0] = 0
                #考虑挤走另一个英雄的情况(跳跃时不考虑)
                if con.WHO_IS_LEFT == 1 and self.pos[0] < 20 + con.hero1_pos[0] - 9 and \
                        self.event_UP == False :
                    if self.pos[0] >= 20:
                        con.hero1_pos[0] = self.pos[0] - 20 + 9
                        con.flag1_change = 1
                        self.pos[0] += 1
                        con.hero1_pos[0] += 1
                    else:
                        self.pos[0] += 2.5
            if self.event_RIGHT == True:
                self.pos[0] += 6
                # 防止走出地图外
                if self.pos[0] >=120:
                    self.pos[0] = 120
                #考虑挤走另一个英雄的情况(跳跃时不考虑)
                if con.WHO_IS_LEFT == 2 and self.pos[0] + 20 > con.hero1_pos[0] + 9 and \
                        self.event_UP == False :
                    if self.pos[0] + 20 <= 120:
                        con.hero1_pos[0] = self.pos[0] + 20 - 9
                        con.flag1_change = 1
                        self.pos[0] -= 1
                        con.hero1_pos[0] -= 1
                    else:
                        self.pos[0] -= 2.5
            if self.event_1 == True:
                pass
            if self.event_2 == True:
                pass
            if self.event_3 == True:
                pass
            if self.event_4 == True:
                self.the_handle_4()
            if self.event_5 == True:
                self.the_handle_5()
            if self.event_6 == True:
                self.the_handle_6()
    def the_handle_j(self):
        # 攻击判断函数之j键
        #draw_ikun()
        if con.WHO_IS_LEFT == 1 and self.pos[0] + 2 * USIZE >= con.hero2_pos[0]:
            con.hero2_life -= ATTACK - con.hero2_defend
            if con.hero2_life <= 0:
                con.hero2_life = 0
            con.flag2_life_change = 1
            if con.hero1_energy + 3 <= 50:
                con.hero1_energy += 3
            else:
                con.hero1_energy = 50
            con.flag1_energy_change = 1
            sound_manager.play_knife()
        elif con.WHO_IS_LEFT == 2 and self.pos[0] <= con.hero2_pos[0] + 2 * USIZE:
            con.hero2_life -= ATTACK - con.hero2_defend
            if con.hero2_life <= 0:
                con.hero2_life = 0
            con.flag2_life_change = 1
            if con.hero1_energy + 3 <= 50:
                con.hero1_energy += 3
            else:
                con.hero1_energy = 50
            con.flag1_energy_change = 1
            sound_manager.play_knife()
    def the_handle_k(self):
        # 攻击判断函数之k键
        # draw_ikun()
        if con.WHO_IS_LEFT == 1 and self.pos[0] + 2 * USIZE >= con.hero2_pos[0]:
            con.hero2_life -= ATTACK/2 - con.hero2_defend
            if con.hero2_life <= 0:
                con.hero2_life = 0
            con.flag2_life_change = 1
            if con.hero1_energy + 4.5 <= 50:
                con.hero1_energy += 4.5
            else:
                con.hero1_energy = 50
            con.flag1_energy_change = 1
            sound_manager.play_leg()
        elif con.WHO_IS_LEFT == 2 and self.pos[0] <= con.hero2_pos[0] + 2 * USIZE:
            con.hero2_life -= ATTACK/2 - con.hero2_defend
            if con.hero2_life <= 0:
                con.hero2_life = 0
            con.flag2_life_change = 1
            if con.hero1_energy + 3 <= 50:
                con.hero1_energy += 3
            else:
                con.hero1_energy = 50
            con.flag1_energy_change = 1
            sound_manager.play_leg()
    def the_handle_l(self):
        pass
    def the_handle_u(self):
        if con.counts%6 == 0:
            con.shenwei0 = 1
        if con.counts%6 == 1:
            con.shenwei1 = 1
        if con.counts % 6 == 2:
            con.shenwei2 = 1
        if con.counts % 6 == 3:
            con.shenwei3 = 1
        if con.counts % 6 == 4:
            con.shenwei4 = 1
        if con.counts % 6 == 5:
            con.shenwei5 = 1
        con.flag_shenwei = con.shenwei0 + con.shenwei1 + con.shenwei2 + con.shenwei3 + con.shenwei4 + con.shenwei5
        if con.flag_shenwei == 1:
            con.shenwei_size = (40*USIZE,40*USIZE)
        if con.flag_shenwei == 2:
            con.shenwei_size = (30 * USIZE, 30 * USIZE)
        if con.flag_shenwei == 3:
            con.shenwei_size = (20*USIZE,20*USIZE)
        if con.flag_shenwei == 4:
            con.shenwei_size = (10*USIZE,10*USIZE)
        if con.flag_shenwei == 5:
            con.shenwei_size = (5*USIZE,5*USIZE)
        if con.flag_shenwei == 6:
            con.flag_shenwei = 0
            con.shenwei0 = 0
            con.shenwei1 = 0
            con.shenwei2 = 0
            con.shenwei3 = 0
            con.shenwei4 = 0
            self.event_u = False
            con.skill_protect = 0
            con.in_shenwei = False#神威施放结束
    def the_handle_i(self):
        if con.counts%5 == 0:
            con.feibiao0 = 1
        if con.counts%5 == 1:
            con.feibiao1 = 1
        if con.counts % 5 == 2:
            con.feibiao2 = 1
        if con.counts % 5 == 3:
            con.feibiao3 = 1
        if con.counts % 5 == 4:
            con.feibiao4 = 1
        con.flag_feibiao = con.feibiao0 + con.feibiao1 + con.feibiao2 + con.feibiao3 + con.feibiao4
        if con.flag_feibiao == 5:
            con.flag_feibiao = 0
            con.feibiao0 = 0
            con.feibiao1 = 0
            con.feibiao2 = 0
            con.feibiao3 = 0
            con.feibiao4 = 0
            con.skill_protect = 0
            self.event_i = False
    def the_handle_o(self):
        #限定技&组合技：歼敌意志
        if con.counts%5 == 0:
            con.jiandi0 = 1
        if con.counts%5 == 1:
            con.jiandi1 = 1
        if con.counts % 5 == 2:
            con.jiandi2 = 1
        if con.counts % 5 == 3:
            con.jiandi3 = 1
        if con.counts % 5 == 4:
            con.jiandi4 = 1
        con.flag_jiandi = con.jiandi0 + con.jiandi1 + con.jiandi2 + con.jiandi3 + con.jiandi4
        if con.flag_jiandi == 5:
            con.flag_jiandi = 0
            con.jiandi0 = 0
            con.jiandi1 = 0
            con.jiandi2 = 0
            con.jiandi3 = 0
            con.jiandi4 = 0
            con.skill_protect = 0
            self.event_o = False

    def the_handle_1(self):
        # 攻击判断函数之1键
        if con.WHO_IS_LEFT == 2 and self.pos[0] + 2 * USIZE >= con.hero1_pos[0]:
            con.hero1_life -= ATTACK - con.hero1_defend
            if con.hero1_life <= 0:
                con.hero1_life = 0
            con.flag1_life_change = 1
            if con.hero2_energy + 3  <= 50:
                con.hero2_energy += 3
            else:
                con.hero2_energy = 50
            con.flag2_energy_change = 1
            sound_manager.play_knife()
        elif con.WHO_IS_LEFT == 1 and self.pos[0] <= con.hero1_pos[0] + 2 * USIZE:
            con.hero1_life -= ATTACK - con.hero1_defend
            if con.hero1_life <= 0:
                con.hero1_life = 0
            con.flag1_life_change = 1
            if con.hero2_energy + 3 <= 50:
                con.hero2_energy += 3
            else:
                con.hero2_energy = 50
            con.flag2_energy_change = 1
            sound_manager.play_knife()
    def the_handle_2(self):
        # 攻击判断函数之2键
        if con.WHO_IS_LEFT == 2 and self.pos[0] + 2 * USIZE >= con.hero1_pos[0]:
            con.hero1_life -= ATTACK/2 + con.hero1_defend
            if con.hero1_life <= 0:
                con.hero1_life = 0
            con.flag1_life_change = 1
            if con.hero2_energy + 4.5 + con.hero2_energy_add <= 50:
                con.hero2_energy += 4.5 + con.hero2_energy_add
            else:
                con.hero2_energy = 50
            con.flag2_energy_change = 1
            sound_manager.play_leg()
        elif con.WHO_IS_LEFT == 1 and self.pos[0] <= con.hero1_pos[0] + 2 * USIZE:
            con.hero1_life -= ATTACK/2 + con.hero1_defend
            if con.hero1_life <= 0:
                con.hero1_life = 0
            con.flag1_life_change = 1
            if con.hero2_energy + 4.5 + con.hero2_energy_add <= 50:
                con.hero2_energy += 4.5 + con.hero2_energy_add
            else:
                con.hero2_energy = 50
            con.flag2_energy_change = 1
            sound_manager.play_leg()
    def the_handle_3(self):
        pass
    def the_handle_4(self):
        if con.counts%5 == 0:
            con.ikun0 = 1
        if con.counts%5 == 1:
            con.ikun1 = 1
        if con.counts % 5 == 2:
            con.ikun2 = 1
        if con.counts % 5 == 3:
            con.ikun3 = 1
        if con.counts % 5 == 4:
            con.ikun4 = 1
        con.flag_ikun = con.ikun0 + con.ikun1 + con.ikun2 + con.ikun3 + con.ikun4
        if con.flag_ikun == 5:
            con.flag_ikun = 0
            con.ikun0 = 0
            con.ikun1 = 0
            con.ikun2 = 0
            con.ikun3 = 0
            con.ikun4 = 0
            con.skill_protect = 0
            self.event_4 = False

    def the_handle_5(self):
        if con.counts%5 == 0:
            con.tongling0 = 1
        if con.counts%5 == 1:
            con.tongling1 = 1
        if con.counts % 5 == 2:
            con.tongling2 = 1
        if con.counts % 5 == 3:
            con.tongling3 = 1
        if con.counts % 5 == 4:
            con.tongling4 = 1
        con.flag_tongling = con.tongling0 + con.tongling1 + con.tongling2 + con.tongling3 + con.tongling4
        if con.flag_tongling == 5:
            con.flag_tongling = 0
            con.tongling0 = 0
            con.tongling1 = 0
            con.tongling2 = 0
            con.tongling3 = 0
            con.tongling4 = 0
            con.skill_protect = 0
            self.event_5 = False
    def the_handle_6(self):
        if con.counts % 5 == 0:
            con.fumo0 = 1
        if con.counts % 5 == 1:
            con.fumo1 = 1
        if con.counts % 5 == 2:
            con.fumo2 = 1
        if con.counts % 5 == 3:
            con.fumo3 = 1
        if con.counts % 5 == 4:
            con.fumo4 = 1
        con.flag_fumo = con.fumo0 + con.fumo1 + con.fumo2 + con.fumo3 + con.fumo4
        if con.flag_fumo == 5:
            con.flag_fumo = 0
            con.fumo0 = 0
            con.fumo1 = 0
            con.fumo2 = 0
            con.fumo3 = 0
            con.fumo4 = 0
            con.skill_protect = 0
            self.event_6 = False
hero1 = Hero()
hero1.set('left')
hero1.send_pos()
hero2 = Hero()
hero2.set('right')
hero2.send_pos()