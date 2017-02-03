"""
Flatpath, go forward forever.

http://codeincomplete.com/posts/javascript-racer/
http://www.extentofthejam.com/pseudo/
http://pixel.garoux.net/screen/game_list

Usage:
* UP/DOWN/LEFT/RIGHT
* SPACE : hide/show road map
* TAB : replay this road
* RETURN : go to a new road

TODO:
* hill road
* more road sprites
* sound

"""

import math
import random
import time

from .starfish import pygm
from .starfish import consts
from .starfish import sptdraw
from .starfish import utils


IMG_POS_BACKGROUND = {
  'HILLS': { 'x':    5, 'y':    5, 'w': 1280, 'h':  480 },
  'SKY':   { 'x':    5, 'y':  495, 'w': 1280, 'h':  480 },
  'TREES': { 'x':    5, 'y':  985, 'w': 1280, 'h':  480 },
}


IMG_POS_SPRITES = {
  'PALM_TREE':              { 'x':    5, 'y':    5, 'w':  215, 'h':  540 },
  'BILLBOARD08':            { 'x':  230, 'y':    5, 'w':  385, 'h':  265 },
  'TREE1':                  { 'x':  625, 'y':    5, 'w':  360, 'h':  360 },
  'DEAD_TREE1':             { 'x':    5, 'y':  555, 'w':  135, 'h':  332 },
  'BILLBOARD09':            { 'x':  150, 'y':  555, 'w':  328, 'h':  282 },
  'BOULDER3':               { 'x':  230, 'y':  280, 'w':  320, 'h':  220 },
  'COLUMN':                 { 'x':  995, 'y':    5, 'w':  200, 'h':  315 },
  'BILLBOARD01':            { 'x':  625, 'y':  375, 'w':  300, 'h':  170 },
  'BILLBOARD06':            { 'x':  488, 'y':  555, 'w':  298, 'h':  190 },
  'BILLBOARD05':            { 'x':    5, 'y':  897, 'w':  298, 'h':  190 },
  'BILLBOARD07':            { 'x':  313, 'y':  897, 'w':  298, 'h':  190 },
  'BOULDER2':               { 'x':  621, 'y':  897, 'w':  298, 'h':  140 },
  'TREE2':                  { 'x': 1205, 'y':    5, 'w':  282, 'h':  295 },
  'BILLBOARD04':            { 'x': 1205, 'y':  310, 'w':  268, 'h':  170 },
  'DEAD_TREE2':             { 'x': 1205, 'y':  490, 'w':  150, 'h':  260 },
  'BOULDER1':               { 'x': 1205, 'y':  760, 'w':  168, 'h':  248 },
  'BUSH1':                  { 'x':    5, 'y': 1097, 'w':  240, 'h':  155 },
  'CACTUS':                 { 'x':  929, 'y':  897, 'w':  235, 'h':  118 },
  'BUSH2':                  { 'x':  255, 'y': 1097, 'w':  232, 'h':  152 },
  'BILLBOARD03':            { 'x':    5, 'y': 1262, 'w':  230, 'h':  220 },
  'BILLBOARD02':            { 'x':  245, 'y': 1262, 'w':  215, 'h':  220 },
  'STUMP':                  { 'x':  995, 'y':  330, 'w':  195, 'h':  140 },
  'SEMI':                   { 'x': 1365, 'y':  490, 'w':  122, 'h':  144 },
  'TRUCK':                  { 'x': 1365, 'y':  644, 'w':  100, 'h':   78 },
  'CAR03':                  { 'x': 1383, 'y':  760, 'w':   88, 'h':   55 },
  'CAR02':                  { 'x': 1383, 'y':  825, 'w':   80, 'h':   59 },
  'CAR04':                  { 'x': 1383, 'y':  894, 'w':   80, 'h':   57 },
  'CAR01':                  { 'x': 1205, 'y': 1018, 'w':   80, 'h':   56 },
  'PLAYER_UPHILL_LEFT':     { 'x': 1383, 'y':  961, 'w':   80, 'h':   45 },
  'PLAYER_UPHILL_STRAIGHT': { 'x': 1295, 'y': 1018, 'w':   80, 'h':   45 },
  'PLAYER_UPHILL_RIGHT':    { 'x': 1385, 'y': 1018, 'w':   80, 'h':   45 },
  'PLAYER_LEFT':            { 'x':  995, 'y':  480, 'w':   80, 'h':   41 },
  'PLAYER_STRAIGHT':        { 'x': 1085, 'y':  480, 'w':   80, 'h':   41 },
  'PLAYER_RIGHT':           { 'x':  995, 'y':  531, 'w':   80, 'h':   41 }
}


FP_COLOR_WHITE = '#FFFFFF'
FP_COLOR_BLACK = '#000000'
FP_COLOR_YELLOW = '#EEEE00'
FP_COLOR_BLUE = '#00EEEE'


FP_COLORS = {
  'SKY':  '#72D7EE',
  'TREE': '#005108',
  'FOG':  '#005108',
  'LIGHT':  {'road': '#6B6B6B', 'grass': '#10AA10', 'rumble': '#555555', 'lane': '#CCCCCC'},
  'DARK':   {'road': '#696969', 'grass': '#009A00', 'rumble': '#BBBBBB'                   },
  'START':  {'road': FP_COLOR_WHITE,   'grass': FP_COLOR_WHITE,   'rumble': FP_COLOR_WHITE},
  'FINISH': {'road': FP_COLOR_BLACK,   'grass': FP_COLOR_BLACK,   'rumble': FP_COLOR_BLACK},
  'START_Y':  {'road': FP_COLOR_YELLOW, 'grass': '#10AA10', 'rumble': '#555555', 'lane': '#CCCCCC'},
}


FP_ROAD = {
  'LENGTH': {'NONE': 0, 'SHORT':  25, 'MEDIUM':  50, 'LONG':  100 }, # num segments
  'CURVE':  {'NONE': 0, 'EASY':    2, 'MEDIUM':   4, 'HARD':    6 },
  'HILL':   {'NONE': 0, 'LOW':    20, 'MEDIUM':  40, 'HIGH':   60 },
}


FP_ROAD_SPRTS = {
    'chest': {'imgs': ['img_sprts/i_chest1.png'], 'score': 100,},
    'coin1': {'imgs': ['img_sprts/i_coin1.png'], 'score': 1,},
    'coin5': {'imgs': ['img_sprts/i_coin5.png'], 'score': 5,},
    'coin20': {'imgs': ['img_sprts/i_coin20.png'], 'score': 20,},
    'health': {'imgs': ['img_sprts/i_health.png'], 'score': 10,},
    'heart': {'imgs': ['img_sprts/i_heart.png'], 'score': 50,},
    'pot1': {'imgs': ['img_sprts/i_pot1.png'], 'score': -5,},
    'pot2': {'imgs': ['img_sprts/i_pot2.png'], 'score': -1,},
    'shell': {'imgs': ['img_sprts/p_shell.png'], 'score': -20,},
    'rockd': {'imgs': ['img_sprts/rock_d2.png'], 'score': -10,},
    'rockr': {'imgs': ['img_sprts/rock_r2.png'], 'score': -50,},
    #'ashra_defeat': {'imgs': ['img_sprts/ashra_defeat1.png'], 'score': -100,},
    #'bear': {'imgs': ['img_sprts/bear2.png'], 'score': -80,},
    #'dinof': {'imgs': ['img_sprts/dinof2.png'], 'score': -50,},
    'blobb': {'imgs': ['img_sprts/blobb1.png'], 'score': -50,},
    'chick_fly': {'imgs': ['img_sprts/chick_fly3.png'], 'score': 70,},
    'clown': {'imgs': ['img_sprts/clown1.png'], 'score': -100,},
}



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


class FPSptBg(pygm.SptImgOne):
    def __init__(self, img_file, pos, *args, **kwargs):
        super(FPSptBg, self).__init__(img_file, pos)


class FPSptSprts(pygm.SptImgOne):
    def __init__(self, img_file, pos, *args, **kwargs):
        super(FPSptSprts, self).__init__(img_file, pos)


class FPSptFog(sptdraw.SptDrawBase):
    def __init__(self, size, c=[0, 81, 8, 0], h=30, *args, **kwargs):
        super(FPSptFog, self).__init__(size)

        self.c = c
        self.h = h

        self.draw_on()

    def draw_on(self, *args, **kwargs):
        #self.fill(self.c)

        d = 2
        n = int(self.h / d)
        for i in range(n):
            rct = [0, i * d, self.size[0], d]
            #ca = 255 / n * (n - i)
            ca = 200 / n * (n - i)
            self.c[3] = ca
            self.pygm.draw.rect(self.surf, self.c, rct)


class FPSptRdSprts(pygm.SptImg):
    def __init__(self, img_file, *args, **kwargs):
        super(FPSptRdSprts, self).__init__(img_file)

    @classmethod
    def create_by_img(cls, img):
        return cls(img)

        # for test
        #o = SptTmpx((40, 40))
        #return o


