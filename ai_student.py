import random
import numpy as np

class Node:
    # Class that represent a node of the tree
    def __init__(self, value, board, player, move):
        self.value = value
        self.board = board
        self.move = move
        self.player = player  # Player that played the move right now

        self.depth = 6
        self.children = []

    def create_children(self, player, list_parent_node, list_board):
        if self.depth == 0:
            return
        else:
            list_children = []
            new_list_board = []
            for i in range(len(list_parent_node)):

                board = list_board[i]
                parent = list_parent_node[i]
                available_moves = get_availables_moves(board)

                for move in available_moves:

                    row, col = move[0], move[1]
                    new_board = np.copy(board)
                    new_board[row][col] = player

                    child_node = Node(0, new_board, player, move)

                    parent.children.append(child_node)
                    list_children.append(child_node)
                    new_list_board.append(new_board)

            list_board = new_list_board
            list_parent_node = list_children
            self.depth -= 1
            self.create_children(get_opponent_player(player), list_parent_node, list_board)


def evaluate_win_game(board, player, maximizing_player, col):
    if check_connect4(board, player, col):
        if player == maximizing_player:
            return True, 1000
        else:
            return True, -1000
    return False, 0


def evaluate_position(board, maximizing_player):
    total_score = 0
    list_score_pos = [[3, 4, 5, 7, 5, 4, 3],
                      [4, 6, 8, 10, 8, 6, 4],
                      [5, 8, 11, 13, 11, 8, 5],
                      [5, 8, 11, 13, 11, 8, 5],
                      [4, 6, 8, 10, 8, 6, 4],
                      [3, 4, 5, 7, 5, 4, 3]]

    for i in range(6):
        for j in range(7):
            tile = board[i][j]
            if tile == maximizing_player:
                total_score += list_score_pos[i][j]
            elif tile == get_opponent_player(maximizing_player):
                total_score -= list_score_pos[i][j]

    return total_score


def minimax(root_node, depth, maximizing_player):

    if root_node.move != None:

        enter, value_player = evaluate_win_game(root_node.board, root_node.player, maximizing_player, root_node.move[1])
        value_player *= (depth + 1)

        if enter:
            root_node.children = []
            root_node.value = value_player
            return root_node.value

    if depth == 0:
        root_node.value = evaluate_position(root_node.board, maximizing_player)
        return root_node.value

    if root_node.player != maximizing_player:
        max_eval = -np.inf
        for child in root_node.children:
            eval = minimax(child, depth - 1, maximizing_player)
            max_eval = max(max_eval, eval)
        root_node.value = max_eval
        return max_eval

    else:
        min_eval = np.inf
        for child in root_node.children:
            eval = minimax(child, depth - 1, maximizing_player)
            min_eval = min(min_eval, eval)
        root_node.value = min_eval
        return min_eval


def choose_best_score_with_move(root_node, depth, maximizing_player):
    best_score = minimax(root_node, depth, maximizing_player)
    list_best_move = []

    for child in root_node.children:
        if child.value == best_score:
            list_best_move.append(child.move)

    if len(list_best_move) == 1:
        return list_best_move[0][1]

    else:
        return random.choice(list_best_move)[1]


def update_board(board, move, player):
    # This function updates the board
    board[move[0]][move[1]] = player


def get_availables_col(board):
    # Returns the available moves
    return np.where(board[0] == 0)[0]


def get_availables_moves(board):

    first_row = board[0]
    available_col = []
    for i in range(len(first_row)):
        if first_row[i] == 0:
            available_col.append(i)

    available_moves = []
    for col in available_col:
        for i in reversed(range(6)):
            if board[i][col] == 0:
                available_moves.append([i, col])
                break

    return available_moves


def check_connect4(board, player, col):
    # This function checks if the player won with his last move.
    # The arguments are the board and the last move of the last player.
    # First, we locate the row of this last move.
    row = 6
    for i in reversed(range(6)):
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

def ai_student(board, player):
    # This function is the AI that choose the best move

    board_copy = board.copy()

    if check_first_stroke(board_copy):
        return 3  # Best strategy to begin at the middle

    depth_tree = 6

    # Create the tree of all possible moves
    root_node = Node(0, board_copy, get_opponent_player(player), None)
    root_node.create_children(player, [root_node], [board_copy])

    best_col = choose_best_score_with_move(root_node, depth_tree, player)
    return best_col


board = [[0, 0, 0, 2, 0, 0, 0],
         [0, 0, 1, 1, 0, 0, 0],
         [0, 2, 1, 1, 1, 0, 0],
         [0, 1, 2, 1, 2, 0, 0],
         [1, 2, 1, 2, 1, 2, 0],
         [2, 2, 2, 1, 1, 2, 0]]

print(ai_student(board, 1))