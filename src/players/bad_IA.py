from src.functions import *
import random as rd

class BAD_IA:

    def __init__(self):
        pass

    def get_move(self, arg_board, player):
        board = np.copy(arg_board)
        nonfull_cols = np.where(board[0] == 0)[0]
        for col in nonfull_cols:

            # Creates the attack and defense moves, to check if one is a winning move
            attack_board = np.copy(update_board(board, col, player))
            defense_board = np.copy(update_board(board, col, abs(player - 3)))

            # Plays if winning move for him
            if check_win(attack_board, col, player):
                return col
            
            # Plays if winning move for opponent
            elif check_win(defense_board, col, abs(player - 3)):
                return col
            
        # Otherwise, plays random
        return rd.choice(nonfull_cols)