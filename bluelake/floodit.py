"""
"""

import random

from bluelake.starfish import pygm
from bluelake.starfish import consts
from bluelake.starfish import sptdraw
from bluelake.starfish import utils


FI_BLOCK_COLORS = [
    consts.BLUE,
    consts.RED,
    consts.GREEN,
    consts.YELLOW,
    consts.GRAY,
    consts.DEEP_RED,
]


class FISptBlock(sptdraw.SptDrawBase):
    def __init__(self, size, blk_clr=consts.GREEN, *args, **kwargs):
        super(FISptBlock, self).__init__(size)

        self.blk_clr = blk_clr

        self.draw_on()

    def draw_on(self, *args, **kwargs):
        self.fill(self.blk_clr)
        #self.pygm.draw.circle(self.surf, consts.WHITE,
        #                      (self.size[0] / 2, self.size[1] / 2),
        #                      self.size[0] / 2, 0)

    def change_color(self, clr):
        self.blk_clr = clr
        self.fill(self.blk_clr)


class FISptImgi(pygm.SptImg):
    def __init__(self, img_file, *args, **kwargs):
        super(FISptImgi, self).__init__(img_file)


class FISptBlkFlag(pygm.PyGMSprite):
    def __init__(self, blk_size=(), blk_cn=len(FI_BLOCK_COLORS),
                 *args, **kwargs):
        super(FISptBlkFlag, self).__init__(*args, **kwargs)

        self.blk_size = blk_size
        self.blk_cn = blk_cn

        self.blks = []
        self.lbls = []

        self.rct_top = 10
        self.rct_left = 200

        self.init_board_flag()

    def init_board_flag(self):
        for i in range(self.blk_cn):
            c = i
            blk = FISptBlock(self.blk_size, self.blk_color_by_idx(c))
            self.blks.append(blk)

            self.disp_add(blk)
            blk.rect.top = self.rct_top + 20
            blk.rect.left = self.rct_left + self.blk_size[0] * i * 2

            lb1 = pygm.SptLbl(str(i + 1), c=consts.GREEN, font_size=12)
            self.lbls.append(lb1)
            lb1.rect.top = self.rct_top
            lb1.rect.left = self.rct_left + self.blk_size[0] * i * 2 + 8
            self.disp_add(lb1)

    def blk_color_by_idx(self, idx):
        return FI_BLOCK_COLORS[idx]


