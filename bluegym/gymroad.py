"""
Sandroad for Gym
"""

import math

from bluelake import sandroad
from . import mxngym


class GMGymRoad(sandroad.GMFlatpath, mxngym.BLMixinGym):
    def __init__(self, title, winw, winh, *args, **kwargs):
        sandroad.GMFlatpath.__init__(self, title, winw, winh, *args, **kwargs)

        self.straight = self.scn1.straight
        self.road = self.scn1.straight.road

        mxngym.BLMixinGym.__init__(self,
            action_set=['NOOP', 'UP', 'RIGHT', 'DOWN', 'LEFT'],
            out_rect=[0, 0, 640, 480],
            main_game=self.road,
            simu=True)

    # override
    def close_check_event(self):
        self.do_not_check_event()
        self.scn1.do_not_check_event()
        self.straight.do_not_check_event()
        self.road.do_not_check_event()

    # override

    def act__0(self, action):
        reward = self.fly.sc

        # do action
        a = self.action_idx(action)
        #print 'a:', a
        if a == 1:
            self.fly.e_keys_dn = [a]
            ##self.fly.e_keys_up = [a]
        else:
            self.fly.e_keys_dn = []
            ##self.fly.e_keys_up = []

        self.step()

        reward = self.fly.sc - reward

        if self.fly.game_over:
            reward = -1

        return reward

    def act_1(self, action):
        acts = [
            # dn, up
            [[], [0, 1, 2, 3], '+ +'],  # + +
            [[0], [1, 3], '^ +'],  # ^ +
            [[2], [1, 3], 'v +'],  # v +
            [[1], [0, 2], '+ >'],  # + >
            [[3], [0, 2], '+ <'],  # + <
            [[0, 1], [], '^ >'],  # ^ >
            [[2, 1], [], 'v >'],  # v >
            [[0, 3], [], '^ <'],  # ^ <
            [[2, 3], [], 'v <'],  # v <
        ]

        ak = acts[action]
        self.road.e_keys_dn = ak[0]
        self.road.e_keys_up = ak[1]
        print (ak[2])

        self.step()

        #reward = self.get_reward_1()
        reward = self.get_reward_2()
        return reward

    def get_reward_1(self):
        reward = float(self.road.speed) / float(self.road.speed_max)
        reward += 0.01
        reward /= 10.0

        player_x = math.fabs(self.road.player_x)
        player_deviation = float(player_x) / float(self.road.road_w)
        ##reward -= player_deviation / 80.0
        speed_df = (float(self.road.speed_max) - float(self.road.speed))
        reward -= player_deviation / (speed_df + 2.0)

        if self.road.game_over:
            reward = self.road.game_score

        return reward

    def get_reward_2(self):

        if self.road.game_over:
            return self.road.game_score

        if self.road.speed > 0.0:
            reward = float(self.road.speed) / float(self.road.speed_max)
            reward += 0.01
            reward /= 10.0
        else:
            reward = -0.001

        player_x = math.fabs(self.road.player_x)
        player_deviation = float(player_x) / float(self.road.road_w)
        ##reward -= player_deviation / 80.0
        speed_df = (float(self.road.speed_max) - float(self.road.speed))
        reward -= player_deviation / (speed_df + 2.0)

        return reward

    def get_reward_3(self):  # TODO:

        if self.road.game_over:
            return self.road.game_score

        if self.road.speed > 0.0:
            reward = float(self.road.speed) / float(self.road.speed_max)
            reward += 0.01
            reward /= 10.0
        else:
            reward = -0.001

        player_x = math.fabs(self.road.player_x)
        player_deviation = float(player_x) / float(self.road.road_w)
        ##reward -= player_deviation / 80.0
        speed_df = (float(self.road.speed_max) - float(self.road.speed))
        reward -= player_deviation / (speed_df + 2.0)

        return reward


    def act(self, action):
        acts = [
            # dn, up
            [[], [0, 1, 2, 3], '+ +'],  # + +
            [[0], [1, 3], '^ +'],  # ^ +
            [[1], [0, 2], '+ >'],  # + >
            [[2], [1, 3], 'v +'],  # v +
            [[3], [0, 2], '+ <'],  # + <
            #[[0, 1], [], '^ >'],  # ^ >
            #[[2, 1], [], 'v >'],  # v >
            #[[0, 3], [], '^ <'],  # ^ <
            #[[2, 3], [], 'v <'],  # v <
        ]

        action = self.action_idx(action)
        ak = acts[action]
        self.road.e_keys_dn = ak[0]
        self.road.e_keys_up = ak[1]
        #print ak[2]

        car_pos_pre = self.road.position

        self.step()

        #reward = self.road.position - car_pos_pre

        #reward = self.get_reward_21()
        #reward = self.get_reward_22()
        #reward = self.get_reward_23(car_pos_pre=car_pos_pre)
        #o#reward = self.get_reward_24(car_pos_pre=car_pos_pre)
        reward = self.get_reward_25(car_pos_pre=car_pos_pre)

        return reward

    def get_reward_21(self):  # TODO:

        if self.road.game_over:
            return self.road.game_score

        if self.road.speed > 0.0:
            reward = float(self.road.speed) / float(self.road.speed_max)
            reward += 0.01
            reward /= 10.0
        else:
            reward = -0.001

        player_x = math.fabs(self.road.player_x)
        player_deviation = float(player_x) / float(self.road.road_w)
        ##reward -= player_deviation / 80.0
        speed_df = (float(self.road.speed_max) - float(self.road.speed))
        reward -= player_deviation / (speed_df + 2.0)

        return reward

    def get_reward_22(self):

        if self.road.game_over:
            return self.road.game_score

        speed = float(self.road.speed)
        speed_max = float(self.road.speed_max)
        speed_max_half = 100.0  #float(self.road.speed_max) / 2.0

        if self.road.speed > 0.0:
            if speed < speed_max_half:
                reward = speed / speed_max
                reward += 0.01
            else:
                reward = (speed_max_half - speed) / speed_max
            #reward /= 10.0
            reward /= 5.0
        else:
            #reward = -0.001
            reward = -0.01

        player_x = math.fabs(self.road.player_x)
        player_deviation = float(player_x) / float(self.road.road_w)
        ##reward -= player_deviation / 80.0
        speed_df = (float(self.road.speed_max) - float(self.road.speed))
        reward -= player_deviation / (speed_df + 2.0)

        return reward

    def get_reward_23(self, car_pos_pre=0.0):

        if self.road.game_over:
            return self.road.game_score

        '''
        speed = float(self.road.speed)
        speed_max = float(self.road.speed_max)
        speed_max_half = 100.0  #float(self.road.speed_max) / 2.0

        if self.road.speed > 0.0:
            if speed < speed_max_half:
                reward = speed / speed_max
                reward += 0.01
            else:
                reward = (speed_max_half - speed) / speed_max
            #reward /= 10.0
            reward /= 5.0
        else:
            #reward = -0.001
            reward = -0.01

        player_x = math.fabs(self.road.player_x)
        player_deviation = float(player_x) / float(self.road.road_w)
        ##reward -= player_deviation / 80.0
        speed_df = (float(self.road.speed_max) - float(self.road.speed))
        reward -= player_deviation / (speed_df + 2.0)
        '''

        reward = self.road.position - car_pos_pre

        reward -= 1.0
        reward /= 5000.0

        reward += (self.get_reward_22() / 50.0)

        return reward



    def get_reward_24(self, car_pos_pre=0.0):

        if self.road.game_over:
            return self.road.game_score

        r_spd = self.get_reward_spd_22()
        r_rdw = self.get_reward_rdw_22()
        r_pos = self.get_reward_pos_22(car_pos_pre=car_pos_pre)

        reward = r_spd + r_rdw + r_pos

        #print r_spd, r_rdw, r_pos, reward

        return reward



    def get_reward_spd_22(self):

        speed = float(self.road.speed)
        speed_max = float(self.road.speed_max)
        speed_max_half = 100.0  #float(self.road.speed_max) / 2.0

        if self.road.speed > 0.0:
            if speed < speed_max_half:
                reward = speed / speed_max
                reward += 0.01
            else:
                reward = (speed_max_half - speed) / speed_max
            reward /= 3.0#5.0#10.0 #
        else:
            #reward = -0.001
            reward = -0.01

        return reward


    def get_reward_rdw_22(self):

        player_x = math.fabs(self.road.player_x)
        player_deviation = float(player_x) / float(self.road.road_w)
        reward = player_deviation / 100.0

        return -reward


    def get_reward_pos_22(self, car_pos_pre=0.0):

        reward = float(self.road.position - car_pos_pre)
        #print '=' * 40, reward

        reward -= 1.0
        reward /= 5000.0

        return reward


    def get_reward_25(self, car_pos_pre=0.0):

        if self.road.game_over:
            return self.road.game_score

        r_pos = self.get_reward_pos_25(car_pos_pre=car_pos_pre)

        reward = r_pos

        #print r_spd, r_rdw, r_pos, reward

        return reward

    def get_reward_pos_25(self, car_pos_pre=0.0):

        if self.road.position > 0.0 and self.road.position > car_pos_pre:
            pos_sn = int(self.road.position / self.road.seg_len)
            pre_sn = int(car_pos_pre / self.road.seg_len)
            reward = float(pos_sn - pre_sn) / 10.0 # float(self.road.seg_len) # 100.0
        elif self.road.position <= car_pos_pre:
            reward = -0.01
        else:
            reward = 0.0

        return reward



    # override
    #def reset_game(self, keep_segs=True):
    def reset_game(self, keep_segs=False):
        print ('===> reset')
        if keep_segs:
            self.straight.road_reset_keep_segs()
        else:
            self.straight.road_reset()

    # override
    def game_over(self):
        return self.road.game_over


def main():
    sf = GMGymRoad('Flibird', 640, 480)
    sf.mainloop()


if __name__ == '__main__':
    main()
