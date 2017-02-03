"""
"""

import os
import math
import json


def dir_base(f=None, up_dir=0):
    if not f:
        f = __file__
    b = os.path.dirname(os.path.abspath(f))

    for i in range(up_dir):
        b = os.path.join(b, '../')

    return b


def dir_abs(d, f=None, up_dir=0):
    b = dir_base(f, up_dir)
    d = os.path.join(b, d)
    return d


def is_path_abs(d):
    return os.path.isabs(d)


def clr_from_str(s, a=255):
    s = s[1:]
    c = []
    for i in range(3):
        ccs = s[i * 2:(i + 1) * 2]
        cc = int(ccs, 16)
        c.append(cc)

    c.append(a)
    return tuple(c)


def fn_if_tri(i, a, b):
    if i:
        return a
    else:
        return b


def math_round(i):
    if i % 1 >= 0.5:
        return math.ceil(i)
    else:
        return math.floor(i)


def math_floor(i):
    return math.floor(i)


def json_dumps(o):
    return json.dumps(o)


def json_loads(s):
    return json.loads(s)
