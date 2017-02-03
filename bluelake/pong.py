"""
Game Pong from Atari.


whole screen:

0                     160
=========================

24
-------------------------
34
-------------------------





194
-------------------------

210
=========================



"""

import random
import math

from starfish import pygm
from starfish import consts
from starfish import sptdraw
from starfish import utils


COLOR_PONG_GD = (144, 72, 17, 255)
COLOR_PONG_MY = (213, 130, 74, 255)
COLOR_PONG_AI = (92, 186, 92, 255)


class SptBall(sptdraw.SptDrawBase):
    def __init__(self, size, color=consts.WHITE, *args, **kwargs):
        super(SptBall, self).__init__(size)

        self.color = color

        self.draw_on()

    def draw_on(self, *args, **kwargs):
        self.fill(self.color)
        #self.pygm.draw.circle(self.surf, self.color,
        #                      (self.size[0] / 2, self.size[1] / 2),
        #                      self.size[0] / 2, 0)


class SptPaddle(sptdraw.SptDrawBase):
    def __init__(self, size, color, *args, **kwargs):
        super(SptPaddle, self).__init__(size)

        self.color = color

        self.draw_on()

    def draw_on(self, *args, **kwargs):
        self.fill(self.color)
        #self.pygm.draw.rect(self.surf, self.color,
        #                    (-self.size[0] / 2, -self.size[1] / 2,
        #                     self.size[0], self.size[1]))


class SptGround(sptdraw.SptDrawBase):
    def __init__(self, size, color, *args, **kwargs):
        super(SptGround, self).__init__(size)

        self.color = color

        self.draw_on()

    def draw_on(self, *args, **kwargs):
        self.fill(self.color)


