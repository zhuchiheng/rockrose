"""
Hillside, go forward forever.

http://codeincomplete.com/posts/javascript-racer/
http://www.extentofthejam.com/pseudo/
http://pixel.garoux.net/screen/game_list

Usage:
* UP/DOWN/LEFT/RIGHT or (j k n / f d v)
* TAB : replay this road
* RETURN : go to a new road
* BACKSLASH (\): save road to file (named by time)
* BACKSPACE (<-): load saved road file
* SPACE : hide/show road map
* SLASH (/): hide/show road sprites
* PERIOD (.): hide/show road sides
* U (u): change score to gas

TODO:

"""

import math
import random
import time

from starfish import pygm
from starfish import consts
from starfish import sptdraw
from starfish import utils


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


FP_ROAD_SIDES_IMG = 'img_flatpath/images/sprites.png'

FP_ROAD_SIDES = [
    'TREE1',
    'TREE2',
    'PALM_TREE',
    'DEAD_TREE1',
    'DEAD_TREE2',
    'BUSH1',
    'BUSH2',
    'STUMP',
    'CACTUS',
    'BOULDER1',
    'BOULDER2',
    'BOULDER3',
    'COLUMN',
    'BILLBOARD01',
    'BILLBOARD02',
    'BILLBOARD03',
    'BILLBOARD04',
    'BILLBOARD05',
    'BILLBOARD06',
    'BILLBOARD07',
    'BILLBOARD08',
    'BILLBOARD09',
]


FP_COLOR_WHITE = '#FFFFFF'
FP_COLOR_BLACK = '#000000'
FP_COLOR_YELLOW = '#EEEE00'
FP_COLOR_BLUE = '#00EEEE'


FP_COLORS = {
  'SKY':  '#72D7EE',
  'TREE': '#005108',
  'FOG':  '#005108',
  'LIGHT':  {'road': '#6B6B6B', 'grass': '#10AA10', 'rumble': '#555555', 'lane': '#CCCCCC'},
  #'LIGHT':  {'road': '#6B6B6B', 'grass': '#FF0000', 'rumble': '#555555', 'lane': '#CCCCCC'},
  'DARK':   {'road': '#696969', 'grass': '#009A00', 'rumble': '#BBBBBB'                   },
  #'DARK':   {'road': '#696969', 'grass': '#0000FF', 'rumble': '#BBBBBB'                   },
  'START':  {'road': FP_COLOR_WHITE,   'grass': FP_COLOR_WHITE,   'rumble': FP_COLOR_WHITE},
  'FINISH': {'road': FP_COLOR_BLACK,   'grass': FP_COLOR_BLACK,   'rumble': FP_COLOR_BLACK},
  'START_Y':  {'road': FP_COLOR_YELLOW, 'grass': '#10AA10', 'rumble': '#555555', 'lane': '#CCCCCC'},
}


