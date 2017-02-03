"""
Bluelake PyGame Base.
"""

import random
import sys
import time

from collections import OrderedDict

import pygame
from pygame import locals as pg_locals

from . import consts
from . import utils


class PyGMBase(object):
    pass


class PyGMDisplayBase(PyGMBase):

    disp_type = 'dispbase'
    disp_id_seq = 0

    def __init__(self, *args, **kwargs):
        self.pygm = pygame
        self.pglc = pg_locals

        self.parent = None
        self.children = OrderedDict()  # {}

        self.events = []
        self.flag_check_event = True

        self.surf = None

        self.rect = self.pygm.Rect(0, 0, 0, 0)

        self.flag_hide = False

        self.tm = str(time.time()) + '-' + str(random.random())

        self.id_seq = PyGMDisplayBase.disp_seq()

    @classmethod
    def disp_seq(cls):
        cls.disp_id_seq += 1
        return cls.disp_id_seq

    def disp_n(self):
        return len(self.children)

    def disp_name(self, c):
        if isinstance(c, (PyGMDisplayBase,)):
            cname = str(c.disp_type) + '_' + str(id(c)) + '_' + str(c.tm)
            cname += '_' + str(c.id_seq)
        else:
            cname = 'surf' + '_' + str(id(c)) + '_' + str(hash(c))
        return cname

    def disp_add(self, c):
        cname = self.disp_name(c)
        self.children[cname] = c
        try:
            # AttributeError: 'pygame.Surface' object has no attribute 'parent'
            c.parent = self  # TODO: pygame.Surface.get_parent(...)
        except:
            pass

    def disp_del(self, c):
        try:
            c.parent = None
        except:
            pass
        cname = self.disp_name(c)
        if cname in self.children.keys():
            del self.children[cname]

    def disp_rm_from_parent(self):
        cname = self.disp_name(self)
        if cname in self.parent.children.keys():
            del self.parent.children[cname]

    def get_rect(self):
        return self.rect

    def update(self, surf_main, fps_clock, events, *args, **kwargs):

        # TODO: depth-first-search --> broad-first

        for cname, child in self.children.items():

            if isinstance(child, (PyGMDisplayBase,)):

                # check if hide
                if child.flag_hide:
                    continue

                events = child.handle_event(events)

                child.refresh(fps_clock)

                # draw on main surface
                child.update(surf_main, fps_clock, events)
            else:
                rct = self.get_rect()

                # draw on main surface
                surf_main.blit(child, rct)

    def hide(self, flag=None):
        if flag is None:
            flag = not self.flag_hide
        self.flag_hide = flag

    def refresh(self, fps_clock, *args, **kwargs):
        pass  # to be over written

    def handle_event(self, events, *args, **kwargs):
        return events

    def do_check_event(self):
        self.flag_check_event = True

    def do_not_check_event(self):
        self.flag_check_event = False


class PyGMGame(PyGMDisplayBase):

    disp_type = 'pygm'

    def __init__(self, win_title, win_w, win_h, win_bk_color=(255, 255, 255),
                 *args, **kwargs):
        super(PyGMGame, self).__init__(*args, **kwargs)

        self.win_title = win_title
        self.win_w = win_w
        self.win_h = win_h
        self.win_bk_color = win_bk_color

        self.thrds = []

        self.init(*args, **kwargs)

    def init(self, *args, **kwargs):
        self.pygm.init()

        self.pygm.display.init()

        self.pygm.display.set_caption(self.win_title)
        # TODO: self.pygm.RESIZABLE / FULLSCREEN
        self.surf_main = self.pygm.display.set_mode((self.win_w, self.win_h))

        self.FPS = kwargs.get('fps', 30)  # frames per second setting
        self.fps_clock = self.pygm.time.Clock()

    def surf_main_update(self, c=(255, 255, 255)):
        self.surf_main.fill(c)

    def disp_update(self):
        self.refresh(self.fps_clock)

        self.surf_main_update(self.win_bk_color)

        for cname, child in self.children.items():
            self.events = child.handle_event(self.events)
            child.refresh(self.fps_clock)
            child.update(self.surf_main, self.fps_clock, self.events)

        self.pygm.display.update()

    def mainloop(self):
        while 1:
            self.step()

    def step(self, fps=None):
        if fps is None:
            fps = self.FPS

        # clear the event buffer
        self.events = []

        for event in self.pygm.event.get():
            if event.type == self.pglc.QUIT:
                self.quit()
            else:
                self.events.append(event)

        self.disp_update()
        self.fps_clock.tick(fps)

    def pause(self):
        pass

    def resume(self):
        pass

    def quit(self):
        # stop other threads
        for thrd in self.thrds:
            thrd.stop()
            thrd.join()

        self.pygm.quit()
        sys.exit()

    def reset(self, *args, **kwargs):
        pass

    def game_over(self):
        return False

    def thrd_add(self, thrd, *args, **kwargs):
        self.thrds.append(thrd)

    def surf_main_to_img_str(self, fmt='RGBA', rect=None):
        if self.surf_main is None:
            raise Exception('surf_main_to_img_str: No surf_main')

        if rect:
            surf = self.surf_main.subsurface(rect)
        else:
            surf = self.surf_main

        data = self.pygm.image.tostring(surf, fmt)
        return data

    def surf_main_to_img_file(self, to, rect=None):
        """
        NOTE: here we can use StringIO
            from StringIO import StringIO
            to = StringIO()
            spt.to_img_file(to)
            print to.getvalue()
        """
        if self.surf_main is None:
            raise Exception('surf_main_to_img_file: No surf_main')

        if rect:
            surf = self.surf_main.subsurface(rect)
        else:
            surf = self.surf_main

        self.pygm.image.save(surf, to)

    def capture_screen(self, to, *args, **kwargs):
        self.surf_main_to_img_file(to)


