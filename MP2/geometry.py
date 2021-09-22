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

def check_collinear_intersect(line1, line2):
    #assumes line1 and line2 collinear.
    #horizontal case: make sure pointing left to right
    if line1[2] < line1[0]: line1 = (line1[2], line1[3], line1[0], line1[1])
    if line2[2] < line2[0]: line2 = (line2[2], line2[3], line2[0], line2[1])

    if max(line1[0], line2[0]) > min(line1[2], line2[2]): return False

    #vertical case: make sure pointing up
    if line1[3] < line1[1]: line1 = (line1[2], line1[3], line1[0], line1[1])
    if line2[3] < line2[1]: line2 = (line2[2], line2[3], line2[0], line2[1])

    if max(line1[1], line2[1]) > min(line1[3], line2[3]): return False

    return True

def orientation(a, b, c):
    #a, b, c are points
    #use the slope of AB(m1) compared to slope of BC(m2).
    #if m1 = m2, then collinear. if m1 > m2, then clockwise turn. if m1 < m2, ccw turn.
    #we can use m1 - m2. since m = dy/dx, we can do mult instead of div
    #return either 0, 1, or 2 as collinear, CW, CCW. 

    delta = (b[1] - a[1]) * (c[0] - b[0]) - (c[1] - b[1]) * (b[0] - a[0])
    if delta == 0: return 0
    if delta > 0 : return 1
    if delta < 0 : return 2

def check_lines_intersect(line1, line2):
    #we have 4 total orientations. let line1 = a, b and line2 = c,d
    #then we have: (a, b, c), (a, b, d), (c, d, a), (c, d, b)
    a, b, c, d = (line1[0], line1[1]), (line1[2], line1[3]), (line2[0], line2[1]), (line2[2], line2[3])
    o1, o2, o3, o4 = orientation(a, b, c), orientation(a, b, d), orientation(c, d, a), orientation(c, d, b)

    #collinear case, where line1 and line2 are collinear
    if o1 == 0 and o2 == 0 and o3 == 0 and o4 == 0: return check_collinear_intersect(line1, line2)
    #intersection case, where o1 != o2 and o3 != o4
    if o1 != o2 and o3 != o4: return True
    return False

def min_dist_between_lines(line1, line2):
    #check if lines intersect
    if check_lines_intersect(line1, line2): return 0

    d1 = min_dist_point_to_line((line1[0], line1[1]), line2)
    d2 = min_dist_point_to_line((line1[2], line1[3]), line2)
    d3 = min_dist_point_to_line((line2[0], line2[1]), line1)
    d4 = min_dist_point_to_line((line2[2], line2[3]), line1)

    return min(d1, d2, d3, d4)

def min_dist_point_to_line(dot, line):
    dist1 = dot_to_dot_dist(dot, (line[0], line[1])) #dist to endpoint 1
    dist2 = dot_to_dot_dist(dot, (line[2], line[3])) #dist to endpoint 2

    start_to_dot = (line[0], line[1], dot[0], dot[1])
    end_to_dot = (line[2], line[3], dot[0], dot[1])
    sign1 = sign(dot_product(line, start_to_dot))
    sign2 = sign(dot_product(line, end_to_dot))

    if sign1 == sign2: 
        if sign1 == -1: return dist1
        else:           return dist2
    
    length_of_line = line_length(line)
    proj = dot_product(line, start_to_dot) / length_of_line
    v = vec_form(line)
    point = (line[0] + proj * v[0] / length_of_line, line[1] + proj * v[1] / length_of_line)
    dist3 = dot_to_dot_dist(dot, point)

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
    tolerance = alien.get_width() + granularity / math.sqrt(2)
    
    if alien.is_circle():
        center = alien.get_centroid()
        for wall in walls:
            dist = min_dist_point_to_line(center, wall)
            if dist < tolerance or np.isclose(dist, tolerance): return True
    else:
        head_and_tail = alien.get_head_and_tail()
        line = (head_and_tail[0][0], head_and_tail[0][1], head_and_tail[1][0], head_and_tail[1][1])
        for wall in walls:
            dist = min_dist_between_lines(line, wall)
            if dist < tolerance or np.isclose(dist, tolerance): return True

    return False

def does_alien_touch_goal(alien, goals):
    """Determine whether the alien touches a goal
        
        Args:
            alien (Alien): Instance of Alien class that will be navigating our map
            goals (list): x, y coordinate and radius of goals in the format [(x, y, r), ...]. There can be multiple goals
        
        Return:
            True if a goal is touched, False if not.
    """
    
    if alien.is_circle():
        for goal in goals:
            dist = dot_to_dot_dist(alien.get_centroid(), (goal[0], goal[1]))
            tolerance = alien.get_width() + goal[2]
            if dist < tolerance or np.isclose(dist, tolerance): return True
    else:
        head_n_tail = alien.get_head_and_tail()
        line = (head_n_tail[0][0], head_n_tail[0][1], head_n_tail[1][0], head_n_tail[1][1])
        for goal in goals:
            dist = min_dist_point_to_line((goal[0], goal[1]), line)
            tolerance = alien.get_width() + goal[2]
            if dist < tolerance or np.isclose(dist, tolerance): return True
    return False

def is_alien_within_window(alien, window,granularity):
    """Determine whether the alien stays within the window
        
        Args:
            alien (Alien): Alien instance
            window (tuple): (width, height) of the window
            granularity (int): The granularity of the map
    """

    walls = [(0, 0, window[0], 0), (0, 0, 0, window[1]), 
             (window[0], 0, window[0], window[1]), (0, window[1], window[0], window[1])]
    
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
        touch_goal_result = does_alien_touch_goal(alien, goals)
        in_window_result = is_alien_within_window(alien, window, 0)

        assert touch_wall_result == truths[0], f'does_alien_touch_wall(alien, walls) with alien config {config} returns {touch_wall_result}, expected: {truths[0]}'
        assert touch_goal_result == truths[1], f'does_alien_touch_goal(alien, goals) with alien config {config} returns {touch_goal_result}, expected: {truths[1]}'
        assert in_window_result == truths[2], f'is_alien_within_window(alien, window) with alien config {config} returns {in_window_result}, expected: {truths[2]}'

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
        test_helper(alien_vert, alien_positions[i], alien_vert_truths[i])

    #Edge case coincide line endpoints
    test_helper(edge_horz_alien, edge_horz_alien.get_centroid(), (True, False, False))
    test_helper(edge_horz_alien, (110,55), (True, True, True))
    test_helper(edge_vert_alien, edge_vert_alien.get_centroid(), (True, False, True))


    print("Geometry tests passed\n")