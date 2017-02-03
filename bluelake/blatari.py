"""
Pygame + Atari_Py
"""

import sys
sys.path.insert(0, '../')  # NOTE: set where atati_py is

try:
    import atari_py
except ImportError as e:
    raise error.DependencyNotInstalled("{}. (HINT: you can install Atari dependencies by running 'pip install gym[atari]'.)".format(e))


# from gym.envs.atari_env
ACTION_MEANING = {
    0 : "NOOP",
    1 : "FIRE",
    2 : "UP",
    3 : "RIGHT",
    4 : "LEFT",
    5 : "DOWN",
    6 : "UPRIGHT",
    7 : "UPLEFT",
    8 : "DOWNRIGHT",
    9 : "DOWNLEFT",
    10 : "UPFIRE",
    11 : "RIGHTFIRE",
    12 : "LEFTFIRE",
    13 : "DOWNFIRE",
    14 : "UPRIGHTFIRE",
    15 : "UPLEFTFIRE",
    16 : "DOWNRIGHTFIRE",
    17 : "DOWNLEFTFIRE",
}


# action key mapping for handle key events
from pygame import locals as pglcls

ACTION_KEY_MAPS = {
    pglcls.K_RETURN: 0,
    pglcls.K_SPACE: 1,

    pglcls.K_UP: 2,
    pglcls.K_RIGHT: 3,
    pglcls.K_LEFT: 4,
    pglcls.K_DOWN: 5,

    pglcls.K_y: 2,
    pglcls.K_j: 3,
    pglcls.K_g: 4,
    pglcls.K_h: 5,

    pglcls.K_u: 6,
    pglcls.K_t: 7,
    pglcls.K_m: 8,
    pglcls.K_b: 9,

    pglcls.K_w: 10,
    pglcls.K_d: 11,
    pglcls.K_a: 12,
    pglcls.K_s: 13,

    pglcls.K_e: 14,
    pglcls.K_q: 15,
    pglcls.K_c: 16,
    pglcls.K_z: 17,
}


"""
"""

import os
import random
import math

import numpy as np

from starfish import pygm
from starfish import consts
from starfish import sptdraw
from starfish import utils


class SptOneFrame(sptdraw.SptDrawBase):
    def __init__(self, size, *args, **kwargs):
        super(SptOneFrame, self).__init__(size)

        self.draw_on()

    def draw_on(self, *args, **kwargs):
        self.fill(consts.GREEN)
        self.pygm.draw.circle(self.surf, consts.WHITE,
                              (self.size[0] / 2, self.size[1] / 2),
                              self.size[0] / 2, 0)


class SptTmpi(pygm.SptImg):
    def __init__(self, img_file, *args, **kwargs):
        super(SptTmpi, self).__init__(img_file)


