"""
Bluelake Mixin for OpenAI Gym.
"""

import math
import random
import time

import numpy as np


class BLMixinGym(object):
    def __init__(self, action_set=['NOOP', 'UP'],
                 out_rect=[0, 0, 2, 3],
                 main_game=None,
                 simu=True,
                 *args, **kwargs):
        """
        Args:
            out_rect: the screen rect export to outside, [x, y, w, h]
            main_game: the main sprite on which the game logic is
        """

        self.action_set = action_set
        self.out_rect = out_rect

        self.main_game = main_game

        # if run game in gym, do not check events
        self.simu = simu
        if self.simu:
            self.close_check_event()

    # override
    def close_check_event(self):
        self.do_not_check_event()

    # override
    def act(self, action):
        # do action
        a = self.action_idx(action)

        self.main_game.e_keys_dn = [a]
        #self.main_game.e_keys_up = [a]

        reward = self.main_game.sc

        self.step()

        reward = self.main_game.sc - reward

        if self.main_game.game_over:
            reward = -1

        return reward

    # override
    def reset_game(self):
        self.main_game.reset()

    # override
    def game_over(self):
        return self.main_game.game_over

    def action_idx(self, action):
        try:
            i = self.action_set.index(action)
        except:
            i = None
        return i

    def getMinimalActionSet(self):
        return self.action_set

    def getScreenDims(self):
        return (self.out_rect[2], self.out_rect[3])

    def get_scrn_rgb__0(self):
        a = []

        # <1>
        #data = self.pong.surf_to_img_str(fmt='RGB')

        # <2>
        rct = self.out_rect
        data = self.surf_main_to_img_str(fmt='RGB', rect=rct)

        for d in data:
            a.append(ord(d))

        return a

    def to_rgb(self, a, screen_height, screen_width):
        b = np.fromiter(a, dtype=np.uint8)

        #c = b.reshape((screen_height, screen_width, 4))
        c = b.reshape((screen_height, screen_width, 3))

        return c

    def get_scrn_rgb(self):
        a = []

        # <1>
        #data = self.pong.surf_to_img_str(fmt='RGB')

        # <2>
        rct = self.out_rect
        data = self.surf_main_to_img_str(fmt='RGB', rect=rct)

        for d in data:
            a.append(ord(d))

        a = self.to_rgb(a, self.out_rect[3], self.out_rect[2])

        # compatible for new gym
        a = a[:, :, [2, 1, 0]]

        return a

    def get_surf_rgb__0(self):
        image_data = self.pygm.surfarray.array3d(
            self.pygm.display.get_surface())
        return image_data

    def get_surf_rgb(self):
        image_data = self.pygm.surfarray.array3d(
            self.pygm.display.get_surface())

        # compatible for new gym
        image_data = self.img_to_gym(np.array(image_data))

        return image_data

    def img_to_gym(self, im):
        image_data = np.swapaxes(im, 0, 1)
        # compatible for new gym
        image_data = image_data[:, :, [2, 1, 0]]
        return image_data

    def getScreenRGB(self, arr):
        #a = self.get_scrn_rgb()  # slow
        a = self.get_surf_rgb()  # fast
        return a

    def getRAM(self, ram):
        a = self.get_scrn_rgb()
        return a

    def frame_step(self, action):  # for not using gym
        r = self.act(self.action_set[action])
        obv = self.get_surf_rgb()
        term = self.game_over()
        return obv, r, term
