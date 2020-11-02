'''
Software Carpentry Lazor Project
EN.540.635
Tianxin Zhang & Cameron Czerpak
'''

import os
import numpy
import scipy 
import matplotlib.pyplot as plt
import time
import numba as nb
#Using @git before functions
#numba here can extremely accelerate the code in pyhon

#f is file_name
lazer = []
intersect_point = []
block = {}
for line in open(f).readlines():
    line = line.strip('\n')
    if line == 'GRID START' or line == 'GRID STOP' or line[0] == '#' or line =='':
        continue
    elif line[0].isupper():
        line = line.split(' ')
        if line[0] == 'L':
            #previous(initial step, next step (x+vx, y+vy))
            lazer.append((line[1],line[2]),(line[1]+line[3], line[2]+line[4]))
        elif line[0] == 'P':
            intersect_point.append((line[1],line[2]))
        else:
            if line[1].isdigit():
                block[line[0] = int(line[1])
            else:
                for i in line:
                      if ##### Check other database 
                      

class Lazor_class(object):
    #I guess we should have both Lazor class and Block class;
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
        self.initial_pos = initial_pos
        self.direction = direction
        # Comment out in future
        print("Lazor Initial Position")
        print(self.initial_pos)
        print("Lazor Initial Direction")
        print(self.direction)
        
    def reflect_block(self, direction, grid):
        '''
        update direction if lazor hits reflect block
        during lazor data
        '''

    def refract_block(self, direction, grid):
        '''
        splits lazor direction into 2 paths
        during lazor data
        '''

    def opaque_block(self, drection, grid):
        '''
        Stops lazor movement during lazor data
        '''

    def lazor_data(self, grid):
        '''
        uses block type to determine info on lazor we need for solving
        '''
        # Read grid with ABC etc

        # While loop
        # Add direction to initial position
        # while in_array is true
        # the lazor is in the array

            # Add the diredtion to current position

            # check if current position is 0 or 1
            # if 0, lazor can travel there
            # change 0 to 1 to show lazor
            # is there, continue

            # if A its a reflect block
            # call reflect block to
            # change direction, but don;t change letter
            # on grid

            # if it's opaque call opaque_block and
            # stop lazor

            # if refract, call refract block
            # call lazor data again with new direciton
            # and continue with current direction

        # Check if intersect_points have gone from
        # 0 to 1
        # if true output solutions as a text file
        #
        # if not true, repeate with new grid
        # next loop of board_solver_process


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
    # set up our lists and dictionaries
    block_count = {'A': 0,
                   'B': 0,
                   'C': 0}
    block_count_names = ['A', 'B', 'C']
    # read added to end of lazor list to
    # show which function variable is
    # defined in
    lazor_list_read = []
    intersect_points = []
    
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
    grid_x_len = len(grid_text[0])
    grid_y_len = len(grid_text)
    # convert grid text size to actual grid size
    grid_x_len = grid_x_len * 2 + 1
    grid_y_len = grid_y_len * 2 + 1

    # make grid of correct size zeros
    # Source
    # https://stackoverflow.com/questions/13157961/2d-array-of-zeros
    grid = [[0] * grid_x_len] * grid_y_len

    # Add blocks to grid
    grid_text_y = 1
    for line in grid_text:
        grid_line = [0]
        # grid_text_x = 1
        for letter in line:
            # put letter into correct size grid
            grid_line.append(letter)
            grid_line.append(0)
        # increment
        grid[grid_text_y] = grid_line
        grid_text_y = grid_text_y + 2

    # index rest of .bff file to find
    # block count, lazor, and interesct points

    for line in board_open[grid_end:]:
        # if the beginning of the line isn't in
        # a block name, it must be lazor info
        # or intersecting point info
        if not line[0] in block_count_names:
            if line[0] == 'L':
                lazor_list_read.append(
                    [tuple(map(int, line.replace('L', '').split()[s:s + 2]))
                     for s in [0, 2]])
            elif line[0] == 'P':
                intersect_points.append(
                    tuple(map(int, line.replace('P', '').split())))
        # if line starts with block letter
        # add it to the dictionary
        if line[0] in block_count_names:
            # add number of block type to dictionary
            block_count[line[0]] = int(line[2])
    print(grid)
    print(block_count)
    print(intersect_points)
    print(lazor_list_read)
    return (grid, block_count, intersect_points, lazor_list_read,
            grid_x_len, grid_y_len)

def in_array(grid_x_len, grid_y_len, lazor_pos_x, lazor_pos_y):
    '''
    Adapted from Weekly Challenge 7 Given code "def pos_chk(x, y, nBlocks):"
    Validate if the coordinates specified (x and y) are within the maze.

    **Parameters**

        x: *int*
            An x coordinate to check if it resides within the maze.
        y: *int*
            A y coordinate to check if it resides within the maze.
        nBlocks: *int*
            How many blocks wide the maze is.  Should be equivalent to
            the length of the maze (ie. len(maze)).

    **Returns**

        valid: *bool*
            Whether the coordiantes are valid (True) or not (False).
    '''
    # https://www.flake8rules.com/rules/W503.html
    # Choosing current best practice
    # Does show error but anit-pattern does
    # too
    return (lazor_pos_x >= 0 and lazor_pos_x < grid_x_len and
            lazor_pos_y >= 0 and lazor_pos_y < grid_y_len)

def out_to_solution(file_path, solution, grid):
    '''
    This is a function to output the solution to a text file
    to show where the blocks need to present for solution
    :param file_path: the file path for the bff file
    :param solution: the solution generated
    :param grid: the board for the game
    :no return in this case
    '''
    output = file_path.split('.')[0]+'_solution.txt'
    name = file_path.split('.')[0].split(os.sep)[1]
    file_1 = open(outpot, 'w')
    file_1.write("Plese look at the solution for %s \n" % name)
    for sol in solution:
        c = s[0]
        grid[c[1]][c[0]] = sol[1]
    for i in grid:
        for xi in i:
            file_1.write(xi + '\t')
        file_1.write('\n')
    file_1.close()
    print('Solution: %s and output file: %s. \n' % (name,output))
    

def board_solver_process(board):
    '''
    Function that solvers the given puzzle

    ** Parameters **
            board: *string*
                name of the .bff file we wish to solve

    '''
    # Read input file
    grid, block_count, intersect_points, lazor_list_read = read_input_file(
        board)

    # Add lazor list to lazor class
    for lazor_list_index in lazor_list_read:
        Lazor_class(lazor_list_index[0], lazor_list_index[1])

    # Make every possible combination of solutions

    # sort solutions by most likely to work

    # begin testing

    # save solution

if __name__ == '__main__':
    board_solver_process('mad_1.bff')
