# geometry.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by James Gao (jamesjg2@illinois.edu) on 9/03/2021
# Inspired by work done by Jongdeog Lee (jlee700@illinois.edu)

"""
This file contains geometry functions necessary for solving problems in MP2
"""

import math
import numpy as np
from alien import Alien


# #makes sure line is pointing from left to right, 
# def correct_direction(line):

def vec_form(line):
    # return (abs(line[2] - line[0]), abs(line[3] - line[1]))
    return(line[2] - line[0], line[3] - line[1])

def line_length(line):
    return dot_to_dot_dist((line[0], line[1]), (line[2], line[3]))

def dot_product(line1, line2):
    #assumes line are in (startx, starty, endx, endy)
    a, b = vec_form(line1), vec_form(line2)
    return a[0] * b[0] + a[1] * b[1]

def cross_product(line1, line2):
    #assumes line are in (startx, starty, endx, endy)
    a, b = vec_form(line1), vec_form(line2)
    return a[0] * b[1] - a[1] * b[0]

def dot_to_dot_dist(a, b):
    dist = math.pow((a[0] - b[0]), 2) + math.pow((a[1] - b[1]), 2)
    return math.sqrt(dist)

def sign(val):
    if val == 0: return 0
    if val < 0: return -1
    if val > 0: return 1

def check_lines_intersect(line1, line2):
    #test x range
    #ensure line1 and line2 pointing right
    temp1, temp2 = line1, line2
    if line1[2] < line1[0]: 
        line1 = (line1[2], line1[3], line1[0], line1[1])
    if line2[2] < line2[0]: 
        line2 = (line2[2], line2[3], line2[0], line2[1])

    if max(line1[0], line2[0]) > min(line1[2], line1[2]): return False
    #test y range
    #ensure line1 and line2 pointing up
    if line1[3] < line1[1]: 
        line1 = (line1[2], line1[3], line1[0], line1[1])
    if line2[3] < line2[1]: 
        line2 = (line2[2], line2[3], line2[0], line2[1])

    if max(line1[1], line2[1]) > min(line1[3], line1[3]): return False

    #revert lines to original
    line1, line2 = temp1, temp2
    temp1, temp2 = (line1[0], line1[1], line2[0], line2[1]), (line1[0], line1[1], line2[2], line2[3])
    sign1, sign2 = sign(cross_product(line2, temp1)), sign(cross_product(line2, temp2))
    if 

    # return True

def min_dist_between_lines(line1, line2):
    #check if lines intersect
    if check_lines_intersect(line1, line2): 
        print("intersect: " + str(line1) + ", " + str(line2))
        return 0

    d1 = dot_to_dot_dist((line1[0], line1[1]), (line2[0], line2[1]))
    d2 = dot_to_dot_dist((line1[0], line1[1]), (line2[2], line2[3]))
    d3 = dot_to_dot_dist((line1[2], line1[3]), (line2[0], line2[1]))
    d4 = dot_to_dot_dist((line1[2], line1[3]), (line2[2], line2[3]))

    print("distances: ", end = "")
    print(d1, d2, d3, d4)

    return min(d1, d2, d3, d4)


# def min_dist_between_lines(line1, line2):
#     #line 1 is reference line!

#     #check if lines cross first

#     temp1 = (line1[0], line1[1], line2[0], line2[1])
#     temp2 = (line1[0], line1[1], line2[2], line2[3])

#     sign1 = sign(cross_product(line1, temp1))
#     sign2 = sign(cross_product(line1, temp2))

#     print("lines: " + str(line1) + ", " + str(line2) + ", signs: " + str(sign1) + "," + str(sign2))

#     if sign1 == 0 and sign2 == 0: return 0 #collinear
#     if sign1 != sign2: #potentially crosses

    
#     d1 = dot_to_dot_dist((line1[0], line1[1]), (line2[0], line2[1]))
#     d2 = dot_to_dot_dist((line1[0], line1[1]), (line2[2], line2[3]))
#     d3 = dot_to_dot_dist((line1[2], line1[3]), (line2[0], line2[1]))
#     d4 = dot_to_dot_dist((line1[2], line1[3]), (line2[2], line2[3]))

#     print("distances: ", end = "")
#     print(d1, d2, d3, d4)

#     return min(d1, d2, d3, d4)

