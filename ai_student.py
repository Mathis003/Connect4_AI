import random
import numpy as np

class Node:
    # Class that represent a node of the tree
    def __init__(self, move, value, board, count):
        self.__value = value
        self.__move = move
        self.__board = board
        self.__count = count
        self.__children = []

    def set_count(self, new_count):
        self.__count = new_count

    def get_count(self):
        return self.__count

    def get_children(self):
        return self.__children

    def get_value(self):
        return self.__value

    def set_value(self, new_value):
        self.__value = new_value

    def get_board(self):
        return self.__board

    def get_move(self):
        return self.__move

class Tree:
    # Class that represent the tree of all the possible moves for one move of the player
    def __init__(self, depth, board, player, opponent_player, root_move, root_value):
        self.depth = depth
        self.board = board
        self.player = player
        self.opponent_player = opponent_player
        self.root_move = root_move
        self.root_value = root_value

        self.root = Node(root_move, root_value, board, 1)

        self.number_move_played = number_move_played(self.board)
        self.count = 1

        self.createTree(depth)

    def createTree(self, depth):
        for i in range(depth):
            if i == 0:
                list_children = self.createChildren(self.root, self.board, self.player)
            else:
                for i in range(len(list_children)):
                    root = self.root.get_children()[i]
                    list_children += self.createChildren(root, self.board, self.player)

            # Inverse the players
            save_player = self.player
            self.player = self.opponent_player
            self.opponent_player = save_player

    def createChildren(self, root, board, player):
        all_possible_moves = determine_all_possible_moves(board)
        for move in all_possible_moves:
            new_board = np.copy(board)
            row, col = move[0], move[1]
            new_board[row][col] = player

            root.set_count(self.evaluation(new_board, self.player, row, col, root.get_count()))
            root.get_children().append(Node(move, root.get_count(), new_board, root.get_count()))
        return root.get_children()

    # TODO !!!!!!!!!!!!!!
    def evaluation(self, board, player, row, col, count):
        if search_win_stroke(board, player, row, col):
            if player == 1:
                count += 1
                return count
            else:
                count -= 1
                return count
        else:
            return count

def minimax(root_position, depth, alpha, beta, maximizing_player, minimizing_player):
    if depth == 0 or root_position.get_children() == []:
        return root_position.get_value()

    if maximizing_player:
        maxEval = -float('inf')
        for child in root_position.get_children():
            eval = minimax(child, depth - 1, alpha, beta, minimizing_player, maximizing_player)
            child.set_value(eval)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval

    else:
        minEval = float('inf')
        for child in root_position.get_children():
            eval = minimax(child, depth - 1, alpha, beta, maximizing_player, minimizing_player)
            child.set_value(eval)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval

def choose_best_score_with_move(player, opponent_player, root_position):
    best_score = minimax(root_position, 2, - float('inf'), float('inf'), player, opponent_player)
    list_best_score_child = []

    for child in root_position.get_children():
        if child.get_value() == best_score:
            list_best_score_child.append(child)

    if len(list_best_score_child) == 1:
        return (best_score, list_best_score_child[0].get_move()[1])
    else:
        return (best_score, random.choice(list_best_score_child).get_move()[1])

def number_move_played(board):
    sum = 0
    for row in range(6):
        for col in range(7):
            if board[row][col] != 0:
                sum += 1
    return sum

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

def determine_all_possible_moves(board):
    list_column = [i for i in range(len(board[0]))]
    list_column = remove_full_columns(board, list_column)
    list_moves = create_possible_moves(board, list_column)
    return list_moves

def ai_student(board, player):

    # If this is the first stroke of the game
    if Check_if_first_stroke_of_the_games(board):
        return int(len(board[0]) / 2) # Play at the middle (best strategy)

    opponent_player = 1
    if player == 1:
        opponent_player = 2

    list_moves = determine_all_possible_moves(board)

    if len(list_moves) == 1:
        col = list_moves[0][1]
        return col

    dico_best_score_with_move = {}
    for move in list_moves:
        tree = Tree(2, board, player, opponent_player, move, 0) # depth, board, player, opponent_player, root_move, root_value
        score, col = choose_best_score_with_move(player, opponent_player, tree.root)
        dico_best_score_with_move[score] = col

    max_score = max(dico_best_score_with_move.keys())
    col = dico_best_score_with_move[max_score]
    return col