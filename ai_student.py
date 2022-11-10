import random
import numpy as np

def remove_full_columns(board, list_column):
    for i in range(len(board[0])):
        if board[0][i] != 0:
            list_column.remove(i)
    return list_column

def create_possible_moves(board, list_column):
    list_possible_moves = []
    for col in list_column:
        for i in reversed(range(len(board))):
            if board[i][col] == 0:
                list_possible_moves.append([i, col])
                break
    return list_possible_moves

def search_win_stroke(board, player, row, col):
    # The try/except allows to avoid error IndexOutOfBounds !
    # Vertical
    try:
        if (board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player):
            return True
    except:
        pass

    # Horizontale
    try:
        if (board[row][col + 1] == player and board[row][col - 1] == player and board[row][col - 2] == player):
            return True
    except:
        pass
    try:
        if (board[row][col + 1] == player and board[row][col - 1] == player and board[row][col + 2] == player):
            return True
    except:
        pass
    try:
        if (board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player):
            return True
    except:
        pass
    try:
        if (board[row][col - 1] == player and board[row][col - 2] == player and board[row][col - 3] == player):
            return True
    except:
        pass

    # Diagonale
    try:
        if (board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player):
            return True
    except:
        pass
    try:
        if (board[row - 1][col - 1] == player and board[row - 2][col - 2] == player and board[row - 3][col - 3] == player):
            return True
    except:
        pass
    try:
        if (board[row + 1][col - 1] == player and board[row + 2][col - 2] == player and board[row + 3][col - 3] == player):
            return True
    except:
        pass
    try:
        if (board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player):
            return True
    except:
        pass
    try:
        if (board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row + 1][col - 1] == player):
            return True
    except:
        pass
    try:
        if (board[row + 1][col - 1] == player and board[row + 2][col - 2] == player and board[row - 1][col + 1] == player):
            return True
    except:
        pass
    try:
        if (board[row - 1][col - 1] == player and board[row - 2][col - 2] == player and board[row + 1][col + 1] == player):
            return True
    except:
        pass
    try:
        if (board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row - 1][col - 1] == player):
            return True
    except:
        pass

    return False

def Check_if_first_stroke_of_the_games(board):
    for i in range(len(board[0])):
        if board[-1][i] != 0:
            return False
    return True


def evaluation_function(board, list_moves):
    random_number = random.randint(0, len(list_moves) - 1)
    return list_moves[random_number][1]



def ai_student(board, player):

    # If this is the first stroke of the game
    if Check_if_first_stroke_of_the_games(board):
        return int(len(board[0]) / 2) # Play at the middle (best strategy)

    opponent_player = 1
    if player == 1:
        opponent_player = 2

    list_column = [i for i in range(len(board[0]))]
    list_column = remove_full_columns(board, list_column)
    list_moves = create_possible_moves(board, list_column)

    if len(list_moves) == 1:
        col = list_moves[0][1]
        return col

    # Check if the player can win => Play the move.
    for move in list_moves:
        row, col = move[0], move[1]
        if search_win_stroke(board, player, row, col):
            return col

    # Check if the opponent player can win the next turn => Play the move to counter him.
    for move in list_moves:
        row, col = move[0], move[1]
        if search_win_stroke(board, opponent_player, row, col):
            return col

    # Check if the possible move allows to the opponent player to win the next turn => Remove the move from the list
    for move in list_moves:
        row, col = move[0], move[1]
        # Simulate that the move is played
        board[row, col] = player
        if row > 0:
            if search_win_stroke(board, opponent_player, row - 1, col):
                list_moves.remove([row, col])

        board[row, col] = 0 # Reupdate the good value

    # In this case if none of the player can win => Choose the best stroke to play
    # (None of the stroke allows to the opponent to directly wins).

    return evaluation_function(board, list_moves)