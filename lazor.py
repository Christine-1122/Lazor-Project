'''
Software Carpentry Lazor Project
EN.540.635
Tianxin Zhang & Cameron Czerpak
'''
import numpy as np
import time
import random


class Lazor_class(object):
    '''
    Class for Lazor. Contains functions for how the lazor
    interacts with different block types and the points
    the lazor needs to cross
    '''

    def __init__(self, initial_pos, direction):
        '''
        Initialize Lazor_class with given initial
        position and associated direction
        ** Parameters **
            initial_pos: *typle* *int*
                Initial position of lazor
            direction: *tuple* *int*
                Direction of lazor
        '''
        # Add direction and position to class
        self.initial_pos = initial_pos
        self.direction = direction

    def intersect_pts_remaining(self, grid, intersect_points):
        '''
        Determine how many intersection points haven't been
        crossed after the lazor moves through the grid
        ** Parameters **
            grid: *list, list* *int*
                Grid with all blocks (A,B,and/orC) placed
            intersect_points: *list, tuple* *int*
                xy positions of points the lazor must cross
        ** Returns **
            intersect_pts_notcrossed: *list, tuple* *int*
                intersect_points not crossed by lazor
        '''
        # add intersection points to class
        self.intersect_points = intersect_points
        # determine where the lazor goes
        lazor_moves = self.lazor_data(grid)[1]
        # determine how many intersection points are left
        # from the lazor's movement
        intersect_pts_notcrossed = []
        for k in intersect_points:
            if k not in lazor_moves:
                intersect_pts_notcrossed.append(k)
        return intersect_pts_notcrossed

    def lazor_data(self, grid):
        '''
        Determine how many intersection points haven't been
        crossed after the lazor moves through the grid
        ** Parameters **
            grid: *list, list* *int*
                Grid with all blocks (A,B,and/orC) placed
        ** Returns **
            block_intersect: *list, tuple* *int*
                positions of blocks that the lazor intersected
            lazor_moves: *list, tuple* *int*
                positions on grid that the lazor intersected
        '''
        # Create variable for lazor position and direction
        # from class within the lazor data function
        lazor_pos = self.initial_pos
        direction = self.direction

        # Set up lists for block intersections and
        # lazor movement
        block_intersect = []
        lazor_moves = []
        lazor_moves.append(self.initial_pos)

        def in_array(lazor_pos, direction):
            '''
            Adapted from Weekly Challenge 7 Given code
            Validate if the coordinates specified (x and y)
            from lazor position are in the grid
            **Parameters**
                lazor_pos: *tuple*
                    lazor position (x, y)
                direction: *tuple*
                    lazor dirction (x, y)
            **Returns**
                True or False *bool*
                    Whether the coordiantes are valid (True) or not (False)
            '''
            # https://www.flake8rules.com/rules/W503.html
            # Choosing current best practice
            # Does show error but anit-pattern does
            # too
            # update lazor position x, and y with direction
            lazor_pos_x = lazor_pos[0] + direction[0]
            lazor_pos_y = lazor_pos[1] + direction[1]
            # get x and y length of grid
            grid_x_len = len(grid[0])
            grid_y_len = len(grid)
            # determine if lazor position is in grid
            return (lazor_pos_x >= 0 and lazor_pos_x < grid_x_len and
                    lazor_pos_y >= 0 and lazor_pos_y < grid_y_len)

        def block_new(lazor_pos, direction):
            '''
            Determine the position of the next block
            ** Parameters **
                lazor_pos: *tuple* *int*
                    lazor position (x, y)
                direction: *tuple* *int*
                    lazor dirction (x, y)
            ** Returns **
                block_1: *tuple* *int*
                    next block on path
            '''
            # determine initial x0 and y0
            x_0, y_0 = lazor_pos
            # determine new x and y
            x_1 = lazor_pos[0] + direction[0]
            y_1 = lazor_pos[1] + direction[1]

            # Determine next block location
            x_1y_0 = x_1 % 2 + y_0 % 2
            x_0y_1 = x_0 % 2 + y_1 % 2
            if x_1y_0 != 0:
                # create new block location
                block_1 = (x_1, y_0)
            elif x_0y_1 != 0:
                # create new block location
                block_1 = (x_0, y_1)
            else:
                return False
            # Return new block
            return block_1

        def reflect_block(lazor_pos, direction, block_next):
            '''
            When the lazor hits a reflect block, this function
            is called to change the lazor direction
            ** Parameters **
                lazor_pos: *tuple* *int*
                    lazor position (x, y)
                direction: *tuple* *int*
                    lazor dirction (x, y)
                block_next: *tuple* *int*
                    next block on path
            ** Returns **
                direction: *tuple* *int*
                    updated direction of lazor
            '''
            reflect_x = block_next[0] - lazor_pos[0]
            reflect_y = block_next[1] - lazor_pos[1]

            reflect_x_scale = 2 * reflect_x
            reflect_y_scale = 2 * reflect_y

            # update direction
            direction = (direction[0] - reflect_x_scale,
                         direction[1] - reflect_y_scale)
            return direction

        def refract_block(lazor_pos, direction, block_next):
            '''
            When the lazor hits a refract block, this function
            is called to change the lazor direction by calling
            the reflect_block function, and have the lazor
            continue on its current path.
            ** Parameters **
                lazor_pos: *tuple* *int*
                    lazor position (x, y)
                direction: *tuple* *int*
                    lazor dirction (x, y)
                block_next: *tuple* *int*
                    next block on path
            ** Returns **
                direction: *tuple* *int*
                    updated direction of lazor
            '''
            initial_pos_new = (lazor_pos[0] + direction[0],
                               lazor_pos[1] + direction[1])
            # start a new lazor along the orgin direction
            lazor_split = Lazor_class(initial_pos_new, direction)
            lazor_moves_split = lazor_split.lazor_data(grid)
            # get all the block and point crossed by the new lazor
            for i in lazor_moves_split[0]:
                block_intersect.append(i)
            for i in lazor_moves_split[1]:
                lazor_moves.append(i)
            # reflect the current lazor
            direction = reflect_block(lazor_pos, direction, block_next)
            return direction

        # Using function above, determine how the lazor moves
        # through the grid, and intersection points which are
        # crossed
        while in_array(lazor_pos, direction):
            # Determine next block and block type
            block_next = block_new(lazor_pos, direction)
            block_next_type = grid[block_next[1]][block_next[0]]
            # Check block type anc call appropriate function
            if block_next_type == 'A':
                direction = reflect_block(lazor_pos, direction, block_next)
            elif block_next_type == 'C':
                direction = refract_block(lazor_pos, direction, block_next)
            elif block_next_type == 'B':
                # End lazor's movement due to hitting
                # an opaque block
                return block_intersect, lazor_moves
            # If 'o', append block next due to it being
            # a free space
            elif block_next_type == 'o':
                block_intersect.append(block_next)

            # update the current point to the next point
            lazor_pos = (lazor_pos[0] + direction[0],
                         lazor_pos[1] + direction[1])
            lazor_moves.append(lazor_pos)
        return block_intersect, lazor_moves