class PongBallActor(object):
    def __init__(self, ball, grnd_pn, pdl_my, pdl_ai):
        self.ball = ball
        self.grnd_pn = grnd_pn
        self.pdl_my = pdl_my
        self.pdl_ai = pdl_ai

        self.e_keys_up = []
        self.e_keys_dn = []

        self.pos_ball_top_min = self.grnd_pn.rect.top
        self.pos_ball_top_max = self.grnd_pn.rect.top + \
            self.grnd_pn.rect.height - self.ball.rect.height

        self.pos_ball_left_min = self.pdl_my.rect.left + self.pdl_my.rect.width
        self.pos_ball_left_max = self.pdl_ai.rect.left - self.pdl_ai.rect.width

        self.dire = 2  # angle : 2 * pi
        self.dire_last = self.dire

        self.speed = 5#2
        self.stopped = False

        self.n_rch_right = 0  # for replace ai

        self.init_ball_di_rand()

    def reset(self):
        self.stopped = False
        self.n_rch_right = 0  # for replace ai
        self.init_ball_di_rand()

    def init_ball_di_rand(self):
        self.dire = random.random() * math.pi * 2
        dia = self.get_ball_di_area(self.dire)

        while dia not in [2, 4, 6, 8]:
            self.dire = random.random() * math.pi * 2
            dia = self.get_ball_di_area(self.dire)

    def refresh(self, fps_clock, *args, **kwargs):
        self.move_ball_pos()

        return self.check_ball_pos()

    def move_ball_pos(self):
        if not self.stopped:
            #print self.dire
            #print self.speed * math.sin(self.dire)
            #print self.speed * math.cos(self.dire)
            #print '-' * 60
            self.ball.rect.top += self.speed * math.sin(self.dire)
            self.ball.rect.left += self.speed * math.cos(self.dire)

    def check_ball_pos(self):
        r = 0  # normal run

        if not self.stopped:
            ball_top = self.ball.rect.top
            ball_left = self.ball.rect.left

            if ball_top < self.pos_ball_top_min:
                self.ball.rect.top = self.pos_ball_top_min
                self.reflect_ball_di('top')
            elif ball_top > self.pos_ball_top_max:
                self.ball.rect.top = self.pos_ball_top_max
                self.reflect_ball_di('bottom')
            else:
                pass

            if ball_left < self.pos_ball_left_min:
                self.ball.rect.left = self.pos_ball_left_min

                if self.check_pdl_my_pos():
                    self.reflect_ball_di('left')
                else:
                    r = 1  # my lost
                    self.stopped = True

            elif ball_left > self.pos_ball_left_max:
                self.ball.rect.left = self.pos_ball_left_max

                if self.check_pdl_ai_pos():
                    self.reflect_ball_di('right')
                else:
                    r = 2  # ai lost
                    ##self.stopped = True

            else:
                pass

        else:
            r = 9  # stopped

        return r

    def reflect_ball_di(self, at):

        if at == 'top' or at == 'bottom':
            self.dire = math.pi * 2.0 - self.dire

        elif at == 'left' or at == 'right':
            '''
            dia = self.get_ball_di_area(self.dire)
            if dia in [2, 4]:
                self.dire = math.pi - self.dire
            elif dia in [6, 8]:
                self.dire = math.pi * 3.0 - self.dire
            else:
                pass
            '''
            self.dire = math.pi - self.dire
            if self.dire < 0.0:
                self.dire += math.pi * 2.0

        else:
            pass

    def get_ball_di_area(self, di):
        eng_small = 0.2#1e-1#1e-3

        if di < eng_small or math.fabs(math.pi * 2.0 - di) < eng_small:
            return 1
        elif di - (math.pi / 2.0) < eng_small:
            return 3
        elif di - math.pi < eng_small:
            return 5
        elif di - (math.pi / 2.0) * 3.0 < eng_small:
            return 7

        elif 0.0 < di < (math.pi / 2.0):
            return 2
        elif (math.pi / 2.0) < di < math.pi:
            return 4
        elif math.pi < di < (math.pi / 2.0) * 3.0:
            return 6
        elif (math.pi / 2.0) * 3.0 < di < math.pi * 2.0:
            return 8
        else:
            return 9

    def check_pdl_my_pos(self):
        pdl_my_top = self.pdl_my.rect.top
        pdl_my_h = self.pdl_my.rect.height
        ball_top = self.ball.rect.top
        ball_h = self.ball.rect.height

        if ball_top > pdl_my_top - ball_h and ball_top < pdl_my_top + pdl_my_h:
            return True
        else:
            return False

    def check_pdl_ai_pos(self):
        #return True  # TODO: after PongPaddleAI

        # NOTE: now we do not have real paddle ai, so we use a temporal
        # method to judge my win: after the ball reach the right side
        # for x times. x -> 1 is very easy 0_.
        self.n_rch_right += 1
        if self.n_rch_right > 1:#5:#
            self.n_rch_right = 0
            return False
        else:
            return True


class PongPaddleAI(object):
    def __init__(self, ball, grnd_pn, pdl_my, pdl_ai):
        self.ball = ball
        self.grnd_pn = grnd_pn
        self.pdl_my = pdl_my
        self.pdl_ai = pdl_ai

        self.e_keys_up = []
        self.e_keys_dn = []

        self.pos_pdl_ai_top_min = self.grnd_pn.rect.top
        self.pos_pdl_ai_top_max = self.grnd_pn.rect.top + \
            self.grnd_pn.rect.height - self.pdl_ai.rect.height

        self.dire = 2  # 0:^ 1:> 2:v 3:<
        self.dire_last = self.dire

        self.speed = 6#2
        self.stopped = True

    def reset(self):
        pass

    def simu_gen_key(self):
        k = random.choice([0, 2])
        self.e_keys_dn = [k]

    def refresh(self, fps_clock, *args, **kwargs):
        self.simu_gen_key()

        self.turn_di(self.e_keys_dn, self.e_keys_up)
        self.move_pdl_ai_pos()

    def turn_di(self, e_keys_dn=[], e_keys_up=[]):
        if len(e_keys_dn) > 0:
            self.dire_last = self.dire
            self.dire = e_keys_dn[-1]  # the last down
            self.stopped = False

        elif len(e_keys_up) > 0:
            if len(e_keys_up) >= len(e_keys_dn):
                self.stopped = True
            elif e_keys_up[-1] == self.dire:
                self.stopped = True
            else:
                pass

    def move_pdl_ai_pos(self):
        if not self.stopped:
            if self.dire == 0:
                #self.pdl_ai.rect.top -= self.speed

                if self.pdl_ai.rect.top > self.pos_pdl_ai_top_min:
                    self.pdl_ai.rect.top -= self.speed
                else:
                    pass

                if self.pdl_ai.rect.top < self.pos_pdl_ai_top_min:
                    self.pdl_ai.rect.top = self.pos_pdl_ai_top_min

            #elif self.dire == 1:
            #    self.pdl_ai.rect.left += self.speed

            elif self.dire == 2:
                #self.pdl_ai.rect.top += self.speed

                if self.pdl_ai.rect.top < self.pos_pdl_ai_top_max:
                    self.pdl_ai.rect.top += self.speed
                else:
                    pass

                if self.pdl_ai.rect.top > self.pos_pdl_ai_top_max:
                    self.pdl_ai.rect.top = self.pos_pdl_ai_top_max

            #elif self.dire == 3:
            #    self.pdl_ai.rect.left -= self.speed