class FPSptRoadB(sptdraw.SptDrawBase):

    def __init__(self, size, cfg, *args, **kwargs):
        super(FPSptRoadB, self).__init__(size)

        self.cfg = cfg

        self.car = kwargs.get('car')

        self.bg_sky = kwargs.get('bg_sky')
        self.bg_hills = kwargs.get('bg_hills')
        self.bg_trees = kwargs.get('bg_trees')

        self.clr_dark_road = utils.clr_from_str(FP_COLORS['DARK']['road'])
        self.clr_dark_grass = utils.clr_from_str(FP_COLORS['DARK']['grass'])


        self.rd_reset(init=True)

        self.add_fog()


    def prms_reset(self, keep_segs=False):
        self.e_keys_up = []
        self.e_keys_dn = []

        self.camera_x = 0.0
        self.camera_y = 0.0
        self.camera_z = 500.0#1000.0#0.0  == self.camera_h

        self.xw = 0.0
        self.yw = 0.0
        self.zw = 0.0

        self.xc = 0.0
        self.yc = 0.0
        self.zc = 0.0  ##

        self.xp = 0.0
        self.yp = 0.0

        self.xs = 0.0
        self.ys = 0.0

        self.d = 200.0#100.0#10.0#30.0#1.0

        self.w = self.size[0]
        self.h = self.size[1]


        if not keep_segs:
            self.segments = []

            self.rd_sprt_objs = {}

            self.rd_sprt_cache = []  # for sprites render order

            self.track_len = 0.0


        self.seg_len = 200.0#100.0#20.0#60.0#200.0#
        self.road_w = 2400#2000#600.0#200.0#1000.0#200#
        self.camera_h = 500.0#1000.0#

        self.speed_max = 300.0#180.0#200.0#100.0

        self.lane_w = 60


        self.seg_n = 300#200
        #self.seg_draw_n = 200#150
        self.seg_draw_n = 70#100#200#150


        self.speed = 0.0

        self.position = 0.0

        self.player_x = 0.0#100.0#1000.0#


        self.centrifugal = 0.1#0.06#0.08#0.01#0.3

        self.player_seg = None

        self.base_seg = None  # the segment just under the car


        self.player_di = 0 # 0:^ 1:> 2:v 3:<

        self.player_go = 0 # 0:- 1:^ 2:v


        self.speed_dt_up = 1.0#2.0#3.0
        self.speed_dt_dn = 2.0#4.0#6.0
        self.speed_dt_na = 1.0#3.0

        self.player_x_dt = 60.0#30.0#20.0

        self.last_seg_i = 0

        self.score = 0

        self.game_over = False
        self.game_score = 0.0

        self.tm_start = 0.0
        self.tm_end = 0.0
        self.tm_last_once = 0.0

        self.sky_speed    = 0.1#0.05#
        self.hill_speed   = 0.2#0.1#
        self.tree_speed   = 0.3#0.15#


    def rd_reset(self, init=False, keep_segs=False, segs_file=None):

        #if not init and not keep_segs:
        if not init:
            self.rd_sprts_del_all_objs()

        self.prms_reset(keep_segs=keep_segs)

        if segs_file is not None:
            try:
                segs = self.rd_seg_json_load(segs_file)

                self.segments = segs
                self.track_len = len(self.segments) * self.seg_len
            except Exception as e:
                print (e)
                self.init_rd_segs_rand_1()

        else:
            if not keep_segs:
                self.init_rd_segs_rand_1()

        self.draw_on()

        self.rd_seg_render()


    def init_rd_segs_rand_1(self):
        #self.rd_seg_init(self.seg_n)
        #self.rd_seg_init(self.seg_draw_n)
        #self.rd_seg_init(100)#20#500#2#10#4#1#100#200
        #self.rd_seg_init(random.randint(30, 100))
        self.rd_seg_init(random.randint(1, 10))  # for a3c train

        self.rd_seg_init_rand_curve()

        #self.add_curves()

        #self.add_low_rolling_hills(20, 2.0)
        ##self.add_low_rolling_hills(30, 4.0)

        #self.rd_seg_init_rand(10)#50#10#3#1
        #segnrand = random.randint(3, 30)
        segnrand = random.randint(2, 6)  # for a3c train
        self.rd_seg_init_rand(segnrand)

        # for segment draw
        #self.rd_seg_init(self.seg_draw_n)
        #self.rd_seg_init(100)#20#500#2#10#4#1#100#200
        self.rd_seg_init(10)  # for a3c train

        self.rd_start_seg_init()

        self.rd_sprts_init_rand()



    def draw_on(self, *args, **kwargs):
        self.fill(self.clr_dark_grass)


    def add_fog(self):

        self.fog = FPSptFog(self.size)
        self.fog.rect.top = 240
        self.fog.rect.left = 0
        self.disp_add(self.fog)



    def get_seg_base_i(self, pos=None):
        if pos is None:
            pos = self.position

        i = int(pos / self.seg_len)
        #x#i = int(utils.math_round(pos / self.seg_len))
        #i = int(math.floor(pos / self.seg_len))
        #i = int(math.ceil(pos / self.seg_len))

        seg_n = len(self.segments)
        i = (i + seg_n) % seg_n
        return i

    def rd_get_segs(self, whole=False):
        if whole:
            segs = self.segments
        else:
            segs = self.segments[:-self.seg_draw_n]
        return segs


    # #### geometry #### #

    def geo_prjc_scale(self, d, zc):
        if zc == 0.0:
            return 1.0
        else:
            return d / zc

    def xc_to_xp(self, xc, d, zc):
        if zc == 0.0:
            #xp = float('inf')
            #xp = 2 ** 64
            xp = xc
        else:
            xp = xc * (d / zc)
        return xp

    def yc_to_yp(self, yc, d, zc):
        if zc == 0.0:
            #yp = float('inf')
            #yp = 2 ** 64
            yp = yc
        else:
            yp = yc * (d / zc)
        return yp


    def xp_to_xs(self, xp, w):
        #xs = w / 2.0 + w / 2.0 * xp 
        xs = w / 2.0 + xp 
        return xs

    def yp_to_ys(self, yp, h):
        #ys = h / 2.0 - h / 2.0 * yp 
        ys = h / 2.0 - yp 
        return ys



    def rd_seg_init(self, a=500):

        for n in range(a):
            self.rd_seg_add(0.0, 0.0)


    def rd_seg_add(self, curve=0.0, yw=0.0):
        #print '+', curve, yw

        n = len(self.segments)
        #print n

        if n % 2 == 0:
        #if n % 4 == 0:
            c = FP_COLORS['LIGHT']
            #c = {'road': FP_COLOR_WHITE}
        else:
            c = FP_COLORS['DARK']
            #c = {'road': FP_COLOR_BLACK}

        seg = {
            'index': n,

            'p1': {'world': {'z': (n + 1) * self.seg_len,
                             'y': self.seg_lasy_y()},
                   'camera': {},
                   'screen': {}},
            'p2': {'world': {'z': (n + 2) * self.seg_len,
                             'y': yw},
                   'camera': {},
                   'screen': {}},

            'curve': curve,
            'color': c,
            'sprites': [],
            'looped': 0,
        }

        self.segments.append(seg)

        self.track_len = len(self.segments) * self.seg_len
        #self.track_len = (len(self.segments) - self.seg_draw_n) * self.seg_len



    def seg_lasy_y(self):
        seg_n = len(self.segments)

        if seg_n == 0:
            return 0.0
        else:
            return self.segments[seg_n - 1]['p2']['world'].get('y', 0.0)


    def rd_seg_init_rand(self, n=50):
        #print 'rd_seg_init_rand', n

        for i in range(n):
            p = random.random()
            #print p

            rl = random.choice([1, -1])

            enter = random.randint(10, 40)
            hold = random.randint(10, 40)
            leave = random.randint(10, 40)

            if p < 0.3:
                curve = 0.0
                yw = 0.0
            #elif p < 0.8:
            #    curve = 0.0
            #    yw = random.random() * 10.0
            else:
                curve = rl * random.random() * 6.0
                yw = 0.0

            self.add_road(enter, hold, leave, curve, yw)


    def rd_seg_init_rand_2(self, n=50):
        for i in range(n):
            p = random.random()
            #print p

            rl = random.choice([1, -1])

            if p < 0.35:
                self.add_road(FP_ROAD['LENGTH']['MEDIUM'],
                              FP_ROAD['LENGTH']['MEDIUM'],
                              FP_ROAD['LENGTH']['MEDIUM'],
                              rl * FP_ROAD['CURVE']['MEDIUM'])
            elif p < 0.7:
                self.add_road(FP_ROAD['LENGTH']['MEDIUM'],
                              FP_ROAD['LENGTH']['MEDIUM'],
                              FP_ROAD['LENGTH']['MEDIUM'],
                              rl * FP_ROAD['CURVE']['EASY'])
            else:
                enter = random.randint(10, 100)
                hold = random.randint(10, 100)
                leave = random.randint(10, 100)
                self.add_road(enter, hold, leave, 0.0, 0.0)


    def rd_seg_init_rand_curve(self, n=5):
        #print 'rd_seg_init_rand', n

        for i in range(n):

            rl = random.choice([1, -1])

            enter = random.randint(10, 40)
            hold = random.randint(10, 40)
            leave = random.randint(10, 40)

            curve = rl * random.random() * 8.0
            yw = 0.0

            self.add_road(enter, hold, leave, curve, yw)


    def rd_start_seg_init(self, n=3):
        seg_n = len(self.segments)
        if seg_n == 0:
            return

        #self.segments[0]['color'] = FP_COLORS['START_Y']
        #self.segments[2]['color'] = FP_COLORS['START_Y']

        for i in range(n):
            self.segments[i]['color'] = FP_COLORS['START_Y']


    def rd_sprts_init_rand(self, n=None):
        seg_n = len(self.segments)
        if n is None:
            #n = seg_n / 20
            n = int(seg_n / random.randint(10, 30))

        for i in range(n):
            j = random.randint(10, seg_n - 10)
            sprt = random.choice(list(FP_ROAD_SPRTS.keys()))

            s = {
                'name': sprt,
                'type': 1,  # image / animate / ...
                'obj': None,  # need to create at render
                ##'x_i': None,  # get real (random) x from x_pos
                'x_i': random.randint(0, 4),
                'score': FP_ROAD_SPRTS[sprt].get('score', 0),
            }
            self.segments[j]['sprites'].append(s)


    def rd_sprts_del_all_objs(self):
        ks = []
        sprts = []
        for k, sprt in self.rd_sprt_objs.items():
            ks.append(k)
            sprts.append(sprt)

        for k in ks:
            del self.rd_sprt_objs[k]
        for sprt in sprts:
            self.disp_del(sprt)


    def util_limit(self, value, mn, mx):
        return max(mn, min(value, mx))

    def util_accelerate(self, v, accel, dt):
        return v + (accel * dt)


    def util_increase(self, start, increment, mx): # with looping
        result = start + increment
        while (result >= mx):
          result -= mx
        while (result < 0):
          result += mx
        return result


    def util_ease_in(self, a, b, percent):
        return a + (b - a) * math.pow(percent, 2)

    def util_ease_out(self, a, b, percent):
        return a + (b - a) * (1 - math.pow(1 - percent, 2))

    def util_ease_in_out(self, a, b, percent):
        return a + (b - a) * ((-math.cos(percent * math.pi)/2) + 0.5)


    def util_curve_percent_remaining(self, n, total):
        return (n % total) / total



    def add_road(self, enter, hold, leave, curve, yw=0.0):
        #print enter, hold, leave, curve, yw

        start_y = self.seg_lasy_y()
        end_y = start_y + (int(yw) * self.seg_len)
        total = enter + hold + leave

        for n in range(enter):
            self.rd_seg_add(self.util_ease_in(0, curve, float(n)/enter),
                            self.util_ease_out(start_y, end_y,
                                               float(n)/total))

        for n in range(hold):
            self.rd_seg_add(curve,
                            self.util_ease_out(start_y, end_y,
                                               (float(n)+enter)/total))

        for n in range(leave):
            self.rd_seg_add(self.util_ease_out(curve, 0, n/leave),
                            self.util_ease_out(start_y, end_y,
                                               (float(n)+enter+hold)/total))


    def add_curves(self):
        self.add_road(FP_ROAD['LENGTH']['MEDIUM'],
                      FP_ROAD['LENGTH']['MEDIUM'],
                      FP_ROAD['LENGTH']['MEDIUM'],
                      -FP_ROAD['CURVE']['EASY'])
        self.add_road(FP_ROAD['LENGTH']['MEDIUM'],
                      FP_ROAD['LENGTH']['MEDIUM'],
                      FP_ROAD['LENGTH']['MEDIUM'],
                      FP_ROAD['CURVE']['MEDIUM'])
        self.add_road(FP_ROAD['LENGTH']['MEDIUM'],
                      FP_ROAD['LENGTH']['MEDIUM'],
                      FP_ROAD['LENGTH']['MEDIUM'],
                      FP_ROAD['CURVE']['EASY'])
        self.add_road(FP_ROAD['LENGTH']['MEDIUM'],
                      FP_ROAD['LENGTH']['MEDIUM'],
                      FP_ROAD['LENGTH']['MEDIUM'],
                      -FP_ROAD['CURVE']['EASY'])
        self.add_road(FP_ROAD['LENGTH']['MEDIUM'],
                      FP_ROAD['LENGTH']['MEDIUM'],
                      FP_ROAD['LENGTH']['MEDIUM'],
                      -FP_ROAD['CURVE']['MEDIUM'])
        self.add_road(FP_ROAD['LENGTH']['MEDIUM'],
                      FP_ROAD['LENGTH']['MEDIUM'],
                      FP_ROAD['LENGTH']['MEDIUM'],
                      0.0)


    def add_low_rolling_hills(self, num, height):
        num = num or ROAD['LENGTH']['SHORT']
        height = height or ROAD['HILL']['LOW']

        self.add_road(num, num, num, 0,  height/2.0)
        self.add_road(num, num, num, 0, -height)
        self.add_road(num, num, num, 0,  height)
        self.add_road(num, num, num, 0,  0)
        self.add_road(num, num, num, 0,  height/2.0)
        self.add_road(num, num, num, 0,  0)

    def rd_seg_get_cleared(self, segs=None):
        if not segs:
            segs = self.segments

        segs_c = []
        for seg in segs:
            if not seg['sprites']:
                segs_c.append(seg)
            else:
                seg_c = {}
                for k, v in seg.items():
                    if k not in ['sprites']:
                        seg_c[k] = v
                    else:
                        seg_c[k] = []
                        for spr in seg['sprites']:
                            spr_n = {}
                            for sk, sv in spr.items():
                                if sk not in ['obj']:
                                    spr_n[sk] = sv
                                else:
                                    spr_n[sk] = None
                            seg_c[k].append(spr_n)
                segs_c.append(seg_c)

        return segs_c

    def rd_seg_json_save(self, f):
        sc = self.rd_seg_get_cleared(self.segments)
        s = utils.json_dumps(sc)
        with open(f, 'w') as fo:
            fo.write(s)

    def rd_seg_json_load(self, f):
        with open(f, 'r') as fi:
            s = fi.read()
        segs = utils.json_loads(s)
        return segs


    def rd_seg_render__1_o(self):
        """straight"""

        xc1 = self.road_w / 2 - self.player_x
        xc2 = -self.road_w / 2 - self.player_x
        xc3 = self.road_w / 2 - self.player_x
        xc4 = -self.road_w / 2 - self.player_x

        xcl1 = xc1 - self.lane_w
        xcl2 = xc2 + self.lane_w
        xcl3 = xc3 - self.lane_w
        xcl4 = xc4 + self.lane_w


        xcr1 = self.lane_w - self.player_x
        xcr2 = -self.lane_w - self.player_x
        xcr3 = self.lane_w - self.player_x
        xcr4 = -self.lane_w - self.player_x


        yc = self.camera_h

        #print '=' * 80
        #print 'self.position', self.position

        for i, seg in enumerate(self.segments):
            zw1 = seg['p1']['world']['z']
            zw2 = seg['p2']['world']['z']

            zc1 = zw1 - self.camera_z - self.position
            zc2 = zw2 - self.camera_z - self.position
            #zc1 = self.position - (zw1 - self.camera_z)
            #zc2 = self.position - (zw2 - self.camera_z)

            xp1 = self.xc_to_xp(xc1, self.d, zc1)
            xs1 = self.xp_to_xs(xp1, self.w)

            xp2 = self.xc_to_xp(xc2, self.d, zc1)
            xs2 = self.xp_to_xs(xp2, self.w)

            xp3 = self.xc_to_xp(xc3, self.d, zc2)
            xs3 = self.xp_to_xs(xp3, self.w)

            xp4 = self.xc_to_xp(xc4, self.d, zc2)
            xs4 = self.xp_to_xs(xp4, self.w)


            yp1 = self.yc_to_yp(yc, self.d, zc1)
            ys1 = self.yp_to_ys(yp1, self.h)

            ys2 = ys1

            yp3 = self.yc_to_yp(yc, self.d, zc2)
            ys3 = self.yp_to_ys(yp3, self.h)

            ys4 = ys3


            self.render_polygon(None,
                                0, ys1, self.w, ys2,
                                self.w, ys4, 0, ys3,
                                seg['color']['grass'])


            self.render_polygon(None,
                                xs1, ys1, xs2, ys2,
                                xs4, ys4, xs3, ys3,
                                seg['color']['road'])


            if 1:#i % 2 == 1:

                xpl1 = self.xc_to_xp(xcl1, self.d, zc1)
                xsl1 = self.xp_to_xs(xpl1, self.w)

                xpl2 = self.xc_to_xp(xcl2, self.d, zc1)
                xsl2 = self.xp_to_xs(xpl2, self.w)

                xpl3 = self.xc_to_xp(xcl3, self.d, zc2)
                xsl3 = self.xp_to_xs(xpl3, self.w)

                xpl4 = self.xc_to_xp(xcl4, self.d, zc2)
                xsl4 = self.xp_to_xs(xpl4, self.w)


                self.render_polygon(None,
                                    xs1, ys1, xsl1, ys1,
                                    xsl3, ys3, xs3, ys3,
                                    seg['color']['rumble'])

                self.render_polygon(None,
                                    xs2, ys2, xsl2, ys2,
                                    xsl4, ys4, xs4, ys4,
                                    seg['color']['rumble'])


                xpr1 = self.xc_to_xp(xcr1, self.d, zc1)
                xsr1 = self.xp_to_xs(xpr1, self.w)

                xpr2 = self.xc_to_xp(xcr2, self.d, zc1)
                xsr2 = self.xp_to_xs(xpr2, self.w)

                xpr3 = self.xc_to_xp(xcr3, self.d, zc2)
                xsr3 = self.xp_to_xs(xpr3, self.w)

                xpr4 = self.xc_to_xp(xcr4, self.d, zc2)
                xsr4 = self.xp_to_xs(xpr4, self.w)

                self.render_polygon(None,
                                    xsr1, ys1, xsr2, ys2,
                                    xsr4, ys4, xsr3, ys3,
                                    seg['color']['rumble'])



    def rd_seg_render__2_o(self):
        """curve test 1"""

        #theta_i = math.pi /180.0 * 0.1
        #theta_i = math.pi /180.0 * 0.5
        theta_i = math.pi /180.0 * 0.9
        #theta_i = 0.0

        xc1 = self.road_w / 2 - self.player_x
        xc2 = -self.road_w / 2 - self.player_x
        xc3 = self.road_w / 2 - self.player_x
        xc4 = -self.road_w / 2 - self.player_x

        yc = self.camera_h

        print ('=' * 80)
        print ('self.position', self.position)

        # <2>
        seg_n = len(self.segments)
        segbi = self.get_seg_base_i()
        print ('segbi', segbi)


        # TODO: do at update
        #dpx1 = self.seg_len * math.tan(theta_i)
        #self.player_x -= dpx1


        # <1>
        #for i, seg in enumerate(self.segments):
        # <2>
        for i in range(self.seg_draw_n):
            #'''
            # <2>
            si = (segbi + i) % seg_n
            #print si

            seg = self.segments[si]

            #x#zw1 = (i+1)*self.seg_len
            #zw2 = (i+2)*self.seg_len
            #'''

            # <1>
            zw1 = seg['p1']['world']['z']
            zw2 = seg['p2']['world']['z']


            zc1 = zw1 - self.camera_z - self.position
            zc2 = zw2 - self.camera_z - self.position

            curve_d = 500

            #x#xc1 = self.road_w / 2 - self.player_x - curve_d * i
            #xc2 = -self.road_w / 2 - self.player_x - curve_d * i
            #xc3 = self.road_w / 2 - self.player_x - curve_d * i
            #xc4 = -self.road_w / 2 - self.player_x - curve_d * i


            xp1 = self.xc_to_xp(xc1, self.d, zc1)
            xs1 = self.xp_to_xs(xp1, self.w)

            xp2 = self.xc_to_xp(xc2, self.d, zc1)
            xs2 = self.xp_to_xs(xp2, self.w)

            xp3 = self.xc_to_xp(xc3, self.d, zc2)
            xs3 = self.xp_to_xs(xp3, self.w)

            xp4 = self.xc_to_xp(xc4, self.d, zc2)
            xs4 = self.xp_to_xs(xp4, self.w)


            yp1 = self.yc_to_yp(yc, self.d, zc1)
            ys1 = self.yp_to_ys(yp1, self.h)

            ys2 = ys1

            yp3 = self.yc_to_yp(yc, self.d, zc2)
            ys3 = self.yp_to_ys(yp3, self.h)

            ys4 = ys3


            #'''
            #if 1:
            #if i < self.seg_draw_n / 2:
            if i < self.seg_draw_n / 4:
                theta1 = theta_i * i
                theta2 = theta_i * (i + 1)

                dx1 = self.seg_len * math.tan(theta1)
                dx2 = self.seg_len * math.tan(theta2)

                xs1 += dx1
                xs2 += dx1
                xs3 += dx2 #+ dx1
                xs4 += dx2 #+ dx1

            #'''


            self.render_polygon(None,
                                0, ys1, self.w, ys2,
                                self.w, ys4, 0, ys3,
                                seg['color']['grass'])


            self.render_polygon(None,
                                xs1, ys1, xs2, ys2,
                                xs4, ys4, xs3, ys3,
                                seg['color']['road'])



    def rd_seg_render__3_o(self):
        """curve test 2: draw a circle"""

        #theta_i = math.pi /180.0 * 0.1
        #theta_i = math.pi /180.0 * 0.5
        theta_i = math.pi /180.0 * 0.9
        #theta_i = 0.0

        #xc1 = self.road_w / 2 - self.player_x
        #xc2 = -self.road_w / 2 - self.player_x
        #xc3 = self.road_w / 2 - self.player_x
        #xc4 = -self.road_w / 2 - self.player_x


        # <3>
        #engi = math.pi / 2.0 / self.seg_draw_n
        engi = math.pi / 2.0 / 60#10#20
        rad = self.road_w * 4#2
        rad1 = rad + self.road_w / 2
        rad2 = rad - self.road_w / 2


        yc = self.camera_h

        print ('=' * 80)
        print ('self.position', self.position)

        # <2>
        seg_n = len(self.segments)
        segbi = self.get_seg_base_i()
        print ('segbi', segbi)


        # TODO: do at update
        #dpx1 = self.seg_len * math.tan(theta_i)
        #self.player_x -= dpx1


        # <1>
        #for i, seg in enumerate(self.segments):
        # <2>
        for i in range(self.seg_draw_n):
            #'''
            # <2>
            si = (segbi + i) % seg_n
            #print si

            seg = self.segments[si]

            #x#zw1 = (i+1)*self.seg_len
            #zw2 = (i+2)*self.seg_len
            #'''

            # <1>
            zw1 = seg['p1']['world']['z']
            zw2 = seg['p2']['world']['z']


            zc1 = zw1 - self.camera_z - self.position
            zc2 = zw2 - self.camera_z - self.position

            curve_d = 500

            #x#xc1 = self.road_w / 2 - self.player_x - curve_d * i
            #xc2 = -self.road_w / 2 - self.player_x - curve_d * i
            #xc3 = self.road_w / 2 - self.player_x - curve_d * i
            #xc4 = -self.road_w / 2 - self.player_x - curve_d * i


            # <3>
            xx1 = rad1 * math.cos(engi * i)
            xx2 = rad2 * math.cos(engi * i)
            xx3 = rad1 * math.cos(engi * (i + 1))
            xx4 = rad2 * math.cos(engi * (i + 1))

            xc1 = (rad - xx1) - self.player_x
            xc2 = (rad - xx2) - self.player_x
            xc3 = (rad - xx3) - self.player_x
            xc4 = (rad - xx4) - self.player_x



            xp1 = self.xc_to_xp(xc1, self.d, zc1)
            xs1 = self.xp_to_xs(xp1, self.w)

            xp2 = self.xc_to_xp(xc2, self.d, zc1)
            xs2 = self.xp_to_xs(xp2, self.w)

            xp3 = self.xc_to_xp(xc3, self.d, zc2)
            xs3 = self.xp_to_xs(xp3, self.w)

            xp4 = self.xc_to_xp(xc4, self.d, zc2)
            xs4 = self.xp_to_xs(xp4, self.w)


            yp1 = self.yc_to_yp(yc, self.d, zc1)
            ys1 = self.yp_to_ys(yp1, self.h)

            ys2 = ys1

            yp3 = self.yc_to_yp(yc, self.d, zc2)
            ys3 = self.yp_to_ys(yp3, self.h)

            ys4 = ys3


            '''
            #if 1:
            #if i < self.seg_draw_n / 2:
            if i < self.seg_draw_n / 4:
                theta1 = theta_i * i
                theta2 = theta_i * (i + 1)

                dx1 = self.seg_len * math.tan(theta1)
                dx2 = self.seg_len * math.tan(theta2)

                xs1 += dx1
                xs2 += dx1
                xs3 += dx2 #+ dx1
                xs4 += dx2 #+ dx1

            '''


            self.render_polygon(None,
                                0, ys1, self.w, ys2,
                                self.w, ys4, 0, ys3,
                                seg['color']['grass'])


            self.render_polygon(None,
                                xs1, ys1, xs2, ys2,
                                xs4, ys4, xs3, ys3,
                                seg['color']['road'])




    def rd_seg_render__4_o(self):
        """curve"""

        #theta_i = math.pi /180.0 * 0.1
        #theta_i = math.pi /180.0 * 0.5
        theta_i = math.pi /180.0 * 0.9
        #theta_i = 0.0

        xc1 = self.road_w / 2 - self.player_x
        xc2 = -self.road_w / 2 - self.player_x
        xc3 = self.road_w / 2 - self.player_x
        xc4 = -self.road_w / 2 - self.player_x

        #xcl1 = xc1 - self.lane_w
        #xcl2 = xc2 + self.lane_w
        #xcl3 = xc3 - self.lane_w
        #xcl4 = xc4 + self.lane_w

        xcr1 = self.lane_w - self.player_x
        xcr2 = -self.lane_w - self.player_x
        xcr3 = self.lane_w - self.player_x
        xcr4 = -self.lane_w - self.player_x


        yc = self.camera_h

        print ('=' * 80)
        print ('self.position', self.position)

        # <2>
        seg_n = len(self.segments)
        segbi = self.get_seg_base_i()
        print ('segbi', segbi)


        self.player_seg = self.segments[segbi]

        b_curve = self.player_seg.get('curve', 0.0)
        #b_percent = 0.5
        b_percent = self.util_curve_percent_remaining(self.position,
                                                      self.seg_len)

        dx_curve = - (b_curve * b_percent)
        x_curve  = 0


        # <1>
        #for i, seg in enumerate(self.segments):
        # <2>
        for i in range(self.seg_draw_n):
            #'''
            # <2>
            si = (segbi + i) % seg_n
            #print si

            seg = self.segments[si]
            #'''

            '''
            #x#
            if seg['index'] < segbi:
                zw1 = (i+1)*self.seg_len
                zw2 = (i+2)*self.seg_len

            else:
                # <1>
                zw1 = seg['p1']['world']['z']
                zw2 = seg['p2']['world']['z']
            '''

            zw1 = seg['p1']['world']['z']
            zw2 = seg['p2']['world']['z']


            zc1 = zw1 - self.camera_z - self.position
            zc2 = zw2 - self.camera_z - self.position


            # for curve
            xc1 = xc1 - x_curve
            xc2 = xc2 - x_curve
            xc3 = xc3 - x_curve - dx_curve
            xc4 = xc4 - x_curve - dx_curve

            xcl1 = xc1 - self.lane_w
            xcl2 = xc2 + self.lane_w
            xcl3 = xc3 - self.lane_w
            xcl4 = xc4 + self.lane_w

            xcr1 = xcr1 - x_curve
            xcr2 = xcr2 - x_curve
            xcr3 = xcr3 - x_curve - dx_curve
            xcr4 = xcr4 - x_curve - dx_curve


            x_curve  = x_curve + dx_curve
            dx_curve = dx_curve + seg.get('curve', 0.0)


            xp1 = self.xc_to_xp(xc1, self.d, zc1)
            xs1 = self.xp_to_xs(xp1, self.w)

            xp2 = self.xc_to_xp(xc2, self.d, zc1)
            xs2 = self.xp_to_xs(xp2, self.w)

            xp3 = self.xc_to_xp(xc3, self.d, zc2)
            xs3 = self.xp_to_xs(xp3, self.w)

            xp4 = self.xc_to_xp(xc4, self.d, zc2)
            xs4 = self.xp_to_xs(xp4, self.w)


            yp1 = self.yc_to_yp(yc, self.d, zc1)
            ys1 = self.yp_to_ys(yp1, self.h)

            ys2 = ys1

            yp3 = self.yc_to_yp(yc, self.d, zc2)
            ys3 = self.yp_to_ys(yp3, self.h)

            ys4 = ys3


            '''
            #if 1:
            #if i < self.seg_draw_n / 2:
            if i < self.seg_draw_n / 4:
                theta1 = theta_i * i
                theta2 = theta_i * (i + 1)

                dx1 = self.seg_len * math.tan(theta1)
                dx2 = self.seg_len * math.tan(theta2)

                xs1 += dx1
                xs2 += dx1
                xs3 += dx2 #+ dx1
                xs4 += dx2 #+ dx1

            '''


            self.render_polygon(None,
                                0, ys1, self.w, ys2,
                                self.w, ys4, 0, ys3,
                                seg['color']['grass'])


            self.render_polygon(None,
                                xs1, ys1, xs2, ys2,
                                xs4, ys4, xs3, ys3,
                                seg['color']['road'])


            if 1:#i % 2 == 1:

                xpl1 = self.xc_to_xp(xcl1, self.d, zc1)
                xsl1 = self.xp_to_xs(xpl1, self.w)

                xpl2 = self.xc_to_xp(xcl2, self.d, zc1)
                xsl2 = self.xp_to_xs(xpl2, self.w)

                xpl3 = self.xc_to_xp(xcl3, self.d, zc2)
                xsl3 = self.xp_to_xs(xpl3, self.w)

                xpl4 = self.xc_to_xp(xcl4, self.d, zc2)
                xsl4 = self.xp_to_xs(xpl4, self.w)


                self.render_polygon(None,
                                    xs1, ys1, xsl1, ys1,
                                    xsl3, ys3, xs3, ys3,
                                    seg['color']['rumble'])

                self.render_polygon(None,
                                    xs2, ys2, xsl2, ys2,
                                    xsl4, ys4, xs4, ys4,
                                    seg['color']['rumble'])


                xpr1 = self.xc_to_xp(xcr1, self.d, zc1)
                xsr1 = self.xp_to_xs(xpr1, self.w)

                xpr2 = self.xc_to_xp(xcr2, self.d, zc1)
                xsr2 = self.xp_to_xs(xpr2, self.w)

                xpr3 = self.xc_to_xp(xcr3, self.d, zc2)
                xsr3 = self.xp_to_xs(xpr3, self.w)

                xpr4 = self.xc_to_xp(xcr4, self.d, zc2)
                xsr4 = self.xp_to_xs(xpr4, self.w)

                self.render_polygon(None,
                                    xsr1, ys1, xsr2, ys2,
                                    xsr4, ys4, xsr3, ys3,
                                    seg['color']['rumble'])



    def rd_seg_render(self):
        """curve"""

        #theta_i = math.pi /180.0 * 0.1
        #theta_i = math.pi /180.0 * 0.5
        theta_i = math.pi /180.0 * 0.9
        #theta_i = 0.0

        xc1 = self.road_w / 2 - self.player_x
        xc2 = -self.road_w / 2 - self.player_x
        xc3 = self.road_w / 2 - self.player_x
        xc4 = -self.road_w / 2 - self.player_x

        #xcl1 = xc1 - self.lane_w
        #xcl2 = xc2 + self.lane_w
        #xcl3 = xc3 - self.lane_w
        #xcl4 = xc4 + self.lane_w

        xcr1 = self.lane_w - self.player_x
        xcr2 = -self.lane_w - self.player_x
        xcr3 = self.lane_w - self.player_x
        xcr4 = -self.lane_w - self.player_x


        yc = self.camera_h

        #print '=' * 80
        #print 'self.position', self.position

        # <2>
        seg_n = len(self.segments)
        segbi = self.get_seg_base_i()
        #print 'segbi', segbi, ' / ', seg_n


        self.player_seg = self.segments[segbi]

        self.base_seg = self.segments[(segbi + 2) % seg_n]
        # for test
        #self.base_seg['color'] = FP_COLORS['FINISH']


        b_curve = self.player_seg.get('curve', 0.0)
        #b_percent = 0.5
        b_percent = self.util_curve_percent_remaining(self.position,
                                                      self.seg_len)

        dx_curve = - (b_curve * b_percent)
        x_curve  = 0

        #print 'b_curve', b_curve
        #print 'world z', self.player_seg['p1']['world']['z']
        #print 'world y', self.player_seg['p1']['world'].get('y', 0.0)

        # clear the sprites cache
        self.rd_sprt_cache = []

        # <1>
        #for i, seg in enumerate(self.segments):
        # <2>
        for i in range(self.seg_draw_n):
            #'''
            # <2>
            si = (segbi + i) % seg_n
            #print si

            seg = self.segments[si]
            #'''

            '''
            # for test
            if i < 10:
                print '>>> ', i
                print 'curve', seg.get('curve', 0.0)
                print 'world z', seg['p1']['world']['z']
                print 'world y', seg['p1']['world'].get('y', 0.0)
                #print '-' * 30
            '''

            '''
            #x#
            if seg['index'] < segbi:
                zw1 = (i+1)*self.seg_len
                zw2 = (i+2)*self.seg_len

            else:
                # <1>
                zw1 = seg['p1']['world']['z']
                zw2 = seg['p2']['world']['z']
            '''

            zw1 = (i+1)*self.seg_len
            zw2 = (i+2)*self.seg_len

            zc1 = zw1 - self.camera_z - (self.position % self.seg_len)
            zc2 = zw2 - self.camera_z - (self.position % self.seg_len)

            '''
            #x#
            zw1 = seg['p1']['world']['z']
            zw2 = seg['p2']['world']['z']

            zc1 = zw1 - self.camera_z - self.position
            zc2 = zw2 - self.camera_z - self.position
            '''

            # for curve
            xc1 = xc1 - x_curve
            xc2 = xc2 - x_curve
            xc3 = xc3 - x_curve - dx_curve
            xc4 = xc4 - x_curve - dx_curve

            xcl1 = xc1 - self.lane_w
            xcl2 = xc2 + self.lane_w
            xcl3 = xc3 - self.lane_w
            xcl4 = xc4 + self.lane_w

            xcr1 = xcr1 - x_curve
            xcr2 = xcr2 - x_curve
            xcr3 = xcr3 - x_curve - dx_curve
            xcr4 = xcr4 - x_curve - dx_curve


            x_curve  = x_curve + dx_curve
            dx_curve = dx_curve + seg.get('curve', 0.0)


            # for hills
            yw1 = seg['p1']['world'].get('y', 0.0)
            yw2 = seg['p2']['world'].get('y', 0.0)

            yc1 = yc - yw1
            yc2 = yc - yw2

            #print yw1, yw2


            xp1 = self.xc_to_xp(xc1, self.d, zc1)
            xs1 = self.xp_to_xs(xp1, self.w)

            xp2 = self.xc_to_xp(xc2, self.d, zc1)
            xs2 = self.xp_to_xs(xp2, self.w)

            xp3 = self.xc_to_xp(xc3, self.d, zc2)
            xs3 = self.xp_to_xs(xp3, self.w)

            xp4 = self.xc_to_xp(xc4, self.d, zc2)
            xs4 = self.xp_to_xs(xp4, self.w)


            yp1 = self.yc_to_yp(yc1, self.d, zc1)
            ys1 = self.yp_to_ys(yp1, self.h)

            ys2 = ys1

            yp3 = self.yc_to_yp(yc2, self.d, zc2)
            ys3 = self.yp_to_ys(yp3, self.h)

            ys4 = ys3

            '''
            # for test
            if i < 10:
                print xs1, ys1, xs2, ys2
                print xs4, ys4, xs3, ys3
                print '-' * 30
            '''

            # grass
            self.render_polygon(None,
                                0, ys1, self.w, ys2,
                                self.w, ys4, 0, ys3,
                                seg['color']['grass'])


            # road
            self.render_polygon(None,
                                xs1, ys1, xs2, ys2,
                                xs4, ys4, xs3, ys3,
                                seg['color']['road'])


            if 1:#i % 2 == 1:

                xpl1 = self.xc_to_xp(xcl1, self.d, zc1)
                xsl1 = self.xp_to_xs(xpl1, self.w)

                xpl2 = self.xc_to_xp(xcl2, self.d, zc1)
                xsl2 = self.xp_to_xs(xpl2, self.w)

                xpl3 = self.xc_to_xp(xcl3, self.d, zc2)
                xsl3 = self.xp_to_xs(xpl3, self.w)

                xpl4 = self.xc_to_xp(xcl4, self.d, zc2)
                xsl4 = self.xp_to_xs(xpl4, self.w)


                self.render_polygon(None,
                                    xs1, ys1, xsl1, ys1,
                                    xsl3, ys3, xs3, ys3,
                                    seg['color']['rumble'])

                self.render_polygon(None,
                                    xs2, ys2, xsl2, ys2,
                                    xsl4, ys4, xs4, ys4,
                                    seg['color']['rumble'])


                xpr1 = self.xc_to_xp(xcr1, self.d, zc1)
                xsr1 = self.xp_to_xs(xpr1, self.w)

                xpr2 = self.xc_to_xp(xcr2, self.d, zc1)
                xsr2 = self.xp_to_xs(xpr2, self.w)

                xpr3 = self.xc_to_xp(xcr3, self.d, zc2)
                xsr3 = self.xp_to_xs(xpr3, self.w)

                xpr4 = self.xc_to_xp(xcr4, self.d, zc2)
                xsr4 = self.xp_to_xs(xpr4, self.w)

                self.render_polygon(None,
                                    xsr1, ys1, xsr2, ys2,
                                    xsr4, ys4, xsr3, ys3,
                                    seg['color']['rumble'])

                # for test
                #self.pygm.draw.circle(self.surf, consts.BLUE,
                #                      (int(xsr1), 116 - int(ys1)),
                #                      3, 0)


            # render road sprites
            # TODO: check if this seg is looped

            seg_scale = self.geo_prjc_scale(self.d, zc1)

            x_rnd = random.randint(1, self.road_w / 2 - 10) * seg_scale

            #x_sprt = (xs1 + xs2) / 2.0
            #y_sprt = (ys1 + ys3) / 2.0

            x_dt = x_rnd * seg_scale

            x_pos = [xsr1, xsr2,
                     (xsr1 + xsl1) / 2.0,
                     (xsr2 + xsl2) / 2.0,
                     xsl1, xsl2]

            #x_sprt = xsr1
            x_sprt = (xsr1 + xsl1) / 2.0
            #x_sprt = random.choice(x_pos)

            x_i = random.randint(0, len(x_pos) - 1)  # NOTE: not used now !!
            ##x_i = 2

            y_sprt = ys1

            scale_sprt = seg_scale * 8.0#10.0#2.0

            obj = self.rd_sprts_render(seg, x_pos, x_i, y_sprt, scale_sprt)
            if obj:
                self.rd_sprt_cache.append(obj)

        # render the sprites with right order
        for obj in self.rd_sprt_cache[::-1]:
            self.disp_add(obj)


    def render_polygon(self, ctx, x1, y1, x2, y2, x3, y3, x4, y4, color):

        #d = 200#100#240#50#
        #a = 60

        #pnts = [[x1, y1], [x2, y2], [x3, y3], [x4, y4], [x1, y1]]
        #pnts = [[x1, y1-d], [x2, y2-d], [x3, y3-d], [x4, y4-d], [x1, y1-d]]
        #pnts = [[x1, y1+a], [x2, y2+a], [x3, y3+a], [x4, y4+a], [x1, y1+a]]

        # reflect the y-
        d = 116
        pnts = [[x1, d-y1], [x2, d-y2], [x3, d-y3], [x4, d-y4], [x1, d-y1]]

        c = utils.clr_from_str(color)

        try:
            self.pygm.draw.polygon(self.surf, c, pnts)
        except Exception as e:
            #print '-' * 60
            pass


    def rd_sprts_render(self, seg, x_pos, x_i, y, scale):
        sprts = seg.get('sprites')
        if not sprts:
            return None

        for i, info in enumerate(sprts):
            sprt = info['name']

            obj_k = str(seg['index']) + '_' + str(i) + '_' + sprt

            obj = info.get('obj')

            '''
            # TODO: <1>
            if not obj:
                obj = FPSptRdSprts.create_by_img(FP_ROAD_SPRTS[sprt][0])
                info['obj'] = obj
                self.disp_add(obj)
            '''

            # <2>
            if obj:
                self.disp_del(obj)
                # NOTE: objs will be deleted at rd_sprts_del_all_objs()
                ##del self.rd_sprt_objs[obj_k]

            img = FP_ROAD_SPRTS[sprt]['imgs'][0]
            obj = FPSptRdSprts.create_by_img(img)

            # avoid: pygame.error: Width or height is too large
            if scale > 500:
                #print 'scale <1>', scale
                pass
            else:
                try:
                    obj.scale(scale)
                except:
                    #print 'scale <2>', scale
                    pass

            x_i_saved = info.get('x_i')
            #if not x_i_saved:
            #    info['x_i'] = x_i
            #    x_i_saved = x_i

            obj.rect.top = 116 - y + 240 - obj.rect.height
            obj.rect.left = x_pos[x_i_saved] - obj.rect.width / 2
            #obj.scale(scale)

            info['obj'] = obj
            ##self.disp_add(obj)  # NOTE: render out here
            self.rd_sprt_objs[obj_k] = obj  # for reset to delete all

            # NOTE: only show one
            break

        return obj


    def handle_event(self, events, *args, **kwargs):
        #print '>>> ', events
        if not self.flag_check_event:
            return events
        else:
            return self.check_key(events)


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

    def key_to_di_b(self, k):
        if k == self.pglc.K_f or k == self.pglc.K_j:
            return 0
        elif k == self.pglc.K_k:
            return 1
        elif k == self.pglc.K_SPACE or k == self.pglc.K_v or k == self.pglc.K_n:
            return 2
        elif k == self.pglc.K_d:
            return 3
        else:
            return None


    def check_key(self, events):
        #print id(events)
        r_events = []

        e_keys_up = []
        e_keys_dn = []

        for event in events:
            #print event
            if event.type == self.pglc.KEYUP:
                di = self.key_to_di(event.key)
                if di is None:
                    di = self.key_to_di_b(event.key)
                if di is not None:
                    e_keys_up.append(di)
                else:
                    r_events.append(event)

            elif event.type == self.pglc.KEYDOWN:
                di = self.key_to_di(event.key)
                if di is None:
                    di = self.key_to_di_b(event.key)
                if di is not None:
                    e_keys_dn.append(di)
                else:
                    r_events.append(event)

            else:
                r_events.append(event)

        self.e_keys_up = e_keys_up
        self.e_keys_dn = e_keys_dn

        return r_events


    def refresh__1(self, fps_clock, *args, **kwargs):
        #print '>>> refresh'

        #'''
        if self.player_di == 3: # <
            self.player_x -= 9
            if self.player_x < -1000:
                self.player_di = 1
        elif self.player_di == 1:
            self.player_x += 19
            if self.player_x > 1000:
                self.player_di = 3
        #'''

        #'''
        self.position += 10.0#5.0#1.0
        self.position += random.randint(2, 10)

        if self.position > self.track_len:
            self.position -= self.track_len
        #'''

        self.draw_on()

        self.rd_seg_render()


    def refresh(self, fps_clock, *args, **kwargs):
        self.check_player_di(self.e_keys_dn, self.e_keys_up)

        self.draw_on()

        self.rd_seg_render()

        self.update_world()

        self.check_if_car_out_road()

        self.check_score()

        self.check_tm()

        self.update_bg()


    def check_player_di(self, e_keys_dn, e_keys_up):
        if 0 in e_keys_dn:
            self.player_go = 1
        elif 2 in e_keys_dn:
            self.player_go = 2

        if 1 in e_keys_dn:
            self.player_di = 1
        elif 3 in e_keys_dn:
            self.player_di = 3

        if 0 in e_keys_up:
            if self.player_go != 2:
                self.player_go = 0
        if 2 in e_keys_up:
            if self.player_go != 1:
                self.player_go = 0

        if 1 in e_keys_up:
            if self.player_di != 3:
                self.player_di = 0
        if 3 in e_keys_up:
            if self.player_di != 1:
                self.player_di = 0

    def update_world(self):
        if self.player_go == 1:
            self.speed += self.speed_dt_up
        elif self.player_go == 2:
            self.speed -= self.speed_dt_dn
        else:
            self.speed -= self.speed_dt_na

        # if on the grass, slow down
        if self.player_x < -self.road_w / 2 or \
            self.player_x > self.road_w / 2:
            self.speed -= 10

        if self.speed < 0.0:
            self.speed = 0.0
        elif self.speed > self.speed_max:
            self.speed = self.speed_max

        self.position += self.speed
        if self.position > self.track_len:
            self.position -= self.track_len
            # for check score
            self.last_seg_i = 0

            self.game_over = True
            self.game_score = 1.0

        if self.player_di == 1:
            #self.player_x += self.player_x_dt
            self.player_x += self.speed / 5 + 20
        elif self.player_di == 3:
            #self.player_x -= self.player_x_dt
            self.player_x -= self.speed / 5 + 20
        else:
            pass

        p_curve = self.player_seg.get('curve', 0.0)
        #print 'p_curve', p_curve
        p_dt = self.speed * p_curve * self.centrifugal
        #print p_dt
        #self.player_x -= p_dt
        self.player_x += p_dt


    def check_if_car_out_road(self):

        # decrease score when go out the road
        if self.player_x < -self.road_w / 2 or \
            self.player_x > self.road_w / 2:
            if self.score > 0:
                self.score -= 1
            #self.score -= 1
            #if self.score < 0:
            #    self.score = 0

            self.game_over = True
            self.game_score = -1.0

    def check_score(self):

        # make sure we check score once for a segment
        seg_i = self.player_seg['index']
        if seg_i > self.last_seg_i:
            self.last_seg_i = seg_i
        else:
            return

        # NOTE: here we should use the segment just under the car
        #sprts = self.player_seg['sprites']
        sprts = self.base_seg['sprites']
        if not sprts:
            return

        # NOTE: we now only use the first sprite !
        sprt = sprts[0]

        x_i = sprt.get('x_i')
        if x_i is None:
            return

        scr = sprt.get('score')
        if not scr:  # None or 0
            return

        obj = sprt.get('obj')
        if not obj:  # None or 0
            return

        #rd_w_half = self.road_w / 2
        #x_pos = [rd_w_half + self.lane_w,
        #         rd_w_half - self.lane_w]

        sprt_x = obj.rect.left
        sprt_w = obj.rect.width
        car_x = self.player_x
        car_w = self.car.rect.width * 2

        sprt_at = 10000
        if x_i == 0:
            sprt_at = 40
        elif x_i == 1:
            sprt_at = -40
        elif x_i == 2:
            sprt_at = 580
        elif x_i == 3:
            sprt_at = -580
        elif x_i == 4:
            sprt_at = 1100
        elif x_i == 5:
            sprt_at = -1100

        #print 'sprt_x', sprt_x
        #print 'car_x', car_x
        #print 'car_w', car_w
        #print 'sprt_at', (car_x - car_w / 2), sprt_at, (car_x + car_w / 2)
        #print '-' * 40

        w_half = car_w / 2 + sprt_w / 2

        #if (car_x + car_w / 2) < sprt_x < (car_x + car_w / 2):
        if (car_x - w_half) < sprt_at < (car_x + w_half):
            self.score += scr


    def check_tm(self):
        if self.position > self.seg_len * 2:
            if self.tm_start == 0.0:
                self.tm_start = time.time()
                self.tm_end = self.tm_start
            else:
                self.tm_end = time.time()
                self.tm_last_once = self.tm_end - self.tm_start
        else:
            self.tm_start = 0.0
            #self.tm_end = 0.0


    def update_bg(self):

        # always move the cloud
        for sky in self.bg_sky:
            sky.rect.left -= 1#self.sky_speed

            if sky.rect.left + sky.rect.width < 0:
                sky.rect.left += sky.rect.width * 2
            if sky.rect.left - sky.rect.width > 0:
                sky.rect.left -= sky.rect.width * 2

        if self.speed <= 0.0:
            return

        p_curve = self.player_seg.get('curve', 0.0)
        #p_curve = 3
        #print 'p_curve', p_curve

        p_dt = self.speed * p_curve * self.centrifugal
        #p_dt = 40
        #p_dt = -40
        #p_dt = random.randint(-100, 100)
        #print p_dt

        for sky in self.bg_sky:
            #print sky
            sky.rect.left += int(self.sky_speed * p_dt)

            # always move the cloud
            #sky.rect.left -= self.sky_speed

            if sky.rect.left + sky.rect.width < 0:
                sky.rect.left += sky.rect.width * 2
            if sky.rect.left - sky.rect.width > 0:
                sky.rect.left -= sky.rect.width * 2

        for hill in self.bg_hills:
            hill.rect.left += int(self.hill_speed * p_dt)
            if hill.rect.left + hill.rect.width < 0:
                hill.rect.left += hill.rect.width * 2
            if hill.rect.left - hill.rect.width > 0:
                hill.rect.left -= hill.rect.width * 2

        for trees in self.bg_trees:
            trees.rect.left += int(self.tree_speed * p_dt)
            if trees.rect.left + trees.rect.width < 0:
                trees.rect.left += trees.rect.width * 2
            if trees.rect.left - trees.rect.width > 0:
                trees.rect.left -= trees.rect.width * 2



