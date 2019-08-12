import pygame,sys,time
from pygame.locals import *

from constants import *
from core.hero import hero1,hero2
from libs.sound_manager import sound_manager

class GameBoard:
    def __init__(self):
        self.fontObj = pygame.font.Font('res/Kaiti_GB2312.ttf', 40)
        self.scoreFont = pygame.font.Font('res/Kaiti_GB2312.ttf', 32)
        self.scoreFont2 = pygame.font.Font('res/Kaiti_GB2312.ttf', 130)
        self.full_screen = False  # 是否全屏
        self.screen = self._new_screen(SCREEN_SIZE)

    def draw(self):
        self.draw_board()
        pygame.display.update()

    def draw_board(self):
        self.screen.fill(WHITE)
        kunbackground = pygame.image.load(r'res\background.png')
        kunbackground = pygame.transform.scale(kunbackground,(1400,700))  # 调整图片大小
        self.screen.blit(kunbackground, (0,0))
        #kunbackground = pygame.image.load('res\kunbackground.jpg')
        #kunbackground = pygame.transform.scale(kunbackground,(500,500))  # 调整图片大小
        #self.screen.blit(kunbackground, (0,0))
        hero1.draw_self(self.screen)
        hero2.draw_self(self.screen)

        #画计时器
        the_time = hero1.fontObj.render(str(con.counts), True, BLACK)
        self.screen.blit(the_time, (680, 10))
        pygame.draw.line(self.screen, PURPLE, (675, 6 * USIZE), (724, 6 * USIZE), 3)

        if con.counts >= 98:
            if con.flag_play_war_begin == 0:
                sound_manager.play_war_begin()
                con.flag_play_war_begin = 1
            fighting = self.scoreFont2.render('战斗开始 ！', True, BLACK)
            self.screen.blit(fighting, (453, 200))

        if con.winner == 1:
            xi_win = self.scoreFont2.render('熙熙 WIN ！', True, BLACK)
            self.screen.blit(xi_win, (400 , 200))
        elif con.winner == 2:
            kun_win = self.scoreFont2.render('坤坤 WIN ！', True, BLACK)
            self.screen.blit(kun_win, (400, 200))
        #画技能特效
        self.draw_ikun()
        self.draw_feibiao()
        self.draw_shenwei()
        self.draw_zhaohuan()
        self.draw_jiandi()
        self.draw_fumo()

        #画防护罩
        if hero1.event_s == True:
            self.draw_defend_box(hero1)
        if hero2.event_DOWN == True:
            self.draw_defend_box(hero2)
    def draw_ikun(self):
        #坤坤攻击 之 地爆天坤
        if con.flag_ikun == 0:
            return
        if con.winner != 0:
            return
        name = self.scoreFont2.render('秘技·地爆天坤', True, PURPLE)
        self.screen.blit(name, (250, 20))

        basketball = pygame.image.load(r'res\basketball.jpg')
        if con.flag_ikun == 1:
            basketball = pygame.transform.scale(basketball,(30*USIZE,30*USIZE))  # 调整图片大小
            self.screen.blit(basketball, (550, 100))
        elif con.flag_ikun == 2:
            basketball = pygame.transform.scale(basketball,(50*USIZE,50*USIZE))  # 调整图片大小
            self.screen.blit(basketball, (450, 100))
        elif con.flag_ikun == 3:
            basketball = pygame.transform.scale(basketball,(70*USIZE,70*USIZE))  # 调整图片大小
            self.screen.blit(basketball, (350, 50))
        elif con.flag_ikun == 4:
            basketball = pygame.transform.scale(basketball,(90*USIZE,90*USIZE))  # 调整图片大小
            self.screen.blit(basketball, (250, 0))
    def draw_feibiao(self):
        #熙熙攻击 之 千里追踪术
        if con.flag_feibiao == 0:
            return
        if con.winner != 0:
            return
        name = self.scoreFont2.render('秘技·千里追踪术', True, RED)
        self.screen.blit(name, (200, 20))

        feibiao = pygame.image.load(r'res\feibiao.jpg')
        if con.flag_feibiao == 1:
            feibiao = pygame.transform.scale(feibiao,(80*USIZE,80*USIZE))  # 调整图片大小
            self.screen.blit(feibiao, (con.hero2_pos[0]*USIZE-275, con.hero2_pos[1]*USIZE-300))
        elif con.flag_feibiao == 2:
            feibiao = pygame.transform.scale(feibiao,(50*USIZE,50*USIZE))  # 调整图片大小
            self.screen.blit(feibiao, (con.hero2_pos[0]*USIZE-135, con.hero2_pos[1]*USIZE-150))
        elif con.flag_feibiao == 3:
            feibiao = pygame.transform.scale(feibiao,(40*USIZE,40*USIZE))  # 调整图片大小
            self.screen.blit(feibiao, (con.hero2_pos[0]*USIZE-80, con.hero2_pos[1]*USIZE-100))
        elif con.flag_feibiao == 4:
            feibiao = pygame.transform.scale(feibiao,(20*USIZE,20*USIZE))  # 调整图片大小
            self.screen.blit(feibiao, (con.hero2_pos[0]*USIZE+20, con.hero2_pos[1]*USIZE+50))
    def draw_shenwei(self):
        #熙熙攻击 之 神威
        if con.in_shenwei:
            name = self.scoreFont2.render('时空间忍术·神威', True, PURPLE)
            self.screen.blit(name, (200, 20))
    def draw_zhaohuan(self):
        #坤坤攻击 之 通灵术
        if con.flag_tongling == 0:
            return
        if con.winner != 0:
            return
        name = self.scoreFont2.render('忍法·附身通灵术', True, PURPLE)
        self.screen.blit(name, (200, 20))

        name2 = self.scoreFont.render('敌方受到伤害：30', True, ORANGE)
        self.screen.blit(name2, (1130, 120))

        name3 = self.scoreFont.render('己方回复生命：40', True, ORANGE)
        self.screen.blit(name3, (1130, 160))

        tongling = pygame.image.load(r'res\tongling.jpg')
        tongling = pygame.transform.scale(tongling,(60*USIZE,60*USIZE))  # 调整图片大小
        self.screen.blit(tongling, (con.hero2_pos[0]*USIZE-200, con.hero2_pos[1]*USIZE-250))

    def draw_jiandi(self):
        #熙熙攻击 之 歼敌意志
        if con.flag_jiandi == 0:
            return
        if con.winner != 0:
            return
        name = self.scoreFont2.render(' 秘技·歼敌意志', True, PURPLE)
        self.screen.blit(name, (200, 20))
        name2 = self.fontObj.render('己方生命条数 -1', True, BLACK)
        self.screen.blit(name2, (50, 150))
        pygame.draw.line(self.screen,ORANGE,(50,200),(355,200),7)

        name3 = self.fontObj.render('敌方生命条数 -1', True, BLACK)
        self.screen.blit(name3, (1050, 150))
        pygame.draw.line(self.screen,ORANGE,(1050,200),(1355,200),7)

    def draw_fumo(self):
        #坤坤攻击 之 附魔
        if con.flag_fumo == 0:
            return
        if con.winner != 0:
            return
        name = self.scoreFont2.render('秘技·附魔', True, RED)
        self.screen.blit(name, (375, 20))
        name2 = self.fontObj.render('能量回复巨额提升！', True, ORANGE)
        self.screen.blit(name2, (1050, 150))

    def _new_screen(self, size, full=False):
        if full:
            self.full_screen = True
            return pygame.display.set_mode(size, pygame.FULLSCREEN)

        self.full_screen = False
        return pygame.display.set_mode(size)

    def draw_defend_box(self,hero):
        #画防护罩
        pygame.draw.line(self.screen,GRAY,(hero.pos[0]*USIZE,(hero.pos[1]-5)*USIZE),(hero.pos[0]*USIZE,(hero.pos[1]+30)*USIZE),5)
        pygame.draw.line(self.screen,GRAY,((hero.pos[0]+20)*USIZE,(hero.pos[1]-5)*USIZE),((hero.pos[0]+20)*USIZE,(hero.pos[1]+30)*USIZE),5)
        pygame.draw.line(self.screen, GRAY, (hero.pos[0]*USIZE,(hero.pos[1]+30)*USIZE),((hero.pos[0]+20)*USIZE,(hero.pos[1]+30)*USIZE), 5)
        pygame.draw.line(self.screen,GRAY,(hero.pos[0]*USIZE,hero.pos[1]*USIZE),((hero.pos[0]+20)*USIZE,hero.pos[1]*USIZE),5)
        pygame.draw.line(self.screen,GRAY,(hero.pos[0]*USIZE,(hero.pos[1]-5)*USIZE),((hero.pos[0]+20)*USIZE,(hero.pos[1]-5)*USIZE),5)
        name = self.fontObj.render('  防护罩', True, BLACK)
        self.screen.blit(name, (hero.pos[0]*USIZE,(hero.pos[1]-4)*USIZE-4))