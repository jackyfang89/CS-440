# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Kelvin Ma (kelvinm2@illinois.edu) on 01/24/2021

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,fast)


# Feel free to use the code below as you wish
# Initialize it with a list/tuple of objectives
# Call compute_mst_weight to get the weight of the MST with those objectives
# TODO: hint, you probably want to cache the MST value for sets of objectives you've already computed...
from collections import deque
import heapq
import math
from copy import deepcopy

class MST:
    def __init__(self, objectives):
        self.elements = {key: None for key in objectives}

        # TODO: implement some distance between two objectives 
        # ... either compute the shortest path between them, or just use the manhattan distance between the objectives
        self.distances   = {
                (i, j): self.DISTANCE(i, j)
                for i, j in self.cross(objectives)
            }
        
    # Prim's algorithm adds edges to the MST in sorted order as long as they don't create a cycle
    def compute_mst_weight(self):
        weight      = 0
        for distance, i, j in sorted((self.distances[(i, j)], i, j) for (i, j) in self.distances):
            if self.unify(i, j):
                weight += distance
        return weight

    # helper checks the root of a node, in the process flatten the path to the root
    def resolve(self, key):
        path = []
        root = key 
        while self.elements[root] is not None:
            path.append(root)
            root = self.elements[root]
        for key in path:
            self.elements[key] = root
        return root
    
    # helper checks if the two elements have the same root they are part of the same tree
    # otherwise set the root of one to the other, connecting the trees
    def unify(self, a, b):
        ra = self.resolve(a) 
        rb = self.resolve(b)
        if ra == rb:
            return False 
        else:
            self.elements[rb] = ra
            return True

    # helper that gets all pairs i,j for a list of keys
    def cross(self, keys):
        return (x for y in (((i, j) for j in keys if i < j) for i in keys) for x in y)

    def DISTANCE(self, obj_a, obj_b):
        return manhattan(obj_a, obj_b)

def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """

    points_to_visit = list(maze.waypoints)
    q = []
    q.append(maze.start)
    visited = []
    visited.append(maze.start)

    last_waypoint = points_to_visit[0]
    parent = {}

    #BFS
    while (len(q) > 0):
        curr = q.pop(0)
        # print(str(curr[0]) + "," + str(curr[1]))

        if curr in points_to_visit:
            points_to_visit.remove(curr)
        if len(points_to_visit) == 0:
            last_waypoint = curr
            break

        for n in maze.neighbors(curr[0], curr[1]):
            if n not in visited:
                parent[n] = curr
                q.append(n)
                visited.append(n)
    
    #get path from parent
    path = [last_waypoint]
    while path[-1] != maze.start:
        path.append(parent[path[-1]])
    path.reverse()

    return path

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_single_cost(curr_cell, cost, goal):
    # return cost + abs(goal[0] - curr_cell[0]) + abs(goal[1] - curr_cell[1])
    return cost + manhattan(curr_cell, goal)

def astar_single(maze):
    """
    Runs A star for part 2 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """

    #use most of BFS, but replace queue with priority queue(heapq in python)
    #need f(x) = g(x) + h(x), where g(x) = actual distance from x to start
    #and h(x) = estimated distance from x to end

    points_to_visit = list(maze.waypoints)
    h = [] #heapq

    #heapq keeps track of cost estimate to goal, cell, # steps taken t0 reach that cell
    #cost estimate is first so heapq works 
    start_state = (astar_single_cost(maze.start, 0, points_to_visit[0]), maze.start, 0)

    heapq.heappush(h, start_state)

    visited = []
    visited.append(maze.start)

    last_waypoint = points_to_visit[0]
    parent = {}

    #AStar
    while (len(h) > 0):
        curr = heapq.heappop(h)
        curr_cell = curr[1]
        curr_cost = curr[2]
        # print(str(curr[0]) + ", " + str(curr[1]) + ", " + str(curr[2]))

        if curr_cell in points_to_visit:
            points_to_visit.remove(curr_cell)
        if len(points_to_visit) == 0:
            last_waypoint = curr_cell
            break

        for n in maze.neighbors(curr_cell[0], curr_cell[1]):
            if n not in visited:
                # print("neighbor: " + str(n))
                parent[n] = curr_cell
                # cost_estimate = (astar_cost(curr_cost, curr_cell, points_to_visit[0]), n)
                cost_estimate = astar_single_cost(n, curr_cost + 1, points_to_visit[0])
                # print("cost: " + str(cost_estimate))
                heapq.heappush(h, (cost_estimate, n, curr_cost + 1))
                visited.append(n)

    #get path from parent
    path = [last_waypoint]
    while path[-1] != maze.start:
        path.append(parent[path[-1]])
    path.reverse()

    return path

def astar_multiple_cost(curr, steps, points):
    weights = []
    for point in points:
        temp = deepcopy(points)
        temp.remove(point)
        mst = MST(temp)
        mst_weight = mst.compute_mst_weight()
        cost = mst_weight + manhattan(curr, point) + steps
        # cost = steps
        # weights.append((cost, point))
        weights.append(cost)

    weights.sort()
    return weights[0]

def save_path(parent, last_waypoint, start):
    path = [last_waypoint]
    # print("end: " + str(last_waypoint))
    # for x in parent:
    #     print(x, parent[x])
    while path[-1] != start:
        # print(path[-1])
        path.append(parent[path[-1]])
    path.reverse()

    return path

def astar_multiple(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """

    #use the MST waypoints by taking out one waypoint at a time and getting weight
    #min weight is the target waypoint

    points_to_visit = list(maze.waypoints)
    # print(points_to_visit)
    h, visited = [], []
    parent = {}

    # weights = mst_weights(points_to_visit, maze.start)
    # weights.sort()
    # print(weights)

    # start_target = weights[0][1]
    # print(astar_multiple_cost(maze.start, 0, points_to_visit))
    heapq.heappush(h, (astar_multiple_cost(maze.start, 0, points_to_visit), maze.start, 0)) #heap elements are (estimate, cell, # steps taken to cell)
    last_waypoint = points_to_visit[0]
    curr_start = maze.start

    path = []

    # for n in maze.neighbors(maze.start[0], maze.start[1]):
    #     print("n: " + str(n) + ", " + str(astar_multiple_cost(n, 0, points_to_visit)))

    while (len(h) > 0):
        curr = heapq.heappop(h)
        curr_cell, curr_steps = curr[1], curr[2]

        # print(curr_cell)

        #when we hit a waypoint, need to recalculate min MST weights
        if curr_cell in points_to_visit:
            # print("removed")
            points_to_visit.remove(curr_cell)
            curr_steps = 0
            # weights = mst_weights(curr_cell, curr_steps, points_to_visit)
            # print("new weights: " + str(weights))

            if len(path) != 0:
                path.remove(path[-1])
            path.extend(save_path(parent, curr_cell, curr_start))

            curr_start = curr_cell
            parent.clear()
            visited.clear()
            visited.append(curr_cell)
            h.clear()
            # print("points: " + str(points_to_visit))
        
        if len(points_to_visit) == 0:
            break

        # target = weights[0][1]

        for n in maze.neighbors(curr_cell[0], curr_cell[1]):
            if n not in visited:
                parent[n] = curr_cell
                visited.append(n)
                cost_etimate = astar_multiple_cost(n, curr_steps + 1, points_to_visit)
                print("n: " + str(n) + ", cost: " + str(cost_etimate))
                heapq.heappush(h, (cost_etimate, n, curr_steps + 1))

    # for x in path:
    #     print(x)

    return path

def fast(maze):
    """
    Runs suboptimal search algorithm for part 4.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    return []
    
            
