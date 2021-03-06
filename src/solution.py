import sys
import matplotlib
import matplotlib.pyplot as plt

import data

from collections import deque


def rotate_til_depot_first(tour):
    dq = deque(tour)
    while dq[0] != 0:
        dq.rotate()
    return list(dq)


class Solution:
    routes = []

    def __init__(self, instance):
        self.instance = instance
        self.routes = []

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def valid_solution(self):
        "To check whether a solution is valid, we are going to ensure the arcs enters"
        "and leaves each vertex exactly once. We also need to check the number of vehicles leaving and entering a depot"
        " are equal. Lastly then we ensure the capacity for each vehicle does not exceed their maximum capacity."
        "The capacity is handled in the solverCH.py, when the solution is being created"
        # To complete

        isValid = True
        # Lets start of by checking the arcs of the solution.
        leavingVehicles = 0
        enteringVehicles = 0
        max_capacity = self.instance.capacity
        routes = self.fulfilled_sol()
        customer_visited = [
            customer_point for route in routes for customer_point in route[1:-1]]

        # check if visiting customer more than once
        if len(customer_visited) != len(set(customer_visited)):
            print("visited a customer more than once")
            return False
        if 0 in customer_visited:
            print("visited depots in middle of tour")
            return False

        # check capacity
        for i in range(len(routes)):
            # print(i, self.instance.route_capacity(routes[i]), self.instance.route_capacity(
            #     routes[i]) > self.instance.capacity)
            if self.instance.route_capacity(routes[i]) > self.instance.capacity:
                print("capacity exceeded at [{}]:{}".format(i, routes[i]))
                return False

        for firstRoute in routes:
            # checking capacity
            route_capacity = sum([self.instance.route_capacity(firstRoute)])
            if route_capacity > max_capacity:
                return False

            if firstRoute[0] == 0:
                leavingVehicles += 1
            if firstRoute[-1] == 0:
                enteringVehicles += 1

            for secondRoute in routes:

                if firstRoute != secondRoute:
                    # Constraint #1
                    # If there are any points greater than 0, then two routes intersect
                    for i in self.intersection(firstRoute, secondRoute):
                        if i > 0:
                            isValid = False

        # Constraint #2
        if leavingVehicles == enteringVehicles:
            pass
            # print("Leaving Vehicles: \t", leavingVehicles,
            #       "\nEntering Vehicles: \t", enteringVehicles)
        else:
            isValid = False
        # print("The validity of the solution  is: ", isValid)
        return (isValid)

    def cost(self):
        return sum([self.instance.route_length(r) for r in self.routes])

    def route_index_capacity(self, index):
        return self.instance.route_capacity(self.routes[index])

    def write_to_file(self, filename):
        with open(filename, "w") as filehandle:
            for route in self.fulfilled_sol():
                filehandle.write(
                    ",".join(map(lambda x: str(self.instance.nodes[x]["id"]), route)) + "\n")

    def plot_lines(self, points, color=None, style='bo-'):
        "Plot lines to connect a series of points."
        plt.plot([self.instance.nodes[p]["pt"].x for p in points], [self.instance.nodes[p]["pt"].y for p in points],
                 style, color=color)
        plt.axis('scaled')
        plt.axis('off')

    def fulfilled_sol(self):
        routes = [rotate_til_depot_first(
            r) for r in self.routes]
        for r in routes:
            if r[-1] != 0:
                r += [0]
        return routes

    def plot_instance_points(self):
        self.instance.plot_points(show=False)

    def plot_routes(self, split=False, output_filename=None):
        "routes is a list of routes (alternatively it can be a grand route).  The depot is red square."
        colormap = plt.cm.get_cmap('hsv', len(self.routes))

        if split:
            ax1 = plt.subplot(1, len(self.routes), 1)
            for (index, route) in enumerate(self.routes):
                start = route[0]
                plt.subplot(1, len(self.routes), index +
                            1, sharex=ax1, sharey=ax1)
                # self.plot_instance_points()
                self.plot_lines(
                    list(route) + [start], color=colormap(index), style="o-")
                # Mark the start city with a red square
                self.plot_lines([start], style='rs')
        else:
            c = 0
            for route in self.routes:
                start = route[0]
                # self.plot_instance_points()
                self.plot_lines(
                    list(route) + [start], color=colormap(c), style="o-")
                # Mark the start city with a red square
                self.plot_lines([start], style='rs')
                c += 1
        if output_filename is None:
            plt.show()
        else:
            plt.savefig(output_filename)

    @staticmethod
    def intersection(array1, array2):
        "This method compares two arrays whether they have any elements in common."
        "It is done to uphold the first constraint of no routes are overlapping"
        return [value for value in array1 if value in array2]

    @staticmethod
    def plot_table(outputfile_names=None, inserted_row_labels=None, table_vals=None):
        "Filling a table with results"
        fig = plt.figure()
        #col_labels = ('KLB', 'CH Cost', 'CH Time (sec)', 'Custom CH Cost', 'Custom CH Time (sec)', 'Custom LS Cost', 'Custom LS Time (sec)')
        col_labels = ('KLB', 'CH Cost', 'CH Time (sec)')

        # Draw table
        the_table = plt.table(cellText=table_vals,
                              rowLabels=[inserted_row_labels],
                              colLabels=col_labels,
                              loc='center')
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(24)
        the_table.scale(6, 6)

        # Removing ticks and spines enables you to get the figure only with table
        plt.tick_params(axis='x', which='both', bottom=False,
                        top=False, labelbottom=False)
        plt.tick_params(axis='y', which='both', right=False,
                        left=False, labelleft=False)
        for pos in ['right', 'top', 'bottom', 'left']:
            plt.gca().spines[pos].set_visible(False)

        plt.savefig("../results/"+outputfile_names+'.png',
                    bbox_inches='tight', pad_inches=0.05)
