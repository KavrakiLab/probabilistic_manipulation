# <Print generated MDP for input to PRISM model checker>
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

import sys
from mdp import *
import build_mdp
import helper_tools
import importlib


def printInitialLine(initial_state, config):
    if config.int_encoding:
        printInitialLineInt(initial_state, config)
    elif config.obj_to_loc_encoding:
        printInitialLineObj(initial_state, config)
    elif config.loc_to_obj_encoding:
        printInitialLineLoc(initial_state, config)

def printInitialLineInt(initial_state, config):
    print("    x : [0..{}] init {};".format((config.num_place_locs**config.num_objects), state2i(initial_state, config)))

def printInitialLineObj(initial_state, config):
    for i in range(len(config.prism_names)):
        print("{} : [0..{}] init {};".format(config.prism_names[i],config.num_place_locs-1, initial_state.obj_locs[i]))

def printInitialLineLoc(initial_state, config):
    config.initial_place_counts = [0]*config.num_place_locs
    for l in initial_state.obj_locs:
        config.initial_place_counts[l] = config.initial_place_counts[l]+1
    for i in range(len(config.prism_loc_names)):
        if i == 1:
            continue
        print("{} : [0..{}] init {};".format(config.prism_loc_names[i],config.place_limits[i], config.initial_place_counts[i]))

def main():
    if len(sys.argv) != 2:
        print("ERROR! Please run: python3 print_file.py config_file.py")
        quit()
    config = importlib.import_module(sys.argv[1][:-3])

    initial_state = State()
    initial_state.obj_locs=config.initial_state_list

    ## Print the MDP
    print("mdp")
    print("")
    print("module M1")
    print("")
    printInitialLine(initial_state, config)
    print("")


    states = build_mdp.createMDPStates(initial_state, config.initial_state_str, config.initial_state_tpl, config)

    for s in states:
        for t in s.transitions:
            if config.human_readable:
                str = "     "+state2str(s)+ " ->"
                for s_p, pr in t.prob_distr:
                    # print(tr)
                    # s_p, pr = tr
                    str = str + " {}: ".format(pr) + state2str(s_p)+" "
                str = str + ";"
                print(str)
            else:
                if config.int_encoding:
                    str = "    [{}] {} ->".format(t.action, state2prismstr_int(s, False, config))
                elif config.obj_to_loc_encoding:
                    str = "    [{}] {} ->".format(t.action, state2prismstr_obj(s,config.prism_names))
                elif config.loc_to_obj_encoding:
                    str = "    [{}] {} ->".format(t.action, state2prismstr_loc(s,config.prism_loc_names,config))
                for s_p, pr in t.prob_distr:
                    # print(tr)
                    # s_p, pr = tr
                    if config.int_encoding:
                        str = str + " {}: {} +".format(pr, state2prismstr_int(s_p, True, config))
                    elif config.obj_to_loc_encoding:
                        str = str + " {}: {} +".format(pr, state2prismstr_obj(s_p, config.primed_prism_names))
                    elif config.loc_to_obj_encoding:
                        str = str + " {}: {} +".format(pr, state2prismstr_loc(s_p, config.primed_prism_loc_names, config))

                str = str[:-1] + ";"
                print(str)


    print("")
    print("endmodule")

    print("")
    print("// labels")

    if config.int_encoding:
        helper_tools.printGoalStateLabels(config)
    elif config.obj_to_loc_encoding:
        helper_tools.printGoalStateLabelsPrism(config)
    elif config.loc_to_obj_encoding:
        helper_tools.printGoalStateLabelsPrism(config)
    # print("label \"goal1\" = (x3=1) & (x4=1) & (x5=1) & (h=0);")

    print("rewards \"steps\"")
    print("    true : 1;")
    print("endrewards")

    # Certain states aren't possible
    # Not sure if these are needed. Probably not necessary if we set the initial state correctly
    #     [] x=0 -> (x'=0);
    #     [] x=3 -> (x'=3);
    #     [] x=5 -> (x'=5);
    #     [] x=10 -> (x'=10);
    #     [] x=15 -> (x'=15);
    #     [] x=16 -> (x'=16);

if __name__ == "__main__":
    main()