# #### ####


class PyGMScene(PyGMDisplayBase):
    disp_type = 'scene'
    def __init__(self, *args, **kwargs):
        super(PyGMScene, self).__init__(*args, **kwargs)


class PyGMSprite(PyGMDisplayBase):
    disp_type = 'sprite'
    def __init__(self, *args, **kwargs):
        super(PyGMSprite, self).__init__(*args, **kwargs)

    def font_load(self, fnt_file, fnt_size=12):
        fnt = SptLoadCache.get_font(fnt_file, fnt_size)
        return fnt

    def img_load(self, img_file):
        img = SptLoadCache.get(img_file)
        return img

    def rotate(self, angl):
        if not self.surf:
            return

        rct_org = self.rect
        surf_org = self.surf
        self.disp_del(self.surf)
        self.surf = self.pygm.transform.rotate(surf_org, angl)
        self.surf = self.pygm.transform.flip(self.surf, True, False)
        self.disp_add(self.surf)

        self.rect = self.surf.get_rect()
        self.rect.top = rct_org.top
        self.rect.left = rct_org.left

    def scale(self, s=None, dt=None):
        if not self.surf:
            return

        if s is None:
            if dt is None:
                s = 1
            else:
                s = 1 + dt

        rct_org = self.rect
        surf_org = self.surf
        w = int(rct_org.width * s)
        h = int(rct_org.height * s)
        #print w, h
        self.disp_del(self.surf)
        self.surf = self.pygm.transform.scale(surf_org, (w, h))
        self.disp_add(self.surf)

        self.rect = self.surf.get_rect()
        self.rect.top = rct_org.top
        self.rect.left = rct_org.left


# #### ####


class SptLoadCache(object):
    img_cache = {}  # images
    snd_cache = {}  # sounds
    fnt_cache = {}  # fonts

    @classmethod
    def get(cls, img_file, *args, **kwargs):
        # use absolute path
        img_file = cls.abs_path(img_file)

        if img_file not in cls.img_cache.keys():
            img = pygame.image.load(img_file).convert_alpha()
            cls.img_cache[img_file] = img
        else:
            img = cls.img_cache[img_file]
        return img

    @classmethod
    def get_font(cls, fnt_file, fnt_size=12, *args, **kwargs):
        fnt_id = fnt_file + str(fnt_size)

        if fnt_id not in cls.fnt_cache.keys():
            fnt = pygame.font.Font(fnt_file, fnt_size)
            cls.fnt_cache[fnt_id] = fnt
        else:
            fnt = cls.fnt_cache[fnt_id]
        return fnt

    @classmethod
    def abs_path(cls, pth):
        if utils.is_path_abs(pth):
            return pth
        else:
            return utils.dir_abs(pth, up_dir=1)


class SptImg(PyGMSprite):
    disp_type = 'spt_img'
    def __init__(self, img_file, *args, **kwargs):
        super(SptImg, self).__init__(*args, **kwargs)

        self.img_file = img_file
        self.img = self.img_load(self.img_file)
        self.disp_add(self.img)

        self.rect = self.img.get_rect()

        self.surf = self.img


