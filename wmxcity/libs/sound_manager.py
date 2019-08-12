import os
import pygame

class SoundManager:
    music_path = os.path.join('res','background.mp3')

    def __init__(self):
        self._init_music()
        self.sound_KO = self._load_sound('sound_KO.ogg')
        self.sound_ikun = self._load_sound('sound_ikun.ogg')
        self.sound_feibiao = self._load_sound('feibiao.ogg')
        self.sound_shenwei = self._load_sound('sound_shenwei.ogg')
        self.sound_war_begin = self._load_sound('war_begin.ogg')
        self.sound_tongling = self._load_sound('sound_tongling.ogg')
        self.sound_jiandi = self._load_sound('sound_jiandi.ogg')
        self.sound_fumo = self._load_sound('sound_fumo.ogg')
        self.sound_leg = self._load_sound('sound_leg.ogg')
        self.sound_knife = self._load_sound('sound_knife.ogg')
    #背景音乐
    @classmethod
    def _init_music(cls):
        pygame.mixer.init()
        pygame.mixer.music.load(cls.music_path)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

    @staticmethod
    def _load_sound(file_name):
        return pygame.mixer.Sound(os.path.join('res',file_name))

    @staticmethod
    def replay_music():
        pygame.mixer.music.rewind()
        pygame.mixer.music.unpause()

    @staticmethod
    def pause_music():
        pygame.mixer.music.pause()

    @staticmethod
    def resume_music():
        pygame.mixer.music.unpause()

    def play_sound_be_attacked(self):
        self.sound_be_attacked.play()

    def play_sound_be_killed(self):
        self.sound_be_killed.play()

    def play_sound_fail(self):
        self.sound_fail.play()

    def play_sound_KO(self):
        self.sound_KO.play()

    def play_sound_ikun(self):
        self.sound_ikun.play()

    def play_sound_feibiao(self):
        self.sound_feibiao.play()

    def play_sound_shenwei(self):
        self.sound_shenwei.play()

    def play_war_begin(self):
        self.sound_war_begin.play()

    def play_tongling(self):
        self.sound_tongling.play()

    def play_jiandi(self):
        self.sound_jiandi.play()

    def play_fumo(self):
        self.sound_fumo.play()

    def play_leg(self):
        self.sound_leg.play()

    def play_knife(self):
        self.sound_knife.play()
# 单例模式
sound_manager = SoundManager()
