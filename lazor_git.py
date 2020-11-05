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
from itertools import combinations


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
    # print(board_open)
    # print("\n")
    # remove \n from each line
    # Source below
    # https://stackoverflow.com/questions/9347419/python-strip-with-n
    board_open = [line.replace('\n', '')
                  for line in board_open if line != '\n']
    # Logic here??? replace the \n in each sentence
    # print(board_open)
    # print('\n')

    # Create grid; search element key word
    grid_start = board_open.index('GRID START')
    # print(grid_start)
    # print('\n')
    grid_end = board_open.index("GRID STOP")
    # print(grid_end)
    grid_text = [line.replace(' ', '')
                 for line in board_open[grid_start + 1:grid_end]]
    # print("GRID TEXT: ")
    # print(grid_text)

    # Length of grid text to make grid
    # Source
    # (https://stackoverflow.com/questions/7108080/
    # python-get-the-first-character-of-the-first-string-in-a-list)
    grid_x_len = len(grid_text[0])
    # print(grid_x_len)
    grid_y_len = len(grid_text)
    # print(grid_y_len)
    # convert grid text size to actual grid size
    grid_x_len = grid_x_len * 2 + 1
    grid_y_len = grid_y_len * 2 + 1

    # for mad_1.bff total of 9*9 as steps differences

    # make grid of correct size zeros
    # Source
    # https://stackoverflow.com/questions/13157961/2d-array-of-zeros
    grid = [[0] * grid_x_len] * grid_y_len
    # print("The grid is : ")
    # print(grid)
    # print(len(grid))
    # print("\n")

    # Add blocks to grid
    grid_text_y = 1
    for line in grid_text:
        grid_line = [0]
        # print("TEST GRID LINE")
        # print(grid_line)
        # print("\n")
        # grid_text_x = 1
        for letter in line:
            # put letter into correct size grid
            grid_line.append(letter)
            grid_line.append(0)
        # increment
        # print("Grid Line")
        # print(grid_line)# 4 lines of [0 o 0 o]
        # print('\n')
        grid[grid_text_y] = grid_line
        grid_text_y = grid_text_y + 2
        # Every other line show the result
    lazor = []
    for line in board_open[grid_end:]:
        # Start here we deal with fixed blocks, L and P
        # if the beginning of the line isn't in
        # a block name, it must be lazor info
        # or intersecting point info
        # line = line.strip('\n')
        if not line[0] in block_count_names:
            if line[0] == 'L':
                line = line.split(" ")
                lazor.append(((int(line[1]), int(line[2])), (int(
                    line[1]) + int(line[3]), int(line[2]) + int(line[4]))))
                # except:
                #     continue

                # lazor_list_read.append(
                #     [tuple(map(int, line.replace('L', '').split()[s:s + 2]))
                # for s in [0, 2]])
                # Seperating into two parts: initial and direction
                # seems like s in [0,1] or [0,1] is same
            elif line[0] == 'P':  # is a list
                intersect_points.append(
                    tuple(map(int, line.replace('P', '').split())))

        # if line starts with block letter
        # add it to the dictionary
        if line[0] in block_count_names:
            # add number of block type to dictionary
            block_count[line[0]] = int(line[2])

    print(grid)
    print('\n')
    print(block_count)
    print(intersect_points)
    # print(lazor_list_read)

    print(lazor)
    block_new = {k: v for k, v in block_count.items() if v != 0}
    # This is the original start point and move direction
    # print("\nLazor list read: ")
    # print(lazor_list_read)
    # Generate possible blocks that can put in the grid
    possible_position = []
    fixed_block = []
    # Attention: first if grid then grid[0] otherwise will be error
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if str(grid[i][j]) == 'o':
                possible_position.append((j, i))
            elif str(grid[i][j]).isupper():
                fixed_block.append(((j, i), grid[i][j]))
                # yarn_5: Fixed Blocks: 	[((3, 1), 'B'), ((1, 11), 'B')]
    # print("possible_position \n")
    # print(possible_position)
    # print("Fixed Blocks: \t")
    # print(fixed_block)
    # Find out a way to delete all zero since it is not user friendly to look at possible_position
    # adding possible position and fixed block for solving the algorithm
    return (grid, block_count, intersect_points, lazor,
            grid_x_len, grid_y_len, possible_position, fixed_block, block_new)


