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
import time
from typing import final

class MST:
    def __init__(self, objectives):
        self.elements = {key: None for key in objectives}

        # TODO: implement some distance between two objectives 
        # ... either compute the shortest path between them, or just use the manhattan distance between the objectives
        self.distances   = {
                (i, j): self.DISTANCE(i, j)
                for i, j in self.cross(objectives)
            }
        
        # print("cross")
        # for i, j in self.cross(objectives):
        #     print(i, j)
        
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

class State:
    def __init__(self, cell, prev, to_visit, steps, mst_weight, visited, h_weight):
        self.cell = cell
        self.prev = prev
        self.to_visit = to_visit
        self.steps = steps
        self.mst_weight = mst_weight
        self.visited = visited
        self.h_weight = h_weight

        self.weight = heuristic(self) + self.steps

    def __lt__(self, other):
        # return self.weight <= other.weight
        return self.weight < other.weight

    def __eq__(self, other):
        if other == None:
            return False
        # return self.cell == other.cell and self.to_visit == other.to_visit and self.weight == other.weight
        return self.cell == other.cell and self.to_visit == other.to_visit

    def __hash__(self):
        # return hash((self.cell, tuple(self.to_visit.keys()), self.weight))
        return hash((self.cell, tuple(self.to_visit.keys())))

def nearest_waypoint(state):
    if len(state.to_visit) == 0:
        return None

    # min_point = state.to_visit[0]
    min_point = list(state.to_visit.keys())[0]
    min_dist = manhattan(state.cell, min_point)

    for point in state.to_visit:
        if manhattan(state.cell, point) < min_dist:
            min_point = point
            min_dist = manhattan(state.cell, point)
    
    return min_point

def heuristic(state):
    nearest = nearest_waypoint(state)
    if nearest == None: return 0
    # return manhattan(nearest, state.cell)
    return (manhattan(nearest, state.cell) + state.mst_weight) * state.h_weight
    # return 0

def backtrack(start_state, final_state):
    # print("start: " + str(start_state.cell) + ", end: " + str(final_state.cell))

    path = []
    curr = final_state
    while curr != start_state:
        # print(curr.cell)
        path.append(curr.cell)
        curr = curr.prev
    
    path.append(start_state.cell)
    path.reverse()
    return path 
    
"""
current issue: runtime too long on larger mazes
slowdown reasons: 
1. state.visited is a list. change to dict for faster lookup
2. visited_states is also a list. change to dict too?
3. curr.to_visit also list, but this might be optimal/easiest

work on 1 and 2 for now 2:04 pm
working on 1 and 2. Corner: forgot lol, Autograder: 85?
1 and 2 done 2:18pm. Corner: 0.34s, Autograder: 88 - failing too many states for corner and medium

2:25: working on too many states. fixing bugs on state.visited. Also working on 3.

2:48: local test cases work, but autograder runs out of time. still too slow. Deepcopy too slow?

3:29: runs faster, huge actually runs, autograder "failed to execute correctly"

6:31: fewer calls to deepcopy, still too slow. Too many states visited? 1,2,3 all done

6:39: changed hash function to only hash on cell and to_visit. Cut runtime from 60s to 4s. Heuristic now wrong. 
      tested by setting heuristic to 0, and we get correct path.

"""

