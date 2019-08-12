import pygame,sys,time
from pygame.locals import *
from constants import *
from core.game_board import GameBoard
from libs.sound_manager import sound_manager
from core.hero import hero1,hero2


COUNT = pygame.USEREVENT + 1
pygame.time.set_timer(COUNT, 1000)

class CityGame:

    def __init__(self):
        pygame.init()
        self.board =GameBoard()
        pygame.display.set_caption(TITLE)

    def vir_handle_event(self,event):
        if event.type == KEYDOWN or event.type == KEYUP:
            hero1.handle_event_man(event)
            hero2.handle_event_man(event)
    def do_handle_event(self):
        hero1.the_handle_event_man()
        hero2.the_handle_event_man()
    def start(self):
        self.board.draw()
        #pygame.key.set_repeat(1, 50)#按键一直按下时，每隔50ms触发一次KETDOWN事件，每次触发后1ms开始响应
        while True:
            # 判断目前谁在左边
            if hero1.pos[0] <= hero2.pos[0]:
                con.WHO_IS_LEFT = 1
            else:
                con.WHO_IS_LEFT = 2
            # 事件处理
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if con.state == 'over':
                    break
                hero1.hero_everytime()#每次循环都要对英雄状态进行更新、判断
                hero2.hero_everytime()
                self.vir_handle_event(event)  # 逻辑上处理事件
                if event.type == COUNT:
                    if con.winner == 0:
                        con.counts -= 1
                    if con.counts == 0:
                        if hero1.life >= hero2.life:
                            con.winner = 1
                            con.gameover()
                        else:
                            con.winner = 2
                            con.gameover()
            if con.state != 'over':
                self.do_handle_event()  # 物理上处理事件
            self.board.draw()

if __name__ == '__main__':
    game = CityGame()
    game.start()