def min_dist_point_to_line(dot, line):
    dist1 = dot_to_dot_dist(dot, (line[0], line[1])) #dist to endpoint 1
    dist2 = dot_to_dot_dist(dot, (line[2], line[3])) #dist to endpoint 2
    
    #determine where dot lands in relation to line by getting the vectors 
    #of the two endpoints pointing to dot. if the signs match, then the closest point is 
    #one of the endpoints. if the signs differ, then the point is btween the endpoints

    start_to_dot = (line[0], line[1], dot[0], dot[1])
    end_to_dot = (line[2], line[3], dot[0], dot[1])
    sign1 = sign(dot_product(line, start_to_dot))
    sign2 = sign(dot_product(line, end_to_dot))

    # print("signs: ", end = "")
    # print(sign1, sign2, end = "")
    # print(", point: " + str(dot) + ", line: " + str(line))

    if sign1 == sign2: 
        if sign1 == -1: return dist1
        else:           return dist2
    
    
    length_of_line = line_length(line)
    # print(length_of_line)
    proj = dot_product(line, start_to_dot) / length_of_line


    # print("proj: " + str(proj) + " len: " + str(length_of_line) + " dot length: " + str(line_length(dot_to_line_start)))
    #calculate point of dot projected onto line
    v = vec_form(line)
    point = (line[0] + proj * v[0] / length_of_line, line[1] + proj * v[1] / length_of_line)
    # print("new point: " + str(point))
    dist3 = dot_to_dot_dist(dot, point)

    # print("dot: " + str(dot) + ", point " + str(point) + ", line: " + str(line) + ", distances: ", end = " ")
    # print("proj: " + str(proj) + ", point: " + str(dot) + ", line: " + str(line) + ", distances: ", end = "")
    print("distances: ", end = "")
    print(dist1, dist2, dist3)

    return min(dist1, dist2, dist3)

def does_alien_touch_wall(alien, walls, granularity):
    """ Determine whether the alien touches a wall

        Args:
            alien (Alien): Instance of Alien class that will be navigating our map
            walls (list): List of endpoints of line segments that comprise the walls in the maze in the format [(startx, starty, endx, endx), ...]
            granularity (int): The granularity of the map
        
        Return:
            True if touched, False if not
    """

    # print("touch wall")

    tolerance = alien.get_width() + granularity / math.sqrt(2)
    shape = alien.get_shape()
    print("alien: ", end = "")
    print(alien.get_centroid(), shape, alien.get_width(), alien.get_length(), granularity / math.sqrt(2))
    # print(shape)
    # print("walls: " + str(walls))
    
    if alien.is_circle():
        center = alien.get_centroid()
        # tolerance = alien.get_width() + granularity / math.sqrt(2)
        # print(center)
        for wall in walls:
            # print("xda: " + str(wall))
            dist = min_dist_point_to_line(center, wall)
            # print("dist: " + str(dist) + ", tolerance: " + str(tolerance))
            if dist < tolerance or np.isclose(dist, tolerance): 
                print("true: " + str(wall))
                return True
    else:
        head_and_tail = alien.get_head_and_tail()
        # print(head_and_tail)
        line = (head_and_tail[0][0], head_and_tail[0][1], head_and_tail[1][0], head_and_tail[1][1])
        print(line)
        # tolerance = alien.get_width() + granularity / math.sqrt(2)
        for wall in walls:
            # print(line, wall)
            # print(wall)
            dist = min_dist_between_lines(line, wall)
            if dist < tolerance or np.isclose(dist, tolerance): 
                print("true. wall: " + str(wall) + ", dist: " + str(dist))
                return True

    print("false")
    return False

def does_alien_touch_goal(alien, goals):
    """Determine whether the alien touches a goal
        
        Args:
            alien (Alien): Instance of Alien class that will be navigating our map
            goals (list): x, y coordinate and radius of goals in the format [(x, y, r), ...]. There can be multiple goals
        
        Return:
            True if a goal is touched, False if not.
    """
    
    center = alien.get_centroid()
    for goal in goals:
        dist = dot_to_dot_dist(center, (goal[0], goal[1])) 
        tolerance = goal[2] + alien.get_width()
        if dist < tolerance or np.isclose(dist, tolerance): return True
    return False

def is_alien_within_window(alien, window,granularity):
    """Determine whether the alien stays within the window
        
        Args:
            alien (Alien): Alien instance
            window (tuple): (width, height) of the window
            granularity (int): The granularity of the map
    """

    # print("within window")
    # print(alien.get_shape())
    print("alien: ", end = "")
    print(alien.get_centroid(), alien.get_shape(), alien.get_width())
    print("maze: ", end = "")
    print(window, granularity)
    walls = [(0, 0, window[0], 0), (0, 0, 0, window[1]), 
             (window[0], 0, window[0], window[1]), (0, window[1], window[0], window[1])]

    center = alien.get_centroid()
    tolerance = alien.get_width() + granularity / math.sqrt(2)
    for wall in walls:
        # dist = min_dist_point_to_line(center, wall)
        # if dist < tolerance or np.isclose(dist, tolerance): return False
        # print("wall: " + str(wall))
        touch = does_alien_touch_wall(alien, [wall], granularity)
        # print(wall, touch)
        # if touch: print()
        # print("window: " + str(dist))

    
    # return True
    return not does_alien_touch_wall(alien, walls, granularity)