class SptImgOne(PyGMSprite):
    def __init__(self, img_file, pos, flip_h=False, flip_v=False,
                 *args, **kwargs):
        super(SptImgOne, self).__init__()

        self.pos = pos

        self.img_file = img_file

        self.img_org = self.img_load(self.img_file)

        rct = [self.pos['x'], self.pos['y'], self.pos['w'], self.pos['h']]
        self.img = self.img_org.subsurface(rct)
        if flip_h:
            self.img = self.pygm.transform.flip(self.img, True, False)
        elif flip_v:
            self.img = self.pygm.transform.flip(self.img, False, True)

        self.disp_add(self.img)

        self.rect = self.img.get_rect()

        self.surf = self.img


# TODO:
class SptImgAnim(PyGMSprite):
    disp_type = 'spt_img_anim'
    def __init__(self, img_files, intvl=3, *args, **kwargs):
        super(SptImgAnim, self).__init__(*args, **kwargs)

        self.img_files = img_files
        self.imgs = []
        for img_file in self.img_files:
            img = self.img_load(img_file)
            self.imgs.append(img)

        self.imgn = len(self.imgs)
        self.imgi = 0

        #self.disp_add(self.imgs[self.imgi])

        self.rect = self.imgs[self.imgi].get_rect()

        self.intvl = intvl
        self.cnt = 0

    def refresh(self, fps_clock, *args, **kwargs):
        self.cnt += 1

        if self.cnt % self.intvl == 0:
            self.animate()

    def animate(self):

        if 0:#self.imgi >= len(self.img_files):
            self.disp_rm_from_parent()
        else:
            for cname, child in self.children.items():
                self.disp_del(child)

            self.disp_add(self.imgs[self.imgi])
            self.imgi += 1
            self.imgi %= self.imgn


class SptImgOneAnim(PyGMSprite):
    disp_type = 'spt_img_one_anim'

    def __init__(self, img_file=None, poses=None, intvl=3,
                 move_step_h=0, move_step_v=0,
                 flip_h=False, flip_v=False,
                 rct_move=None,
                 seq=0, *args, **kwargs):
        super(SptImgOneAnim, self).__init__(*args, **kwargs)

        self.img_file = img_file
        self.poses = poses

        self.intvl = intvl
        self.move_step_h = move_step_h
        self.move_step_v = move_step_v
        self.flip_h = flip_h
        self.flip_v = flip_v
        self.rct_move = rct_move
        self.seq = 0

        self.imgs = []

        if self.img_file is not None:

            # <1> for one image
            #for pos in self.poses:
            #    img = SptImgOne(self.img_file, pos)
            #    self.imgs.append(img)

            # <2> for multi images
            if isinstance(img_file, (list, tuple, set)):
                img_files = self.img_file
                posss = self.poses
            elif isinstance(img_file, (str, basestring, unicode)):
                img_files = [self.img_file]
                posss = [self.poses]
            else:
                raise Exception('Wrong parameters')

            for img_file, poses in zip(img_files, posss):
                imgs = self.make_frames(
                    img_file, poses, flip_h=self.flip_h, flip_v=self.flip_v)
                self.imgs.extend(imgs)

            self.imgn = len(self.imgs)
            self.imgi = 0

            #self.disp_add(self.imgs[self.imgi])

            self.rect = self.imgs[self.imgi].get_rect()

        self.rect_orig = None

        self.cnt = 0

        self.stopped = False
        self.started = False
        self.finished = False

    def make_frames(self, img_file, poses, flip_h=False, flip_v=False):
        imgs = []
        for pos in poses:
            img = SptImgOne(img_file, pos, flip_h=flip_h, flip_v=flip_v)
            imgs.append(img)
        return imgs

    @classmethod
    def cre_by_imgs(cls, imgs, intvl=3, rct_move=None,
                    *args, **kwargs):
        a = cls(None, None, intvl=intvl, rct_move=rct_move, *args, **kwargs)
        a.imgs = imgs
        a.imgn = len(imgs)
        a.imgi = 0
        a.rect = a.imgs[a.imgi].get_rect()
        return a

    def rct_move_left(self):
        if not self.rct_move:
            return 0
        else:
            m = 0
            for mv in self.rct_move:
                m += mv[1]
            return m

    def refresh(self, fps_clock, *args, **kwargs):
        self.cnt += 1

        self.animate()

    def animate(self):

        if self.stopped:
            return

        if self.imgi == 0:
            if 1:#self.finished:
                self.started = True
                self.finished = False

        if self.cnt % self.intvl != 0:
            return

        rct_top = self.rect.top
        rct_left = self.rect.left
        rct_width = self.rect.width
        rct_height = self.rect.height

        if self.rect_orig is None:
            self.rect_orig = self.imgs[self.imgi].rect

        if 0:#self.imgi >= len(self.img_files):
            self.disp_rm_from_parent()
        else:
            for cname, child in self.children.items():
                self.disp_del(child)

            self.disp_add(self.imgs[self.imgi])
            self.rect = self.imgs[self.imgi].get_rect()

            #rct_top = self.rect.top
            #rct_left = self.rect.left

            #self.imgs[self.imgi].rect.top = rct_top + \
            #    self.imgi * self.move_step_v
            #self.imgs[self.imgi].rect.left = rct_left + \
            #    self.imgi * self.move_step_h

            if self.rct_move:
                top_move = self.rct_move[self.imgi][0]
                left_move = self.rct_move[self.imgi][1]
            else:
                top_move = 0
                left_move = 0
            self.imgs[self.imgi].rect.top = rct_top + top_move
            self.imgs[self.imgi].rect.left = rct_left + left_move

            # TODO:
            if self.flip_v:
                self.imgs[self.imgi].rect.top += \
                    (self.imgs[self.imgi].rect.height - rct_height)
            if self.flip_h:
                self.imgs[self.imgi].rect.left += \
                    (self.imgs[self.imgi].rect.width - rct_width)

            #if self.imgi == self.imgn - 1:
            #    self.finished = True
            #else:
            #    self.finished = False

            self.rect_orig = self.imgs[self.imgi].rect

            self.imgi += 1
            self.imgi %= self.imgn

        if self.imgi == 0:
            if self.started:
                self.finished = True
                self.started = False

    def anim_start(self):
        self.stopped = True

    def anim_stop(self):
        self.stopped = False

    @staticmethod
    def make_poses(w, h, iw, ih):
        poses = []
        if h == ih:
            for i in range(w / iw):
                pos = {'x': i * iw, 'y': 0, 'w': iw, 'h': ih}
                poses.append(pos)
        elif w == iw:
            for i in range(h / ih):
                pos = {'x': 0, 'y': i * ih, 'w': iw, 'h': ih}
                poses.append(pos)
        else:
            for i in range(w / iw):
                for j in range(h / ih):
                    pos = {'x': i * iw, 'y': i * ih, 'w': iw, 'h': ih}
                    poses.append(pos)
        return poses


