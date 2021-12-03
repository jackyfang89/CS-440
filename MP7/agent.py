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
        s_prime = self.generate_state(environment)

        # TODO: write your function here
        # print('hi')
        self.Q[s_prime][1] = 23

        print(self.Q[s_prime][1])


        return None

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