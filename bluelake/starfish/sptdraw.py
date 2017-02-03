"""
Bluelake Drawable Base.
"""

import math
import random

from . import pygm
from . import consts


class SptDrawBase(pygm.PyGMSprite):

    disp_type = 'drawbase'

    def __init__(self, size=(0, 0), *args, **kwargs):
        super(SptDrawBase, self).__init__()

        self.size = size

        self.surf = self.pygm.Surface(self.size,
            flags=self.pglc.SRCALPHA, depth=32)

        self.disp_add(self.surf)

        self.rect = self.surf.get_rect()

        #self.draw_on()

    def fill(self, c):
        self.surf.fill(c)

    def clear(self):
        c = (255, 255, 255, 0)
        self.surf.fill(c)

    def draw_on(self, *args, **kwargs):
        pass

    def surf_to_img_str(self, fmt='RGBA'):
        data = self.pygm.image.tostring(self.surf, fmt)
        return data

    def surf_to_img_file(self, to):
        """
        NOTE: here we can use StringIO
            from StringIO import StringIO
            to = StringIO()
            spt.to_img_file(to)
            print to.getvalue()
        """
        self.pygm.image.save(self.surf, to)

    def surf_from_img_buf(self, string, size, fmt='RGBA'):
        surf = self.pygm.image.frombuffer(string, size, fmt)
        self.disp_del(self.surf)
        self.surf = surf
        self.disp_add(self.surf)
        self.rect = self.surf.get_rect()
        return self.surf

    def surf_from_img_str(self, string, size, format='RGBA', flipped=False):
        surf = self.pygm.image.fromstring(string, size, fmt, flipped=flipped)
        self.disp_del(self.surf)
        self.surf = surf
        self.disp_add(self.surf)
        self.rect = self.surf.get_rect()
        return self.surf


# TODO:
class SptDrawMaskBase(pygm.PyGMSprite):
    def __init__(self, size=(0, 0), msk_size=None, *args, **kwargs):
        super(SptDrawMaskBase, self).__init__()

        self.size = size

        if msk_size is None:
            self.msk_size = self.size
        else:
            self.msk_size = msk_size

        self.msk = self.pygm.Mask(self.msk_size)

        self.surf = self.pygm.Surface(self.size,
            flags=self.pglc.SRCALPHA, depth=32)#,
            # ValueError: masks argument must be sequence of four numbers
            #masks=self.msk)

        self.disp_add(self.surf)

        self.rect = self.surf.get_rect()

        #.draw_on()

    def fill(self, c):
        self.surf.fill(c)

    def draw_on(self, *args, **kwargs):
        pass


class SptDrawFunc(SptDrawBase):
    def __init__(self, size, f, x_range=(0, 100), line_width=1,
                 *args, **kwargs):
        super(SptDrawFunc, self).__init__(size)

        self.f = f
        self.x_range = x_range
        self.line_width = line_width

        self.scale = 1

        self.draw_on()

    def draw_on(self, *args, **kwargs):

        #self.pygm.draw.circle(self.surf, consts.WHITE,
        #                      (self.size[0] / 2, self.size[1] / 2),
        #                      self.size[0] / 2, 0)

        xs = range(self.x_range[0], self.x_range[1], 1)
        ys = [self.f(x) for x in xs]

        self.scale = (1.0 * self.size[1]) / max(ys)

        #xs = [x / self.scale for x in xs]
        ys = [y * self.scale for y in ys]

        for i in range(len(xs) - 1):
            self.pygm.draw.line(self.surf, consts.GREEN,
                                (xs[i], ys[i]), (xs[i + 1], ys[i + 1]),
                                self.line_width)
