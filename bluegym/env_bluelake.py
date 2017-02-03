"""
Gym Environment for Bluelake Compatible with Atari.


## ALE apis those the games should implement :

        self.ale = bluelake.pong.GMPong('Pong', 800, 550)

        self._action_set = self.ale.getMinimalActionSet()

        (screen_width,screen_height) = self.ale.getScreenDims()

            reward += self.ale.act(action)

        return ob, reward, self.ale.game_over(), {}

    (screen_width,screen_height) = ale.getScreenDims()

    ale.getScreenRGB(arr) # says rgb but actually bgr

    ram_size = ale.getRAMSize()

    ale.getRAM(ram)

        self.ale.reset_game()

"""

import numpy as np
import os

import gym
from gym import error, spaces
from gym import utils
from gym.utils import seeding

import logging
logger = logging.getLogger(__name__)


def to_rgb(ale):
    (screen_width,screen_height) = ale.getScreenDims()
    arr = np.zeros((screen_height, screen_width, 4), dtype=np.uint8)

    a = ale.getScreenRGB(arr)
    b = np.fromiter(a, dtype=np.uint8)
    c = b.reshape((screen_height, screen_width, 3))

    return c


def to_ram(ale):
    ram_size = ale.getRAMSize()
    ram = np.zeros((ram_size),dtype=np.uint8)
    a = ale.getRAM(ram)
    c = np.frombuffer(a, dtype=np.uint8)
    return c


class BBluelakeEnv(gym.Env, utils.EzPickle):
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self, gm_name=None, gm_size=None,
                 obs_type='ram', frameskip=(2, 5),
                 *args, **kwargs):

        utils.EzPickle.__init__(self, obs_type)
        assert obs_type in ('ram', 'image')
        self.gm_name = gm_name
        self.gm_size = gm_size
        self._obs_type = obs_type
        self.frameskip = frameskip

        self.viewer = None

        game = bluegym_get_game_by_name(self.gm_name)
        self.ale = game(self.gm_name,
                        self.gm_size[0], self.gm_size[1],
                        simu=True,
                        **kwargs)

        self._seed()

        (screen_width, screen_height) = self.ale.getScreenDims()
        self._buffer = np.empty((screen_height, screen_width, 4), dtype=np.uint8)

        self._action_set = self.ale.getMinimalActionSet()
        self.action_space = spaces.Discrete(len(self._action_set))

        (screen_width,screen_height) = self.ale.getScreenDims()
        if self._obs_type == 'ram':
            self.observation_space = spaces.Box(low=np.zeros(128), high=np.zeros(128)+255)
        elif self._obs_type == 'image':
            self.observation_space = spaces.Box(low=0, high=255, shape=(screen_height, screen_width, 3))
        else:
            raise error.Error('Unrecognized observation type: {}'.format(self._obs_type))

        # do a step to start mainloop()
        action = self._action_set[0]
        self.ale.act(action)

    def _seed(self, seed=None):
        self.np_random, seed1 = seeding.np_random(seed)
        # Derive a random seed. This gets passed as a uint, but gets
        # checked as an int elsewhere, so we need to keep it below
        # 2**31.
        seed2 = seeding.hash_seed(seed1 + 1) % 2**31
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
        self._buffer = self.ale.getScreenRGB(self._buffer)
        return self._buffer[:, :, [2, 1, 0]]  # says rgb but actually bgr

    def _get_ram(self):
        return to_ram(self.ale)

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

    def _render(self, mode='human', close=False):  # TODO:
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

    def get_action_meanings(self):  # TODO:
        return [ACTION_MEANING[i] for i in self._action_set]


# import all bluegym games

from .gymfdt import GMGymFdt
from .gymroad import GMGymRoad
from .gymbird import GMGymBird


BB_GAME_NAME = {
    'gymfdt': GMGymFdt,
    'gymroad': GMGymRoad,
    'gymbird': GMGymBird,
}


def bluegym_get_game_by_name(name):
    return BB_GAME_NAME.get(name)


# register bluelake env

from gym.envs.registration import registry, register

def gym_env_register_bluelake(
        game_name, game_size,
        game_id,
        obs_type='image',
        frameskip=(1, 2),
        *args, **kwargs):

    kws = {
        'gm_name': game_name,
        'gm_size': game_size,
        'obs_type': obs_type,
        'frameskip': frameskip,
    }

    kws.update(**kwargs)

    register(
        id=game_id,
        entry_point='bluegym.env_bluelake:BBluelakeEnv',
        kwargs=kws,
        timestep_limit=10000,
        nondeterministic=True,
    )
