"""
http://github.com/yenchenlin/DeepLearningFlappyBird
"""

import math
import random
import time

import numpy as np

from .starfish import pygm
from .starfish import consts
from .starfish import sptdraw
from .starfish import utils


def dir_prefix(p):
    return utils.dir_abs(p, __file__)


class FBSptBird(pygm.SptImgAnim):
    """34x24"""
    def __init__(self, *args, **kwargs):

        self.bird_imgs = [
            dir_prefix('img_flibird/sprites/redbird-upflap.png'),
            dir_prefix('img_flibird/sprites/redbird-midflap.png'),
            dir_prefix('img_flibird/sprites/redbird-downflap.png'),
        ]

        super(FBSptBird, self).__init__(self.bird_imgs)


class FBSptPipe(pygm.SptImg):
    """52x320"""

    pipe_seq = 0

    def __init__(self, img_file, *args, **kwargs):
        super(FBSptPipe, self).__init__(img_file)

        FBSptPipe.pipe_seq += 1
        self.seq = FBSptPipe.pipe_seq


class FBSptPipesTwo(pygm.PyGMSprite):
    def __init__(self, *args, **kwargs):
        super(FBSptPipesTwo, self).__init__()

        self.pipe_up = FBSptPipe(dir_prefix('img_flibird/sprites/pipe-green.png'))
        self.pipe_up.rect.top = 0
        self.pipe_up.rect.left = 0
        self.disp_add(self.pipe_up)
        self.pipe_up.rotate(180)

        self.pipe_dn = FBSptPipe(dir_prefix('img_flibird/sprites/pipe-green.png'))
        self.pipe_dn.rect.top = 440
        self.pipe_dn.rect.left = 0
        self.disp_add(self.pipe_dn)