FP_ROAD = {
  'LENGTH': {'NONE': 0, 'SHORT':  25, 'MEDIUM':  50, 'LONG':  100 }, # num segments
  'CURVE':  {'NONE': 0, 'EASY':    2, 'MEDIUM':   4, 'HARD':    6 },
  'HILL':   {'NONE': 0, 'LOW':    20, 'MEDIUM':  40, 'HIGH':   60 },
  #'HILL':   {'NONE': 0, 'LOW':    2, 'MEDIUM':  4, 'HIGH':   6 },
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
        self.fill(self.c)

        d = 2
        n = self.h / d
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


class FPSptRdSides(pygm.SptImgOne):
    def __init__(self, img_file, pos, *args, **kwargs):
        super(FPSptRdSides, self).__init__(img_file, pos)

    @classmethod
    def create_by_img(cls, img, pos):
        return cls(img, pos)


class FPRoadSprts(pygm.PyGMSprite):
    def __init__(self, *args, **kwargs):
        super(FPRoadSprts, self).__init__(*args, **kwargs)


class FPRoadSides(pygm.PyGMSprite):
    def __init__(self, *args, **kwargs):
        super(FPRoadSides, self).__init__(*args, **kwargs)


class FPSptRoadGround(sptdraw.SptDrawBase):

    def __init__(self, size, cfg, *args, **kwargs):
        super(FPSptRoadGround, self).__init__(size)

        self.cfg = cfg

    def render_polygon(self, ctx, x1, y1, x2, y2, x3, y3, x4, y4, color):

        y1 = utils.math_round(y1)
        y2 = utils.math_round(y2)
        y3 = utils.math_round(y3)
        y4 = utils.math_round(y4)

        pnts = [[x1, y1], [x2, y2], [x3, y3], [x4, y4], [x1, y1]]

        c = utils.clr_from_str(color)

        try:
            self.pygm.draw.polygon(self.surf, c, pnts)
        except Exception as e:
            #print '-' * 60
            pass


class FPSptRoadB(sptdraw.SptDrawBase):

    def __init__(self, size, cfg, *args, **kwargs):
        super(FPSptRoadB, self).__init__(size)

        self.cfg = cfg

        #self.fog = kwargs.get('fog')

        self.rd_ground = kwargs.get('grd')
        self.rd_sprts = kwargs.get('sprts')
        self.rd_sides = kwargs.get('sides')

        self.car = kwargs.get('car')

        self.bg_sky = kwargs.get('bg_sky')
        self.bg_hills = kwargs.get('bg_hills')
        self.bg_trees = kwargs.get('bg_trees')

        self.clr_dark_road = utils.clr_from_str(FP_COLORS['DARK']['road'])
        self.clr_dark_grass = utils.clr_from_str(FP_COLORS['DARK']['grass'])

        self.fog = None

        self.rd_reset(init=True)

        self.add_fog()


    def prms_reset(self, keep_segs=False):
        self.e_keys_up = []
        self.e_keys_dn = []

        self.camera_x = 0.0
        self.camera_y = 0.0
        self.camera_z = 0.0

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

        self.cv_max = 8.0#10.0#6.0
        self.wy_max = 30.0#4.8#

        self.d = 230.0#200.0#100.0#1000.0#30.0#80.0#500##10.0##1.0#

        self.w = self.size[0]
        self.h = self.size[1]


        if not keep_segs:
            self.segments = []

            self.rd_sprt_objs = {}
            self.rd_sprt_cache = []  # for sprites render order
            self.rd_sprt_objs_be = {}
            self.rd_sprt_cache_be = []  # for sprites render order
            self.flag_show_rd_sprts = True

            self.rd_side_objs = {}
            self.rd_side_cache = []  # for sides render order
            self.rd_side_objs_be = {}
            self.rd_side_cache_be = []  # for sides render order
            self.flag_show_rd_sides = False

            self.track_len = 0.0

            self.gas_max = 0.0


        self.seg_len = 200.0#100.0#300.0#400.0##100.0#20.0#60.0#200.0#
        self.road_w = 2000.0#2400#600.0#200.0#1000.0#200#
        self.camera_h = 1000.0#500.0#400.0#800.0#200#  ==  self.camera_z

        self.speed_max = 500.0#300.0#180.0#200.0#100.0

        self.field_of_view = 100.0
        self.camera_depth = 1.0 / math.tan(self.field_of_view / 2. * math.pi / 180.)  #0.83909963117728

        self.lanes = 3
        self.lane_w = 60

        self.rumble_len  = 2#3


        self.seg_n = 300#200
        self.seg_draw_n = 150#130#200#100#70#30#100#200###


        self.position = 0.0

        self.player_x = 0.0#100.0#1000.0#
        self.player_z = None  # player relative z distance from camera (computed)


        self.centrifugal = 0.025#0.1#0.2#0.3#0.06#0.08#0.01#

        self.player_seg = None

        self.base_seg = None  # the segment just under the car


        self.player_di = 0 # 0:^ 1:> 2:v 3:<

        self.player_go = 0 # 0:- 1:^ 2:v


        self.speed = 0.0

        self.speed_dt_up = 1.0#2.0#3.0
        self.speed_dt_dn = 4.0#3.0#2.0#6.0
        self.speed_dt_na = 1.0#3.0

        self.player_x_dt = 60.0#30.0#20.0

        self.flag_hill_up = False

        self.last_seg_i = 0

        #self.gas_max = 0.0
        self.gas = self.gas_max
        self.gas_dt_dn = 2.0

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
            self.rd_sides_del_all_objs()

        self.prms_reset(keep_segs=keep_segs)

        if segs_file is not None:
            try:
                segs = self.rd_seg_json_load(segs_file)

                self.segments = segs
                self.track_len = len(self.segments) * self.seg_len
                #self.rd_car_gas_init()
            except Exception as e:
                print e
                self.init_rd_segs_rand_1()

        else:
            if not keep_segs:
                self.init_rd_segs_rand_1()

        # always re-init gas
        self.rd_car_gas_init()

        self.rd_ground.clear()
        self.clear()

        self.rd_seg_render()


    def init_rd_segs_rand_1(self):
        #self.rd_seg_init(self.seg_n)
        #self.rd_seg_init(self.seg_draw_n)
        #self.rd_seg_init(100)#20#500#2#10#4#1#100#200
        self.rd_seg_init(random.randint(30, 100))

        #self.add_curves()

        #self.add_low_rolling_hills(20, 2.0)
        #self.add_low_rolling_hills(20, 3.4)
        ##self.add_low_rolling_hills(20, 4.8)
        #self.add_low_rolling_hills(10, 4.5)#o#
        #self.add_low_rolling_hills(20, 2.4)
        #o#self.add_low_rolling_hills(20, 20.0)#24)
        #self.add_low_rolling_hills(30, 4.0)

        ##self.rd_seg_init_rand(10)#50#10#3#1
        segnrand = random.randint(3, 70)
        self.rd_seg_init_rand(segnrand)

        # for segment draw
        #self.rd_seg_init(self.seg_draw_n)
        self.rd_seg_init(100)#20#500#2#10#4#1#100#200

        ##self.test_rd_add_hill()

        self.rd_car_gas_init()

        self.rd_start_seg_init(n=3, a=3)

        self.rd_sprts_init_rand()

        self.rd_sides_init_rand()


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


    def rd_seg_init(self, a=500):

        for n in range(a):
            self.rd_seg_add(0.0, 0.0)


    def rd_seg_add(self, curve=0.0, yw=0.0):

        n = len(self.segments)
        #print n

        #if n % 2 == 0:
        #if n % 4 == 0:
        if math.floor(n / self.rumble_len) % 2 == 0:
            c = FP_COLORS['LIGHT']
        else:
            c = FP_COLORS['DARK']

        seg = {
            'index': n,

            'p1': {'world': {'z': (n + 1) * self.seg_len,
                             'y': self.seg_lasy_y()},
                   'camera': {'z': self.camera_h},
                   'screen': {}},
            'p2': {'world': {'z': (n + 2) * self.seg_len,
                             'y': yw},
                   'camera': {'z': self.camera_h},
                   'screen': {}},

            'curve': curve,
            'color': c,
            'sprites': [],
            'sides': [],
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
            elif p < 0.5:
                curve = 0.0
                #yw = random.random() * 30.0#10.0
                #yw = random.random() * 2.4#5.0#4.0#2.0
                yw = rl * random.random() * self.wy_max
            else:
                #curve = rl * random.random() * 6.0
                curve = rl * random.random() * self.cv_max
                #curve = 0.0
                yw = 0.0

            self.add_road(enter, hold, leave, curve, yw)

            # for back to water level
            if yw != 0.0:
                self.add_road(enter, hold, leave, curve, -yw)


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



    def rd_car_gas_init(self):
        segn = len(self.segments)
        #self.gas_max = segn * self.road_w * 2.0
        #self.gas_max = segn * 2.0
        self.gas_max = segn * (random.random() + 1.0)  #1.2#1.1#
        #print self.gas_max

        if self.gas_max < 1000.0:
            self.gas_max *= 1.1
        elif self.gas_max > 10000.0:
            self.gas_max *= 0.5
        else:
            self.gas_max *= 0.7

        #print self.gas_max
        self.gas = self.gas_max


    def rd_score_to_gas(self, per=10):
        if self.score >= per:
            gas_add = per * (random.random() + 3.0)
            self.gas_max += gas_add
            self.gas += gas_add
            self.score -= per


    def rd_start_seg_init(self, n=3, a=0):
        seg_n = len(self.segments)
        if seg_n == 0:
            return

        #self.segments[0]['color'] = FP_COLORS['START_Y']
        #self.segments[2]['color'] = FP_COLORS['START_Y']

        for i in range(a, a + n):
            self.segments[i]['color'] = FP_COLORS['START_Y']


    def rd_sprts_init_rand(self, n=None):
        seg_n = len(self.segments)
        if n is None:
            #n = seg_n / 20
            n = seg_n / random.randint(10, 30)

        for i in range(n):
            j = random.randint(10, seg_n - 10)
            sprt = random.choice(FP_ROAD_SPRTS.keys())

            s = {
                'name': sprt,
                'type': 1,  # image / animate / ...
                'obj': None,  # need to create at render
                'x_i': random.randint(0, 4),
                'score': FP_ROAD_SPRTS[sprt].get('score', 0),
            }
            self.segments[j]['sprites'].append(s)


    def rd_sides_init_rand(self, n=None):
        seg_n = len(self.segments)
        if n is None:
            #n = seg_n / 20
            n = seg_n / random.randint(10, 30)

        for i in range(n):
            j = random.randint(10, seg_n - 10)
            sprt = random.choice(FP_ROAD_SIDES)

            s = {
                'name': sprt,
                'type': 1,  # image / animate / ...
                'obj': None,  # need to create at render
                'x_i': random.randint(0, 1),
                'score': 0,
            }
            self.segments[j]['sides'].append(s)


    # util functions from js

    def util_limit(self, value, mn, mx):
        return max(mn, min(value, mx))

    def util_accelerate(self, v, accel, dt):
        return v + (accel * dt)

    def util_interpolate(self, a, b, percent):
        return float(a) + float(b - a) * percent

    def util_increase(self, start, increment, mx): # with looping
        result = start + increment
        while (result >= mx):
          result -= mx
        while (result < 0):
          result += mx
        return result


    def util_project(self, p, camera_x, camera_y, camera_z, camera_depth,
                     width, height, road_width):

        camera_x = float(camera_x)
        camera_y = float(camera_y)
        camera_z = float(camera_z)
        camera_depth = float(camera_depth)
        width = float(width)
        height = float(height)
        road_width = float(road_width)

        p['camera']['x'] = float(p['world'].get('x', 0.0)) - camera_x
        p['camera']['y'] = float(p['world'].get('y', 0.0)) - camera_y
        p['camera']['z'] = float(p['world'].get('z', 0.0)) - camera_z

        p['screen']['scale'] = camera_depth / p['camera']['z']

        p['screen']['x'] = utils.math_round((width / 2.) + (p['screen']['scale'] * p['camera']['x'] * width/2.))
        p['screen']['y'] = utils.math_round((height / 2.) - (p['screen']['scale'] * p['camera']['y'] * height/2.))
        p['screen']['w'] = utils.math_round((p['screen']['scale'] * road_width * width/2.))

        #p['screen']['x'] = (width / 2.) + (p['screen']['scale'] * p['camera']['x'] * width/2.)
        #p['screen']['y'] = (height / 2.) - (p['screen']['scale'] * p['camera']['y'] * height/2.)
        #p['screen']['w'] = (p['screen']['scale'] * road_width * width/2.)

        #p['screen']['x'] = utils.math_floor((width / 2.) + (p['screen']['scale'] * p['camera']['x'] * width/2.))
        #p['screen']['y'] = utils.math_floor((height / 2.) - (p['screen']['scale'] * p['camera']['y'] * height/2.))
        #p['screen']['w'] = utils.math_floor((p['screen']['scale'] * road_width * width/2.))

    def util_overlap(self, x1, w1, x2, w2, percent):
        half = (percent or 1.0) / 2.0
        min1 = x1 - (w1*half)
        max1 = x1 + (w1*half)
        min2 = x2 - (w2*half)
        max2 = x2 + (w2*half)
        return not ((max1 < min2) or (min1 > max2))

    def util_ease_in(self, a, b, percent):
        return a + (b - a) * math.pow(percent, 2)

    def util_ease_out(self, a, b, percent):
        return a + (b - a) * (1 - math.pow(1 - percent, 2))

    def util_ease_in_out(self, a, b, percent):
        return a + (b - a) * ((-math.cos(percent * math.pi)/2) + 0.5)


    def util_curve_percent_remaining(self, n, total):
        return float(n % total) / total



    def add_road(self, enter, hold, leave, curve, yw=0.0):
        #print enter, hold, leave, curve, yw

        start_y = self.seg_lasy_y()
        #end_y = start_y + (int(yw) * self.seg_len)
        end_y = start_y + (yw * self.seg_len)
        total = enter + hold + leave

        for n in range(enter):
            #self.rd_seg_add(self.util_ease_in(0, curve, float(n)/enter),
            self.rd_seg_add(self.util_ease_in_out(0, curve, float(n)/enter),
                            self.util_ease_in_out(start_y, end_y, float(n)/total))

        for n in range(hold):
            self.rd_seg_add(curve,
                            self.util_ease_in_out(start_y, end_y, float(enter+n)/total))

        for n in range(leave):
            #self.rd_seg_add(self.util_ease_out(curve, 0, n/leave),
            self.rd_seg_add(self.util_ease_in_out(curve, 0, n/leave),
                            self.util_ease_in_out(start_y, end_y, float(enter+hold+n)/total))


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


    def add_low_rolling_hills__0(self, num, height):
        num = num or FP_ROAD['LENGTH']['SHORT']
        height = height or FP_ROAD['HILL']['LOW']

        self.add_road(num, num, num, 0,  height/2.0)
        self.add_road(num, num, num, 0, -height)
        self.add_road(num, num, num, 0,  height)
        self.add_road(num, num, num, 0,  0)
        self.add_road(num, num, num, 0,  height/2.0)
        self.add_road(num, num, num, 0,  0)


    def add_low_rolling_hills(self, num, height):
        num = num or FP_ROAD['LENGTH']['SHORT']
        height = height or FP_ROAD['HILL']['LOW']

        self.add_road(num, num, num, 0,  height)
        self.add_road(num, num, num, 0, -height)
        self.add_road(num, num, num, 0,  height/2.0)
        self.add_road(num, num, num, 0,  -height/2.0)


    def add_low_rolling_hills__1(self, num, height):
        num = 40
        up = 40#10
        dn = 50#13#20

        for i in range(num):
            #self.rd_seg_add(0.0, float(i))
            #self.rd_seg_add(0.0, float(i) * 30)
            #self.rd_seg_add(0.0, -float(i) * 30)
            #self.rd_seg_add(0.0, -float(i) * 20)
            self.rd_seg_add(0.0, -float(i) * up)

        for i in range(num):
            #self.rd_seg_add(0.0, float(num - 1 - i))
            #self.rd_seg_add(0.0, float(num - 1 - i) * 30)
            #self.rd_seg_add(0.0, -float(num - 1 - i) * 30)
            #self.rd_seg_add(0.0, -float(num - 1 - i) * 20)
            self.rd_seg_add(0.0, -float(num - 1 - i) * up)

        for i in range(num):
            #self.rd_seg_add(0.0, float(i))
            ##self.rd_seg_add(0.0, float(i) * 40)
            self.rd_seg_add(0.0, float(i) * dn)
            #self.rd_seg_add(0.0, -float(i) * 30)
            #self.rd_seg_add(0.0, -float(i) * 20)

        for i in range(num):
            #self.rd_seg_add(0.0, float(num - 1 - i))
            ##self.rd_seg_add(0.0, float(num - 1 - i) * 40)
            self.rd_seg_add(0.0, float(num - 1 - i) * dn)
            #self.rd_seg_add(0.0, -float(num - 1 - i) * 30)
            #self.rd_seg_add(0.0, -float(num - 1 - i) * 20)


    def test_rd_add_hill__1(self):
        self.segments[10]['p2']['world']['y'] = 100.0
        self.segments[11]['p1']['world']['y'] = 100.0

        self.segments[11]['p2']['world']['y'] = 200.0
        self.segments[12]['p1']['world']['y'] = 200.0

        self.segments[12]['p2']['world']['y'] = 300.0
        self.segments[13]['p1']['world']['y'] = 300.0

        self.segments[13]['p2']['world']['y'] = 200.0
        self.segments[14]['p1']['world']['y'] = 200.0

        self.segments[14]['p2']['world']['y'] = 100.0
        self.segments[15]['p1']['world']['y'] = 100.0


    def test_rd_add_hill(self):
        n = 40#100#20
        hm = 600.0#1000.0#400.0#300.0#
        for i in range(n):
            a = float(i) / float(n) * math.pi #/ 2.0
            #print math.sin(a)
            wy = math.sin(a) * hm
            print wy
            self.segments[10 + i]['p2']['world']['y'] = wy
            self.segments[11 + i]['p1']['world']['y'] = wy


    # for save json road

    def rd_seg_get_cleared(self, segs=None):
        if not segs:
            segs = self.segments

        segs_c = []
        for seg in segs:
            if (not seg['sprites']) and (not seg['sides']):
                segs_c.append(seg)
            else:
                seg_c = {}
                for k, v in seg.items():
                    if k not in ['sprites', 'sides']:
                        seg_c[k] = v
                    else:
                        seg_c[k] = []
                        for spr in seg[k]:
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



    # #### geometry #### #

    def geo_prjc_scale(self, d, zc):
        if zc == 0.0:
            return 1.0
        else:
            return float(d) / float(zc)

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
        #xs = w + xp 
        return xs

    def yp_to_ys(self, yp, h):
        #ys = h / 2.0 - h / 2.0 * yp 
        ys = h / 2.0 + h / 2.0 * yp 
        #ys = h / 2.0 - yp
        #if ys < 0:
        #    ys += h
        #o#ys = h / 2.0 + yp #- 300
        #ys = h - yp 
        #ys = yp
        #ys = (h / 2.0 - yp + h) % h
        return ys


    # render road


    def rd_sprts_load_all_objs(self):
        pass

    def rd_sprts_del_all_objs(self):
        for k, sprt in self.rd_sprt_objs.items():
            #print k, sprt
            self.disp_del(sprt)
            del self.rd_sprt_objs[k]
        for k, sprt in self.rd_sprt_objs_be.items():
            self.rd_sprts.disp_del(sprt)
            del self.rd_sprt_objs_be[k]

    def rd_sides_del_all_objs(self):
        for k, sprt in self.rd_side_objs.items():
            #print k, sprt
            self.disp_del(sprt)
            del self.rd_side_objs[k]
        for k, sprt in self.rd_side_objs_be.items():
            self.rd_sides.disp_del(sprt)
            del self.rd_side_objs_be[k]


    #def rd_seg_render__r9_oo(self):
    def rd_seg_render(self):
        
        #if self.speed <= 0.0:
        #    return

        seg_n = len(self.segments)
        segbi = self.get_seg_base_i()
        #print 'segbi', segbi, ' / ', seg_n

        self.player_seg = self.segments[segbi]
        self.base_seg = self.segments[(segbi + 4) % seg_n]
        # for test
        #self.base_seg['color'] = FP_COLORS['FINISH']
        #self.player_seg['color'] = FP_COLORS['FINISH']

        b_curve = self.player_seg.get('curve', 0.0)
        b_percent = self.util_curve_percent_remaining(self.position,
                                                      self.seg_len)

        dx_curve = - (b_curve * b_percent)
        x_curve  = 0

        b_yw1 = self.player_seg['p1']['world'].get('y', 0.0)
        b_yw2 = self.player_seg['p2']['world'].get('y', 0.0)

        # for smooth the controll
        player_x = self.player_x / 500.0  # TODO:

        player_z = self.camera_h * self.camera_depth
        #x#player_percent = self.util_curve_percent_remaining(self.position + player_z, self.seg_len)
        player_percent = self.util_curve_percent_remaining(self.position, self.seg_len)
        player_y = self.util_interpolate(b_yw1, b_yw2, player_percent)

        # for check rander
        max_y = self.h

        # clear the sprites cache
        for obj in self.rd_sprt_cache[::-1]:
            self.disp_del(obj)
        for obj in self.rd_sprt_cache_be[::-1]:
            self.rd_sprts.disp_del(obj)
        self.rd_sprt_cache = []
        self.rd_sprt_cache_be = []

        # clear the sprites cache
        for obj in self.rd_side_cache[::-1]:
            self.disp_del(obj)
        for obj in self.rd_side_cache_be[::-1]:
            self.rd_sides.disp_del(obj)
        self.rd_side_cache = []
        self.rd_side_cache_be = []


        for i in range(self.seg_draw_n):
            si = (segbi + i) % seg_n
            #print si

            seg = self.segments[si]
            segment = seg

            segment['looped'] = segment['index'] < self.player_seg['index']
            camera_z = self.position - (self.track_len if segment['looped'] else 0)

            # coordinate transmit
            self.util_project(segment['p1'],
                              (player_x * self.road_w) - x_curve - dx_curve,
                              #(player_x * self.road_w) - x_curve,
                              player_y + self.camera_h,
                              camera_z, self.camera_depth,
                              self.w, self.h, self.road_w)
            self.util_project(segment['p2'],
                              (player_x * self.road_w) - x_curve,
                              #(player_x * self.road_w) - x_curve - dx_curve,
                              player_y + self.camera_h,
                              camera_z, self.camera_depth,
                              self.w, self.h, self.road_w)

            ##x_curve  = x_curve + dx_curve
            x_curve  = x_curve - dx_curve  # NOTE: same with sandroad
            dx_curve = dx_curve + seg.get('curve', 0.0)
            #dx_curve = dx_curve + seg.get('curve', 0.0) / 10.0

            x1, y1, w1, x2, y2, w2 = \
                segment['p1']['screen']['x'], \
                segment['p1']['screen']['y'], \
                segment['p1']['screen']['w'], \
                segment['p2']['screen']['x'], \
                segment['p2']['screen']['y'], \
                segment['p2']['screen']['w']

            #if i == 10:
            #    print '-' * 40
            #    print 'player_x', player_x
            #    print 'player_z', player_z
            #    print 'player_percent', player_percent
            #    print 'b_yw1', b_yw1
            #    print 'b_yw2', b_yw2
            #    print 'player_y', player_y
            #    print 'camera_z', camera_z
            #    print 'self.camera_depth', self.camera_depth
            #    print 'world z', segment['p1']['world'].get('z', 0.0)
            #    print 'p[camerax]', segment['p1']['camera']['x']
            #    print 'p[cameray]', segment['p1']['camera']['y']
            #    print 'p[cameraz]', segment['p1']['camera']['z']
            #    print 'p[screenscale]', segment['p1']['screen']['scale']
            #    print i, x1, y1, w1, x2, y2, w2


            # check whether to render segment
            #if ((segment['p1']['camera']['z'] <= self.camera_depth) or  # behind us
            #    (segment['p2']['screen']['y'] >= segment['p1']['screen']['y']) or  # back face cull
            #    (segment['p2']['screen']['y'] >= max_y)):  # clip by (already rendered) segment
            if ((segment['p1']['camera']['z'] < self.camera_depth) or  # behind us
                (segment['p2']['screen']['y'] > segment['p1']['screen']['y']) or  # back face cull
                (segment['p2']['screen']['y'] > max_y)):  # clip by (already rendered) segment
                #continue

                # #### road back

                # render road sprites

                if seg.get('sprites') or seg.get('sides'):

                    zw1 = (i + 1) * self.seg_len
                    zw2 = (i + 2) * self.seg_len

                    zc1 = zw1 - self.camera_z - (self.position % self.seg_len)
                    zc2 = zw2 - self.camera_z - (self.position % self.seg_len)

                    seg_scale = self.geo_prjc_scale(self.d, zc1)
                    seg_scale *= 3.0#4.0

                    y_sprt = self.h - y1 - 120 #- 100


                    if i < 100 and self.flag_show_rd_sprts and seg.get('sprites'):
                        x_pos = [
                            x1,
                            x1 + w1 / 3,
                            x1 + w1 / 3 * 2,
                            x1 - w1 / 3,
                            x1 - w1 / 3 * 2,
                            x1 + w1,
                        ]

                        x_i = random.randint(0, len(x_pos) - 1)  # NOTE: not used now !!

                        scale_sprt = seg_scale * 3.3#4.0#8.0#10.0#2.0

                        #print i, y_sprt, scale_sprt

                        obj_k, obj = self.rd_sprts_render(seg, x_pos, x_i, y_sprt, scale_sprt, be=True)
                        if obj:
                            self.rd_sprt_cache_be.append(obj)
                            self.rd_sprt_objs_be[obj_k] = obj  # for reset to delete all


                    if i < 150 and self.flag_show_rd_sides and seg.get('sides'):
                        sx_pos = [
                            x1 - w1,
                            x1 + w1,
                        ]

                        obj_k, obj = self.rd_sides_render(seg, sx_pos, 0, y_sprt, seg_scale, be=True)#scale_sprt)
                        if obj:
                            self.rd_side_cache_be.append(obj)
                            self.rd_side_objs_be[obj_k] = obj  # for reset to delete all


            # #### road front
            else:
                # for check rander
                max_y = segment['p2']['screen']['y']

                # grass
                # <1> draw grass at the same surface with road
                #self.render_polygon(None,
                #                    0, y1, self.w, y1,
                #                    self.w, y2, 0, y2,
                #                    seg['color']['grass'])

                # <2> draw grass at a separated surface with road
                self.rd_ground_render(self.rd_ground,
                                      #0, y1, self.w, y1,
                                      #self.w, y2, 0, y2,
                                      0, y1+1, self.w, y1+1,
                                      self.w, y2+1, 0, y2+1,
                                      seg['color']['grass'])


                # road
                self.render_polygon(None,
                                    x1-w1, y1, x1+w1, y1, x2+w2, y2, x2-w2, y2,
                                    seg['color']['road'])


                # lanes
                lanes = self.lanes

                r1 = w1 / max(6,  2 * lanes)
                r2 = w2 / max(6,  2 * lanes)
                l1 = w1 / max(32, 8 * lanes)
                l2 = w2 / max(32, 8 * lanes)

                # rumble
                self.render_polygon(None,
                                    x1-w1-r1, y1, x1-w1, y1, x2-w2, y2, x2-w2-r2, y2,
                                    seg['color']['rumble'])

                self.render_polygon(None,
                                    x1+w1+r1, y1, x1+w1, y1, x2+w2, y2, x2+w2+r2, y2,
                                    seg['color']['rumble'])

                # lane
                if 'lane' in seg['color'].keys():
                    lanew1 = w1 * 2 / lanes
                    lanew2 = w2 * 2 / lanes
                    lanex1 = x1 - w1 #+ lanew1
                    lanex2 = x2 - w2 #+ lanew2

                    for lane in range(lanes - 1):
                        lanex1 += lanew1
                        lanex2 += lanew2
                        self.render_polygon(None,
                                            lanex1 - l1 / 2, y1, lanex1 + l1/2, y1,
                                            lanex2 + l2 / 2, y2, lanex2 - l2/2, y2,
                                            seg['color']['lane'])

                # fog
                if self.fog:
                    self.fog.rect.top = y1 - 2


                # render road sprites

                if seg.get('sprites') or seg.get('sides'):

                    zw1 = (i + 1) * self.seg_len
                    zw2 = (i + 2) * self.seg_len

                    zc1 = zw1 - self.camera_z - (self.position % self.seg_len)
                    zc2 = zw2 - self.camera_z - (self.position % self.seg_len)

                    seg_scale = self.geo_prjc_scale(self.d, zc1)
                    seg_scale *= 3.0#4.0

                    y_sprt = self.h - y1 - 120 #- 100


                    if i < 100 and self.flag_show_rd_sprts and seg.get('sprites'):
                        x_pos = [
                            x1,
                            x1 + w1 / 3,
                            x1 + w1 / 3 * 2,
                            x1 - w1 / 3,
                            x1 - w1 / 3 * 2,
                            x1 + w1,
                        ]

                        x_i = random.randint(0, len(x_pos) - 1)  # NOTE: not used now !!

                        scale_sprt = seg_scale * 3.3#4.0#8.0#10.0#2.0

                        #print i, y_sprt, scale_sprt

                        obj_k, obj = self.rd_sprts_render(seg, x_pos, x_i, y_sprt, scale_sprt)
                        if obj:
                            self.rd_sprt_cache.append(obj)
                            self.rd_sprt_objs[obj_k] = obj  # for reset to delete all


                    if i < 150 and self.flag_show_rd_sides and seg.get('sides'):
                        sx_pos = [
                            x1 - w1,
                            x1 + w1,
                        ]

                        obj_k, obj = self.rd_sides_render(seg, sx_pos, 0, y_sprt, seg_scale)#scale_sprt)
                        if obj:
                            self.rd_side_cache.append(obj)
                            self.rd_side_objs[obj_k] = obj  # for reset to delete all


        # render the sprites with right order
        if self.flag_show_rd_sprts:
            for obj in self.rd_sprt_cache[::-1]:
                self.disp_add(obj)
            for obj in self.rd_sprt_cache_be[::-1]:
                self.rd_sprts.disp_add(obj)

        # render the sprites with right order
        if self.flag_show_rd_sides:
            for obj in self.rd_side_cache[::-1]:
                self.disp_add(obj)
            for obj in self.rd_side_cache_be[::-1]:
                self.rd_sides.disp_add(obj)


    def render_polygon(self, ctx, x1, y1, x2, y2, x3, y3, x4, y4, color):

        y1 = utils.math_round(y1)
        y2 = utils.math_round(y2)
        y3 = utils.math_round(y3)
        y4 = utils.math_round(y4)

        pnts = [[x1, y1], [x2, y2], [x3, y3], [x4, y4], [x1, y1]]

        #print pnts

        c = utils.clr_from_str(color)

        try:
            self.pygm.draw.polygon(self.surf, c, pnts)
        except Exception as e:
            #print e
            #print '-' * 60
            pass


    def rd_ground_render(self, ctx, x1, y1, x2, y2, x3, y3, x4, y4, color):
        self.rd_ground.render_polygon(None, x1, y1, x2, y2, x3, y3, x4, y4, color)


    def rd_sprts_render(self, seg, x_pos, x_i, y, scale, be=False):
        sprts = seg.get('sprites')
        if not sprts:
            return None

        for i, info in enumerate(sprts):
            sprt = info['name']

            obj_k = str(seg['index']) + '_' + str(i) + '_' + sprt

            obj = info.get('obj')

            if obj:
                #pass
                if not be:
                    self.disp_del(obj)
                    # NOTE: objs will be deleted at rd_sprts_del_all_objs()
                    if obj_k in self.rd_sprt_objs.keys():
                        del self.rd_sprt_objs[obj_k]
                else:
                    self.rd_sprts.disp_del(obj)
                    # NOTE: objs will be deleted at rd_sprts_del_all_objs()
                    if obj_k in self.rd_sprt_objs_be.keys():
                        del self.rd_sprt_objs_be[obj_k]

            # create a new sprite every time for to scale
            img = FP_ROAD_SPRTS[sprt]['imgs'][0]
            obj = FPSptRdSprts.create_by_img(img)

            # avoid: pygame.error: Width or height is too large
            if scale > 5.0:#500.0:#100.0:#
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
            #^#self.rd_sprt_objs[obj_k] = obj  # for reset to delete all

            # NOTE: only show one
            break

        return obj_k, obj


    def rd_sides_render(self, seg, x_pos, x_i, y, scale, be=False):
        sprts = seg.get('sides')
        if not sprts:
            return None

        for i, info in enumerate(sprts):
            sprt = info['name']

            obj_k = str(seg['index']) + '_' + str(i) + '_' + sprt

            obj = info.get('obj')

            if obj:
                #pass
                if not be:
                    self.disp_del(obj)
                    # NOTE: objs will be deleted at rd_sides_del_all_objs()
                    if obj_k in self.rd_side_objs.keys():
                        del self.rd_side_objs[obj_k]
                else:
                    self.rd_sides.disp_del(obj)
                    # NOTE: objs will be deleted at rd_sides_del_all_objs()
                    if obj_k in self.rd_side_objs_be.keys():
                        del self.rd_side_objs_be[obj_k]

            # create a new sprite every time for to scale
            img = FP_ROAD_SIDES_IMG
            pos = IMG_POS_SPRITES[sprt]
            obj = FPSptRdSides.create_by_img(img, pos)

            # avoid: pygame.error: Width or height is too large
            #print 'scale <0>', scale
            if scale > 5.0:#2.0:#100.0:#500.0:#
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
            ##obj.rect.left = x_pos[x_i_saved] - obj.rect.width / 2
            if x_i_saved == 0:
                obj.rect.left = x_pos[x_i_saved] - obj.rect.width / 2 * 3
            else:
                obj.rect.left = x_pos[x_i_saved] + obj.rect.width / 2
            #obj.scale(scale)

            info['obj'] = obj
            ##self.disp_add(obj)  # NOTE: render out here
            #self.rd_side_objs[obj_k] = obj  # for reset to delete all

            # NOTE: only show one
            break

        return obj_k, obj


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

        self.rd_ground.clear()
        self.clear()

        self.rd_seg_render()

        self.check_at_hill_bottom()

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


    def check_at_hill_bottom(self):

        now_seg = self.base_seg#self.player_seg

        b_yw1 = now_seg['p1']['world'].get('y', 0.0)
        b_yw2 = now_seg['p2']['world'].get('y', 0.0)

        #print (b_yw2 - b_yw1) / self.wy_max

        #dy_max = self.wy_max * self.road_w  # 6000.0

        if b_yw1 < b_yw2:  # up
            if self.speed > 100.0:
                self.speed -= (b_yw2 - b_yw1) / self.wy_max  # 30.0

            #print b_yw2 - b_yw1
            if not self.flag_hill_up:
                self.flag_hill_up = True

                if self.speed > self.speed_max / 2.0:
                    if b_yw2 - b_yw1 > 4.0:
                    #if b_yw2 - b_yw1 > random.random() * 5.0 + 3.0:
                        #print b_yw2 - b_yw1
                        #print 'x' * 40
                        self.speed /= 2.0

        elif b_yw1 > b_yw2:  # down
            #if self.speed > 100.0:
            self.speed += (b_yw1 - b_yw2) / self.wy_max  # 30.0
            self.flag_hill_up = False

        else:
            self.flag_hill_up = False
            #pass

    def update_world(self):
        if self.player_go == 1 and self.gas > 0.0:
            #if self.gas > 0.0:
            self.speed += self.speed_dt_up

            self.gas -= self.gas_dt_dn
            if self.gas < 0.0:
                self.gas = 0.0
        elif self.player_go == 2:
            self.speed -= self.speed_dt_dn
        else:
            self.speed -= self.speed_dt_na

        # if on the grass, slow down
        #if self.player_x < -self.road_w / 2 or \
        #    self.player_x > self.road_w / 2:
        if self.player_x < -self.road_w / 4 - 100 or \
            self.player_x > self.road_w / 4 + 100:
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
            #self.player_x += self.speed / 5 + 20
            #self.player_x += self.speed / 10 + 10
            self.player_x += self.speed / 20 + 10
        elif self.player_di == 3:
            #self.player_x -= self.player_x_dt
            #self.player_x -= self.speed / 5 + 20
            #self.player_x -= self.speed / 10 + 10
            self.player_x -= self.speed / 20 + 10
        else:
            pass

        p_curve = self.player_seg.get('curve', 0.0)
        #print 'p_curve', p_curve
        p_dt = self.speed * p_curve * self.centrifugal
        #print p_dt
        #self.player_x -= p_dt
        self.player_x += p_dt  # NOTE: same with sandroad


    def check_if_car_out_road(self):
        #print self.player_x

        # decrease score when go out the road
        #if self.player_x < -self.road_w / 2 or \
        #    self.player_x > self.road_w / 2:
        if self.player_x < -self.road_w / 4 - 100 or \
            self.player_x > self.road_w / 4 + 100:

            if self.player_x < -self.road_w / 4 - 100:
                self.player_x = -self.road_w / 4 - 100 - 2

            if self.player_x > self.road_w / 4 + 100:
                self.player_x = self.road_w / 4 + 100 + 2

            if self.score > 0:
                self.score -= 1
            #self.score -= 1
            #if self.score < 0:
            #    self.score = 0

            self.game_over = True
            self.game_score = -1.0

    def check_score(self):

        now_seg = self.base_seg#self.player_seg

        # make sure we check score once for a segment
        ##seg_i = self.player_seg['index']
        seg_i = now_seg['index']
        if seg_i > self.last_seg_i:
            self.last_seg_i = seg_i
        else:
            return

        # NOTE: here we should use the segment just under the car
        ##sprts = self.player_seg['sprites']
        #sprts = self.base_seg['sprites']
        sprts = now_seg['sprites']
        if not sprts:
            return

        #print sprts

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
        car_w = self.car.rect.width #* 2

        sprt_at = 10000
        if x_i == 0:
            sprt_at = 0
        elif x_i == 1:
            sprt_at = 160
        elif x_i == 2:
            sprt_at = 360
        elif x_i == 3:
            sprt_at = -160
        elif x_i == 4:
            sprt_at = -360
        elif x_i == 5:
            sprt_at = 580

        #w_half = car_w / 2 + sprt_w / 2
        w_half = sprt_w + 20

        #print 'sprt_at', car_x, (car_x - w_half), sprt_at, (car_x + w_half)

        #if (car_x + car_w / 2) < sprt_x < (car_x + car_w / 2):
        if (car_x - w_half) < sprt_at < (car_x + w_half):
            self.score += scr


    def check_tm(self):
        if self.position > self.seg_len * 3:
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
        ##p_dt *= -1.0  # NOTE:
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


        #self.fog = FPSptFog((640, 480))
        #self.fog.rect.top = 240
        #self.fog.rect.left = 0
        #self.disp_add(self.fog)

        self.rd_ground = FPSptRoadGround((640, 480), self.cfg)
        self.rd_ground.rect.top = 0#240
        self.rd_ground.rect.left = 0
        self.disp_add(self.rd_ground)

        ##self.disp_add(self.fog)

        self.rd_sprts = FPRoadSprts()
        self.rd_sprts.rect.top = 0#240
        self.rd_sprts.rect.left = 0
        self.disp_add(self.rd_sprts)

        self.rd_sides = FPRoadSides()
        self.rd_sides.rect.top = 0#240
        self.rd_sides.rect.left = 0
        self.disp_add(self.rd_sides)

        #self.road = FPSptRoad((640, 240), self.cfg)
        #self.road = FPSptRoadB((640, 240), self.cfg,
        self.road = FPSptRoadB((640, 480), self.cfg,
                               car=self.car,
                               #fog=self.fog,
                               grd=self.rd_ground,
                               sprts=self.rd_sprts,
                               sides=self.rd_sides,
                               bg_sky=[self.bg_sky1, self.bg_sky2],
                               bg_hills=[self.bg_hills1, self.bg_hills2],
                               bg_trees=[self.bg_trees1, self.bg_trees2])
        self.road.rect.top = 0#240
        self.road.rect.left = 0
        self.disp_add(self.road)

        #self.disp_add(self.rd_sprts)
        #self.disp_add(self.rd_sides)
        ##self.disp_add(self.fog)

        self.disp_add(self.car)  # car disp add after road

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

        self.prg_gas = FPSptProgress((4, 100), c_prog=consts.RED)
        self.prg_gas.rect.top = 70#340
        self.prg_gas.rect.left = 618
        self.disp_add(self.prg_gas)


    def rdmap_hide(self):
        self.rdmap.hide()

    def rdmap_reset(self):
        self.rdmap.clear()
        self.rdmap.draw_segs(self.road.rd_get_segs(whole=True),
                             self.road.seg_len)
        self.rdmap.rotate(90)

    def road_sprts_hide(self):
        self.road.flag_show_rd_sprts = not self.road.flag_show_rd_sprts

    def road_sides_hide(self):
        self.road.flag_show_rd_sides = not self.road.flag_show_rd_sides

    def road_reset(self):
        self.road.rd_reset()
        self.rdmap_reset()

    def road_reset_keep_segs(self):
        self.road.rd_reset(init=False, keep_segs=True)

    def road_reset_from_file(self, segs_file='hs_roads/hs_road.txt'):
        segs_file = utils.dir_abs(segs_file, __file__)
        self.road.rd_reset(init=False, keep_segs=False,
                           segs_file=segs_file)
        self.rdmap_reset()

    def road_segs_to_file(self, segs_file=None):
        if not segs_file:
            segs_file = 'hs_roads/hs_road_' + str(int(time.time())) + '.txt'
        segs_file = utils.dir_abs(segs_file, __file__)
        self.road.rd_seg_json_save(segs_file)

    def road_score_to_gas(self):
        self.road.rd_score_to_gas()

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

                elif k == self.pglc.K_BACKSLASH:
                    self.road_segs_to_file()

                elif k == self.pglc.K_SLASH:
                    self.road_sprts_hide()

                elif k == self.pglc.K_PERIOD:
                    self.road_sides_hide()

                elif k == self.pglc.K_u:
                    self.road_score_to_gas()

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

        gasc = self.road.gas / self.road.gas_max
        self.prg_gas.progress(gasc)


class FPSceneA(pygm.PyGMScene):
    def __init__(self, *args, **kwargs):
        super(FPSceneA, self).__init__(*args, **kwargs)

        self.straight = FPStraight({})
        self.straight.rect.top = 0
        self.straight.rect.left = 0
        self.disp_add(self.straight)

    def handle_event(self, events, *args, **kwargs):
        return events

    def refresh(self, fps_clock, *args, **kwargs):
        pass


class GMHillside(pygm.PyGMGame):
    def __init__(self, title, winw, winh, *args, **kwargs):
        super(GMHillside, self).__init__(title, winw, winh)

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
    sf = GMHillside('hillside <:::>', 640, 480)
    #sf = GMHillside('hillside <:::>', 640, 480, road_file='hs_roads/hs_road.txt')
    sf.mainloop()


if __name__ == '__main__':
    main()
