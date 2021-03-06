#!/usr/bin/python3

import argparse

import sys
import os
import fnmatch
import numpy as np
import re
import data
import time
import solution
# import solverCH
from solverLS import SolverLS
import solverCHH
import solverNN
import metaFFD
import ACO
import utilities
from error import TimeOutExeption


from solver import ConstructionHeuristics, MetaHeuristic
from three_opt import ThreeOpt
from two_opt import TwoOPT
from cluster_localsearch import ClusterOPT
from local_search import LocalSearch


# Used for table creation
instance_times_costs = []


def solve(instance, alg, config):
    global instance_times_costs
    temp_instance_times_costs = []
    t0 = time.process_time()
    ch = MetaHeuristic(instance, alg, output_file=config.output_file)
    # returns an object of type Solution
    try:
        sol = ch.construct(config.time_limit-t0)
        temp_instance_times_costs += [0, sol.cost(), round(t0, 2)]
    except TimeOutExeption as e:
        # print("timeout")
        sol = e.solution
    
    # for i in range(len(sol.routes)):
    #     print("[{}:{}]".format(i, sol.route_index_capacity(i)), sol.routes[i])
    assert sol.valid_solution()

    return sol


def boxplotter(filename):
    import pandas as pd

    dataframe = pd.read_csv(filename+'.dat', ' ', na_values='.')
    # color = {'boxes': 'DarkGreen', 'whiskers': 'DarkOrange', 'medians': 'DarkBlue', 'caps': 'Gray'}
    slicer = dataframe.iloc[:, [0, 1, 2]]
    bp = slicer.boxplot(column='Cost', by='Instance')
    axes = plt.gca()
    # axes.set_ylim([0,25000])
    plt.autoscale(enable=True, axis='y')
    plt.title(filename)
    plt.savefig(filename+'_boxplot.png')

# Print the time it takes to resolve and the cost of the algorithm into a .dat file
# This will make it possible for LaTeX to make the plots
# Draw graphs to show the performance


def performance_testing():
    # Heuristics
    h_alg = [solverNN.algorithm, solverCHH.algorithm]
    h_alg_name = ["solverNN.algorithm", "solverCHH.algorithm"]
    ls_alg_name = ["SolverLS_close_index_route_swap", "SolverLS_all_combination_route_swap",
                   "TwoOPT"]
    try:
        for (idx, algo) in enumerate(h_alg):
            with open('../results/'+h_alg_name[idx]+'.dat', "a") as filehandle:
                filehandle.write("{} {} {}\n".format(
                    "Instance", "Cost", "Time"))
                for path, subdirs, files in os.walk('../data'):
                    for name in files:
                        if fnmatch.fnmatch(name, "*.xml"):
                            t0 = time.clock()
                            instance = data.Data(os.path.join(path, name))
                            ch = ConstructionHeuristics(instance, algo)
                            sol = ch.construct(60-t0)
                            splitted_name = re.compile(
                                "^[a-zA-Z]+").findall(name)
                            filehandle.write("{} {} {}".format(
                                splitted_name[0], sol.cost(), round(t0, 2)))
                            filehandle.write("\n")
                            ls_alg = [SolverLS(sol).run_first, SolverLS(sol).run_second,
                                      TwoOPT(sol).run]

                            for (ls_idx, l_alg) in enumerate(ls_alg):
                                with open('../results/'+ls_alg_name[ls_idx]+'_'+h_alg_name[idx]+'.dat', "a") as ls_fh:
                                    if os.stat('../results/'+ls_alg_name[ls_idx]+'_'+h_alg_name[idx]+'.dat').st_size == 0:
                                        ls_fh.write("{} {} {}\n".format(
                                            "Instance", "Cost", "Time"))
                                    t0 = time.clock()
                                    ls = LocalSearch(solution=sol, alg=l_alg)
                                    try:
                                        sol = ls.construct(60-t0)
                                    except TimeOutExeption as e:
                                        print("timeout")
                                        sol = e.solution
                                    ls_fh.write("{} {} {}".format(
                                        splitted_name[0], sol.cost(), round(t0, 2)))
                                    ls_fh.write("\n")
                                    ls_fh.close()
                filehandle.close()
                boxplotter('../results/'+h_alg_name[idx])
                for ls_idx in range(len(ls_alg_name)):
                    boxplotter('../results/' +
                               ls_alg_name[ls_idx]+'_'+h_alg_name[idx])

    except TimeOutExeption as e:
        print("timeout")
        sol = e.solution


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

    parser.add_argument('-g', dest="graphic_sol", action='store_true',
                        help='graphical solution')

    parser.add_argument('instance_file', action='store',
                        help='The path to the file of the instance to solve')

    parser.add_argument('-all', action='store',
                        dest='all',
                        help='The file where to save the solution and, in case, plots')

    parser.add_argument('-performancetest', action='store',
                        dest='performancetest',
                        help='The file where to save the solution and, in case, plots')

    config = parser.parse_args()

    print('instance_file    = {!r}'.format(config.instance_file))
    print('output_file      = {!r}'.format(config.output_file))
    print('time_limit       = {!r}'.format(config.time_limit))
    print('graphical solution= {!r}'.format(config.graphic_sol))
    print('split route       = {!r}'.format(config.split_route))

    if config.performancetest:
        performance_testing()
    else:
        instance = data.Data(config.instance_file)
        # alg = solverNN.algorithm
        # alg = solverCHH.algorithm
        alg = ACO.Ant().algorithm
        # alg = metaFFD.algorithm
        sol = solve(instance, alg, config)
        
        if config.output_file is not None:
            if config.graphic_sol:
                import matplotlib.pyplot as plt
                plt.figure(figsize=(20, 10))
                plt.rcParams.update({'font.size': 22})
                sol.plot_routes(split=config.split_route,
                                output_filename=config.output_file+'_sol'+'.png')
            # sol.write_to_file(config.output_file+'.sol')
            # print(instance_times_costs)
            # sol.plot_table(config.output_file+'_tbl', instance.instance_name, instance_times_costs)
        print("{} routes with total cost {:.1f}"
              .format(len(sol.routes), sol.cost()))


if __name__ == "__main__":
    main(sys.argv[1:])
    sys.exit(0)