class FBSptFly(sptdraw.SptDrawBase):
    def __init__(self, size, *args, **kwargs):
        super(FBSptFly, self).__init__(size)

        self.init_cfg()
        self.init_spts()

    def init_cfg(self):
        self.pipes = []
        self.pipe_wh = (52, 320)
        self.pipes_sc = {}

        self.pos_bird_left = 60

        self.cnt = 0

        self.e_keys_up = []
        self.e_keys_dn = []

        self.dire = 2  # 0:^ 1:> 2:v 3:<
        self.dire_last = self.dire

        self.speed_init = 0#5#4#9#6#2
        self.speed_flap = -9#29#19#
        self.speed_max = 10
        self.speed_d = 1
        self.speed = self.speed_init
        self.speed_pipe = 4

        self.stopped = False

        self.game_over = False

        self.sc = 0
        self.sc_tm_intvl = self.size[0] - self.pos_bird_left + self.pipe_wh[0]
        self.sc_tm_intvl /= self.speed_pipe

        self.start_tm = time.time()

    def init_spts(self):
        self.draw_on()

        self.init_bird()

        self.init_pipes()

        self.init_bsgd()

        self.init_lbl_sc()

    def reset(self):
        self.clear_pipes()
        self.init_cfg()
        self.init_pipes()

        self.init_bird_pos()
        self.move_bsgd()
        self.refresh_sc()

    def draw_on(self, *args, **kwargs):
        self.fill(consts.BLACK)

    def init_bird(self):
        self.bird = FBSptBird()
        self.disp_add(self.bird)
        self.init_bird_pos()

    def init_bird_pos(self):
        self.bird.rect.top = int((self.size[1] - self.bird.rect.height) / 2)
        self.bird.rect.left = self.pos_bird_left

    def init_bsgd(self):
        self.bsgd = pygm.SptImg(dir_prefix('img_flibird/sprites/base.png'))
        self.bsgd.rect.top = self.size[1] - self.bsgd.rect.height #400#
        self.bsgd.rect.left = 0
        self.disp_add(self.bsgd)

    def init_lbl_sc(self):
        self.lbl_sc = pygm.SptLbl(str(self.sc), c=consts.YELLOW, font_size=32)
        self.lbl_sc.rect.top = 200
        self.lbl_sc.rect.left = 130
        self.disp_add(self.lbl_sc)

    def init_pipes(self, gap=None):
    #def init_pipes(self, gap=(100, 150)):  # TODO: for simplying the game for train

        #self.pipest = FBSptPipesTwo()
        #self.pipest.rect.top = -100
        #self.pipest.rect.left = 200
        #self.disp_add(self.pipest)

        #rtop = random.randint(50, self.pipe_wh[1] - 50)
        #rgap = random.randint(50, 200)
        #rleft = self.size[0]  #random.randint(self.size[0] / 2, self.size[0])
        #at = [0-rtop, rleft, 0-rtop + self.pipe_wh[1] + rgap, rleft]
        #print at

        if gap is None:
            gap_t = random.randint(70, 140)
            gap_t -= (gap_t % 5)

            gap_h = random.randint(100, 120)
            gap_h -= (gap_h % 5)
        else:
            gap_t = gap[0]
            gap_h = gap[1]
        rleft = self.size[0]  #random.randint(self.size[0] / 2, self.size[0])
        at = [gap_t - self.pipe_wh[1], rleft,
              gap_t + gap_h, rleft]

        self.add_pipes(at)

    def add_pipes(self, at):
        pipe_up = FBSptPipe(dir_prefix('img_flibird/sprites/pipe-green.png'))
        pipe_up.rect.top = at[0]
        pipe_up.rect.left = at[1]
        self.disp_add(pipe_up)
        pipe_up.rotate(180)

        pipe_dn = FBSptPipe(dir_prefix('img_flibird/sprites/pipe-green.png'))
        pipe_dn.rect.top = at[2]
        pipe_dn.rect.left = at[3]
        self.disp_add(pipe_dn)

        self.pipes.append(pipe_up)
        self.pipes.append(pipe_dn)

    def clear_pipes(self):
        for pipe in self.pipes:
            self.disp_del(pipe)

    def key_to_di(self, k):
        if k == self.pglc.K_UP:
            return 1
        else:
            return None

    def handle_event(self, events, *args, **kwargs):
        if not self.flag_check_event:
            return events
        else:
            return self.check_key(events)

    def check_key(self, events):
        r_events = []

        e_keys_up = []
        e_keys_dn = []

        for event in events:
            if event.type == self.pglc.KEYUP:
                di = self.key_to_di(event.key)
                if di is not None:
                    e_keys_up.append(di)
                else:
                    r_events.append(event)

            elif event.type == self.pglc.KEYDOWN:
                di = self.key_to_di(event.key)
                if di is not None:
                    e_keys_dn.append(di)
                else:
                    r_events.append(event)

            else:
                r_events.append(event)

        self.e_keys_up = e_keys_up
        self.e_keys_dn = e_keys_dn

        return r_events

    def refresh(self, fps_clock, *args, **kwargs):
        if self.stopped:
            return

        self.draw_on()  # i am a draw sprite

        self.turn_bird_di(self.e_keys_dn, self.e_keys_up)

        self.move_pipes()

        self.move_bird()

        self.move_bsgd()

        self.check_bird_pos()

        self.refresh_sc()

    def turn_bird_di(self, e_keys_dn=[], e_keys_up=[]):

        if len(e_keys_dn) > 0:
            self.dire_last = self.dire
            self.dire = 0  # ^
            self.speed = self.speed_flap  # flap once

        else:
            self.speed += self.speed_d  # speed up
            if self.speed > self.speed_max:
                self.speed = self.speed_max

    def move_pipes(self):
        left_max = 0

        fly_pass = False

        for i, pipe in enumerate(self.pipes):
            pipe.rect.left -= self.speed_pipe

            if pipe.rect.left + pipe.rect.width < self.pos_bird_left + 10:

                k = str(pipe.seq)
                if k not in self.pipes_sc.keys():
                    self.pipes_sc[k] = k

                    if pipe.rect.top < 0:  # the upper pipe
                        fly_pass = True
                        self.sc += 1

            if pipe.rect.left + pipe.rect.width < 0:
                self.disp_del(pipe)
                del self.pipes[i]
            else:
                left_max = pipe.rect.left


        if left_max < self.size[0] / 2:
            self.init_pipes()

    def move_bsgd(self):
        self.disp_del(self.bsgd)
        self.disp_add(self.bsgd)
        self.bsgd.rect.left -= self.speed_pipe
        if self.bsgd.rect.left < self.size[0] - self.bsgd.rect.width:
            self.bsgd.rect.left = -3

    def refresh_sc(self):

        self.disp_del(self.lbl_sc)
        self.disp_add(self.lbl_sc)
        self.lbl_sc.lbl_set(str(self.sc))

    def move_bird(self):

        if self.dire == 0:
            self.bird.rect.top += self.speed

            # flap once a time
            self.dire = 2
        elif self.dire == 2:
            self.bird.rect.top += self.speed

    def check_bird_pos(self):
        bird_top = self.bird.rect.top
        bird_left = self.bird.rect.left
        bird_w = self.bird.rect.width
        bird_h = self.bird.rect.height

        bsgd_h = self.bsgd.rect.height

        over = False
        if bird_top < 0:
            self.bird.rect.top = 0
        elif bird_top > (self.size[1] - bsgd_h - bird_h):
            self.bird.rect.top = self.size[1] - bsgd_h - bird_h
            over = True
        else:
            pass

        if not over:
            for pipe in self.pipes:
                colli = self.geo_check_rect_colli(pipe.rect, self.bird.rect)
                if colli:
                    over = True
                    break

        if over:
            self.stopped = True
            self.game_over = True

        return over

    def geo_check_rect_colli(self, rct1, rct2):
        ps2 = [[rct2.left, rct2.top],
               [rct2.left + rct2.width, rct2.top],
               [rct2.left, rct2.top + rct2.height],
               [rct2.left + rct2.width, rct2.top + rct2.height]]

        for ps in ps2:
            colli = self.geo_check_ps_in_rect(ps, rct1)
            if colli:
                return True

        return False

    def geo_check_ps_in_rect(self, ps, rct):
        if ps[0] > rct.left and ps[0] < rct.left + rct.width and \
            ps[1] > rct.top and ps[1] < rct.top + rct.height:
            return True
        else:
            return False


class FBSceneA(pygm.PyGMScene):
    def __init__(self, *args, **kwargs):
        super(FBSceneA, self).__init__(*args, **kwargs)

        self.fly = FBSptFly((288, 512))
        self.fly.rect.top = 0
        self.fly.rect.left = 0
        self.disp_add(self.fly)

    def handle_event(self, events, *args, **kwargs):
        return events

    def refresh(self, fps_clock, *args, **kwargs):
        pass


class GMFliBird(pygm.PyGMGame):
    def __init__(self, title, winw, winh, *args, **kwargs):
        super(GMFliBird, self).__init__(title, winw, winh)

        self.bk = pygm.SptImg(dir_prefix('img_flibird/sprites/background-black.png'))
        self.bk.rect.top = 0
        self.bk.rect.left = 0
        self.disp_add(self.bk)

        self.scn1 = FBSceneA()
        self.disp_add(self.scn1)

        self.fly = self.scn1.fly


def main():
    sf = GMFliBird('Flibird', 288, 512)
    sf.mainloop()


if __name__ == '__main__':
    main()
