import numpy as np
import random as rd
from ai_student import ai_student

# The basic AI used for section 2 of the homework
def ai_random(arg_board, player):
    board = np.copy(arg_board)
    # Collects the moves which can be played (i.e. the nonfull columns)
    nonfull_cols = np.where(board[0] == 0)[0]
    for col in nonfull_cols:
        # Creates the attack and defense moves, to check if one is a winning move
        attack_board = np.copy(update_board(board, col, player))
        defense_board = np.copy(update_board(board, col, abs(player - 3)))
        # Plays if winning move for him
        if check_win(attack_board, col, player):
            # print('Plays attack move')
            return col
        # Plays if winning move for opponent
        elif check_win(defense_board, col, abs(player - 3)):
            # print('Plays defense move')
            return col
    # Otherwise, plays random
    return rd.choice(nonfull_cols)


def update_board(arg_board, col, player):
    board = np.copy(arg_board)
    # The arguments are the board and the last move of the last player
    for i in range(5, -1, -1):
        if board[i][col] == 0:
            board[i][col] = player
            return board


def print_board(board):
    # For visualisation
    for i in range(6):
        print('|', end='')
        for j in range(7):
            if board[i][j] == 1:
                print('🔴 ', end='')  # Change the red dot with '1' or 'x' if your terminal does not support colours
            elif board[i][j] == 2:
                print('🔵 ', end='')  # Change the blue dot with '2' or 'o' if your terminal does not support colours
            else:
                print('   ', end='')
        print('|')
    print('')


def check_win(board, col, player):
    # This function checks if the player won with his last move.
    # The arguments are the board and the last move of the last player.
    # First, we locate the row of this last move.
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


def run_game():
    # Run the game. In 21 turns, the board is full and the game is over
    the_board = np.full((6, 7), 0)
    for x in range(21):
        # print('Player 🔴 turn:')
        ####################################################################################
        ### Replace the line below with your own AI for sections 3 and 4 of the homework ###
        ####################################################################################
        move1 = ai_student(the_board, 1)
        if the_board[0][move1] != 0:
            print('ERROR: The chosen column is already full.')
        the_board = update_board(the_board, move1, 1)
        #print_board(the_board) # Uncomment this line for visualisation / debugging
        if check_win(the_board, move1, 1):
            print('Player 🔴 won!')
            return 1

        # print('Player 🔵 turn:')
        ####################################################################################
        ### Replace the line below with your own AI for sections 3 and 4 of the homework ###
        ####################################################################################
        move2 = ai_random(the_board, 2)
        if the_board[0][move2] != 0:
            print('ERROR: The chosen column is already full.')
        the_board = update_board(the_board, move2, 2)
        #print_board(the_board)  # Uncomment this line for visualisation / debugging
        if check_win(the_board, move2, 2):
            print('Player 🔵 won!')
            return 2
    print('Draw!')
    return 0