def dis_between_points(pointa, pointb):
    '''
    This function creates to calculate the distance between two points
    Return the distance between two points
    '''
    x = abs(pointa[0] - pointb[0])
    y = abs(pointa[1] - pointb[1])
    dis = np.sqrt(x**2 + y**2)
    return dis


class Block:
    '''
    Creating Block class for opaque, reflect and fefract
    '''

    def __init__(self, block_item):
        # Can put the x_grid_len and y_grid_len here
        # Saving block type and position to the block_items dictionary
        self.block_type = block_item[1]
        self.block_position = block_item[0]

    def generate_intersect(self):
        '''
        Generate all posible intersection
        '''
        x_step = self.block_position[0]
        y_step = self.block_position[1]
        possible_intersect_dictionary = {(x_step, y_step - 1): 'up', (x_step, y_step + 1)
                                          : 'down', (x_step - 1, y_step): 'left', (x_step, y_step - 1): 'right'}
        possible_point = ((x_step, y_step - 1),
                          (x_step, y_step + 1),
                          (x_step - 1, y_step),
                          (x_step + 1, y_step))
        return possible_point, possible_intersect_dictionary

    def find_intersection(self, lazor_start_finish):
        '''
        This function find intersection point on the block for given lasor
        if count>1 means the lazor intersect
        Also find how long the lazor travels
        '''
        dis = float('inf')  # Create an unbound upper value
        intersect_point, intersect_dict = Block.generate_intersect(self)
        # one step at a time
        count = 0
        a = (np.nan, np.nan)
        # Find out if an intersection occured
        sol = [[i, dis_between_points(lazor_start_finish[0], i)] for i in intersect_point if Lazor(
            lazor_start_finish).lazor_lintersect(i)]
        sol = sorted(sol, key=lambda x: x[1])
        len1 = len(sol)
        print(len1)
        if len1 != 0:
            a, dis = sol[0]
            # a is the next move here
            count = len1
        else:
            pass
        return a, intersect_point, intersect_dict, count, dis

    def reflect(self, lazor_start_finish):
        a, intersect_point, intersect_dict, _, _ = Block.find_intersection(
            self, lazor_start_finish)
        # Get specific key(values) for a given dictionary
        sur = intersect_dict.get(a)
        ori_dir = Lazor(lazor_start_finish).lazor_direction()
        if all(np.isnan(a)) is True:
            output = np.nan
        else:
            if sur == 'left' or sur == 'right':
                new_dir = (-ori_dir[0], ori_dir[1])
                output = (a[0] + new_dir[0], a[1] + new_dir[1])
            else:
                new_dir = (ori_dir[0], -ori_dir[1])
                output = (a[0] + new_dir[0], a[1] + new_dir[1])
        return(a, output),

    def refrect(self, lazor_start_finish):
        ori_dir = Lazor(lazor_start_finish).lazor_direction()
        reflect_lazor = Block.reflect(self, lazor_start_finish)
        if np.isnan(reflect_lazor[0][0][0]):
            return reflect_lazor + ((np.nan, np.nan),)
        else:
            new = ((reflect_lazor[0][0][0] + ori_dir[0], reflect_lazor[0][0][1] + ori_dir[1]),
                   (reflect_lazor[0][0][0] + 2 * ori_dir[0], reflect_lazor[0][0][1] + 2 * ori_dir[1]))
            # time 2 to go through the REFRECT BLOCK
            # example mad_1 from (3,6) to (2,5) and (1,4);direction(-1,-1)
            return reflect_lazor + (new,)

    def opaque(self, lazor_start_finish):
        # opaque block turns in array false
        # (a,np.nan) is intersection and out value should be nan
        a, _, _, _, _ = Block.find_intersection(self, lazor_start_finish)
        return(a, np.nan),

    def path(self, lazor_start_finish, dest):
        '''
        This is the function showed lazor path
        Lazor_start_finish is the point lazor start and where lazor fnished
        dest: This is destination list
        return value will be new destination point, new lazor, num of intersection and
        distance between lazor start and intersection
        '''
        intersection, _, _, ints_num, dis = Block.find_intersection(
            self, lazor_start_finish)
        if all(np.isnan(intersection)) or ints_num == 1:
            return dest, ((np.nan, np.nan),), ints_num, dis_between_points
        else:
            list_new = []
            if self.block_type == "B":
                new_lazor = Block.opaque(self, lazor_start_finish)
            elif self.block_type == "C":
                new_lazor = Block.refrect(self, lazor_start_finish)
            elif self.block_type == "A":
                new_lazor = Block.reflect(self, lazor_start_finish)
            for i in destination:
                # All the four parameters provided below
                if Lazor(lazor_start_finish).lazor_intersect(i) and point_between((lazor_lintersect[0], intersection), i):
                    pass
                else:
                    list_new.append(i)
            return list_new, new_lazor, ints_num, dis