class FISptBoard(pygm.PyGMSprite):
    def __init__(self, brd_size=(), blk_size=(), blk_cn=6, *args, **kwargs):
        super(FISptBoard, self).__init__(*args, **kwargs)

        self.auto_reset = True

        self.brd_size = brd_size
        self.blk_size = blk_size

        self.blk_cn = blk_cn

        self.rct_top = 90
        self.rct_left = 200

        self.col_n = int(self.brd_size[0] / self.blk_size[0])
        self.row_n = int(self.brd_size[1] / self.blk_size[1])

        self.blk_colors = []
        for i in range(self.row_n):
            a = [-1 for j in range(self.col_n)]
            self.blk_colors.append(a)

        self.brd_blocks = []

        self.init_board()

        self.reset_board()

    def reset_board(self):

        self.init_blk_colors_rand()

        self.reset_blks_color()

        self.flood_color = self.blk_colors[0][0]
        self.flood_color_last = self.flood_color

        # for check board
        self.chk_blk_clrs_first = True
        self.chk_blk_cache = []

        self.do_cnt = 0

        self.blk_fi_n = 0
        self.blk_fi_n_last = self.blk_fi_n

        self.all_ok = False

    def init_board(self):
        for i in range(self.row_n):
            b = []
            for j in range(self.col_n):
                c = 0
                blk = FISptBlock(self.blk_size, self.blk_color_by_idx(c))
                b.append(blk)
                self.blk_colors[i][j] = c

                self.disp_add(blk)
                blk.rect.top = self.rct_top + self.blk_size[1] * i
                blk.rect.left = self.rct_left + self.blk_size[0] * j

            self.brd_blocks.append(b)

    def blk_color_by_idx(self, idx):
        return FI_BLOCK_COLORS[idx]

    def init_blk_colors_rand(self):
        for i in range(self.row_n):
            for j in range(self.col_n):
                self.blk_colors[i][j] = random.randint(0, self.blk_cn - 1)

    def reset_blks_color(self):
        for i in range(self.row_n):
            for j in range(self.col_n):
                c = self.blk_colors[i][j]
                self.brd_blocks[i][j].change_color(self.blk_color_by_idx(c))

    def check_board(self, c):
        self.do_cnt += 1

        self.flood_color_last = self.flood_color
        self.flood_color = c

        if self.chk_blk_clrs_first:
            # the first block
            self.blk_colors[0][0] = self.flood_color
            self.brd_blocks[0][0].change_color(self.blk_color_by_idx(c))

            self.chk_blk_clrs_first = False

            self.blk_fi_n_last = self.blk_fi_n
            self.blk_fi_n = 1
        else:
            self.chk_blk_cache = []
            self.check_board_recu(bgn=(0, 0))

            #self.blk_fi_n = len(self.chk_blk_cache)

        self.blk_fi_n_last = self.blk_fi_n
        self.blk_fi_n = 0
        self.chk_blk_cache = []
        self.check_blk_fldd_recu(bgn=(0, 0))

        #print '=' * 20, self.blk_fi_n, self.blk_fi_n_last
        #print '=' * 20, self.blk_fi_n - self.blk_fi_n_last

        if self.blk_fi_n == self.row_n * self.col_n:
        #if self.chk_all_flooded():
            self.all_ok = True

            # for test
            if self.auto_reset:
                self.reset_board()

    def check_board_recu(self, bgn=(0, 0)):
        #print bgn

        i = bgn[0]
        j = bgn[1]

        if 0 <= i < self.row_n and 0 <= j < self.col_n and (i, j) not in self.chk_blk_cache:
            #x#if self.blk_colors[i][j] in [self.flood_color_last, self.flood_color]:
            if self.blk_colors[i][j] == self.flood_color_last:
                self.blk_change_color(i, j, self.flood_color)
            else:
                return

            if 0 <= i - 1 < self.row_n and 0 <= j < self.col_n and (i - 1, j) not in self.chk_blk_cache:
                self.check_board_recu(bgn=(i - 1, j))
            if 0 <= i + 1 < self.row_n and 0 <= j < self.col_n and (i + 1, j) not in self.chk_blk_cache:
                self.check_board_recu(bgn=(i + 1, j))
            if 0 <= i < self.row_n and 0 <= j - 1 < self.col_n and (i, j - 1) not in self.chk_blk_cache:
                self.check_board_recu(bgn=(i, j - 1))
            if 0 <= i < self.row_n and 0 <= j + 1 < self.col_n and (i, j + 1) not in self.chk_blk_cache:
                self.check_board_recu(bgn=(i, j + 1))

    def blk_change_color(self, i, j, c=None):
        #print '=' * 20, i, j
        self.blk_colors[i][j] = c
        self.brd_blocks[i][j].change_color(self.blk_color_by_idx(c))
        self.chk_blk_cache.append((i, j))

    def check_blk_fldd_recu(self, bgn=(0, 0)):
        #print bgn

        i = bgn[0]
        j = bgn[1]

        if 0 <= i < self.row_n and 0 <= j < self.col_n and (i, j) not in self.chk_blk_cache:
            if self.blk_colors[i][j] == self.flood_color:
                self.chk_blk_cache.append((i, j))
                self.blk_fi_n += 1
            else:
                return

            if 0 <= i - 1 < self.row_n and 0 <= j < self.col_n and (i - 1, j) not in self.chk_blk_cache:
                self.check_blk_fldd_recu(bgn=(i - 1, j))
            if 0 <= i + 1 < self.row_n and 0 <= j < self.col_n and (i + 1, j) not in self.chk_blk_cache:
                self.check_blk_fldd_recu(bgn=(i + 1, j))
            if 0 <= i < self.row_n and 0 <= j - 1 < self.col_n and (i, j - 1) not in self.chk_blk_cache:
                self.check_blk_fldd_recu(bgn=(i, j - 1))
            if 0 <= i < self.row_n and 0 <= j + 1 < self.col_n and (i, j + 1) not in self.chk_blk_cache:
                self.check_blk_fldd_recu(bgn=(i, j + 1))

    def chk_all_flooded(self):
        for i in range(self.row_n):
            for j in range(self.col_n):
                if self.blk_colors[i][j] != self.flood_color:
                    return False
        return True


