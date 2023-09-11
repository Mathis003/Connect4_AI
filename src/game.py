from src.functions import *

class Game:

    def __init__(self, player1, player2, verbose):
        self.player1 = player1
        self.player2 = player2
        self.verbose = verbose

    def run(self):
        the_board = np.full((6, 7), 0)
        for x in range(21): # After 21 turns, the board is full and the game is over => draw  
            move1 = self.player1.get_move(the_board, 1)
            the_board = update_board(the_board, move1, 1)
            if self.verbose:
                print_board(the_board)
            if check_win(the_board, move1, 1):
                if self.verbose:
                    print('Player 🔴 won!')
                return 1
            
            move2 = self.player2.get_move(the_board, 2)
            the_board = update_board(the_board, move2, 2)
            if self.verbose:
                print_board(the_board)
            if check_win(the_board, move2, 2):
                if self.verbose:
                    print('Player 🔵 won!')
                return 2
        if self.verbose:
            print('Draw!')
        return 0