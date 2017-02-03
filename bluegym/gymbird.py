"""
Flibird for Gym
"""

from bluelake import flibird
from . import mxngym


class GMGymBird(flibird.GMFliBird, mxngym.BLMixinGym):
    def __init__(self, title, winw, winh, *args, **kwargs):
        flibird.GMFliBird.__init__(self, title, winw, winh, *args, **kwargs)

        mxngym.BLMixinGym.__init__(self,
            action_set=['NOOP', 'UP'],
            out_rect=[0, 0, 288, 512],
            main_game=self.fly,
            simu=True)

    # override
    def close_check_event(self):
        self.do_not_check_event()
        self.fly.do_not_check_event()

    # override
    def act(self, action):
        # do action
        a = self.action_idx(action)

        #print 'a:', a
        if a == 1:
            self.fly.e_keys_dn = [a]
            ##self.fly.e_keys_up = [a]
        else:
            self.fly.e_keys_dn = []
            ##self.fly.e_keys_up = []

        reward = self.main_game.sc

        self.step()

        reward = self.main_game.sc - reward

        if self.main_game.game_over:
            reward = -1

        return reward

    # override
    def reset_game(self):
        print ('===> reset')
        self.fly.reset()

    # override
    def game_over(self):
        return self.fly.game_over


def main():
    sf = GMGymBird('Flibird', 288, 512)
    sf.mainloop()


if __name__ == '__main__':
    main()
