# We will represent the blank tile using a 0, and keep track of its index
test_puzzle = [[2,3,6],[1,5,0],[4,7,8]]
index_blank = (1,2) 
puzzle_size = 3

# Prints a matrix in the square puzzle format
def print_matrix(matrix):
    print("")
    for i in range(len(matrix)):
        row = "\t"
        for j in range(len(matrix)):
            row+= (str(matrix[i][j]) + " ")
        print(row)
    print("")

# Swaps matrix entries at the two indices
# Each index should be a pair, to properly index
def swap_entries(matrix, index1, index2):
    matrix[index1[0]][index1[1]],matrix[index2[0]][index2[1]] = matrix[index2[0]][index2[1]],matrix[index1[0]][index1[1]] 

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

# The operators each return a tuple, this is the new blank index
def move_up(state, index):
    new_index = index[0]-1, index[1]
    swap_entries(state, index, new_index)
    index = new_index
    return index

def move_down(state, index):
    new_index = index[0]+1,index[1]
    swap_entries(state, index, new_index)
    index = new_index
    return index

print_matrix(test_puzzle)
index_blank = move_up(test_puzzle, index_blank)
print_matrix(test_puzzle)
index_blank = move_down(test_puzzle, index_blank)
print_matrix(test_puzzle)
index_blank = move_down(test_puzzle, index_blank)
print_matrix(test_puzzle)
