"""
Multi-theads and pygame template.
"""

import random
import math
import time

import Queue

import pygm
import consts

import multithrd
import snowspt
import sptdraw


class ThrdTime(multithrd.PgThrd):
    def __init__(self, q=None):
        super(ThrdTime, self).__init__(q)

        self.t_last = None

    def do_once(self):
        t = int(time.time())
        if t % 2 == 0 and t != self.t_last:
            #print t
            self.q.put(t)
            self.t_last = t


class MTScene(pygm.PyGMScene):
    def __init__(self, q, *args, **kwargs):
        super(MTScene, self).__init__(*args, **kwargs)

        self.q = q

        self.lb1 = pygm.SptLbl(0, c=consts.WHITE)
        self.lb1.rect.top = 460
        self.lb1.rect.left = 60
        self.disp_add(self.lb1)

        self.sn1 = snowspt.SptSnow((800, 550), 100)
        self.disp_add(self.sn1)


        def f(x):
            #return x ** 3 + x ** 2 + x
            #return x ** 2 + x
            return (x / 2.0) * math.sin(x / 100.0) + 200.0
        self.drfn1 = sptdraw.SptDrawFunc((400, 400), f, (0, 400), 6)
        self.disp_add(self.drfn1)

    def refresh(self, fps_clock, *args, **kwargs):
        if not self.q.empty():  # or use self.q.get_nowait()
            t = self.q.get()
            #print t
            if t:
                self.lb1.lbl_set(t)


class GMMultithrd(pygm.PyGMGame):
    def __init__(self, title, winw, winh, *args, **kwargs):
        super(GMMultithrd, self).__init__(title, winw, winh)

        self.bk = pygm.SptImg('data/img_bk_1.jpg')
        self.bk.rect.top = -230
        self.disp_add(self.bk)

        self.q = Queue.Queue()

        self.scn1 = MTScene(self.q)
        self.disp_add(self.scn1)

        # add a time thread
        self.thrd_tm = ThrdTime(self.q)
        self.thrd_add(self.thrd_tm)
        self.thrd_tm.start()


def main():
    lk = GMMultithrd('Mulit Thrd', 800, 550)
    lk.mainloop()


if __name__ == '__main__':
    main()
