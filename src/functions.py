import numpy as np


################################
### --- Basics functions --- ###
################################

def update_board(arg_board, col, player):
    board = np.copy(arg_board)
    for i in range(5, -1, -1):
        if board[i][col] == 0:
            board[i][col] = player
            return board


def get_availables_moves(board):
    # Get the available columns
    first_row = board[0]
    available_col = []
    for i in range(len(first_row)):
        if first_row[i] == 0:
            available_col.append(i)

    # Get the available moves (with row!)
    available_moves = []
    for col in available_col:
        for i in reversed(range(6)):
            if board[i][col] == 0:
                available_moves.append([i, col])
                break

    return available_moves


def check_win(board, col, player):
    row = 6
    for i in range(6):
        if board[i][col] == player:
            row = i
            break

    # Check left
    if col > 2:
        if board[row][col - 1] == player:
            if board[row][col - 2] == player:
                if board[row][col - 3] == player:
                    return True
                
    # Check 2 lefts and 1 right
    if col > 1 and col < 6:
        if board[row][col - 1] == player:
            if board[row][col - 2] == player:
                if board[row][col + 1] == player:
                    return True
                
    # Check 1 left and 2 rights
    if col > 0 and col < 5:
        if board[row][col - 1] == player:
            if board[row][col + 1] == player:
                if board[row][col + 2] == player:
                    return True
                
    # Check right
    if col < 4:
        if board[row][col + 1] == player:
            if board[row][col + 2] == player:
                if board[row][col + 3] == player:
                    return True
                
    # Check up
    if row > 2:
        if board[row - 1][col] == player:
            if board[row - 2][col] == player:
                if board[row - 3][col] == player:
                    return True
                
    # Check 2 ups and 1 down
    if row > 1 and row < 5:
        if board[row - 1][col] == player:
            if board[row - 2][col] == player:
                if board[row + 1][col] == player:
                    return True
                
    # Check 1 up and 2 downs
    if row > 0 and row < 4:
        if board[row - 1][col] == player:
            if board[row + 1][col] == player:
                if board[row + 2][col] == player:
                    return True
                
    # Check down
    if row < 3:
        if board[row + 1][col] == player:
            if board[row + 2][col] == player:
                if board[row + 3][col] == player:
                    return True
                
    # Check NW (North West)
    if col > 2 and row > 2:
        if board[row - 1][col - 1] == player:
            if board[row - 2][col - 2] == player:
                if board[row - 3][col - 3] == player:
                    return True
                
    # Check 2 NW and 1 SE
    if col > 1 and col < 6 and row > 1 and row < 5:
        if board[row - 1][col - 1] == player:
            if board[row - 2][col - 2] == player:
                if board[row + 1][col + 1] == player:
                    return True
                
    # Check 1 NW and 2 SE
    if col > 0 and col < 5 and row > 0 and row < 4:
        if board[row - 1][col - 1] == player:
            if board[row + 1][col + 1] == player:
                if board[row + 2][col + 2] == player:
                    return True
                
    # Check SE (South East)
    if col < 4 and row < 3:
        if board[row + 1][col + 1] == player:
            if board[row + 2][col + 2] == player:
                if board[row + 3][col + 3] == player:
                    return True
                
    # Check NE
    if col < 4 and row > 2:
        if board[row - 1][col + 1] == player:
            if board[row - 2][col + 2] == player:
                if board[row - 3][col + 3] == player:
                    return True
                
    # Check 2 NE and 1 SW
    if col > 0 and col < 5 and row > 1 and row < 5:
        if board[row - 1][col + 1] == player:
            if board[row - 2][col + 2] == player:
                if board[row + 1][col - 1] == player:
                    return True
                
    # Check 1 NE and 2 SW
    if col > 1 and col < 6 and row > 0 and row < 4:
        if board[row - 1][col + 1] == player:
            if board[row + 1][col - 1] == player:
                if board[row + 2][col - 2] == player:
                    return True
                
    # Check SW
    if col > 2 and row < 3:
        if board[row + 1][col - 1] == player:
            if board[row + 2][col - 2] == player:
                if board[row + 3][col - 3] == player:
                    return True
    return False


def get_opponent_player(player):
    if player == 1:
        return 2
    else:
        return 1


def check_first_stroke(board):
    np_board = board.copy()
    if np.sum(np_board) == 0:
        return True
    return False


#################################
### --- Minimax algorithm --- ###
#################################


def minimax(root_node, depth, maximizing_player):
    # If we reach the maximum depth (base case)
    if depth == 0:
        if root_node.value == 0:
            root_node.value += score_evaluation(root_node.player, get_opponent_player(root_node.player), root_node.board, root_node.move, maximizing_player, factor_mult1=5, factor_mult2=10)
        return root_node.value
    else:
        if root_node.children == []:
            return root_node.value

    # If it's the maximizing player
    if root_node.player != maximizing_player:
        max_eval = -np.inf
        for child in root_node.children:
            eval = minimax(child, depth - 1, maximizing_player) # Recursive call
            max_eval = max(max_eval, eval)
        root_node.value = max_eval # Update the value of the node
        return max_eval

    # If it's the minimizing player
    else:
        min_eval = np.inf
        for child in root_node.children:
            eval = minimax(child, depth - 1, maximizing_player) # Recursive call
            min_eval = min(min_eval, eval)
        root_node.value = min_eval # Update the value of the node
        return min_eval


################################
### --- Score evaluation --- ###
################################

def evaluate_win_game(board, player, maximizing_player, col):
    if check_win(board, col, player):
        # If the maximizing player wins
        if player == maximizing_player:
            return (True, 1000000)
        # If the minimizing player wins
        else:
            return (True, -1000000)
    # If no one win
    return (False, 0)


def evaluate_score(opponent_player, board, move, factor_mult):
    total_score = 0
    row, col = move[0], move[1]

    for j in range(-1, 2, 2): # For each direction
        count = 0
        for i in range(3):
            try:
                if board[row][col + j * i] == opponent_player:
                    count += 1
                else:
                    break
            except:
                break

        total_score += count * factor_mult

    for j in range(-1, 2, 2):  # For each direction
        count = 0
        for i in range(3):
            try:
                if board[row + j * i][col] == opponent_player:
                    count += 1
                else:
                    break
            except:
                break

        total_score += count * factor_mult

    for j in range(-1, 2, 2):  # For each direction
        count = 0
        for i in range(3):
            try:
                if board[row + j * i][col + j * i] == opponent_player:
                    count += 1
                else:
                    break
            except:
                break

        total_score += count * factor_mult

    for j in range(-1, 2, 2):  # For each direction
        count = 0
        for i in range(3):
            try:
                if board[row - j * i][col + j * i] == opponent_player:
                    count += 1
                else:
                    break
            except:
                break

        total_score += count * factor_mult

    return total_score


def evaluate_board_position(move):
    list_score_pos = [[3, 4, 5, 7, 5, 4, 3],
                      [4, 6, 8, 10, 8, 6, 4],
                      [5, 8, 11, 13, 11, 8, 5],
                      [5, 8, 11, 13, 11, 8, 5],
                      [4, 6, 8, 10, 8, 6, 4],
                      [3, 4, 5, 7, 5, 4, 3]]

    score = list_score_pos[move[0]][move[1]]
    return 80 * score


def score_evaluation(player, opponent_player, board, move, maximizing_player, factor_mult1, factor_mult2):
    score = evaluate_score(opponent_player, board, move, factor_mult1) + evaluate_score(player, board, move, factor_mult2) + evaluate_board_position(move)

    if player != maximizing_player:
        return -score

    return score