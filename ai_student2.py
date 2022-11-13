import random
import numpy
import math

class Bitboard:

    # Represent the board as a bitboard
    # 6 13 20 27 34 41 48   55 62     Additional row (Only for computer reasons)
    # +---------------------+
    # | 5 12 19 26 33 40 47 | 54 61     top row
    # | 4 11 18 25 32 39 46 | 53 60
    # | 3 10 17 24 31 38 45 | 52 59
    # | 2  9 16 23 30 37 44 | 51 58
    # | 1  8 15 22 29 36 43 | 50 57
    # | 0  7 14 21 28 35 42 | 49 56 63  bottom row
    # +---------------------+

    def __init__(self, board, player):
        self.board = board
        self.player = player
        self.height = 0

    #                0 0 0 0 0 0 0  0 0 0 0 0 0 0   6 13 20 27 34 41 48
    # . . . . . . .  0 0 0 0 0 0 0  0 0 0 0 0 0 0   5 12 19 26 33 40 47
    # . . . . . . .  0 0 0 0 0 0 0  0 0 0 0 0 0 0   4 11 18 25 32 39 46
    # . . . . . . .  0 0 0 0 0 0 0  0 0 0 0 0 0 0   3 10 17 24 31 38 45
    # . . . O . . .  0 0 0 0 0 0 0  0 0 0 1 0 0 0   2  9 16 23 30 37 44
    # . . . X X . .  0 0 0 1 1 0 0  0 0 0 0 0 0 0   1  8 15 22 29 36 43
    # . . O X O . .  0 0 0 1 0 0 0  0 0 1 0 1 0 0   0  7 14 21 28 35 42
    # -------------
    # 0 1 2 3 4 5 6
    # => Return 0000000 0000000 0000010 0000011 0000000 0000000 0000000 // for X's
    def get_bitboard(self):
        # Returns a bitboard representation of the board
        position, mask = "", ""
        for j in reversed(range(7)):
            for i in range(6):
                # For position
                if self.board[i][j] == self.player:
                    position += "1"
                else:
                    position += "0"
                # For mask
                if self.board[i][j] == 0:
                    mask += "0"
                else:
                    mask += "1"

        return (position, mask)

    def get_position_mask_bitmap(self):
        position, mask = '', ''
        # Start with right-most column
        for j in range(6, -1, -1):
            # Add 0-bits to sentinel
            mask += '0'
            position += '0'
            # Start with bottom row
            for i in range(0, 6):
                mask += ['0', '1'][self.board[i, j] != 0]
                position += ['0', '1'][self.board[i, j] == self.player]
        return int(position, 2), int(mask, 2)

    #                 6 13 20 27 34 41 48
    # . . . . . . .   5 12 19 26 33 40 47
    # . . . . . . .   4 11 18 25 32 39 46
    # . . . 0 . . .   3 10 17 24 31 38 45
    # . . . O . . .   2  9 16 23 30 37 44
    # . . X X X . .   1  8 15 22 29 36 43
    # . x O X O . .   0  7 14 21 28 35 42
    # -------------
    # 0 1 2 3 4 5 6
    # => Return [0, 8, 17, 26, 31, 35, 42]
    def get_height(self):
        pass

class Connect4:

    def __init__(self, board, player):
        self.bitboard = Bitboard(board, player)
        self.position, self.mask = self.bitboard.get_bitboard()

        self.player = player
        self.player_position = self.position
        self.opponent_player_position = self.position & self.mask

    def check_if_connect4(self):
        # Operations on bitstring
        # & = AND operator
        # | = OR operator
        # >> = Shift right
        # << = Shift left

        # Vertical Check
        intermediary_position = self.player_position & (self.player_position >> 1)
        if intermediary_position & (intermediary_position >> 2):
            return True
        # Horizontal Check
        intermediary_position = self.player_position & (self.player_position >> 7)
        if intermediary_position & (intermediary_position >> 14):
            return True
        # Diagonal / Check
        intermediary_position = self.player_position & (self.player_position >> 8)
        if intermediary_position & (intermediary_position >> 16):
            return True
        # Diagonal \ Check
        intermediary_position = self.player_position & (self.player_position >> 6)
        if intermediary_position & (intermediary_position >> 12):
            return True
        return False


def ai_student(board, player):
    best_col = 0
    bitboard = Bitboard(board, player)
    print(bitboard.get_bitboard())
    print(bitboard.get_position_mask_bitmap())
    return best_col