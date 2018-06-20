#! python2

import numpy as np
import copy

Reward = {
    -2: 20,
    -1: -5,
    0: -5,
    1: -5,
    2: 100,
}
Actions = [1, 0]  # 1 for +1, 0 for -1
U = {}
for key in Reward.keys():
    U[key] = 0
U_ = copy.deepcopy(U)
while 1:
    difference = 0
    for key in Reward.keys():
        if key in [-2, 2]:
            U_[key] = 0
        else:
            values = []
            for action in Actions:
                if action:
                    value = 0.3 * (U[key+1] + Reward[key+1]) + 0.7 * (U[key-1] + Reward[key-1])
                    # print U[key+1], U[key-1]
                    # print key, action, value
                    values.append(value)
                else:
                    value = 0.2 * (U[key+1] + Reward[key+1]) + 0.8 * (U[key-1] + Reward[key-1])
                    # print U[key+1], U[key-1]
                    # print key, action, value
                    values.append(value)
            new_value = max(values)
            difference += np.abs(U[key] - new_value)
            U_[key] = new_value
    U = copy.deepcopy(U_)
    print U
    if difference < 0.01:
        break