class FPSptRoadMap(sptdraw.SptDrawBase):
    def __init__(self, size, segs, rad, *args, **kwargs):
        super(FPSptRoadMap, self).__init__(size)

        self.segs = segs
        self.rad = rad

        #self.fill(consts.WHITE)

        self.draw_segs(self.segs, self.rad)

    def xy_to_cntr(self, x, y):
        return [self.size[0] / 2 + x, self.size[1] / 2 - y]

    def cv_to_engl(self, curve, rad):
        a = float(curve) / rad
        #a *= 10.0
        #print a

        s = 1.0
        if a < 0.0:
            s = -1.0

        if a < -1.0:
            a = -1.0
        elif a > 1.0:
            a = 1.0

        #tht_d = math.acos(a)
        tht_d = math.asin(a)
        return tht_d

    def get_segs_pnts(self, segs, rad):
        pnts = []

        x, y = 0.0, 0.0
        tht = 0.0
        rad_m = 4.0#2.0#1.0#

        cv_s = 0
        cv_l = 0.0

        pnts.append([x, y])

        for seg in segs:
            curve = seg.get('curve', 0.0)
            if curve == 0.0:

                if cv_s:
                    tht_d = self.cv_to_engl(cv_l, rad)
                    #tht += tht_d
                    tht -= tht_d
                    rad_m = 20.0#10.0#50.0#

                    cv_s = 0
                    cv_l = 0.0
                else:
                    rad_m = 0.5#1.0#0.1#
            else:

                if cv_s:
                    cv_l += curve

                else:
                    cv_s = 1

                continue

            x += rad_m * math.cos(tht)
            y += rad_m * math.sin(tht)

            pnts.append([x, y])

        #print pnts
        return pnts

    def get_segs_pnts_1(self, segs, rad):
        pnts = []

        x, y = 0.0, 0.0
        tht = 0.0
        rad_m = 4.0#2.0#1.0#

        pnts.append([x, y])

        for seg in segs:
            curve = seg.get('curve', 0.0)

            if curve == 0.0:
                rad_m = 1.0#0.1#

            else:
                a = float(curve) / rad
                a *= 10.0
                #print a
                if a < -1.0:
                    a = -1.0
                elif a > 1.0:
                    a = 1.0

                #tht_d = math.acos(a)
                tht_d = math.asin(a)  # TODO:
                tht += tht_d

                rad_m = 10.0#50.0#

            x += rad_m * math.cos(tht)
            y += rad_m * math.sin(tht)

            pnts.append([x, y])

        #print pnts
        return pnts


    def draw_segs(self, segs, rad):
        pnts = self.get_segs_pnts(segs, rad)
        #print pnts

        if len(pnts) <= 1:
            return

        #if len(pnts) > 0:
        #    pnts.append(pnts[0])

        cpnts = [self.xy_to_cntr(p[0], p[1]) for p in pnts]

        c = utils.clr_from_str(FP_COLOR_BLUE)

        #self.pygm.draw.polygon(self.surf, c, cpnts)
        self.pygm.draw.lines(self.surf, c, False, cpnts, 3)


