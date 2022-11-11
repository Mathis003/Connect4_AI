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

def search_win_strokePuiss2(board, player, row, col):
    # The try/except allows to avoid error IndexOutOfBounds !
    # Vertical
    count = 0
    try:
        if (board[row + 1][col] == player):
            count += 1
    except:
        pass

    # Horizontale
    try:
        if (board[row][col + 1] == player):
            count += 1
    except:
        pass
    try:
        if (board[row][col - 1] == player):
            count += 1
    except:
        pass

    # Diagonale
    try:
        if (board[row + 1][col + 1] == player):
            count += 1
    except:
        pass
    try:
        if (board[row - 1][col - 1] == player):
            count += 1
    except:
        pass
    try:
        if (board[row - 1][col + 1] == player):
            count += 1
    except:
        pass

    try:
        if (board[row + 1][col - 1] == player):
            count += 1
    except:
        pass
    return count

def search_win_strokePuiss3(board, player, row, col):
    # The try/except allows to avoid error IndexOutOfBounds !
    # Vertical
    count = 0
    try:
        if (board[row + 1][col] == player and board[row + 2][col] == player):
            count += 1
    except:
        pass

    # Horizontale
    try:
        if (board[row][col + 1] == player and board[row][col - 1]):
            count += 1
    except:
        pass
    try:
        if (board[row][col + 1] == player and board[row][col + 2] == player):
            count += 1
    except:
        pass
    try:
        if (board[row][col - 1] == player and board[row][col - 2]):
            count += 1
    except:
        pass

    # Diagonale
    try:
        if (board[row + 1][col + 1] == player and board[row + 2][col + 2] == player):
            count += 1
    except:
        pass
    try:
        if (board[row - 1][col - 1] == player and board[row - 2][col - 2] == player):
            count += 1
    except:
        pass
    try:
        if (board[row - 1][col - 1] == player and board[row + 1][col + 1] == player):
            count += 1
    except:
        pass

    try:
        if (board[row + 1][col - 1] == player and board[row + 2][col - 2] == player):
            count += 1
    except:
        pass
    try:
        if (board[row - 1][col + 1] == player and board[row - 2][col + 2] == player):
            count += 1
    except:
        pass
    try:
        if (board[row - 1][col + 1] == player and board[row + 1][col - 1] == player):
            count += 1
    except:
        pass
    return count


def search_win_stroke(board, player, row, col):
    # The try/except allows to avoid error IndexOutOfBounds !
    # Vertical
    count = 0
    try:
        if (board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player):
            count += 1
    except:
        pass

    # Horizontale
    try:
        if (board[row][col + 1] == player and board[row][col - 1] == player and board[row][col - 2] == player):
            count += 1
    except:
        pass
    try:
        if (board[row][col + 1] == player and board[row][col - 1] == player and board[row][col + 2] == player):
            count += 1
    except:
        pass
    try:
        if (board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player):
            count += 1
    except:
        pass
    try:
        if (board[row][col - 1] == player and board[row][col - 2] == player and board[row][col - 3] == player):
            count += 1
    except:
        pass

    # Diagonale
    try:
        if (board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player):
            count += 1
    except:
        pass
    try:
        if (board[row - 1][col - 1] == player and board[row - 2][col - 2] == player and board[row - 3][col - 3] == player):
            count += 1
    except:
        pass
    try:
        if (board[row + 1][col - 1] == player and board[row + 2][col - 2] == player and board[row + 3][col - 3] == player):
            count += 1
    except:
        pass
    try:
        if (board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player):
            count += 1
    except:
        pass
    try:
        if (board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row + 1][col - 1] == player):
            count += 1
    except:
        pass
    try:
        if (board[row + 1][col - 1] == player and board[row + 2][col - 2] == player and board[row - 1][col + 1] == player):
            count += 1
    except:
        pass
    try:
        if (board[row - 1][col - 1] == player and board[row - 2][col - 2] == player and board[row + 1][col + 1] == player):
            count += 1
    except:
        pass
    try:
        if (board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row - 1][col - 1] == player):
            count += 1
    except:
        pass

    return count

def Check_if_first_stroke_of_the_games(board):
    for i in range(len(board[0])):
        if board[-1][i] != 0:
            return False
    return True


def evaluation_function(board, player, opponent_player, list_moves):
    # Bloque 2 jetons (ennemi) = +10pts (Par blocage)
    # Fait au moins un duo de jetons = +5pts (Par duo)
    dicoPoints_move = {}
    for move in list_moves:
        total_points = 0
        row, col = move[0], move[1]
        total_points += 10 * search_win_strokePuiss3(board, opponent_player, row, col)
        total_points += 5 * search_win_strokePuiss2(board, player, row, col)
        dicoPoints_move[total_points] = move

    maxPoints = max(dicoPoints_move.keys())
    return dicoPoints_move[maxPoints][1]


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
        count = search_win_stroke(board, player, row, col)
        if count > 0:
            return col

    # Check if the opponent player can win the next turn => Play the move to counter him.
    for move in list_moves:
        row, col = move[0], move[1]
        count = search_win_stroke(board, opponent_player, row, col)
        if count > 0:
            return col

    # Check if the possible move allows to the opponent player to win the next turn => Remove the move from the list
    for move in list_moves:
        row, col = move[0], move[1]
        # Simulate that the move is played
        board[row, col] = player
        if row > 0:
            count = search_win_stroke(board, opponent_player, row - 1, col)
            if count > 0:
                list_moves.remove([row, col])

        board[row, col] = 0 # Reupdate the good value

        # Check if the possible move allows to the player to do a Puissance3
        # => Simulate a turn again to see if the player can always win
        for move in list_moves:
            row, col = move[0], move[1]
            count = search_win_strokePuiss3(board, player, row, col)
            if count != 0:
                # Simulate that the player play again to see if he can win (of two ways)
                board[row, col] = player
                list_columnSIMULATION = [i for i in range(len(board[0]))]
                list_columnSIMULATION = remove_full_columns(board, list_columnSIMULATION)
                list_movesSIMULATION = create_possible_moves(board, list_columnSIMULATION)
                for moveSIMULATION in list_movesSIMULATION:
                    countSIMULATION = search_win_stroke(board, player, moveSIMULATION[0], moveSIMULATION[1])
                    if countSIMULATION >= 2:
                        board[row, col] = 0
                        return col
                board[row, col] = 0


    # In this case if none of the player can win => Choose the best stroke to play
    # (None of the stroke allows to the opponent to directly wins).
    return evaluation_function(board, player, opponent_player, list_moves)