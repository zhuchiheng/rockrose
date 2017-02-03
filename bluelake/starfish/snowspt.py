"""
"""

import random

import pygm
import consts


class SptSnowFlake(pygm.PyGMSprite):
    def __init__(self, size, *args, **kwargs):
        super(SptSnowFlake, self).__init__()

        self.size = size

        #self.surf = self.pygm.Surface(self.size)
        self.surf = self.pygm.Surface(self.size,
            flags=self.pglc.SRCALPHA, depth=32)

        #self.surf.set_alpha(160)#0.9)
        #self.surf.fill((255, 255, 255, 128))
        #self.surf = self.surf.convert_alpha()

        self.pygm.draw.circle(self.surf, consts.WHITE,
                              (self.size[0] / 2, self.size[1] / 2),
                              self.size[0] / 2, 0)

        self.disp_add(self.surf)

        self.rect = self.surf.get_rect()


class SptSnow(pygm.PyGMSprite):
    def __init__(self, size, n, *args, **kwargs):
        super(SptSnow, self).__init__()

        self.size = size
        self.n = n

        self.sns_sz = []
        self.sns = []

        self.init(self.n)

    def init(self, n):
        #snfk1 = SptSnowFlake((20, 20))
        #snfk1.rect.top = 100
        #snfk1.rect.left = 200
        #self.disp_add(snfk1)

        sns_sz_tmp = []

        for i in range(n):
            #hw = random.randint(6, 20)
            hw = random.randint(4, 18)
            self.sns_sz.append(hw)
            sns_sz_tmp.append(hw)

        #for i in self.sns_sz:
        for i in sns_sz_tmp:  # only the new ones
            snfk = SptSnowFlake((i, i))
            snfk.rect.top = random.randint(0, 500)
            snfk.rect.left = random.randint(2, 800)
            self.sns.append(snfk)
            self.disp_add(snfk)

    def refresh(self, fps_clock, *args, **kwargs):
        for snfk in self.sns:
            if snfk.rect.top < 550:
                snfk.rect.top += self.get_speed_by_size(snfk.size[0])
                snfk.rect.left += random.randint(-2, 2)
            else:
                snfk.rect.top = random.randint(-30, -10)
                snfk.rect.left = random.randint(2, 800)

    def get_speed_by_size(self, sz):
        spd = sz / 4
        return spd


class SNScene(pygm.PyGMScene):
    def __init__(self, *args, **kwargs):
        super(SNScene, self).__init__(*args, **kwargs)

        self.sn1 = SptSnow((800, 550), 300)
        self.disp_add(self.sn1)

    def refresh(self, fps_clock, *args, **kwargs):
        pass


class GMSnowSpt(pygm.PyGMGame):
    def __init__(self, title, winw, winh, *args, **kwargs):
        super(GMSnowSpt, self).__init__(title, winw, winh)

        #self.bk = SptImg('data/img_snow_2.jpg')
        self.bk = pygm.SptImg('data/img_bk_1.jpg')
        self.bk.rect.top = -230
        self.disp_add(self.bk)

        self.scn1 = SNScene()
        self.disp_add(self.scn1)


def main():
    lk = GMSnowSpt('snowspt', 800, 550)
    lk.mainloop()


if __name__ == '__main__':
    main()
