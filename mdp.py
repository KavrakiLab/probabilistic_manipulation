# <Definition of an MDP>
# Copyright (C) <2021>  <Rice University>
# Written by <Andrew M. Wells> <andrewmw94@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

class Transition:
    action=""
    prob_distr = [] # list of <new state, probability>

    def __init__(self):
        self.action=""
        self.prob_distr=[]

class State:
    obj_locs=[]
    neighbors = []
    act_to_reach_neighbor = []
    transitions = [] # list of transitions

    def __init__(self):
        self.obj_locs=[]
        self.neighbors=[]

def state2i(s, config):
    r = 0
    power = 1
    for i in range(len(s.obj_locs)):
        r = r + s.obj_locs[i] * power
        power = power*config.num_place_locs
    return r

def state2tpl(s):
    tpl = ( )
    for i in s.obj_locs:
        tpl = tpl + (i,)
    return tpl

def state2str(s):
    str = "("
    for i in s.obj_locs:
        str = str + "{},".format(i)
    return str+")"

# def state2prismstr(s, prism_var_list, config):
#     if config.int_encoding:
#         return state2prismstr_int(s)
#     elif config.obj_to_loc_encoding:
#         return state2prismstr_obj(s, prism_var_list)
#     elif config.loc_to_obj_encoding:
#         return state2prismstr_loc(s, prism_var_list, config)


def state2prismstr_int(s, primed, config):
    if primed:
        str = "(x'={})".format(state2i(s,config))
        return str
    else:
        str = "(x={})".format(state2i(s,config))
        return str

def state2prismstr_obj(s, prism_var_list):
    str = ""
    for i in range(len(s.obj_locs)):
        str = str + "({}={}) & ".format(prism_var_list[i], s.obj_locs[i])
    str = str[:-2]
    return str

def state2prismstr_loc(s, prism_var_list, config):
    place_counts = [0]*config.num_place_locs
    for l in s.obj_locs:
        place_counts[l] = place_counts[l]+1
    str = ""
    for i in range(len(place_counts)):
        if i == 1:
            continue
        str = str + "({}={}) & ".format(prism_var_list[i], place_counts[i])
    str = str[:-2]
    return str

def i2state(i, config):
    s = State()
    for j in range(config.num_objects):
        # print("i = {}".format(i))
        n = int(i)
        l = int(config.num_place_locs)
        k = n % l
        # print(k)
        s.obj_locs.append(k)
        i = int(int(i) / int(config.num_place_locs))
    return s

def tpl2state(tpl):
    s = State()
    for i in len(tpl)-1:
        s.obj_locs.append(i)
    return s