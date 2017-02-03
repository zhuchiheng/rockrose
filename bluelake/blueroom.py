"""
Robot Lives in a Lake
"""

import random

from starfish import pygm
from starfish import consts
from starfish import sptdraw
from starfish import utils


# robot mixin

class MxnRobotBase(object):
    pass


class MxnRobotA(MxnRobotBase):
    pass


# robot sprite

class SptRobotA(sptdraw.SptDrawBase, MxnRobotA):
    def __init__(self, size, *args, **kwargs):
        super(SptRobotA, self).__init__(size)

        self.draw_on()

    def draw_on(self, *args, **kwargs):
        self.fill(consts.GREEN)
        self.pygm.draw.circle(self.surf, consts.YELLOW,
                              (self.size[0] / 2, self.size[1] / 2),
                              self.size[0] / 2, 0)


class SptRobotO(pygm.SptImg, MxnRobotA):
    def __init__(self, img_file, *args, **kwargs):
        super(SptRobotO, self).__init__(img_file)


# environment

class SptEnvBase(pygm.PyGMSprite):
    def __init__(self, cfg=None, *args, **kwargs):
        super(SptEnvBase, self).__init__(*args, **kwargs)
        self.cfg = cfg

    def scan_at(self, at_pos, radis=0, cond=None):
        pass  # TODO:


class SptEnvBgA(sptdraw.SptDrawBase):
    def __init__(self, size, walls, *args, **kwargs):
        super(SptEnvBgA, self).__init__(size)

        self.walls = walls

        self.line_width = 4

        self.draw_on()

    def draw_on(self, *args, **kwargs):
        self.fill(consts.WHITE)

        self.draw_walls()

    def draw_walls(self):
        print self.walls
        for wall in self.walls:
            if len(wall) < 1:
                continue
            elif len(wall) == 1:
                p = wall[0]
                self.pygm.draw.circle(self.surf, consts.BLUE,
                                      (p[0], p[1]),
                                      self.line_width, 0)
            else:
                for i in range(len(wall) - 1):
                    p1 = wall[i]
                    p2 = wall[i + 1]
                    self.pygm.draw.line(self.surf, consts.BLUE,
                                        (p1[0], p1[1]), (p2[0], p2[1]),
                                        self.line_width)


class SptEnvCmpWall(sptdraw.SptDrawBase):
    def __init__(self, wall, *args, **kwargs):
        self.wall = wall
        size = self.wall_to_size(self.wall)
        super(SptEnvCmpWall, self).__init__(size)

        self.draw_on()

    def wall_to_size(self, wall=None):
        if wall is None:
            wall = self.wall
        # TODO:

    def draw_on(self, *args, **kwargs):
        #self.fill(consts.WHITE)
        self.draw_wall()

    def draw_wall(self):
            self.pygm.draw.line(self.surf, consts.GREEN,
                                (xs[i], ys[i]), (xs[i + 1], ys[i + 1]),
                                self.line_width)


class SptEnvAWalls(SptEnvBase):
    def __init__(self, cfg=None, *args, **kwargs):
        super(SptEnvAWalls, self).__init__(cfg, *args, **kwargs)

        self.bg_size = self.cfg.get('bg_size', (0, 0))
        self.walls = self.cfg.get('walls', [])

        self.init()

    def init(self):
        self.init_bg()
        self.init_walls()

    def init_bg(self):
        self.bg = SptEnvBgA(self.bg_size, self.walls)
        self.disp_add(self.bg)

    def init_walls(self):
        pass


# scene

class BLSceneA(pygm.PyGMScene):
    def __init__(self, *args, **kwargs):
        super(BLSceneA, self).__init__(*args, **kwargs)

        self.env_cfg_a = {
            'bg_size': (600, 550),
            'walls': [((10, 10), (10, 100)),
                      ((10, 110), (200, 110)),
                      self.make_wall_rand(n=3, bg_size=(600, 550)),
                      self.make_wall_rand(n=4, bg_size=(600, 550)),],
        }

        self.env1 = SptEnvAWalls(self.env_cfg_a)
        self.env1.rect.top = 0
        self.env1.rect.left = 0
        self.disp_add(self.env1)

        self.rb1 = SptRobotA((30, 30))
        self.rb1.rect.top = 100
        self.rb1.rect.left = 100
        self.disp_add(self.rb1)

    def init__1(self):
        self.im1 = SptRobotO('data/Star.png')
        self.im1.rect.top = 100
        self.im1.rect.left = 100
        self.disp_add(self.im1)

        self.lb1 = pygm.SptLbl('hello,', c=consts.GREEN, font_size=32)
        self.lb1.rect.top = 200
        self.lb1.rect.left = 100
        self.disp_add(self.lb1)

    def make_wall_rand(self, n=None, bg_size=None):
        if n is None:
            n = random.randint(3, 8)

        if bg_size is None:
            bg_size = (800, 600)

        wall = []
        for i in range(n):
            wall.append((random.randint(1, bg_size[0]),
                         random.randint(1, bg_size[1])))
        return wall

    def handle_event(self, events, *args, **kwargs):
        return events

    def refresh(self, fps_clock, *args, **kwargs):
        pass


class GMBlueLakeA(pygm.PyGMGame):
    def __init__(self, title, winw, winh, *args, **kwargs):
        super(GMBlueLakeA, self).__init__(title, winw, winh)

        bk_im = utils.dir_abs('data/img_bk_1.jpg', __file__)
        #print bk_im

        #self.bk = SptImg('data/img_snow_2.jpg')
        self.bk = pygm.SptImg('data/img_bk_1.jpg')
        self.bk.rect.top = -230
        self.bk.rect.left = -230
        self.disp_add(self.bk)

        self.scn1 = BLSceneA()
        self.disp_add(self.scn1)


def main():
    sf = GMBlueLakeA('Blue Room A', 800, 550)
    sf.mainloop()


if __name__ == '__main__':
    main()
