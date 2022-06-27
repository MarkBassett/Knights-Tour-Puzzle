# Time to refactor and split validation into a class with methods for each type of input

def check_type(v):
    # Is input type valid
    check_list = [t for t in v.split() if t.isdigit() or not t.isalpha()]
    if len(check_list) == 2:
        return [int(n) for n in v.split()]
    return [-1]

def dimension(v):
    coordinates = check_type(v)
    if coordinates:
        # Is move on a board?
        if [o for o in coordinates if 1 < o > 8]:
            coordinates = [-1]
    return coordinates

def on_board(v):
    coordinates = check_type(v)
    if coordinates == [-1]:
        return [-1]
    else:
        x, y = coordinates
    # if [p for i, p in enumerate(coordinates) if p < 0 or p > board_dimensions[i]]:
    if 0 > x < x_len or 0 > y < y_len:
        return [-1]
    return x - 1, y - 1

def yes_no(v):
    if v == 'y' or v == 'n':
        return [1, v]
    return [-4]

def move(v):
    global play
    coordinates = check_type(v)
    x, y = [n - 1 for n in coordinates]
    # Is move one of the available moves for knight?
    if type(chess_board[x][y]) == int:
        return [x, y]
    else:
        return [-3]


def get_input(message, func):
    while True:
        list_input = func(input(message))
        if list_input[0] < 0:
            print(error_messages[abs(list_input[0] + 1)], end='')
        else:
            break
    return list_input


def possible_moves(x_p, y_p):
    move_adj = [-1, -2, 1, -2, -1, 2, 1, 2, -2, -1, 2, -1, -2, 1, 2, 1]
    moves = []
    for pos in range(0, len(move_adj), 2):
        x_n = move_adj[pos] + x_p
        y_n = move_adj[pos + 1] + y_p
        if -1 < x_n < x_len and -1 < y_n < y_len and chess_board[x_n][y_n] == '_':
            moves.append(x_n)
            moves.append(y_n)
    return moves


def calc_moves(x, y):
    # Available moves for Knight
    available_moves = possible_moves(x, y)
    # Count potential moves for each available move
    moves = len(available_moves)
    min_moves = [0, 0, 9]
    for pos in range(0, len(available_moves), 2):
        x_pos = available_moves[pos]
        y_pos = available_moves[pos + 1]
        no_moves = possible_moves(x_pos, y_pos)
        move_from_pos = 0
        if no_moves:
            move_from_pos = int((len(no_moves) / 2))
            if min_moves[2] > move_from_pos:
                min_moves = [x_pos, y_pos, move_from_pos]
        chess_board[x_pos][y_pos] = move_from_pos
    min_moves.append(moves)
    return min_moves

def solve_tour(tot_av_moves, x_o, y_o, count=1):
    x_s, y_s = tot_av_moves[:2]
    x_o, y_o = x_s, y_s
    count += 1
    reset_chessboard(x_o, y_o, str(count))
    tot_av_moves = calc_moves(x_s, y_s)
    if tot_av_moves[3] == 0 or count == (x_len * y_len) - 1:
        if not does_solution_exist():
            test = [[x, y] for y in range(y_len) for x in range(x_len) if chess_board[x][y] == 0]
            x, y = test[0]
            reset_chessboard(x, y, str(count + 1))
        return
    else:
        return solve_tour(tot_av_moves, x_o, y_o, count)

def does_solution_exist():
    return [x for y in range(y_len) for x in range(x_len) if chess_board[x][y] == '_']



def display_chessboard():
    # Cell size based on size of board
    cell_size = len(str(x_len * y_len))
    # Border
    print(f' {(x_len * (cell_size + 1) + 3) * "-"}')
    # print(' ' + border)
    for y in range(y_len - 1, -1, -1):
        print(f'{y + 1}|', end=' ')
        for x in range(x_len):
            cell = str(chess_board[x][y])
            if cell == '_':
                cell = cell * cell_size
            print(f'{(" " * (cell_size - len(cell)))}{cell}', end=' ')
        print('|')
    print(f' {(x_len * (cell_size + 1) + 3) * "-"}')
    # print column margin
    print(' ' * (2 + cell_size), end='')
    for x in range(1, x_len + 1):
        print(x, end=' ' * cell_size)
    print()


def reset_chessboard(x, y, placeholder):
    chess_board[x][y] = placeholder
    for y in range(y_len):
        for x in range(x_len):
            if type(chess_board[x][y]) != str:
                chess_board[x][y] = '_'


# Initialise chess board
knight = ['X', '*']
error_messages = ["Invalid dimensions!", "Invalid position!", "Invalid move!", "Invalid input!"]
# board_dimensions = []
x_len, y_len = get_input('Enter your board dimensions: ', dimension)
# x_len, y_len = board_dimensions
chess_board = [['_' for y in range(y_len)] for x in range(x_len)]
# Set start position for Knight
x_s, y_s = get_input("Enter the knight's starting position:", on_board)
chess_board[x_s][y_s] = 'X'
tot_av_moves = calc_moves(x_s, y_s)

solve_puzzle = get_input('Do you want to try the puzzle? (y/n):', yes_no)
if solve_puzzle[1] == 'y':
    display_chessboard()
    solve_tour(tot_av_moves, x_s, y_s)
    if does_solution_exist():
        print('No solution exists!')
        play = False
    else:
        play = True
        chess_board = [['_' for y in range(y_len)] for x in range(x_len)]
        chess_board[x_s][y_s] = 'X'
        tot_av_moves = calc_moves(x_s, y_s)
else:
    play = False
    chess_board[x_s][y_s] = '1'
    solve_tour(tot_av_moves, x_s, y_s)
    if does_solution_exist():
        print('No solution exists!')
    else:
        print()
        print("Here's the solution!")
        display_chessboard()

# Main game after initial setup
while play:
    x_o, y_o = x_s, y_s
    x_s, y_s = get_input("Enter your next move:", move)
    chess_board[x_s][y_s] = 'X'
    reset_chessboard(x_o, y_o, '*')
    tot_av_moves =calc_moves(x_s, y_s)
    display_chessboard()
    if tot_av_moves[3] == 0:
        reset_chessboard(x_o, y_o, '*')
        not_visited = sum(chess_board[x].count('_') for x in range(x_len))
        visited = sum(chess_board[x].count('*') for x in range(x_len)) + 1
        if not_visited:
            print('No more possible moves!')
            print(f'Your knight visited {visited} squares!')
        else:
            print('What a great tour! Congratulations!')
        break

