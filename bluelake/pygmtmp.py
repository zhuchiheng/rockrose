"""
"""

import random

from starfish import pygm
from starfish import consts
from starfish import sptdraw
from starfish import utils


class SptTmpx(sptdraw.SptDrawBase):
    def __init__(self, size, *args, **kwargs):
        super(SptTmpx, self).__init__(size)

        self.draw_on()

    def draw_on(self, *args, **kwargs):
        self.fill(consts.GREEN)
        self.pygm.draw.circle(self.surf, consts.WHITE,
                              (self.size[0] / 2, self.size[1] / 2),
                              self.size[0] / 2, 0)


class SptTmpi(pygm.SptImg):
    def __init__(self, img_file, *args, **kwargs):
        super(SptTmpi, self).__init__(img_file)


class SptA(pygm.PyGMSprite):
    disp_type = 'spt_a'

    def __init__(self, img_file=None, *args, **kwargs):
        super(SptA, self).__init__(*args, **kwargs)


class SceneTmpx(pygm.PyGMScene):
    def __init__(self, *args, **kwargs):
        super(SceneTmpx, self).__init__(*args, **kwargs)

        self.sn1 = SptTmpx((200, 200))
        self.sn1.rect.top = 100
        self.sn1.rect.left = 100
        self.disp_add(self.sn1)

        self.im1 = SptTmpi('data/bl2.png')
        self.im1.rect.top = 100
        self.im1.rect.left = 100
        self.disp_add(self.im1)

        self.lb1 = pygm.SptLbl('<*)))><', c=consts.GREEN, font_size=32)
        self.lb1.rect.top = 300
        self.lb1.rect.left = 100
        self.disp_add(self.lb1)

        self.e_keys_up = []
        self.e_keys_dn = []

        self.e_keys_up_last = []
        self.e_keys_dn_last = []

        self.di = -1

    def key_to_di(self, k):
        if k == self.pglc.K_UP:
            return 0
        elif k == self.pglc.K_RIGHT:
            return 1
        elif k == self.pglc.K_DOWN:
            return 2
        elif k == self.pglc.K_LEFT:
            return 3
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

        self.e_keys_up_last = self.e_keys_up
        self.e_keys_dn_last = self.e_keys_dn

        self.e_keys_up = e_keys_up
        self.e_keys_dn = e_keys_dn

        return r_events

    def refresh(self, fps_clock, *args, **kwargs):
        #print self.e_keys_dn
        #print self.e_keys_up

        self.turn_di()

        self.move_me()

    def turn_di(self):
        for k in self.e_keys_dn_last:
            if k not in self.e_keys_up:
                self.e_keys_dn.append(k)

        if len(self.e_keys_dn) > 0:
            self.di = self.e_keys_dn[-1]
        else:
            self.di = None

    def move_me(self):
        if self.di == 0:
            self.im1.rect.top -= 2
        elif self.di == 1:
            self.im1.rect.left += 2
        elif self.di == 2:
            self.im1.rect.top += 2
        elif self.di == 3:
            self.im1.rect.left -= 2


class GMTmpx(pygm.PyGMGame):
    def __init__(self, title, winw, winh, *args, **kwargs):
        super(GMTmpx, self).__init__(title, winw, winh)

        #bk_im = utils.dir_abs('data/img_bk_1.jpg', __file__)
        #self.bk = pygm.SptImg(bk_im)
        self.bk = pygm.SptImg('data/img_bk_1.jpg')
        self.bk.rect.top = -230
        self.bk.rect.left = -230
        self.disp_add(self.bk)

        self.scn1 = SceneTmpx()
        self.disp_add(self.scn1)


def main():
    sf = GMTmpx('<*)))><', 800, 550)
    sf.mainloop()


if __name__ == '__main__':
    main()
