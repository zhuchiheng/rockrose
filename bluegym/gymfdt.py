"""
Floodit for Gym
"""

import random
import time

import numpy as np

from bluelake import floodit
from . import mxngym


class GMGymFdt(floodit.GMFloodIt, mxngym.BLMixinGym):
    def __init__(self, title, winw, winh, blk_n=10, blk_w=30, blk_cn=6,
                 max_do_cnt=40,
                 *args, **kwargs):
        floodit.GMFloodIt.__init__(self, title, winw, winh,
                                   blk_n=blk_n, blk_w=blk_w, blk_cn=blk_cn)

        self.fibrd = self.scn1.fibrd

        mxngym.BLMixinGym.__init__(self,
            action_set=range(self.blk_cn),
            out_rect=[200, 90, self.blk_w * self.blk_n, self.blk_w * self.blk_n],
            main_game=self.scn1.fibrd,
            simu=True)

        # NOTE: max times allowed to try, bigger means easier
        self.max_do_cnt = max_do_cnt  #40  #20

        self.fibrd.auto_reset = False  # reset by gym

    # override
    def close_check_event(self):
        self.do_not_check_event()
        self.scn1.do_not_check_event()
        self.fibrd.do_not_check_event()

    # override
    def act(self, action):

        #ak = self._action_set[action]
        ak = action
        #print '=' * 60, ak

        #self.f1.e_keys_dn = [ak]
        self.scn1.e_keys_up = [ak]
        #print 'o' * 60, self.scn1.e_keys_up

        self.step()

        reward = 0.0

        reward = self.fibrd.blk_fi_n - self.fibrd.blk_fi_n_last
        #reward = float(reward) / 10.0  #100.0  # TODO:
        if reward > 0.0:
            reward = 0.1 + float(reward) / 100.0  #100.0  # TODO:

        if self.fibrd.all_ok:
            print ('@' * 300)
            reward = 1  # TODO:
        elif self.game_over():
            print ('-' * 300)
            #reward = -1
            #reward = -0.1
            reward -= 0.1
            #reward -= 1.0
            #reward = 0.

        return reward

    # override
    def reset_game(self, keep_segs=True):
        print ('===> reset')
        self.fibrd.reset_board()

    # override
    def game_over(self):
        #return self.scn1.game_over
        if self.fibrd.do_cnt > self.max_do_cnt:
            return True
        elif self.fibrd.all_ok:
            return True
        else:
            return False


def main():
    #fl = GMGymFdt('floodit ->', 800, 550)
    fl = GMGymFdt('floodit ->', 800, 550, blk_n=4, blk_cn=3)
    fl.mainloop()


if __name__ == '__main__':
    main()