class SptPong(sptdraw.SptDrawBase):
    def __init__(self, cfg={}, *args, **kwargs):
        self.cfg = cfg
        self.bg_size = self.cfg.get('bg_size', (160, 210))

        super(SptPong, self).__init__(self.bg_size)

        # draw myself
        self.fill(consts.WHITE)

        self.grnd_sc_size = self.cfg.get('grnd_sc_size', (160, 24))
        self.grnd_pn_size = self.cfg.get('grnd_pn_size', (160, 160))
        self.ball_size = self.cfg.get('ball_size', (2, 4))
        self.paddle_size = self.cfg.get('paddle_size', (4, 16))

        self.score_my = 0
        self.score_ai = 0

        # draw game UI

        #self.bg = SptGround(self.bg_size, consts.WHITE)
        #self.bg.rect.top = 0
        #self.bg.rect.left = 0
        #self.disp_add(self.bg)

        self.grnd_sc = SptGround(self.grnd_sc_size, COLOR_PONG_GD)
        self.grnd_sc.rect.top = 0
        self.grnd_sc.rect.left = 0
        self.disp_add(self.grnd_sc)

        self.grnd_pn = SptGround(self.grnd_pn_size, COLOR_PONG_GD)
        self.grnd_pn.rect.top = 34
        self.grnd_pn.rect.left = 0
        self.disp_add(self.grnd_pn)

        self.pdl_my = SptPaddle(self.paddle_size, COLOR_PONG_MY)
        self.pdl_my.rect.top = 35
        self.pdl_my.rect.left = 16
        self.disp_add(self.pdl_my)

        self.pdl_ai = SptPaddle(self.paddle_size, COLOR_PONG_AI)
        self.pdl_ai.rect.top = 35
        self.pdl_ai.rect.left = 140
        self.disp_add(self.pdl_ai)

        self.ball = SptBall(self.ball_size)
        self.ball.rect.top = 35
        self.ball.rect.left = 88
        self.disp_add(self.ball)

        self.sc_my = pygm.SptLbl(str(self.score_my), c=COLOR_PONG_MY,
                                 font_size=22)
        self.sc_my.rect.top = 1
        self.sc_my.rect.left = 20
        self.disp_add(self.sc_my)

        self.sc_ai = pygm.SptLbl(str(self.score_my), c=COLOR_PONG_AI,
                                 font_size=22)
        self.sc_ai.rect.top = 1
        self.sc_ai.rect.left = 116
        self.disp_add(self.sc_ai)

        self.ai_pn_pdl = PongPaddleAI(self.ball, self.grnd_pn,
                                      self.pdl_my, self.pdl_ai)

        self.ball_actor = PongBallActor(self.ball, self.grnd_pn,
                                        self.pdl_my, self.pdl_ai)

        self.cnt = 0

        self.e_keys_up = []
        self.e_keys_dn = []

        self.pos_pdl_my_top_min = self.grnd_pn.rect.top
        self.pos_pdl_my_top_max = self.grnd_pn.rect.top + \
            self.grnd_pn.rect.height - self.pdl_my.rect.height

        self.dire = 2  # 0:^ 1:> 2:v 3:<
        self.dire_last = self.dire

        self.speed = 6#2
        self.stopped = True

        self.game_over = False


    def reset(self):
        self.pdl_my.rect.top = 35
        self.pdl_my.rect.left = 16
        self.pdl_ai.rect.top = 35
        self.pdl_ai.rect.left = 140
        self.ball.rect.top = 35
        self.ball.rect.left = 88

        self.e_keys_up = []
        self.e_keys_dn = []

        self.stopped = True

        self.score_my = 0
        self.score_ai = 0

        self.game_over = False

        self.ai_pn_pdl.reset()
        self.ball_actor.reset()


    def handle_event_1(self, events, *args, **kwargs):
        return events

    def refresh_1(self, fps_clock, *args, **kwargs):
        self.cnt += 1

        # for test
        #'''
        if self.cnt == 3:
            self.surf_to_img_file('log/pong_2.png')

            #data = self.surf_to_img_str(fmt='RGB')
            #print len(data)
            #for d in data:
            #    print ord(d)
        #'''


    def key_to_di(self, k):
        if k == self.pglc.K_UP:
            return 0
        #elif k == self.pglc.K_RIGHT:
        #    return 1
        elif k == self.pglc.K_DOWN:
            return 2
        #elif k == self.pglc.K_LEFT:
        #    return 3
        else:
            return None

    def handle_event(self, events, *args, **kwargs):
        #print '>>> ', events
        if not self.flag_check_event:
            return events
        else:
            return self.check_key(events)

    def check_key(self, events):
        #print id(events)
        r_events = []

        e_keys_up = []
        e_keys_dn = []

        for event in events:
            #print event
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
        #x#self.move_pdl_my(self.e_keys_dn, self.e_keys_up)

        #print self.e_keys_dn
        #print self.e_keys_up

        self.turn_di(self.e_keys_dn, self.e_keys_up)
        self.move_pdl_my_pos()

        # TODO: real AI
        #self.ai_pn_pdl.refresh(fps_clock)

        ball_r = self.ball_actor.refresh(fps_clock)
        #print ball_r
        # TODO: <1> reset game; <2> score
        if ball_r == 0:
            pass
        else:

            if ball_r == 1:
                # NOTE: only when i am lost the game over.
                self.game_over = True
                self.score_ai += 1
            elif ball_r == 2:
                self.score_my += 1
            elif ball_r == 9:
                pass

        self.sc_lbl_refresh()

    def sc_lbl_refresh(self):
        self.sc_my.lbl_set(str(self.score_my))
        self.sc_ai.lbl_set(str(self.score_ai))

    def move_pdl_my(self, e_keys_dn=[], e_keys_up=[]):
        #print e_keys_dn
        #print e_keys_up

        if len(e_keys_dn) > 0:
            pass

        elif len(e_keys_up) > 0:
            for k in e_keys_up:
                if k == 0:  # UP
                    if self.pdl_my.rect.top > self.pos_pdl_my_top_min:
                        self.pdl_my.rect.top -= self.speed
                    else:
                        pass

                elif k == 2:  # DOWN
                    if self.pdl_my.rect.top < self.pos_pdl_my_top_max:
                        self.pdl_my.rect.top += self.speed
                    else:
                        pass

                else:
                    pass

    def turn_di(self, e_keys_dn=[], e_keys_up=[]):
        #print e_keys_dn
        #print e_keys_up

        if len(e_keys_dn) > 0:
            self.dire_last = self.dire
            self.dire = e_keys_dn[-1]  # the last down
            self.stopped = False

        elif len(e_keys_up) > 0:
            if len(e_keys_up) >= len(e_keys_dn):
                self.stopped = True
            elif e_keys_up[-1] == self.dire:
                self.stopped = True
            else:
                pass

    def move_pdl_my_pos(self):
        if not self.stopped:
            if self.dire == 0:

                if self.pdl_my.rect.top > self.pos_pdl_my_top_min:
                    self.pdl_my.rect.top -= self.speed
                else:
                    pass

                if self.pdl_my.rect.top < self.pos_pdl_my_top_min:
                    self.pdl_my.rect.top = self.pos_pdl_my_top_min

            #elif self.dire == 1:
            #    self.pdl_my.rect.left += self.speed

            elif self.dire == 2:

                if self.pdl_my.rect.top < self.pos_pdl_my_top_max:
                    self.pdl_my.rect.top += self.speed
                else:
                    pass

                if self.pdl_my.rect.top > self.pos_pdl_my_top_max:
                    self.pdl_my.rect.top = self.pos_pdl_my_top_max

            #elif self.dire == 3:
            #    self.pdl_my.rect.left -= self.speed


