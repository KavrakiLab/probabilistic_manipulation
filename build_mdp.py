# <Generate a manipulation MDP for input to PRISM model checker>
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

from mdp import *

# Ensure all placement requirement locations are occupied
# And the destination placement is unoccupied
def isLegalPlacement(loc_index, state, config):
    loc_list = config.placement_requirements[loc_index]
    for loc in loc_list:
        loc_occupied = False
        for i in state.obj_locs:
            if i == loc:
                loc_occupied = True
                continue
        if loc_occupied:
            continue
        else:
            return False

    place_counts = [0]*config.num_place_locs
    for l in state.obj_locs:
        place_counts[l] = place_counts[l]+1

    if place_counts[loc_index] >= config.place_limits[loc_index]:
        return False
    return True

#Ensure no objects obstruct the grasp
def isLegalGrasp(loc_index, state, config):
    loc_list = config.grasp_requirements[loc_index]
    for loc in loc_list:
        for i in state.obj_locs:
            if i == loc:
                return False
    return True

def makeStateNeighborsRobotPlaceObjAtI(state, grasped_obj, loc, config):
    array = []
    s_prime = State()
    s_prime.obj_locs = state.obj_locs.copy()
    s_prime.obj_locs[grasped_obj] = loc
    T = Transition()
    T.action = "robotplaces{}at{}".format(grasped_obj, loc)

    #TODO: compute from robot, gripper pair
    prob_success = 1-config.human_interupt_prob

    p_d = (s_prime, prob_success)
    T.prob_distr.append(p_d)
    T.prob_distr.append((state, 1-prob_success))

    array.append((s_prime, T))
    return array

def makeStateNeighborsRobotPlaceObjAtElse(state, grasped_obj, config):
    array = []
    s_prime = State()
    s_prime.obj_locs = state.obj_locs.copy()
    s_prime.obj_locs[grasped_obj] = 1 # We can always use the else region
    T = Transition()
    T.action = "robotplaces{}atELSE".format(grasped_obj)

    #TODO: compute from robot, gripper pair
    prob_success = 1-config.human_interupt_prob

    p_d = (s_prime, prob_success)
    T.prob_distr.append(p_d)
    T.prob_distr.append((state, 1-prob_success))

    array.append((s_prime, T))
    return array

def makeStateNeighborsRobotGraspObjI(state, obj_index, config):
    array = []
    s_prime = State()
    s_prime.obj_locs = state.obj_locs.copy()
    old_loc = s_prime.obj_locs[obj_index]
    s_prime.obj_locs[obj_index] = 0
    T = Transition()
    T.action = "robotpicksup{}at{}".format(obj_index, old_loc)

    #TODO: compute from robot, gripper pair
    # prob_success = 1-config.human_interupt_prob
    prob_success = config.obj_prob_success[obj_index]

    p_d = (s_prime, prob_success)
    T.prob_distr.append(p_d)
    T.prob_distr.append((state, 1-prob_success))


    array.append((s_prime, T))
    return array

def makeStateNeighbors(state, config):
    neighbors = []
    transitions = []

    #if any object is grasped by the robot:
    grasped_obj = -1
    for i in range(config.num_objects):
        if state.obj_locs[i] == 0:
            grasped_obj = i
            break
    # The grasped object can be placed at legal empty location
    if(grasped_obj != -1):
        # 1 if neighbor is available, -1 otherwise
        available_neighbors = [1]*config.num_place_locs
        for l in range(config.num_objects):
            available_neighbors[state.obj_locs[l]] = -1
        for n in range(2,len(available_neighbors)): # Don't count gripper and else region
            if available_neighbors[n] == 1 and (isLegalPlacement(n, state, config) or not config.robot_respect_constraints):
                neighbs = makeStateNeighborsRobotPlaceObjAtI(state, grasped_obj, n, config)
                for s_prime, transition in neighbs:
                    neighbors.append(s_prime)
                    transitions.append(transition)
        # We can fit any object into the ELSE region
        neighbs = makeStateNeighborsRobotPlaceObjAtElse(state, grasped_obj, config)
        for s_prime, transition in neighbs:
            neighbors.append(s_prime)
            transitions.append(transition)

    # Try grasping any object
    else:
        for i in range(config.num_objects):
            if isLegalGrasp(i, state, config) or not config.robot_respect_constraints:
                neighbs = makeStateNeighborsRobotGraspObjI(state, i, config)
                for s_prime, transition in neighbs:
                    neighbors.append(s_prime)
                    transitions.append(transition)

    state.neighbors = neighbors
    state.transitions = transitions

    return neighbors

def createMDPStates(initial_state, initial_state_str, initial_state_tpl, config):
    s = initial_state

    visited_states = {initial_state_str:initial_state_tpl}
    curr_frontier = []
    all_states = []


    curr_frontier.append(s)

    while(len(curr_frontier) > 0):
        #remove state from frontier and add to visited states
        s = curr_frontier[-1]
        curr_frontier.pop()
        my_tpl = {state2str(s) : state2tpl(s)}
        visited_states.update(my_tpl)
        all_states.append(s)
        #check all neighbors and add new ones to frontier
        neighbors = makeStateNeighbors(s, config)
        for n in neighbors:
            if state2str(n) in visited_states:
                pass
            else:
                curr_frontier.append(n)
    return all_states