def solution_check(lazors, grid, intersect_points):
    '''
    For each lazor in lazors, check if there are any
    intersection points that haven't been crossed
    ** Parameters **
        lazors: *object* *list*
            lazor position at start of solving
        grid: *list, list* *combination str and int*
            Grid with all blocks (A,B,and/orC) placed
        intersect_points: *list, tuple* *int*
                xy positions of points the lazor must cross
    ** Returns **
        True or False *bool*
            Whether block locations is a valid solution
    '''

    # add remaining intersect points to list
    for each_lazor in lazors:
        intersect_points = each_lazor.intersect_pts_remaining(
            grid, intersect_points)
    # if intersect_points is empty, all intersection points
    # have been crossed. Return truex to end the code
    if len(intersect_points) == 0:
        return True
    else:
        return False


def read_input_file(board):
    '''
    Open the .bff file, and output data for solving
    ** Parameters **
        board: *.bff file*
            input file with all game data
    ** Returns **
        grid: *list, list* *combination str and int*
            Grid with only o and x filled in at correct points
        block_count: *dict*
            Block totals of each type to dictionary
        intersect_points: *list*
            list of points lazor must intersect for completion
        lazors: *object* *list*
            lazor position and direction at start of solving
        o_locations: *list*
            (x,y) locations 'o's on grid where A,B, and C can go
    '''
    # Checking if a function is in .bff files
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
    try:
        board_open = open(board, 'r')
    except OSError:
        print("File does not exist in folder")
        exit()

    # print(board.split('.')[1])
    # read board file
    board_open = board_open.readlines()
    # remove \n from each line
    # Source below
    # https://stackoverflow.com/questions/9347419/python-strip-with-n
    board_open = [line.replace('\n', '')
                  for line in board_open if line != '\n']
    # Start with making grid
    # Create grid
    assert 'GRID START' in board_open, "GRID START missing from file"
    assert 'GRID STOP' in board_open, "GRID STOP missing from file"
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
                o_locations.append((grid_text_x, grid_text_y))
            # put letter into correct size grid
            grid_line.append(letter)
            grid_line.append(0)
            grid_text_x = grid_text_x + 2
        # increment
        grid[grid_text_y] = grid_line
        grid_text_y = grid_text_y + 2
    assert o_locations != [], "no locations to place blocks in .bff file"
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

    assert intersect_points != [], "Check .bff file for P values"
    lazors = []
    for lazor_index in lazor_list_read:
        lazors.append(Lazor_class(lazor_index[0], lazor_index[1]))
    assert lazors != [], "lazors are missing from .bff file"
    return (grid, block_count, intersect_points, lazors, o_locations)


