import numpy as np
import utils

class Agent:    
    def __init__(self, actions, Ne=40, C=40, gamma=0.7):
        # HINT: You should be utilizing all of these
        self.actions = actions
        self.Ne = Ne # used in exploration function
        self.C = C
        self.gamma = gamma
        self.reset()
        # Create the Q Table to work with
        self.Q = utils.create_q_table()
        self.N = utils.create_q_table()
        
    def train(self):
        self._train = True
        
    def eval(self):
        self._train = False

    # At the end of training save the trained model
    def save_model(self,model_path):
        utils.save(model_path,self.Q)
        utils.save(model_path.replace('.npy', '_N.npy'), self.N)

    # Load the trained model for evaluation
    def load_model(self,model_path):
        self.Q = utils.load(model_path)

    def reset(self):
        # HINT: These variables should be used for bookkeeping to store information across time-steps
        # For example, how do we know when a food pellet has been eaten if all we get from the environment
        # is the current number of points? In addition, Q-updates requires knowledge of the previously taken
        # state and action, in addition to the current state from the environment. Use these variables
        # to store this kind of information.
        self.points = 0
        self.s = None
        self.a = None
    
    def act(self, environment, points, dead):
        '''
        :param environment: a list of [snake_head_x, snake_head_y, snake_body, food_x, food_y] to be converted to a state.
        All of these are just numbers, except for snake_body, which is a list of (x,y) positions 
        :param points: float, the current points from environment
        :param dead: boolean, if the snake is dead
        :return: chosen action between utils.UP, utils.DOWN, utils.LEFT, utils.RIGHT

        Tip: you need to discretize the environment to the state space defined on the webpage first
        (Note that [adjoining_wall_x=0, adjoining_wall_y=0] is also the case when snake runs out of the playable board)
        '''

        # determine reward
        reward = 0
        if points > self.points: reward = 1
        elif dead: reward = -1
        else: reward = -0.1

        # generate state @ time t + 1
        s_prime = self.generate_state(environment)

        # find optimal move at t = 0
        # if self.s == None and self.a == None: #t = 0
        #     move = None
        #     # print(s_prime)
        #     if   s_prime[2] != 2: move = utils.RIGHT
        #     elif s_prime[2] != 1: move = utils.LEFT
        #     elif s_prime[3] != 2: move = utils.DOWN
        #     else: move = utils.UP 

        #     self.a = move
        #     self.s = s_prime
        #     self.points = points
        #     return move
        
        # find optimal move, t != 0
        moves = [utils.RIGHT, utils.LEFT, utils.DOWN, utils.UP] # priority order
        best_move = None
        max_f = float('-inf')
        for move in moves:
            curr_f = 0
            if self.N[s_prime][move] < self.Ne: curr_f = 1
            else: curr_f = self.Q[s_prime][move]
            
            if curr_f > max_f: 
                max_f = curr_f
                best_move = move

        if self._train and self.s != None and self.a != None: #update Q and N tables, N first
            self.N[self.s][self.a] += 1
            
            #calc values needed for updating Q
            alpha = self.C / (self.C + self.N[self.s][self.a])
            best_next_Q = max(self.Q[s_prime][move] for move in moves) 
            new_Q = self.Q[self.s][self.a] + alpha * (reward + self.gamma * best_next_Q - self.Q[self.s][self.a])
            self.Q[self.s][self.a] = new_Q

        self.s = s_prime
        self.a = best_move
        self.points = points

        return best_move

    def generate_state(self, environment):
        # TODO: Implement this helper function that generates a state given an environment 
        food_dir_x = 0
        if   environment[3] < environment[0]: food_dir_x = 1
        elif environment[3] > environment[0]: food_dir_x = 2

        food_dir_y = 0
        if   environment[4] < environment[1]: food_dir_y = 1
        elif environment[4] > environment[1]: food_dir_y = 2

        adjoining_wall_x = 0
        num_grids = utils.DISPLAY_SIZE / utils.GRID_SIZE
        snake_head_row, snake_head_col = self.pos_to_cell(environment[0], environment[1])
        if   snake_head_col - 1 == 0: adjoining_wall_x = 1
        elif snake_head_col + 1 == num_grids - 1: adjoining_wall_x = 2

        adjoining_wall_y = 0
        if   snake_head_row - 1 == 0: adjoining_wall_y = 1
        elif snake_head_row + 1 == num_grids - 1: adjoining_wall_y = 2

        adjoining_body_top, adjoining_body_bottom, adjoining_body_left, adjoining_body_right = 0, 0, 0, 0
        for pos in environment[2]:
            snake_body_row, snake_body_col = self.pos_to_cell(pos[0], pos[1])
            if snake_head_row - 1 == snake_body_row: adjoining_body_top = 1
            if snake_head_row + 1 == snake_body_row: adjoining_body_bottom = 1
            if snake_head_col - 1 == snake_body_col: adjoining_body_left = 1
            if snake_head_col + 1 == snake_body_col: adjoining_body_right = 1

        
        return (food_dir_x, food_dir_y, adjoining_wall_x, adjoining_wall_y, 
            adjoining_body_top, adjoining_body_bottom, adjoining_body_left, adjoining_body_right)

    def pos_to_cell(self, x, y):
        col = x / utils.GRID_SIZE
        row = y / utils.GRID_SIZE

        return (row, col)