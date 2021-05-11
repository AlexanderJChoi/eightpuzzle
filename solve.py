import heapq 


# We will represent the blank tile using a 0, and keep track of its index
test_puzzle = [[2,3,6],[1,5,0],[4,7,8]]
index_blank = (1,2) 
puzzle_size = 3

# the state we are searching for
solution_state = [[1, 2, 3] ,[4, 5, 6] ,[7, 8, 0]]  
solution_index = (2,2)

# Here are some sample puzzles
depth_0_puzzle = [[1, 2, 3],[4, 5, 6],[7, 8, 0]]
depth_0_index = (2,2)

depth_2_puzzle = [[1, 2, 3],[4, 5, 6],[0, 7, 8]]
depth_2_index = (2,0)

depth_4_puzzle = [[1, 2, 3],[5, 0, 6],[4, 7, 8]]
depth_4_index = (1,1)

depth_8_puzzle = [[1, 3, 6],[5, 0, 2],[4, 7, 8]]
depth_8_index = (1,1)

depth_12_puzzle = [[1, 3, 6],[5, 0, 7],[4, 8, 2]]
depth_12_index = (1,1)

depth_16_puzzle = [[1, 6, 7],[5, 0, 3],[4, 8, 2]]
depth_16_index = (1,1)

depth_20_puzzle = [[7, 1, 2],[4, 8, 5],[6, 3, 0]]
depth_20_index = (2,2)

depth_24_puzzle = [[0, 7, 2],[4, 6, 1],[3, 5, 8]]
depth_24_index = (0,0)

# this is the min priority queue data structure
min_heap = []

# We use a dictionary to determine repeated states
dictionary = {}

# Prints a matrix in the square puzzle format
def print_matrix(matrix):
    print("")
    for i in range(len(matrix)):
        row = "\t"
        for j in range(len(matrix)):
            row+= (str(matrix[i][j]) + " ")
        print(row)
    print("")

# Takes a square matrix, and an empty list, copies the matrix into the list
def copy_matrix(m1, m2):
    for i in range(len(m1)):
        m2.append(m1[i].copy())

# Create a unique hash value for a matrix
def hash_matrix(matrix):
    string = ""
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            string+=(str(matrix[i][j]))
    return string

# Swaps matrix entries at the two indices
# Each index should be a pair, to properly index
def swap_entries(matrix, index1, index2):
    matrix[index1[0]][index1[1]],matrix[index2[0]][index2[1]] = matrix[index2[0]][index2[1]],matrix[index1[0]][index1[1]] 

# Interface to create a custom puzzle
def custom_puzzle():
    print("Enter your puzzle, using 0 to represent the blank space. Enter only a single element at a time, pressing <ENTER> after each element.")
    puzzle = []
    index = (-1, -1)
    for i in range(puzzle_size):
        print("Enter row " + str(i) + ":")
        next_line = []
        for j in range (puzzle_size):
            num = int(input())
            next_line.append(num)
            if num == 0:
                index = (i, j)
        puzzle.append(next_line)

    return puzzle, index

# We describe the operators in terms of moving the blank space
# state is a matrix describing a state of the game
# index is a tuple describing the index of the blank space in state
def can_move_up(state, index):
    return (index[0] != 0) 

def can_move_down(state, index):
    return index[0] < (puzzle_size - 1)

def can_move_left(state, index):
    return index[1] != 0

def can_move_right(state, index):
    return index[1] < (puzzle_size - 1)

# The following are the four operatoes
# Each returns a tuple, this is the new blank index
def move_up(state, index):
    new_state = []
    copy_matrix(state, new_state)
    new_index = (index[0]-1, index[1])
    swap_entries(new_state, index, new_index)
    return new_state, new_index

def move_down(state, index):
    new_state = []
    copy_matrix(state, new_state)
    new_index = (index[0]+1,index[1])
    swap_entries(new_state, index, new_index)
    return new_state, new_index

def move_left(state, index):
    new_state = []
    copy_matrix(state, new_state)
    new_index = (index[0],index[1]-1)
    swap_entries(new_state, index, new_index)
    return new_state, new_index

def move_right(state, index):
    new_state = []
    copy_matrix(state, new_state)
    new_index = (index[0],index[1]+1)
    swap_entries(new_state, index, new_index)
    return new_state, new_index

# Returns all valid states we can reach from the input state
# Format of output is a list of (state, index) tuples
def get_adjacent_states(state, index):
    new_states = []
    if(can_move_up(state, index)):
        new_state, new_index = move_up(state, index)
        new_states.append((new_state, new_index))

    if(can_move_down(state, index)):
        new_state, new_index = move_down(state, index)
        new_states.append((new_state, new_index))

    if(can_move_left(state, index)):
        new_state, new_index = move_left(state, index)
        new_states.append((new_state, new_index))

    if(can_move_right(state, index)):
        new_state, new_index = move_right(state, index)
        new_states.append((new_state, new_index))

    return new_states
    
# Compares two (state, index) tuples, for equality
def states_are_equal(state1, index1, state2, index2):
    for i in range(len(state1)):
        for j in range(len(state1[0])):
            if state1[i][j] != state2[i][j]:
                return 0

    if index1[0] != index2[0]:
        return 0

    if index1[1] != index2[1]:
        return 0

    return 1