class SceneAtatiA(pygm.PyGMScene):
    def __init__(self, game='pong', *args, **kwargs):
        super(SceneAtatiA, self).__init__(*args, **kwargs)

        self.e_keys_up = []
        self.e_keys_dn = []

        self.e_keys_up_last = []
        self.e_keys_dn_last = []

        self.game = game
        self.init_game()

        # show usable actions keys
        ai = [str(a) for a in self._action_set]
        am = self.get_action_meanings()
        aks = '   '.join(ai) + ' : ' + ' '.join(am)
        self.lb1 = pygm.SptLbl(aks, c=consts.GREEN, font_size=12)
        self.lb1.rect.top = self.scr_size[1] + 10
        self.lb1.rect.left = 10
        self.disp_add(self.lb1)

        self.im1 = SptTmpi('starfish/data/Star.png')
        self.im1.rect.top = 100
        self.im1.rect.left = self.scr_size[0] + 10
        self.disp_add(self.im1)


    # from gym.envs.atari_env

    def init_game(self, game=None,
                  #obs_type='ram',
                  obs_type='image',
                  #frameskip=(2, 5),
                  frameskip=(1, 2),
                  repeat_action_probability=0.):
        """Frameskip should be either a tuple (indicating a random range to
        choose from, with the top value exclude), or an int."""

        if game is None:
            game = self.game

        #utils.EzPickle.__init__(self, game, obs_type)
        assert obs_type in ('ram', 'image')

        self.game_path = atari_py.get_game_path(game)
        if not os.path.exists(self.game_path):
            raise IOError('You asked for game %s but path %s does not exist'%(game, self.game_path))
        self._obs_type = obs_type
        self.frameskip = frameskip
        self.ale = atari_py.ALEInterface()
        self.viewer = None

        self._seed()

        (screen_width, screen_height) = self.ale.getScreenDims()
        self._buffer = np.empty((screen_height, screen_width, 4), dtype=np.uint8)

        self._action_set = self.ale.getMinimalActionSet()
        self._action_set = list(self._action_set)  # for using index()
        print self._action_set
        print self.get_action_meanings()

        #self.action_space = spaces.Discrete(len(self._action_set))

        # Tune (or disable) ALE's action repeat:
        # https://github.com/openai/gym/issues/349
        assert isinstance(repeat_action_probability, (float, int)), "Invalid repeat_action_probability: {!r}".format(repeat_action_probability)
        self.ale.setFloat('repeat_action_probability'.encode('utf-8'), repeat_action_probability)

        (screen_width,screen_height) = self.ale.getScreenDims()
        #if self._obs_type == 'ram':
        #    self.observation_space = spaces.Box(low=np.zeros(128), high=np.zeros(128)+255)
        #elif self._obs_type == 'image':
        #    self.observation_space = spaces.Box(low=0, high=255, shape=(screen_height, screen_width, 3))
        #else:
        #    raise error.Error('Unrecognized observation type: {}'.format(self._obs_type))

        # NOTE(likun): add the player to display the game
        self.scr_size = (screen_width, screen_height)
        self.player = SptOneFrame(self.scr_size)
        self.player.rect.top = 100
        self.player.rect.left = 100
        self.disp_add(self.player)

    def _seed(self, seed=None):
        #self.np_random, seed1 = seeding.np_random(seed)
        self.np_random = np.random#.randint
        seed1 = np.random.random(seed)
        # Derive a random seed. This gets passed as a uint, but gets
        # checked as an int elsewhere, so we need to keep it below
        # 2**31.
        seed2 = hash(seed1 + 1) % 2**31
        # Empirically, we need to seed before loading the ROM.
        self.ale.setInt(b'random_seed', seed2)
        self.ale.loadROM(self.game_path)
        return [seed1, seed2]

    def _step(self, a):
        reward = 0.0
        action = self._action_set[a]

        if isinstance(self.frameskip, int):
            num_steps = self.frameskip
        else:
            num_steps = self.np_random.randint(self.frameskip[0],
                                               self.frameskip[1])
        for _ in range(num_steps):
            reward += self.ale.act(action)
        ob = self._get_obs()

        return ob, reward, self.ale.game_over(), {}

    def _get_image(self):
        self.ale.getScreenRGB(self._buffer)  # says rgb but actually bgr
        return self._buffer[:, :, [2, 1, 0]]

    def _get_ram(self):
        return self.to_ram(self.ale)

    def to_ram(self, ale):
        ram_size = ale.getRAMSize()
        ram = np.zeros((ram_size),dtype=np.uint8)
        ale.getRAM(ram)
        return ram

    @property
    def _n_actions(self):
        return len(self._action_set)

    def _get_obs(self):
        if self._obs_type == 'ram':
            return self._get_ram()
        elif self._obs_type == 'image':
            img = self._get_image()
        return img

    # return: (states, observations)
    def _reset(self):
        self.ale.reset_game()
        return self._get_obs()

    def _render(self, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return
        img = self._get_image()
        if mode == 'rgb_array':
            return img
        elif mode == 'human':
            from gym.envs.classic_control import rendering
            if self.viewer is None:
                self.viewer = rendering.SimpleImageViewer()
            self.viewer.imshow(img)

    def get_action_meanings(self):
        return [ACTION_MEANING[i] for i in self._action_set]


    # handle key events

    def key_to_act(self, k):
        a = ACTION_KEY_MAPS.get(k)
        #print '$' * 20, a
        return a

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
                di = self.key_to_act(event.key)
                if di is not None:
                    e_keys_up.append(di)
                else:
                    r_events.append(event)

            elif event.type == self.pglc.KEYDOWN:
                di = self.key_to_act(event.key)
                #print '-' * 20, di
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


    # refresh surface

    def refresh(self, fps_clock, *args, **kwargs):
        self.one_step()

    def act_idx_from_rand(self):
        ai = random.choice(range(len(self._action_set)))
        # for test
        ai = 5#4#3#2#1#0  # pong: [ 0  1  3  4 11 12]
        #print self._action_set[ai], self.get_action_meanings()[ai]
        return ai

    def act_idx_from_key(self):
        for k in self.e_keys_dn_last:
            if k not in self.e_keys_up:
                self.e_keys_dn.append(k)

        if len(self.e_keys_dn) > 0:
            a = self.e_keys_dn[-1]
            #print '=' * 20, a
            if a in self._action_set:
                ai = self._action_set.index(a)
            else:
                ai = 0
        else:
            ai = 0
        return ai

    def one_step(self):
        #ai = self.act_idx_from_rand()
        ai = self.act_idx_from_key()
        #print ai

        ob, reward, done, _ = self._step(ai)

        #print len(ob.tostring())
        ##print ob.tostring()
        #print self.scr_size, self.scr_size[0] * self.scr_size[1] * 3

        self.player.surf_from_img_buf(ob.tostring(), self.scr_size, 'RGB')


class GMBlatari(pygm.PyGMGame):
    def __init__(self, title, winw, winh, game='pong', *args, **kwargs):
        super(GMBlatari, self).__init__(title, winw, winh)

        bk_im = utils.dir_abs('starfish/data/img_bk_1.jpg', __file__)
        self.bk = pygm.SptImg(bk_im)
        #self.bk = pygm.SptImg('starfish/data/img_bk_1.jpg')
        self.bk.rect.top = -230
        self.bk.rect.left = -230
        self.disp_add(self.bk)

        self.scn1 = SceneAtatiA(game=game)
        self.disp_add(self.scn1)


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--game', type=str, default='pong')
    args = parser.parse_args()
    game = args.game

    sf = GMBlatari('Blue + Atati', 800, 550, game=game)
    sf.mainloop()


if __name__ == '__main__':
    main()