class FPSptProgress(sptdraw.SptDrawBase):
    def __init__(self, size, c_bg=consts.BLUE, c_prog=consts.GREEN):
        super(FPSptProgress, self).__init__(size)

        self.c_bg = c_bg
        self.c_prog = c_prog

        self.progress(0.0)

    def progress(self, prog):
        y = self.size[1] * prog

        self.fill(self.c_bg)

        #self.pygm.draw.rect(self.surf, consts.GREEN,
        #                    [1, 0, self.size[0] - 2, y])

        # from down to up
        self.pygm.draw.rect(self.surf, self.c_prog,
                            [1, self.size[1] - y,
                             self.size[0] - 2, y])


class FPStraight(pygm.PyGMSprite):
    def __init__(self, cfg, *args, **kwargs):
        super(FPStraight, self).__init__()

        self.cfg = cfg

        self.bg_sky1 = FPSptBg('img_flatpath/images/background.png',
                              IMG_POS_BACKGROUND['SKY'])
        self.bg_sky1.rect.top = 0
        self.bg_sky1.rect.left = 0
        self.disp_add(self.bg_sky1)

        self.bg_sky2 = FPSptBg('img_flatpath/images/background.png',
                              IMG_POS_BACKGROUND['SKY'])
        self.bg_sky2.rect.top = 0
        self.bg_sky2.rect.left = self.bg_sky1.rect.width
        self.disp_add(self.bg_sky2)

        self.bg_hills1 = FPSptBg('img_flatpath/images/background.png',
                                IMG_POS_BACKGROUND['HILLS'])
        self.bg_hills1.rect.top = 0
        self.bg_hills1.rect.left = 0
        self.disp_add(self.bg_hills1)

        self.bg_hills2 = FPSptBg('img_flatpath/images/background.png',
                                IMG_POS_BACKGROUND['HILLS'])
        self.bg_hills2.rect.top = 0
        self.bg_hills2.rect.left = self.bg_hills1.rect.width
        self.disp_add(self.bg_hills2)

        self.bg_trees1 = FPSptBg('img_flatpath/images/background.png',
                                IMG_POS_BACKGROUND['TREES'])
        self.bg_trees1.rect.top = 0
        self.bg_trees1.rect.left = 0
        self.disp_add(self.bg_trees1)

        self.bg_trees2 = FPSptBg('img_flatpath/images/background.png',
                                IMG_POS_BACKGROUND['TREES'])
        self.bg_trees2.rect.top = 0
        self.bg_trees2.rect.left = self.bg_trees1.rect.width
        self.disp_add(self.bg_trees2)

        self.car = FPSptSprts('img_flatpath/images/sprites.png',
                              IMG_POS_SPRITES['PLAYER_STRAIGHT'])
        #print self.road.cameraDepth/self.road.playerZ
        #self.car.scale(self.road.cameraDepth/self.road.playerZ)
        self.car.scale(2)
        self.car.rect.top = 400
        self.car.rect.left = (640 - self.car.rect.width) / 2
        ##self.disp_add(self.car)  # car disp add after road

        #self.road = FPSptRoad((640, 240), self.cfg)
        self.road = FPSptRoadB((640, 240), self.cfg,
                               car=self.car,
                               bg_sky=[self.bg_sky1, self.bg_sky2],
                               bg_hills=[self.bg_hills1, self.bg_hills2],
                               bg_trees=[self.bg_trees1, self.bg_trees2])
        self.road.rect.top = 240
        self.road.rect.left = 0
        self.disp_add(self.road)

        self.disp_add(self.car)

        self.rdmap = FPSptRoadMap((480, 480),
                                  self.road.rd_get_segs(whole=True),
                                  self.road.seg_len)
        self.rdmap.rect.top = 0
        self.rdmap.rect.left = 80
        self.rdmap.rotate(90)
        self.disp_add(self.rdmap)

        self.rdpsd = pygm.SptLbl(str(int(self.road.speed)),
                                 c=consts.GREEN, font_size=12)
        self.rdpsd.rect.top = 456
        self.rdpsd.rect.left = 312
        self.disp_add(self.rdpsd)

        self.scr = pygm.SptLbl(str(int(self.road.score)),
                               c=consts.RED, font_size=16)
        self.scr.rect.top = 40#454
        self.scr.rect.left = 600
        self.disp_add(self.scr)

        self.tm_once = pygm.SptLbl(str(int(self.road.tm_last_once)),
                                   c=consts.YELLOW, font_size=16)
        self.tm_once.rect.top = 20#454
        self.tm_once.rect.left = 600
        self.disp_add(self.tm_once)

        self.prog = FPSptProgress((4, 100), c_prog=consts.YELLOW)
        self.prog.rect.top = 70#340
        self.prog.rect.left = 610
        #self.prog.rotate(180)
        self.disp_add(self.prog)

        self.spd = FPSptProgress((4, 100), c_prog=consts.GREEN)
        self.spd.rect.top = 70#340
        self.spd.rect.left = 602
        #self.spd.rotate(180)
        self.disp_add(self.spd)


    def rdmap_hide(self):
        self.rdmap.hide()

    def rdmap_reset(self):
        self.rdmap.clear()
        self.rdmap.draw_segs(self.road.rd_get_segs(whole=True),
                             self.road.seg_len)
        self.rdmap.rotate(90)

    def road_reset(self):
        self.road.rd_reset()
        self.rdmap_reset()

    def road_reset_keep_segs(self):
        self.road.rd_reset(init=False, keep_segs=True)

    def road_reset_from_file(self, segs_file='sr_roads/sr_road.txt'):
        segs_file = utils.dir_abs(segs_file, __file__)
        self.road.rd_reset(init=False, keep_segs=False,
                           segs_file=segs_file)
        self.rdmap_reset()

    def road_segs_to_file(self, segs_file=None):
        if not segs_file:
            segs_file = 'sr_roads/sr_road_' + str(int(time.time())) + '.txt'
        segs_file = utils.dir_abs(segs_file, __file__)
        self.road.rd_seg_json_save(segs_file)


    def handle_event(self, events, *args, **kwargs):
        #return events

        r_events = []

        for event in events:
            #print event
            if event.type == self.pglc.KEYUP:
                k = event.key
                if k == self.pglc.K_SPACE:
                    # hide / show road map
                    self.rdmap_hide()

                elif k == self.pglc.K_RETURN:
                    self.road_reset()

                elif k == self.pglc.K_TAB:
                    self.road_reset_keep_segs()

                elif k == self.pglc.K_BACKSPACE:
                    self.road_reset_from_file()

                elif k == self.pglc.K_SLASH:
                    self.road_segs_to_file()

                else:
                    r_events.append(event)
            elif event.type == self.pglc.KEYDOWN:
                r_events.append(event)
            else:
                r_events.append(event)

        return r_events


    def refresh(self, fps_clock, *args, **kwargs):
        self.rdpsd.lbl_set(str(int(self.road.speed)))

        self.scr.lbl_set(str(int(self.road.score)))

        self.tm_once.lbl_set(str(int(self.road.tm_last_once)))

        prg = self.road.position / self.road.track_len
        self.prog.progress(prg)

        spdc = self.road.speed / self.road.speed_max
        self.spd.progress(spdc)