class Lazor:

    def __init__(self, lazor_start_finish):
        self.lazor_start_finish = lazor_start_finish
        self.start = lazor_start_finish[0]
        self.finish = lazor_start_finish[1]

    def line(self):
        '''
        To calculate line slope and intersect
        Return slope and intersect
        '''
        k = (self.start[1] - self.finish[1]) / (self.start[0] - self.finish[0])
        b = self.start[1] - k * self.start[0]
        return k, b

    def lazor_intersect(self, test_point):  # P is the test_point
        '''
        Test if lazor pass through the test point
        if y = kx+b and the direction is same, which means the lazor pass the test point
        '''
        x1, y1 = test_point
        k, b = Lazor.line(self)
        direction = Lazor.lazor_direction(self)  # a tuple
        dis = k * x1 - y1 + b
        if test_point == self.start:
            return True
        else:
            sx, sy = self.start
            x_dif = x1 - sx
            y_dif = y1 - sy
            abs_x_dif = abs(x_dif)
            abs_y_dif = abs(y_dif)
            test_direction = (x_dif / abs_x_dif, y_dif / abs_y_dif)

            if dis == 0 and test_direction == direction:
                return True
            else:
                return False

    def lazor_direction(self):
        return (self.finish[0] - self.start[0], self.finish[1] - self.start[1])


def point_between(new_laser, test_point):
    """
    this is the function that calculate if the test point is between two point
    param new_laser: the two point given
    """
    start = new_laser[0]
    end = new_laser[1]
    if min([start[0], end[0]]) <= test_point[0] <= max([start[0], end[0]]) \
            and min([start[1], end[1]]) <= test_point[1] <= max([start[1], end[1]]):
        return True
    else:
        return False


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


def sol_to_file(board, solution, grid):
    '''
    This is a function to output the solution to a text file
    to show where the blocks need to present for solution
    :param file_path: the file path for the bff file
    :param solution: the solution generated
    :param grid: the board for the game
    :no return in this case
    '''
    output = board.split('.')[0] + '_solution.txt'
    name = board.split('.')[0].split(os.sep)[1]
    file_1 = open(outpot, 'w')
    file_1.write("Plese look at the solution for %s \n" % name)

    #################
    INTEST DELETING 0 here for solution
    #################
    # for sol in solution:
    #     c = s[0]
    #     grid[c[1]][c[0]] = sol[1]
    # for i in grid:
    #     for xi in i:
    #         file_1.write(xi + '\t')
    #     file_1.write('\n')
    file_1.close()
    print('Solution: %s and output file: %s. \n' % (name, output))


def solution(board):
    (grid, block_count, intersect_points, lazor, grid_x_len, grid_y_len,
     possible_position, fixed_block, block_new) = read_input_file(board)
    solution = board_solver_process(
        possible_position, fixed_block, lazor, intersect_points, block_new)
    print(solution)
    return solution


