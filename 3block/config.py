# <Configuration file to define MDP built for input to PRISM model checker>
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

human_readable = False

int_encoding = False
obj_to_loc_encoding = False
loc_to_obj_encoding = True

temporal_goals = False
robot_respect_constraints = True


#   we have robot gripper, else, and the other locations for our states
num_place_locs = 5
num_objects = 3

# this is not reason of failure
human_interupt_prob = 0.0 # Probability of staying in the same state

obj_prob_success = [0.8, 0.7, 0.9]
# We can have prob for pick, place separately

# TODO need some way to describe which blocks are on top of others
# list of which locs must be free to pick/place block at location x
placement_requirements = []
placement_requirements.append([]) # gripper
placement_requirements.append([]) # else
placement_requirements.append([3,4]) # top requires left and right support
placement_requirements.append([]) # left
placement_requirements.append([]) # right
# print("placement_requirements: ")
# print(placement_requirements)

# list of which locs must be free to pick block at location x
grasp_requirements = []
grasp_requirements.append([]) # gripper
grasp_requirements.append([]) # else
grasp_requirements.append([]) # top
grasp_requirements.append([2]) # left
grasp_requirements.append([2]) # right

# print("grasp_requirements: ")
# print(grasp_requirements)

place_limits = [1]*num_place_locs
place_limits[1] = num_objects

# initial_state_str = "2,1,0"
# initial_state_list = [2,1]
# initial_state_tpl = (2,1,0)

initial_state_str = "1,3,4"
initial_state_list = [1,3,4]
initial_state_tpl = (1,3,4)

# Names for the prism variables
prism_names = ["x1","x2","x3"]
primed_prism_names = ["x1'","x2'","x3'"]

prism_loc_names = ["x1","x2","x3", "x4", "x5"]
primed_prism_loc_names = ["x1'","x2'","x3'", "x4'", "x5'"]

goal_list = [2,3,4]