class SceneA(pygm.PyGMScene):
    def __init__(self, *args, **kwargs):
        super(SceneA, self).__init__(*args, **kwargs)

        self.pong = SptPong()
        self.pong.rect.top = 0
        self.pong.rect.left = 0
        self.disp_add(self.pong)

        self.lb1 = pygm.SptLbl('hello,', c=consts.GREEN, font_size=32)
        self.lb1.rect.top = 300
        self.lb1.rect.left = 100
        self.disp_add(self.lb1)

        self.cnt = 0

    def handle_event(self, events, *args, **kwargs):
        return events

    def refresh(self, fps_clock, *args, **kwargs):
        self.cnt += 1

        #if self.pong.game_over:
        #    self.pong.reset()


class GMPong(pygm.PyGMGame):
    def __init__(self, title, winw, winh, *args, **kwargs):
        super(GMPong, self).__init__(title, winw, winh)

        bk_im = utils.dir_abs('starfish/data/img_bk_1.jpg', __file__)
        #print bk_im
        #self.bk = pygm.SptImg('data/img_bk_1.jpg')
        self.bk = pygm.SptImg(bk_im)
        self.bk.rect.top = -230
        self.bk.rect.left = -230
        self.disp_add(self.bk)

        self.scn1 = SceneA()
        self.disp_add(self.scn1)

        self.cnt = 0

        self.pong = self.scn1.pong

        # for gym
        # if run game in gym, do not check events
        simu = kwargs.get('simu', False)
        if simu:
            self.do_not_check_event()
            self.pong.do_not_check_event()

    def refresh(self, fps_clock, *args, **kwargs):
        self.cnt += 1

        # for test
        '''
        if self.cnt == 3:
            rct = [0, 0, 160, 210]
            self.surf_main_to_img_file('log/pong_3.png', rect=rct)
        '''

    # #### for gym

    _action_set = ['UP', 'NOP', 'DOWN']

    def action_idx(self, action):
        try:
            i = self._action_set.index(action)
        except:
            i = None
        return i

    def getMinimalActionSet(self):
        return self._action_set

    def getScreenDims(self):
        return (160, 210)

    def act(self, action):
        reward = self.pong.score_my

        # do action
        a = self.action_idx(action)
        #self.pong.dire = a  # 0 / 1 / 2
        #self.pong.e_keys_dn.append(a)
        ##self.pong.e_keys_up.append(a)
        self.pong.e_keys_dn = [a]
        ##self.pong.e_keys_up = [a]

        self.step()

        reward = self.pong.score_my - reward
        reward = reward - self.pong.score_ai

        return reward

    def reset_game(self):
        print '===> reset'
        self.pong.reset()

    def game_over(self):
        return self.pong.game_over

    def get_scrn_rgb(self):
        #self.pong.surf_to_img_file('log/pong_2.png')

        a = []

        # <1>
        #data = self.pong.surf_to_img_str(fmt='RGB')

        # <2>
        rct = [0, 0, 160, 210]
        data = self.surf_main_to_img_str(fmt='RGB', rect=rct)

        #print len(data)
        for d in data:
            #print ord(d)
            a.append(ord(d))

        return a

    def getScreenRGB(self, arr):
        a = self.get_scrn_rgb()
        return a

    def getRAM(self, ram):
        a = self.get_scrn_rgb()
        return a


def main():
    sf = GMPong('Pong', 800, 550)
    sf.mainloop()


if __name__ == '__main__':
    main()
