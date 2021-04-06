# <Convert PRISM model checker adversary to usable format>
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

# from config_file import num_human_locs, num_place_locs, num_objects
import sys
import re
import mdp
import importlib


only_print_desired_actions = True

if(len(sys.argv) != 4):
    print("please run: python3 build_adversary config.py adv adv_states")
    exit()

config = importlib.import_module(sys.argv[1][:-3])

# num_human_locs = config.num_human_locs
# num_place_locs = config.num_place_locs
# num_objects = config.num_objects

adv_file_name = sys.argv[2]
state_file_name = sys.argv[3]

state_prism_to_real_map={}
state_real_to_prism_map={}
with open(state_file_name) as state_file:
    line = state_file.readline()
    while line:
        index = line.find(":")
        if index != -1:
            state_num = int(line[: index])
            state_name = line[index+1 : -1]
            state_prism_to_real_map[state_num] = state_name
            state_real_to_prism_map[state_name] = state_num
        else:
            print("# " + line[:-1])


        # nums = [int(s) for s in re.findall(r'\d+', line)]
        # if len(nums) == 3:#prism_index, dfa_index, mdp_index
        #     state_prism_to_real_map[nums[0]] = [nums[2], nums[1]]
        #     state_real_to_prism_map[nums[2]] = [nums[0]]
        line = state_file.readline()

    # print(state_prism_to_real_map)


with open(adv_file_name) as adv_file:
    line = adv_file.readline()
    while line:
        line = adv_file.readline()
        nums = line.split()
        if len(nums) == 4:#state, state, probability, act
            if int(nums[0]) in state_prism_to_real_map and int(nums[1]) in state_prism_to_real_map:
                if (not only_print_desired_actions) or float(nums[2]) > 0.5:
                    print(state_prism_to_real_map[int(nums[0])] + " -> " + state_prism_to_real_map[int(nums[1])])
            else:
                print("Unrecognized state: ")
                if not (int(nums[0]) in state_prism_to_real_map):
                    print(nums[0])
                if not (int(nums[1]) in state_prism_to_real_map):
                    print(nums[1])
                exit()
        elif len(nums) == 3:#state, state, probability
            if int(nums[0]) in state_prism_to_real_map and int(nums[1]) in state_prism_to_real_map:
                if (not only_print_desired_actions) or float(nums[2]) > 0.5:
                    print(state_prism_to_real_map[int(nums[0])] + " -> " + state_prism_to_real_map[int(nums[1])])
            else:
                print("Unrecognized state: ")
                if not (int(nums[0]) in state_prism_to_real_map):
                    print(nums[0])
                if not (int(nums[1]) in state_prism_to_real_map):
                    print(nums[1])
                exit()
        else:#Invalid line
            continue

        # print(mdp.state2str(mdp.i2state(nums[1])))
        # print(line) 


