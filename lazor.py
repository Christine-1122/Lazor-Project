'''
Software Carpentry Lazor Project
EN.540.635
Tianxin Zhang & Cameron Czerpak
'''

import numpy
import scipy 
import matplotlib.pyplot as plt

class Lazor_class(object):
    '''
    Lazor class used for the solving
    Contains block movement and lazor movement
    Also checks which intersect points have been
    crossed.
    '''

    def __init__(self, initial_pos, direction):
        '''
        Initizalize lazor class with initial position
        of the lazor and the direction it's pointed
        ** Parameters **
            initial_pos: **
                Initial position of lazor
            direction: **
                Direction of lazor
        '''
        # Add direction and position to class
        self.direction = direction
        self.initial_pos = initial_pos


def read_input_file(board):
    '''
    Reads given input file

    ** Parameters **
        board: *string*
            name of the .bff file we wish to solve

    ** Outputs **
        grid: **
            Board grid points
        block_count: **
            Blocks that can be moved
        lazor_read: **
            Lazor start and direction
        intersect_points: **
            Points lazor must intersect

    '''
    # open .bff file
    board_open = open(board, 'r')
    # read board file
    board_open = board_open.readlines()
    # remove \n from each line
    # Source below
    # https://stackoverflow.com/questions/9347419/python-strip-with-n
    board_open = [line.replace('\n', '')
                  for line in board_open if line != '\n']

    # Create grid
    grid_start = board_open.index('GRID START')
    grid_end = board_open.index("GRID STOP")
    grid_text = [line.replace(' ', '')
                 for line in board_open[grid_start + 1:grid_end]]

    # Length of grid text to make grid
    # Source
    # (https://stackoverflow.com/questions/7108080/
    # python-get-the-first-character-of-the-first-string-in-a-list)
    grid_x_length = len(grid_text[0])
    grid_y_length = len(grid_text)
    # convert grid text size to actual grid size
    grid_x_length = grid_x_length * 2 + 1
    grid_y_length = grid_y_length * 2 + 1

    # make grid of correct size zeros
    # Source
    # https://stackoverflow.com/questions/13157961/2d-array-of-zeros
    grid = [[0] * grid_x_length] * grid_y_length

    # Add blocks to grid
    # initial positions
    # grid_text_x = 1
    grid_text_y = 1
    for line in grid_text:
        # set x back to 1 for every line
        grid_text_x = 1
        for letter in line:
            # put letter into correct size grid
            grid[grid_text_y][grid_text_x] = letter
            grid_text_x = grid_text_x + 2
        # increment
        grid_text_y = grid_text_y + 2


if __name__ == '__main__':
    board_solver('mad_1.bff')