# TODO:
class SptImgAnimOne(SptImgAnim):
    disp_type = 'spt_img_anim_one'
    def __init__(self, img_file, pos, *args, **kwargs):
        super(SptImgAnimOne, self).__init__(img_file)

        self.pos = pos

        self.imgn = 13
        self.imgi = 7
        self.imgi_last = 0
        self.imgi_max = 13
        self.imgi_min = 1
        self.img_size = [100, 100]

        self.img_org = self.img
        self.disp_del(self.img)

        self.show_i()

    def show_i(self, i=None):
        if i is None:
            i = self.imgi
        else:
            pass
        
        if i < self.imgi_min:
            i = self.imgi_min
        elif i > self.imgi_max:
            i = self.imgi_max

        if i == self.imgi_last:
            return

        self.imgi_last = self.imgi
        self.imgi = i

        rct = self.pygm.Rect(self.img_size[0] * (i - 1), 0,
                             self.img_size[0], self.img_size[1])

        rct_bk = self.rect
        self.disp_del(self.img)

        self.img = self.img_org.subsurface(rct)
        self.disp_add(self.img)
        self.rect = self.img.get_rect()
        self.rect.top = rct_bk.top
        self.rect.left = rct_bk.left


class SptLbl(PyGMSprite):
    disp_type = 'spt_lbl'
    def __init__(self, s, c=consts.BLACK, font_size=22, ttf='freesansbold.ttf',
                 *args, **kwargs):
        super(SptLbl, self).__init__(*args, **kwargs)

        self.s = s
        self.c = c

        self.font_size = font_size
        self.ttf = ttf

        self.font = self.font_load(self.ttf, self.font_size)
        self.txt = self.font.render(str(self.s), True, self.c)
        self.disp_add(self.txt)

        self.rect = self.txt.get_rect()

        self.flag_changed = False

    def refresh(self, fps_clock, *args, **kwargs):
        self.change_txt()

    def change_txt(self, *args, **kwargs):
        if not self.flag_changed:
            return

        self.disp_del(self.txt)

        self.txt = self.font.render(str(self.s), True, self.c)
        self.disp_add(self.txt)

        self.flag_changed = False

    def lbl_set(self, s, c=None):
        if self.s != s:
            self.s = s
            self.flag_changed = True
            if c is not None:
                self.c = c
