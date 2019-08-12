import sys
import pygame
from libs.sound_manager import sound_manager

#定值
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (20, 160, 15)
BLUE = (0,191,255)
PINK = (255,182,193)
GRAY= (	128,128,128)
PURPLE = (153,50,204)
ORANGE = (255,165,0)
LENGTH = 140 #屏幕长
HEIGHT = 70 #屏幕宽
USIZE = 10 #单位长度
ATTACK = 4#普攻伤害值


class Constants:
    def __init__(self):
        self.state = 'begin'#begin表示游戏正在进行中，over表示游戏结束了
        self.counts = 99 #倒计时器
        self.WHO_IS_LEFT = 1#'1'表示hero1在hero2左边，'2'表示hero2在hero1左边,默认hero1在左边
        self.flag_play_war_begin = 0#确保开场音效只播放一遍
        self.skill_protect = 0  # 为1表示处于放技能状态，此时其他任何攻击无效

        self.hero1_pos = [0, 0]
        self.flag1_change = 0
        self.hero1_life = 100
        self.flag1_life_change = 0
        self.hero1_energy = 0
        self.flag1_energy_change = 0
        self.hero1_defend = 0
        self.hero1_life_num = 2
        self.flag1_life_num_change = 0
        self.flag1_once_attcak = 1#限定技是否可用

        self.hero2_pos = [0, 0]
        self.flag2_change = 0
        self.hero2_life = 100
        self.flag2_life_change = 0
        self.hero2_energy = 0
        self.flag2_energy_change = 0
        self.hero2_defend = 0
        self.hero2_life_num = 2
        self.flag2_life_num_change = 0
        self.flag2_once_attcak = 1#限定技是否可用
        self.hero2_energy_add = 0  # 英雄'坤坤'技能'秘技·附魔':能量恢复巨额加成

        self.winner = 0 #0表示未分胜负，1、2分别表示两个英雄

        self.flag_ikun = 0#为1表示‘地爆天坤’特效图片小，2为中，3为大
        self.ikun0 = 0
        self.ikun1 = 0
        self.ikun2 = 0
        self.ikun3 = 0
        self.ikun4 = 0

        self.flag_feibiao = 0#为1表示‘千里追踪术’特效图片大，2为中，3为小
        self.feibiao0 = 0
        self.feibiao1 = 0
        self.feibiao2 = 0
        self.feibiao3 = 0
        self.feibiao4 = 0

        self.flag_shenwei = 0#为1表示‘神威’特效图片大，2为中，3为小
        self.shenwei0 = 0
        self.shenwei1 = 0
        self.shenwei2 = 0
        self.shenwei3 = 0
        self.shenwei4 = 0
        self.shenwei5 = 0
        self.shenwei_size = (20*USIZE,30*USIZE)#神威技能显示图片的大小
        self.in_shenwei = False#熙熙是否正在施放神威技能

        self.flag_tongling = 0#为1表示‘通灵术’特效图片大，2为中，3为小
        self.tongling0 = 0
        self.tongling1 = 0
        self.tongling2 = 0
        self.tongling3 = 0
        self.tongling4 = 0

        self.flag_jiandi = 0#为1表示‘歼敌意志’特效图片大，2为中，3为小
        self.jiandi0 = 0
        self.jiandi1 = 0
        self.jiandi2 = 0
        self.jiandi3 = 0
        self.jiandi4 = 0

        self.flag_fumo = 0#技能'秘技·附魔'
        self.fumo0 = 0
        self.fumo1 = 0
        self.fumo2 = 0
        self.fumo3 = 0
        self.fumo4 = 0



    def gameover(self):
        if self.state == 'begin':
            sound_manager.play_sound_KO()
            self.state = 'over'

TITLE = '拳皇重生之熙坤格斗'

SCREEN_SIZE = LENGTH*USIZE, HEIGHT*USIZE  # 屏幕尺寸

con = Constants()

#护甲值：6
#j攻击：7