# Lazor-Project

- This is software carpentry lazor project on Github.

- The goal of this project is find lazor game solution automatically

- Group Members: Tianxin Zhang & Cameron Czerpak

Run code:
-------------
Download all .bff files (dark_1.bff, mad_1.bff, mad_4.bff, mad_7.bff, numbered_6.bff, tiny_5.bff, yarn_5.bff) and lazor.py from github and place code in the same folder

To run the solver, run lazpr.py in your terminal and choose your options.

Reply yes or no to the prompts. If you choose yes for running all files from github, the code will run all the .bff files from above assuming they are in the current folder. If you don't have all the code in folder or wish to try the solution on a different file, you may run them individually by replying no to the first prompt and typing the file name you'd like to solve.

Code written for python 3.7

Files included: .bff files (dark_1.bff, mad_1.bff, mad_4.bff, mad_7.bff, numbered_6.bff, tiny_5.bff, yarn_5.bff), lazor.py and README

Instructions: 
-----------------
Code Logic:
  - Code calls start_solve - function for determing what .bff files you are solving
  - start_solve calls board_solver_process which is the main solving function
  - board_solver_process calls read_input_file - function used for opening and reading the files, based on the line differences with different elements, we could return a grid for each file. Outputs are returned to board_solver_process
  - board_solver_process begins a while loop where in every iteration of the loop it randomly places all available blocks on the board and and checks the solution with solution_check
  - solution_check calls the functions in Lazor_class to determine the lazors path through the blocks
  - The output is returned to board_solver_process. If the solution is correct, the correct block placement on the grid is outputted to the terminal and the results are saved as a text file
  
Notes: 
-----------------
  - Code originally used intertools.permutations of o_locations to try every grid combination. We found that solve time for 'mad_1.bff' was greater than 5 minutes. Instead, we chose i = random.sample(o_locations, len(block_list)), since random.sample runs faster than intertools.permutations. This is reflected in run time by even unlucky random guesses taking less than 1 minute on the challenging grids.

UNIT TEST:
--------------
- Time Elapsed and Iterations for each file and iterations.

  - For 'mad_1.bff' file:
  Iterations = 4375
  Time Elapsed = 0.06883692741394043 s

  - For 'mad_4.bff' file:
  Iterations = 64031
  Time Elapsed = 0.9391860961914062 s

  - For 'mad_7.bff' file:
  Iterations = 17402
  Time Elapsed = 0.45905303955078125 s

  - For 'numbered_6.bff' file:
  Iterations = 8027
  Time Elapsed = 0.13559293746948242 s
 
  - For 'yarn_5.bff' file:
  Iterations = 243313
  Time Elapsed = 5.374972820281982 s
  
  - For 'tiny_5.bff':
  Iterations = 2
  Time Elapsed = 0.0005657672882080078 s
  
  - For 'dark_1.bff':
  Iterations = 13
  Time Elapsed = 0.0005540847778320312 s
  
  
Output solution:
---------------

- A, B, C solution in the grid text file (reflect block, opaque block and refract block).
- x in the grid where no block is allowed.
