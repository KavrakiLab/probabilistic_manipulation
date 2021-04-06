# <Write specification for PRISM>
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

import mdp
import itertools
import importlib
import sys

# def state2i(s):
#     r = 0
#     power = 1
#     for i in range(len(s)):
#         r = r + s[i] * power
#         power = power*num_place_locs
#     return r

# # TODO: We assume the human location is 0
def tuple2state(t):
    s = mdp.State()
    for l in t:
        s.obj_locs.append(l)
    s.human_loc = 0
    return s

#We allow repeats in the ELSE region (region 1) only
def nChooseKHelper(l, n, remaining_k):
    if remaining_k == 0:
        return l
    else:
        all_lists = []
        for i in range(n):
            if( i == 1 or (not i in l)):
                new_list = l.copy()
                new_list.append(i)
                all_lists.append(nChooseKHelper(new_list, n, remaining_k-1))
        if remaining_k > 1:
            r = []
            for a in all_lists:
                for b in a:
                    r.append(b)
            return r
        else:
            return all_lists

def getNChooseKChoices(n, k):
    return nChooseKHelper([], n, k)

def printGoalStateLabels(config):
    if (not config.temporal_goals):
        goals = itertools.permutations(config.goal_list)
        counter = 1
        for state in goals:
            # print(state)
            s = tuple2state(state)
            print("label \"goal{}\" = (x={});".format(counter, mdp.state2i(tuple2state(state), config)))
            counter = counter+1
    else: #We want all goals met at some point in time
        for i in range(config.num_place_locs-2):
            #get all the states satisfying this goal
            potential_goals = getNChooseKChoices(config.num_place_locs, config.num_objects)
            set_of_goals = []
            for j in potential_goals:
                for o in j:
                    if o == i:
                        set_of_goals.append(j)
            s = ""
            for tpl in set_of_goals:
                s = s + " (x = {}) | ".format(mdp.state2i(tuple2state(tpl), config))
                # print("# "+mdp.state2str(tuple2state(tpl)))
            print("label \"goal{}\" = ".format(i) + s[:-2] + ";")

def printGoalStateLabelsPrism(config):
    if (not config.temporal_goals):
        goals = itertools.permutations(config.goal_list)
        if config.loc_to_obj_encoding:
            for state in goals:
                print("label \"goal1\" = {};".format(mdp.state2prismstr_loc(tuple2state(state), config.prism_loc_names, config)))
                break
        elif config.obj_to_loc_encoding:
            # Consider cases where #obj > #goals
            if config.num_objects > len(config.goal_list):
                prism_var_perm = itertools.permutations(config.prism_names, len(config.goal_list)) # len(goal) C num_objects
                counter = 1
                for perm in prism_var_perm:
                    subgoal = "label \"goal{}\" = ".format(counter)
                    i = 0
                    for var in perm:
                        subgoal += "({}={})".format(var, config.goal_list[i])
                        i += 1
                        if i < len(perm):
                            subgoal += " & "
                    subgoal += ";"
                    print(subgoal)
                    # print("label \"goal{}\" = {};".format(counter, ))
                    counter += 1
            elif config.num_objects == len(config.goal_list):
                counter = 1
                for state in goals:
                    # print(state)
                    s = tuple2state(state)
                    print("label \"goal{}\" = {};".format(counter, mdp.state2prismstr_obj(tuple2state(state), config.prism_names)))
                    counter = counter+1
    else: #We want all goals met at some point in time
        if config.loc_to_obj_encoding:
            for i in range(config.num_place_locs-2):
                print("label \"goal{}\" = (x{}=1) & (h=0);".format(i, i+3))
        elif config.obj_to_loc_encoding:
            for i in range(config.num_place_locs-2):
                str = "label \"goal{}\" = ".format(i)
                for j in range(config.num_objects):
                    str = str + "(x{}={}) | ".format(j+1, i+2)
                print(str[:-2] + " & (h=0);")


def printGoalFormula(config):
    if config.loc_to_obj_encoding:
        print("Pmax =? [ F \"goal1\" ];")
        print("Rmin =? [ F \"goal1\" ];")
    else:
        counter = 1
        # goals = itertools.permutations(config.goal_list)
        goals = itertools.permutations(config.prism_names, len(config.goal_list))
        s = "Pmax =? [ (F ("
        for state in goals:
            s = s + "\"goal{}\" | ".format(counter)
            counter = counter+1
        s = s[:-2]
        s = s + "))];"
        print(s)

def main():
    if len(sys.argv) != 2:
        print("ERROR! Please run: python3 print_file.py config_folder.config_file.py")
        quit()
    config = importlib.import_module(sys.argv[1][:-3])
    printGoalFormula(config)

if __name__ == "__main__":
    main()