class FPSceneA(pygm.PyGMScene):
    def __init__(self, *args, **kwargs):
        super(FPSceneA, self).__init__(*args, **kwargs)

        self.straight = FPStraight({})
        self.straight.rect.top = 0
        self.straight.rect.left = 0
        self.disp_add(self.straight)

        ''''
        self.sn1 = SptTmpx((200, 200))
        self.sn1.rect.top = 100
        self.sn1.rect.left = 100
        self.disp_add(self.sn1)
        '''

        '''
        self.lb1 = pygm.SptLbl('hello,', c=consts.GREEN, font_size=32)
        self.lb1.rect.top = 200
        self.lb1.rect.left = 100
        self.disp_add(self.lb1)
        '''

    def handle_event(self, events, *args, **kwargs):
        return events

    def refresh(self, fps_clock, *args, **kwargs):
        pass


class GMFlatpath(pygm.PyGMGame):
    def __init__(self, title, winw, winh, *args, **kwargs):
        super(GMFlatpath, self).__init__(title, winw, winh)

        bk_im = utils.dir_abs('starfish/data/img_bk_1.jpg', __file__)
        #self.bk = pygm.SptImg('data/img_bk_1.jpg')
        self.bk = pygm.SptImg(bk_im)
        self.bk.rect.top = -230
        self.bk.rect.left = -230
        #self.disp_add(self.bk)

        self.scn1 = FPSceneA()
        self.disp_add(self.scn1)

        road_file = kwargs.get('road_file')
        if road_file:
            self.scn1.straight.road_reset_from_file(segs_file=road_file)


def main():
    #sf = GMFlatpath('flatpath <:::>', 640, 480)
    sf = GMFlatpath('flatpath <:::>', 640, 480, road_file='sr_road.txt')
    sf.mainloop()


if __name__ == '__main__':
    main()