# Nodes in the Heap will consist of tuples (priority, depth, state, index)
def initialize_start_node(state, index, heuristic_func ):
    heuristic_val = heuristic_func(state)
    depth = 0
    priority = heuristic_val + depth

    new_node = (priority, depth, state, index)
    heapq.heappush(min_heap, new_node)

    hash_val = hash_matrix(state)
    dictionary[hash_val] = 1

# Empties heap to make ready for new solve
def reset_solution():
    while len(min_heap) != 0:
        heapq.heappop(min_heap)
    dictionary.clear()

# Here, we solve a puzzle, using a given heuristic function
def solve_puzzle(state, index, heuristic_func ):
    initialize_start_node(state, index, heuristic_func)
    nodes_expanded = 0
    max_nodes = 1
    while(1):
        if len(min_heap) == 0:
            print("NO SOLUTION FOUND :'(")
            return

        cn_priority, cn_depth, cn_state, cn_index = heapq.heappop(min_heap)
        if states_are_equal(cn_state, cn_index, solution_state, solution_index):
            print("SOLUTION FOUND ^_^")
            print_matrix(cn_state)
            print("SOLUTION DEPTH: " + str(cn_depth))
            print(str(nodes_expanded) + " NODES EXPANDED")
            print("MAX NODES IN MEMORY: " + str(max_nodes))
            return

        print("------------------------")
        print("EXPANDING NODE: ")
        print("NODE DEPTH: " + str(cn_depth))
        print("NODE HEURISTIC VALUE: " + str(heuristic_func(cn_state)))
        print_matrix(cn_state)
        print("------------------------")

        nn_depth = cn_depth + 1
        new_states = get_adjacent_states(cn_state, cn_index)
        for new_state, new_index in new_states:
            hash_val = hash_matrix(new_state)

            if hash_val not in dictionary:
                nn_priority = heuristic_func(new_state) + nn_depth
                new_node = (nn_priority, nn_depth, new_state, new_index)
                heapq.heappush(min_heap, new_node)
                
                dictionary[hash_val] = 1

        nodes_expanded+=1
        if len(min_heap) > max_nodes:
            max_nodes = len(min_heap)

# Here we define each heuristic
def uniform_cost_heuristic(state):
    return 0

def misplaced_tile_heuristic(state):
    count = 0
    for i in range(len(state)):
        for j in range(len(state)):
            if state[i][j] != solution_state[i][j] and state[i][j] != 0:
                count+=1

    return count

def manhattan_distance_heuristic(state):
    count = 0
    for i in range(len(state)):
        for j in range(len(state)):
            for k in range(len(solution_state)):
                for l in range(len(solution_state)):
                    if state[i][j] == solution_state[k][l] and state[i][j] != 0:
                        distance = abs(i-k) + abs(j-l)
                        count += distance

    return count

# Below, is the interface to initialize the puzzle to use, and decide which heuristic to use
while(1):
    chosen_puzzle = []
    chosen_heuristic = uniform_cost_heuristic
    print("Let's Solve an 8 Puzzle!!")
    a = """Which puzzle would you like to use?
            (0) Use a custom puzzle
            (1) Use a 0-depth puzzle
            (2) Use a 2-depth puzzle
            (3) Use a 4-depth puzzle
            (4) Use a 8-depth puzzle
            (5) Use a 12-depth puzzle
            (6) Use a 16-depth puzzle
            (7) Use a 20-depth puzzle
            (8) Use a 24 depth puzzle
            """
    puzzle_option = int(input(a))

    if puzzle_option == 0:
        chosen_puzzle, chosen_index = custom_puzzle()
    elif puzzle_option == 1:
        copy_matrix(depth_0_puzzle, chosen_puzzle)
        chosen_index = depth_0_index
    elif puzzle_option == 2:
        copy_matrix(depth_2_puzzle, chosen_puzzle)
        chosen_index = depth_2_index
    elif puzzle_option == 3:
        copy_matrix(depth_4_puzzle, chosen_puzzle)
        chosen_index = depth_4_index
    elif puzzle_option == 4:
        copy_matrix(depth_8_puzzle, chosen_puzzle)
        chosen_index = depth_8_index
    elif puzzle_option == 5:
        copy_matrix(depth_12_puzzle, chosen_puzzle)
        chosen_index = depth_12_index
    elif puzzle_option == 6:
        copy_matrix(depth_16_puzzle, chosen_puzzle)
        chosen_index = depth_16_index
    elif puzzle_option == 7:
        copy_matrix(depth_20_puzzle, chosen_puzzle)
        chosen_index = depth_20_index
    elif puzzle_option == 8:
        copy_matrix(depth_24_puzzle, chosen_puzzle)
        chosen_index = depth_24_index
    else:
        print("OPTION NOT RECOGNIZED. RESTARTING")
        continue


    a = """Which heuristic would you like to use?\n
            (1) No Heuristic (Uniform Cost Search)
            (2) Misplaced Tile Heuristic
            (3) Manhattan Distance Heuristic
            """
    heuristic_option = int(input(a))
    if heuristic_option == 1:
        chosen_heuristic = uniform_cost_heuristic
    elif heuristic_option == 2:
        chosen_heuristic = misplaced_tile_heuristic
    elif heuristic_option == 3:
        chosen_heuristic = manhattan_distance_heuristic
    else:
        print("OPTION NOT RECOGNIZED. RESTARTING")
        continue


    solve_puzzle(chosen_puzzle, chosen_index, chosen_heuristic)
    reset_solution()