def astar_multiple(maze):
    h, path = [], []
    visited_states = {}

    start_mst = MST(list(maze.waypoints))
    start_to_visit = {}
    for cell in maze.waypoints:
        start_to_visit[cell] = True

    start_state = State(maze.start, None, start_to_visit, 1, start_mst.compute_mst_weight(), {maze.start: True}, 1)

    heapq.heappush(h, start_state)
    visited_states[start_state] = True

    final_state = start_state

    while len(h) > 0:
        curr = heapq.heappop(h)
        visited_states[curr] = True

        if curr.cell in curr.to_visit:
            curr.to_visit = deepcopy(curr.to_visit)
            del curr.to_visit[curr.cell]

            if len(curr.to_visit) == 0:
                final_state = curr
                break
            
            temp_mst = MST(curr.to_visit.keys())
            curr.mst_weight = temp_mst.compute_mst_weight()
            curr.weight = heuristic(curr) + curr.steps

            curr.visited.clear()
            # curr.visited[curr.cell] = True

        for n in maze.neighbors(curr.cell[0], curr.cell[1]):
            #deepcopy is slow. Don't call unless necessary
            # temp = State(n, curr, curr.to_visit, curr.steps + 1, curr.mst_weight, {}, 1)
            temp = State(n, curr, curr.to_visit, curr.steps + 1, curr.mst_weight, curr.visited, 1)

            if temp not in visited_states:
                if n not in temp.visited:
                    temp.visited = deepcopy(curr.visited)
                    temp.visited[n] = True
                    visited_states[temp] = True
                    # print("cell: " + str(temp.cell) + ", mst_weights: " + str(temp.mst_weight) + ", weight: " + str(temp.weight))
                    # print("cell: " + str(temp.cell) + ", path length: " + str(temp.steps))
                    # print
                    heapq.heappush(h, temp)

    print(final_state.cell)
    return backtrack(start_state, final_state)

def fast(maze):
    # """
    # Runs suboptimal search algorithm for part 4.

    # @param maze: The maze to execute the search on.

    # @return path: a list of tuples containing the coordinates of each state in the computed path
    # """

    """
    tested weights and times
    all ran on huge_self

    weight, path length, states explored, execution time(s)
    1,      496, 12233124, 159.67
    1.1,    496, 456119,   55.82
    1.2,    496, 161017,   19.39
    1.25,   496, 93218,    10.92
    1.253,  500, 102876,   11.60
    1.255,  500, 100410,   11.31
    1.26,   500, 95098,    11.21
    1.27,   500, 84560,    9.62
    1.3,    500, 66380,    7.78
    1.4,    500, 35131,    3.81
    1.43,   500, 28472,    3.67
    1.44,   514, 25974,    2.83
    1.45,   514, 23230,    2.40
    1.5,    514, 18654,    2.11
    2,      588, 4523,     0.47
    2.5,    555, 7779,     1

    500 is not good enough? path length is 1 so we didn't finish in time
    """

    return fast_helper(maze, 2.5)


def fast_helper(maze, weight):
    # # use weighted A* search. 
    # # tested weights: 

    h, path = [], []
    visited_states = {}

    start_mst = MST(list(maze.waypoints))
    start_to_visit = {}
    for cell in maze.waypoints:
        start_to_visit[cell] = True

    start_state = State(maze.start, None, start_to_visit, 1, start_mst.compute_mst_weight(), {maze.start: True}, weight)

    heapq.heappush(h, start_state)
    visited_states[start_state] = True

    final_state = start_state

    while len(h) > 0:
        curr = heapq.heappop(h)
        visited_states[curr] = True

        if curr.cell in curr.to_visit:
            curr.to_visit = deepcopy(curr.to_visit)
            del curr.to_visit[curr.cell]

            if len(curr.to_visit) == 0:
                final_state = curr
                break
            
            temp_mst = MST(curr.to_visit.keys())
            curr.mst_weight = temp_mst.compute_mst_weight()
            curr.weight = heuristic(curr) + curr.steps

            curr.visited.clear()
            # curr.visited[curr.cell] = True

        for n in maze.neighbors(curr.cell[0], curr.cell[1]):
            #deepcopy is slow. Don't call unless necessary
            # temp = State(n, curr, curr.to_visit, curr.steps + 1, curr.mst_weight, {}, 1)
            temp = State(n, curr, curr.to_visit, curr.steps + 1, curr.mst_weight, curr.visited, weight)

            if temp not in visited_states:
                if n not in temp.visited:
                    temp.visited = deepcopy(curr.visited)
                    temp.visited[n] = True
                    visited_states[temp] = True
                    # print("cell: " + str(temp.cell) + ", mst_weights: " + str(temp.mst_weight) + ", weight: " + str(temp.weight))
                    # print("cell: " + str(temp.cell) + ", path length: " + str(temp.steps))
                    # print
                    heapq.heappush(h, temp)

    print(final_state.cell)
    return backtrack(start_state, final_state)
    
            
