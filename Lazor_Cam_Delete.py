'''
Software Carpentry Lazor Project
EN.540.635
Tianxin Zhang & Cameron Czerpak
'''
import numpy as np
import time
import scipy
import matplotlib.pyplot as plt
import itertools


class Lazor_class(object):
    '''
    '''
    def __init__(self, initial_pos, direction):
        '''
        '''
        # Add direction and position to class
        self.initial_pos = initial_pos
        self.direction = direction
        
    def lazor_data(self, grid):
        '''
        '''
        lazor_pos = self.initial_pos
        direction = self.direction
        
        def in_array(lazor_pos, direction):
            '''
            Adapted from Weekly Challenge 7 Given code
            "def pos_chk(x, y, nBlocks):"
            Validate if the coordinates specified (x and y)
            are within the maze.

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

            lazor_pos_x = lazor_pos[0] + direction[0]
            lazor_pos_y = lazor_pos[1] + direction[1]
            grid_x_len = len(grid[0])
            grid_y_len = len(grid)
            return (lazor_pos_x >= 0 and lazor_pos_x < grid_x_len and
                    lazor_pos_y >= 0 and lazor_pos_y < grid_y_len)
                    
def read_input_file(board):
    '''
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
    # Start with making grid
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
    # Store blocks allowed locations
    # in o_locations
    o_locations = []
    grid_text_y = 1
    for line in grid_text:
        grid_text_x = 1
        grid_line = [0]
        # grid_text_x = 1
        for letter in line:
            # Add o coordinate to list
            if letter == 'o':
                o_locations.append((grid_text_x,grid_text_y))
            # put letter into correct size grid
            grid_line.append(letter)
            grid_line.append(0)
            grid_text_x = grid_text_x + 2
        # increment
        grid[grid_text_y] = grid_line
        grid_text_y = grid_text_y + 2
    print(o_locations)
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
    lazors = [Lazor_class(lazor_index[0], lazor_index[1]) for lazor_index in lazor_list_read]

    return (grid, block_count, intersect_points, lazors,
            grid_x_len, grid_y_len, o_locations)
            
def board_solver_process(board):
    '''
    '''
    t1 = time.time()

    board_name = str(board)
    board_name = board_name.replace('.bff', '')

    # grid, blocks, lazors, goal = read_input_file(board)
    (grid, block_count, intersect_points, lazors,
        grid_x_len, grid_y_len, o_locations) = read_input_file(
        board)

    # Make list of blocks we can use
    block_list = []
    for b in block_count:
        if b == 'A':
            for ai in range(block_count.get('A')):
                block_list.append('A')
        if b == 'C':
            for ai in range(block_count.get('C')):
                block_list.append('C')
        if b == 'B':
            for ai in range(block_count.get('B')):
                block_list.append('B')

    ##################################
    # Need to add a faster solving method
    # place blocks where the lazor goes
    # current code takes too long
    #

    # intertools permutations is way too slow
    # for i in itertools.permutations(o_locations[:3]):
    # for i in itertools.permutations(o_locations):
    # tries_list = []
    # Random actually works much faster
    unsolved = True
    iterations = 1
    while unsolved:
        i = random.sample(o_locations, len(block_list))
        # tries_list.append(i)
        # if i in tries_list:
        #     continue

        for j in range(len(block_list)):
            # print(j)
            block_xy = i[j]
            i_x = block_xy[0]
            i_y = block_xy[1]
            grid[i_y][i_x] = block_list[j]

        # We now have our grid that we want to test
        #
        solve = ######################### Add your code
        if solve:
            print("Grid Solution")
            print(np.matrix(grid))
            t2 = time.time()
            print('Iterations = %s' % iterations)
            time_elapsed = t2 - t1
            print('Time Elapsed = %s' % time_elapsed)
            print("Solution saved as txt file")
            # Write solution file
            board_solution = board_name + "solution.txt"
            f = open(board_solution, 'w')
            solution_grid = []
            for y in range(1, len(grid), 2):
                for x in grid[y]:
                    if x == 0:
                        grid[y].remove(x)
                solution_grid.append(' '.join(grid[y]))
            solution_grid = '\n'.join(solution_grid)
            f.write(solution_grid)
            f.close()
            return

        # Remove placed blocks from grid
        # for the next loop
        for j in range(len(block_list)):
            block_xy = i[j]
            i_x = block_xy[0]
            i_y = block_xy[1]
            grid[i_y][i_x] = 'o'
        iterations = iterations + 1
        

if __name__ == '__main__':
    board_solver_process("mad_1.bff")
