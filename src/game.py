from src.functions import *

class Game:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def run(self):
        the_board = np.full((6, 7), 0)
        for x in range(21): # After 21 turns, the board is full and the game is over => draw
            
            move1 = self.player1.get_move(the_board, 1)
            if the_board[0][move1] != 0:
                print('ERROR: The chosen column is already full.')
            the_board = update_board(the_board, move1, 1)
            print_board(the_board) # Uncomment this line for visualisation / debugging
            if check_win(the_board, move1, 1):
                print('Player 🔴 won!')
                return 1
            
            move2 = self.player2.get_move(the_board, 2)
            if the_board[0][move2] != 0:
                print('ERROR: The chosen column is already full.')
            the_board = update_board(the_board, move2, 2)
            print_board(the_board)  # Uncomment this line for visualisation / debugging
            if check_win(the_board, move2, 2):
                print('Player 🔵 won!')
                return 2
            
        print('Draw!')
        return 0