if __name__ == '__main__':
    #Walls, goals, and aliens taken from Test1 map
    walls =   [(0,100,100,100),  
                (0,140,100,140),
                (100,100,140,110),
                (100,140,140,130),
                (140,110,175,70),
                (140,130,200,130),
                (200,130,200,10),
                (200,10,140,10),
                (175,70,140,70),
                (140,70,130,55),
                (140,10,130,25),
                (130,55,90,55),
                (130,25,90,25),
                (90,55,90,25)]
    goals = [(110, 40, 10)]
    window = (220, 200)

    def test_helper(alien : Alien, position, truths):
        alien.set_alien_pos(position)
        config = alien.get_config()

        touch_wall_result = does_alien_touch_wall(alien, walls, 0) 
        # touch_goal_result = does_alien_touch_goal(alien, goals)
        # in_window_result = is_alien_within_window(alien, window, 0)

        assert touch_wall_result == truths[0], f'does_alien_touch_wall(alien, walls) with alien config {config} returns {touch_wall_result}, expected: {truths[0]}'
        # assert touch_goal_result == truths[1], f'does_alien_touch_goal(alien, goals) with alien config {config} returns {touch_goal_result}, expected: {truths[1]}'
        # assert in_window_result == truths[2], f'is_alien_within_window(alien, window) with alien config {config} returns {in_window_result}, expected: {truths[2]}'

    #Initialize Aliens and perform simple sanity check. 
    alien_ball = Alien((30,120), [40, 0, 40], [11, 25, 11], ('Horizontal','Ball','Vertical'), 'Ball', window)
    test_helper(alien_ball, alien_ball.get_centroid(), (False, False, True))

    alien_horz = Alien((30,120), [40, 0, 40], [11, 25, 11], ('Horizontal','Ball','Vertical'), 'Horizontal', window)	
    test_helper(alien_horz, alien_horz.get_centroid(), (False, False, True))

    alien_vert = Alien((30,120), [40, 0, 40], [11, 25, 11], ('Horizontal','Ball','Vertical'), 'Vertical', window)	
    test_helper(alien_vert, alien_vert.get_centroid(), (True, False, True))

    edge_horz_alien = Alien((50, 100), [100, 0, 100], [11, 25, 11], ('Horizontal','Ball','Vertical'), 'Horizontal', window)
    edge_vert_alien = Alien((200, 70), [120, 0, 120], [11, 25, 11], ('Horizontal','Ball','Vertical'), 'Vertical', window)

    alien_positions = [
                        #Sanity Check
                        (0, 100),

                        #Testing window boundary checks
                        (25.6, 25.6),
                        (25.5, 25.5),
                        (194.4, 174.4),
                        (194.5, 174.5),

                        #Testing wall collisions
                        (30, 112),
                        (30, 113),
                        (30, 105.5),
                        (30, 105.6), # Very close edge case
                        (30, 135),
                        (140, 120),
                        (187.5, 70), # Another very close corner case, right on corner
                        
                        #Testing goal collisions
                        (110, 40),
                        (145.5, 40), # Horizontal tangent to goal
                        (110, 62.5), # ball tangent to goal
                        
                        #Test parallel line oblong line segment and wall
                        (50, 100),
                        (200, 100),
                        (205.5, 100) #Out of bounds
                    ]

    #Truths are a list of tuples that we will compare to function calls in the form (does_alien_touch_wall, does_alien_touch_goal, is_alien_within_window)
    alien_ball_truths = [
                            (True, False, False),
                            (False, False, True),
                            (False, False, True),
                            (False, False, True),
                            (False, False, True),
                            (True, False, True),
                            (False, False, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True),
                            (False, True, True),
                            (False, False, True),
                            (True, True, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True)
                        ]
    alien_horz_truths = [
                            (True, False, False),
                            (False, False, True),
                            (False, False, False),
                            (False, False, True),
                            (False, False, False),
                            (False, False, True),
                            (False, False, True),
                            (True, False, True),
                            (False, False, True),
                            (True, False, True),
                            (False, False, True),
                            (True, False, True),
                            (True, True, True),
                            (False, True, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, False),
                            (True, False, False)
                        ]
    alien_vert_truths = [
                            (True, False, False),
                            (False, False, True),
                            (False, False, False),
                            (False, False, True),
                            (False, False, False),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True),
                            (False, False, True),
                            (True, True, True),
                            (False, False, True),
                            (True, True, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True)
                        ]

    for i in range(len(alien_positions)):
        test_helper(alien_ball, alien_positions[i], alien_ball_truths[i])
        test_helper(alien_horz, alien_positions[i], alien_horz_truths[i])
        # test_helper(alien_vert, alien_positions[i], alien_vert_truths[i])

    #Edge case coincide line endpoints
    test_helper(edge_horz_alien, edge_horz_alien.get_centroid(), (True, False, False))
    test_helper(edge_horz_alien, (110,55), (True, True, True))
    test_helper(edge_vert_alien, edge_vert_alien.get_centroid(), (True, False, True))


    print("Geometry tests passed\n")