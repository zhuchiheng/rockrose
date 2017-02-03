"""
"""

import random
import copy

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


class OMSptPiece(pygm.SptImgOne):
    def __init__(self, img_file, pos, pcid, *args, **kwargs):
        super(OMSptPiece, self).__init__(img_file, pos)

        self.pcid = pcid

        self.pcid_now = pcid
        self.pos_now = pos


class OMSptBoard(pygm.PyGMSprite):
    disp_type = 'spt_om_board'

    def __init__(self, bd_img=None, pc_size=[64, 64],
                 row_n=4, col_n=6, *args, **kwargs):
        super(OMSptBoard, self).__init__(*args, **kwargs)

        self.bd_img = bd_img
        self.pc_size = pc_size
        self.row_n = row_n
        self.col_n = col_n

        self.pcs = {}#[]

        self.e_keys_up = []
        self.e_keys_dn = []

        self.e_keys_up_last = []
        self.e_keys_dn_last = []

        self.di = -1

        self.bd_init()

    def bd_init(self):
        self.pc_poses = self.get_pc_poses()

        pcids = []

        for pos in self.pc_poses:
            pcids.append(pos[0])
            pc = OMSptPiece(self.bd_img, pos[1], pos[0])
            self.pcs[pos[0]] = pc

        self.pcid_open = random.choice(pcids)

        pc_poses_rand = copy.deepcopy(self.pc_poses)
        random.shuffle(pc_poses_rand)

        for pc in self.pcs.values():
            pcpr = pc_poses_rand.pop(0)
            pc.pcid_now = pcpr[0]
            pc.pos_now = pcpr[1]

            if pc.pcid == self.pcid_open:
                self.pc_open = pc
                continue

            self.disp_add(pc)
            pc.rect.top = pc.pos_now['y']
            pc.rect.left = pc.pos_now['x']

    def get_pc_poses(self):
        poses = []
        for i in range(self.row_n):
            for j in range(self.col_n):
                pos = {'x': j * self.pc_size[0],
                       'y': i * self.pc_size[1],
                       'w': self.pc_size[0],
                       'h': self.pc_size[1]}
                poses.append([(i, j), pos])  # pcid, pos
        return poses

    def find_pc_by_pcid_now(self, pcid_now):
        for pc in self.pcs.values():
            if pc.pcid_now == pcid_now:
                return pc


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

        #self.turn_di()

        self.check_move()

    def turn_di(self):
        for k in self.e_keys_dn_last:
            if k not in self.e_keys_up:
                self.e_keys_dn.append(k)

        if len(self.e_keys_dn) > 0:
            self.di = self.e_keys_dn[-1]
        else:
            self.di = 0

    def check_move(self):

        if len(self.e_keys_up) > 0:
            mv = self.e_keys_up[-1]
        else:
            return

        pcid_now_open = self.pc_open.pcid_now
        i, j = pcid_now_open

        if mv == 0:
            if i == self.row_n - 1:
                return
            else:
                i += 1
        elif mv == 2:
            if i == 0:
                return
            else:
                i -= 1
        elif mv == 1:
            if j == 0:
                return
            else:
                j -= 1
        elif mv == 3:
            if j == self.col_n - 1:
                return
            else:
                j += 1
        else:
            pass

        pc2 = self.find_pc_by_pcid_now((i, j))

        # exchange the pos and pcid

        pos_now_open = self.pc_open.pos_now

        self.pc_open.pos_now = pc2.pos_now
        self.pc_open.pcid_now = pc2.pcid_now

        pc2.pos_now = pos_now_open
        pc2.pcid_now = pcid_now_open

        pc2.rect.top = pc2.pos_now['y']
        pc2.rect.left = pc2.pos_now['x']


class OMSceneA(pygm.PyGMScene):
    def __init__(self, *args, **kwargs):
        super(OMSceneA, self).__init__(*args, **kwargs)

        self.bd = OMSptBoard('data/img_snow_1.jpg')
        self.bd.rect.top = 0
        self.bd.rect.left = 0
        self.disp_add(self.bd)

        self.im1 = SptTmpi('data/bl2.png')
        self.im1.rect.top = 400
        self.im1.rect.left = 100
        self.disp_add(self.im1)

        self.lb1 = pygm.SptLbl('hello,', c=consts.GREEN, font_size=32)
        self.lb1.rect.top = 500
        self.lb1.rect.left = 100
        self.disp_add(self.lb1)


class GMOpenmove(pygm.PyGMGame):
    def __init__(self, title, winw, winh, *args, **kwargs):
        super(GMOpenmove, self).__init__(title, winw, winh)

        #bk_im = utils.dir_abs('data/img_bk_1.jpg', __file__)
        #self.bk = pygm.SptImg(bk_im)
        self.bk = pygm.SptImg('data/img_bk_1.jpg')
        self.bk.rect.top = -230
        self.bk.rect.left = -230
        self.disp_add(self.bk)

        self.scn1 = OMSceneA()
        self.disp_add(self.scn1)


def main():
    sf = GMOpenmove('OpenMove', 800, 550)
    sf.mainloop()


if __name__ == '__main__':
    main()
