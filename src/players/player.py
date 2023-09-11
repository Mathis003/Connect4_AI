from src.functions import *

class Player:

    def __init__(self):
        pass

    def get_move(self, board, _):

        # Get the available moves
        available_moves = get_availables_moves(board)

        while True:
            col = int(input("Colonne n° : "))
            for i in range(len(available_moves)):
                if col == available_moves[i][1]:
                    return col
            print("This column is already full!")