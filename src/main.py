#!/usr/bin/python3

import argparse

import sys
import data
import time
import solution
# import solverCH
# import solverLS
import solverCHH
import solverNN
import utilities
from error import TimeOutExeption


from solver import ConstructionHeuristics
from three_opt import ThreeOpt
from two_opt import TwoOPT
from cluster_localsearch import ClusterOPT
from local_search import LocalSearch

import matplotlib.pyplot as plt
# @my_logger
# @my_timer

plt.figure(figsize=(20, 10))

# @my_logger
# @my_timer

# Used for table creation
instance_times_costs = []
def solve(instance, alg, config):
    global instance_times_costs
    temp_instance_times_costs = []
    t0 = time.clock()
    ch = ConstructionHeuristics(instance, alg)
    # returns an object of type Solution
    try:
        sol = ch.construct(config.time_limit-t0)
        temp_instance_times_costs += [0, sol.cost(), round(t0,2)]
    except TimeOutExeption as e:
        print("timeout")
        sol = e.solution
    print(sol.routes)

    
    ls_alg = ThreeOpt(sol).run
    ls = LocalSearch(solution=sol, alg=ls_alg)
    try:
        sol = ls.construct(config.time_limit-t0)
    except TimeOutExeption as e:
        print("timeout")
        sol = e.solution

    # ls_alg = ClusterOPT(sol).run
    # ls = LocalSearch(solution=sol, alg=ls_alg)
    # try:
    #     sol = ls.construct(config.time_limit-t0)
    # except TimeOutExeption as e:
    #     print("timeout")
    #     sol = e.solution
    # print(sol.routes)
    
    # t0 = time.clock()
    # ls = solverLS.LocalSearch(instance)
    # sol = ls.local_search(sol, config.time_limit-t0) # returns an object of type Solution
    assert sol.valid_solution()
    instance_times_costs += [temp_instance_times_costs+[]]
    temp_instance_times_costs = []
    return sol


def main(argv):

    parser = argparse.ArgumentParser()

    parser.add_argument('-o', action='store',
                        dest='output_file',
                        help='The file where to save the solution and, in case, plots')

    parser.add_argument('-t', action='store',
                        dest='time_limit',
                        type=int,
                        required=True,
                        help='The time limit')

    parser.add_argument('-s', dest="split_route", action='store_true',
                        help='Split the route to different subplot')

    parser.add_argument('instance_file', action='store',
                        help='The path to the file of the instance to solve')

    config = parser.parse_args()

    print('instance_file    = {!r}'.format(config.instance_file))
    print('output_file      = {!r}'.format(config.output_file))
    print('time_limit       = {!r}'.format(config.time_limit))
    print('split route       = {!r}'.format(config.split_route))

    instance = data.Data(config.instance_file)

    # alg = solverNN.algorithm
    alg = solverCHH.algorithm
    sol = solve(instance, alg, config)

    if config.output_file is not None:
        sol.plot_routes(split=config.split_route,
                        output_filename=config.output_file+'_sol'+'.png')
        sol.write_to_file("../results/"+config.output_file+'.sol')
        print(instance_times_costs)
        sol.plot_table(config.output_file+'_tbl', instance.instance_name, instance_times_costs)
    print("{} routes with total cost {:.1f}"
          .format(len(sol.routes), sol.cost()))


if __name__ == "__main__":
    main(sys.argv[1:])