class FISceneA(pygm.PyGMScene):
    def __init__(self, blk_n=14, blk_w=30, blk_cn=6, *args, **kwargs):
        super(FISceneA, self).__init__(*args, **kwargs)

        self.blk_n = blk_n
        self.blk_w = blk_w
        self.blk_cn = blk_cn

        self.fibrd = FISptBoard((self.blk_w * self.blk_n,
                                 self.blk_w * self.blk_n),
                                (self.blk_w, self.blk_w),
                                blk_cn=self.blk_cn)
        self.fibrd.rect.top = 0
        self.fibrd.rect.left = 0
        self.disp_add(self.fibrd)

        self.blkflg = FISptBlkFlag((30, 30), blk_cn=self.blk_cn)
        self.blkflg.rect.top = 0
        self.blkflg.rect.left = 0
        self.disp_add(self.blkflg)

        self.im1 = FISptImgi('data/bl2.png')
        self.im1.rect.top = 100
        self.im1.rect.left = 60
        self.disp_add(self.im1)

        self.bd_do_cnt = self.fibrd.do_cnt

        self.lb1 = pygm.SptLbl(str(self.bd_do_cnt), c=consts.GREEN, font_size=32)
        self.lb1.rect.top = 130
        self.lb1.rect.left = 100
        self.disp_add(self.lb1)

        self.e_keys_up = []
        self.e_keys_dn = []

        self.e_keys_up_last = []
        self.e_keys_dn_last = []

        self.di = -1

    def key_to_di__1(self, k):
        if k == self.pglc.K_1:
            return 0
        elif k == self.pglc.K_2:
            return 1
        elif k == self.pglc.K_3:
            return 2
        elif k == self.pglc.K_4:
            return 3
        elif k == self.pglc.K_5:
            return 4
        elif k == self.pglc.K_6:
            return 5
        else:
            return None

    def key_to_di(self, k):
        if self.pglc.K_1 <= k <= self.pglc.K_1 + self.blk_cn - 1:
            return k - self.pglc.K_1
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
        #print 'x' * 60, self.e_keys_up

        self.check_board()

        self.check_lbls()

    def check_board(self):
        if len(self.e_keys_up) > 0:
            self.di = self.e_keys_up[-1]
            #print '>' * 60, self.di

            self.fibrd.check_board(self.di)

    def check_lbls(self):
        bd_do_cnt = self.fibrd.do_cnt
        if bd_do_cnt != self.bd_do_cnt:
            self.bd_do_cnt = bd_do_cnt
            self.lb1.lbl_set(str(self.bd_do_cnt))


class GMFloodIt(pygm.PyGMGame):
    def __init__(self, title, winw, winh, blk_n=10, blk_w=30,
                 blk_cn=len(FI_BLOCK_COLORS), *args, **kwargs):
        super(GMFloodIt, self).__init__(title, winw, winh)

        bk_im = utils.dir_abs('data/img_bk_1.jpg', __file__)
        self.bk = pygm.SptImg(bk_im)
        self.bk.rect.top = -230
        self.bk.rect.left = -230
        self.disp_add(self.bk)

        self.blk_n = blk_n
        self.blk_w = blk_w
        self.blk_cn = blk_cn

        self.scn1 = FISceneA(blk_n=self.blk_n,
                             blk_w=self.blk_w,
                             blk_cn=self.blk_cn)
        self.disp_add(self.scn1)


def main():
    sf = GMFloodIt('FloodIt', 800, 550)
    #sf = GMFloodIt('FloodIt', 800, 550, blk_n=4, blk_cn=3)
    sf.mainloop()


if __name__ == '__main__':
    main()
