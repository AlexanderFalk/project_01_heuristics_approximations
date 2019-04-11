#!/usr/bin/python3

import argparse

import sys
import os
import fnmatch
import np
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
    print("first sol")
    for i in range(len(sol.routes)):
        print("[{}]".format(i), sol.routes[i])

    chh_cost = sol.cost()

    # ls_alg = ClusterOPT(sol).run
    # ls = LocalSearch(solution=sol, alg=ls_alg)
    # try:
    #     sol = ls.construct(config.time_limit-t0)
    # except TimeOutExeption as e:
    #     print("timeout")
    #     sol = e.solution
        
    # cluster_opt_cost = sol.cost()

    # print("after clusterOPT", chh_cost - cluster_opt_cost)
    # for i in range(len(sol.routes)):
    #     print("[{}]".format(i), sol.routes[i])

    
    # ls_alg = TwoOPT(sol).run
    # ls = LocalSearch(solution=sol, alg=ls_alg)
    # try:
    #     sol = ls.construct(config.time_limit-t0)
    # except TimeOutExeption as e:
    #     print("timeout")
    #     sol = e.solution

    # two_opt_cost = sol.cost()

    # print("after 2opt", cluster_opt_cost - two_opt_cost)

    # for i in range(len(sol.routes)):
    #     print("[{}]".format(i), sol.routes[i])

    
    # ls_alg = ThreeOpt(sol).run
    # ls = LocalSearch(solution=sol, alg=ls_alg)
    # try:
    #     sol = ls.construct(config.time_limit-t0)
    # except TimeOutExeption as e:
    #     print("timeout")
    #     sol = e.solution

    # three_opt_cost = sol.cost()

    # print("after 3opt", two_opt_cost - three_opt_cost)
    # for i in range(len(sol.routes)):
    #     print("[{}]".format(i), sol.routes[i])
    
    # # t0 = time.clock()
    # # ls = solverLS.LocalSearch(instance)
    # # sol = ls.local_search(sol, config.time_limit-t0) # returns an object of type Solution
    # if not sol.valid_solution():
    #     sys.exit(-1)
    # instance_times_costs += [temp_instance_times_costs+[]]
    # temp_instance_times_costs = []
    return sol


# Print the time it takes to resolve and the cost of the algorithm into a .dat file
# This will make it possible for LaTeX to make the plots
# Draw graphs to show the performance
def performance_testing():
    
    # Heuristics
    h_alg = [solverNN.algorithm, solverCHH.algorithm]
    h_alg_name = ["solverNN.algorithm", "solverCHH.algorithm"]
    try:
        for (idx, algo) in enumerate(h_alg):
            with open(h_alg_name[idx]+'.dat', "a") as filehandle:
                filehandle.write("{} {} {}\n".format("Instance", "Cost", "Time"))
                for path, subdirs, files in os.walk('../data'):
                    for name in files:
                        if fnmatch.fnmatch(name, "*.xml"):
                            t0 = time.clock()
                            instance = data.Data(os.path.join(path, name))
                            ch = ConstructionHeuristics(instance, algo)
                            sol = ch.construct(60-t0)

                            filehandle.write("{} {} {}".format(name, sol.cost(), round(t0,2)))
                            filehandle.write("\n")
                filehandle.close()

    except TimeOutExeption as e:
        print("timeout")
        sol = e.solution

def boxplotter():
    # Fixing random state for reproducibility
    np.random.seed(19680801)

    # fake up some data
    spread = np.random.rand(50) * 100
    center = np.ones(25) * 50
    flier_high = np.random.rand(10) * 100 + 100
    flier_low = np.random.rand(10) * -100
    data = np.concatenate((spread, center, flier_high, flier_low))

    fig, axs = plt.subplots(2, 3)

    # basic plot
    axs[0, 0].boxplot(data)
    axs[0, 0].set_title('basic plot')

def main(argv):
    boxplotter()
# def main(argv):

#     parser = argparse.ArgumentParser()

#     parser.add_argument('-o', action='store',
#                         dest='output_file',
#                         help='The file where to save the solution and, in case, plots')

#     parser.add_argument('-t', action='store',
#                         dest='time_limit',
#                         type=int,
#                         required=True,
#                         help='The time limit')

#     parser.add_argument('-s', dest="split_route", action='store_true',
#                         help='Split the route to different subplot')

#     parser.add_argument('-g', dest="graphic_sol", action='store_true',
#                         help='graphical solution')

#     parser.add_argument('-instance_file', action='store',
#                         help='The path to the file of the instance to solve')

#     parser.add_argument('-all', action='store',
#                         dest='all',
#                         help='The file where to save the solution and, in case, plots')

#     parser.add_argument('-performancetest', action='store',
#                         dest='performancetest',
#                         help='The file where to save the solution and, in case, plots')

#     config = parser.parse_args()

#     print('instance_file    = {!r}'.format(config.instance_file))
#     print('output_file      = {!r}'.format(config.output_file))
#     print('time_limit       = {!r}'.format(config.time_limit))
#     print('graphical solution= {!r}'.format(config.graphic_sol))
#     print('split route       = {!r}'.format(config.split_route))

#     if config.performancetest:
#         performance_testing()
#     else:
#         instance = data.Data(config.instance_file)
#         # alg = solverNN.algorithm
#         alg = solverCHH.algorithm
#         sol = solve(instance, alg, config)
#         if config.output_file is not None:
#             if config.graphic_sol:
#                 plt.figure(figsize=(20, 10))
#                 plt.rcParams.update({'font.size': 22})
#                 sol.plot_routes(split=config.split_route,
#                                 output_filename=config.output_file+'_sol'+'.png')
#             sol.write_to_file(config.output_file+'.sol')
#             # print(instance_times_costs)
#             # sol.plot_table(config.output_file+'_tbl', instance.instance_name, instance_times_costs)
#         print("{} routes with total cost {:.1f}"
#                 .format(len(sol.routes), sol.cost()))


if __name__ == "__main__":
    main(sys.argv[1:])
    sys.exit(0)