def board_solver_process(possible_position, fixed_block, lazor, point, block_new):
    '''
    Function that solvers the given puzzle
    ** Parameters **
            board: *string*
                name of the .bff file we wish to solve
    '''
    # Read input file
    (grid, block_count, intersect_points, lazor, grid_x_len, grid_y_len,
     possible_position, fixed_block, block_new) = read_input_file(board)

    # print(sum_block)
    # Check length of dictionary, remove the "0" value one
    # https://stackoverflow.com/questions/17095163/remove-a-dictionary-key-that-has-a-certain-value
    block_new = {k: v for k, v in block_count.items() if v != 0}
    print(block_new)
    sum_block_num = sum(block_new.values())
    key_len = len(block_new.keys())
    print(key_len)
    key = list(block_new.keys())  # shows the available key lists
    # for mad_1 A have 2 and C have 1;
    value_first = list(block_new.values())[0]
    # here showed A equals to 2
    # print(value_first)
    # print(key_len)
    # print(block_new)
    # if block_count.values() == 0:
    # print(fixed_block)
    for item in combinations(possible_position, sum_block_num):  # groups of three
        # All posible combinations for sum of blocks
        if key_len == 1:  # Only one kind of block is available
            block_list = []
            for i in item:
                block_list.append((i, key[0]))
                # Only have the first key since deleted the key not showing up
                # [((9, 7), 'A'), ((1, 9), 'A'), ((3, 9), 'A'), ((5, 9), 'A'), ((7, 9), 'A'), ((9, 9), 'A')]
            block_list.extend(fixed_block)  # adding fixed block to block list
            # print(block_list)
            boolean, result = lazor_check(block_list, lazor, point)
            if boolean == True:
                print('The result solved is: ')
                print(result)
                return boolean, result
        elif key_len == 2:  # 2 different kinds of keys/blocks
            block_list = []
            for i in combinations(item, value_first):  # 2 for A in mad_1
                # the left one not selected in group of three for mad_1
                key_1 = set(item) - set(i)
                # print(item)
                # print(i)
                # ((3, 7), (5, 7), (7, 7))
                # ((5, 7), (7, 7))
                for j in i:
                        # print(j)
                    block_list.append((j, key[0]))
                    # print(block_list)
                    # [((3, 7), 'A'), ((5, 7), 'A'), ((7, 7), 'C'), ((3, 7), 'A'), ((7, 7), 'A'), ((5, 7), 'C'), ((5, 7), 'A'), ((7, 7), 'A')]
                for x_1 in key_1:
                    block_list.append((x_1, key[1]))
                    # print(block_list)
                block_list.extend(fixed_block)
                boolean, result = lazor_check(block_list, lazor, point)
                if boolean == True:
                    return boolean, result
    # print(block_list)
    return block_new, block_list


def lazor_check(block_list, lazor, point):
    test_list = []
    count_2 = 0
    while True:
        lazor_use = []
        for l in lazor:
            point, lazor_use, new_lasor = lazor_trace(
                block_list, point, lazor_use, l)
            if len(lazor_use) == 0:
                if len(point) == 0:
                    return True, block_list
                else:
                    try:
                        np.isnan(new_lazor[0][1])
                        return False, block_list
                    except:
                        lazor = lazor_use
            elif lazor_use == lazor:
                if len(point) == 0:
                    return True, block_list
                else:
                    return False, block_list
            else:
                lazor = lazor_use
                for i in lazor_use:
                    if i in test_list:
                        count_2 += 1
                    else:
                        test.append(i)
                if count_2 > 3:
                    return False, block_list
                else:
                    pass


def lazor_trace(block_list, lazor_use, point, track):
        # deciding on separating the board solver for several functions since the
        # functions are too long to read
            # Lazor possible destinations
    count_1 = 0.0
    dis = float('inf')
    last_step = "None"
    for block_sample in block_list:
        bl = Block(block_sample)
        _, new_lazor, count, new_dis = bl.path(track, point)
        if count > 1:
            if new_dis < last_step:
                last_step = block_sample
                dis = new_dis
            else:
                pass
        else:
            count_1 += 1
    # A block in lasor path
    if last_step != 'None':
        bl = Block(last_step)
        point, new_lazor, count, _ = bl.path(track, point)
        for i in new_lazor:
            try:
                len(i[1])
                lazor_use.append(i)
            except:
                pass
        print(lazor_use)
        print(new_lazor)
    else:
        pass
    # See if lazor intersect a destination point
    if count_1 == len(block_list):
        point_new = [i for i in point if not Lazor(track).lazor_intersect(i)]
        point = point_new
    else:
        pass
    print(point)
    return point, lazor_use, new_lazor


if __name__ == '__main__':
    read_input_file('dark_1.bff')
    solution('dark_1.bff')