def board_solver_process(board):
    '''
    This is the main function for solving the board.
    It calls read_input_file to read the board and inputs,
    then it sets up the potential blocks to be placed.
    Then blocks are randomly placed on the board and the
    the solution is checked.
    ** Parameters **
        board: *.bff file*
            input file with all game data
    ** Returns **
        boardsolution.txt *.txt file*
            Writes solution to text file
    '''
    # Start board timer
    t1 = time.time()

    # Create board name for saving
    board_name = str(board)
    board_name = board_name.replace('.bff', '')

    (grid, block_count, intersect_points, lazors,
        o_locations) = read_input_file(board)

    # Make list of blocks we can use
    block_list = []
    for b in block_count:
        if b == 'A':
            for ai in range(block_count.get('A')):
                block_list.append('A')
        elif b == 'C':
            for ai in range(block_count.get('C')):
                block_list.append('C')
        elif b == 'B':
            for ai in range(block_count.get('B')):
                block_list.append('B')

    # Originally tired every combination, but
    # intertools permutations is way too slow
    # Another way is to use combinations in itertools
    # for i in itertools.permutations(o_locations):
    # tries_list = []
    # Random actually works much faster
    unsolved = True
    iterations = 1
    while unsolved:
        i = random.sample(o_locations, len(block_list))

        for j in range(len(block_list)):
            # print(j)
            block_xy = i[j]
            i_x = block_xy[0]
            i_y = block_xy[1]
            grid[i_y][i_x] = block_list[j]

        # We now have our grid that we want to test
        solve = solution_check(lazors, grid, intersect_points)
        # if solve, we have the grid that works
        # Print the grid solution to the terminal
        # Print the time and number of iterations
        # Then create a txt file that saves the
        # block locations similar to how they're
        # shown in the input file
        if solve:
            print("Grid Solution")
            print(np.matrix(grid))
            t2 = time.time()
            print('Iterations = %s' % iterations)
            time_elapsed = t2 - t1
            print('Time Elapsed = %s s' % time_elapsed)
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


def start_solve():
    '''
    Starts solving process. Allows for user input
    and or using the standard boards for calling
    board_solver_process
    ** Parameters **
        None
    ** Returns **
        None
    '''
    print("You may either run a board file manually by")
    print("typing it's name or by running all .bff files")
    print("from github at once. Do you want to run all")
    print(".bff files from github?")
    print("Type 'yes' or 'no'")
    run_github = input()
    if run_github == 'yes':
        print("Are all files in the correct folder?")
        print("The files are tiny_5.bff, mad_1.bff")
        print("mad_4.bff, mad_7.bff, numbered_6.bff,")
        print("yarn_5.bff and dark_1.")
        print("Confirm with yes or no")
        all_boards = input()
        if all_boards == 'yes':
            board_solver_process("tiny_5.bff")
            board_solver_process("mad_1.bff")
            board_solver_process("mad_4.bff")
            board_solver_process("mad_7.bff")
            board_solver_process("numbered_6.bff")
            board_solver_process("yarn_5.bff")
            board_solver_process("dark_1.bff")
        else:
            print("move files to correct folder")
            print("and try again")
    elif run_github == 'no':
        print("Type the name of your file")
        print("for example, for mad_1.bff")
        print("Type: mad_1.bff")
        input_file = input()
        board_solver_process(input_file)
    else:
        print("Only options are yes or no")


if __name__ == '__main__':
    start_solve()
    # board_solver_process("tiny_5.bff")
    # board_solver_process("mad_1.bff")
    # board_solver_process("mad_4.bff")
    # board_solver_process("mad_7.bff")
    # board_solver_process("numbered_6.bff")
    # board_solver_process("yarn_5.bff")
