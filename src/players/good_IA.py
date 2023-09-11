from src.functions import *
import numpy as np

class Node:
    # Class that represent a node of the tree

    def __init__(self, value, board, player, move, depth):
        self.value = value
        self.board = board
        self.player = player
        self.move = move
        self.depth = depth
        self.children = []


    def create_children(self, player, list_parent_node, list_board, maximizing_player):
        # If we reach the maximum depth
        if self.depth == 0:
            return
        # Else, we create the children
        else:
            list_children = []
            new_list_board = []
            list_no_child = []

            for i in range(len(list_parent_node)):

                # Get the board and the parent node
                board = list_board[i]
                parent = list_parent_node[i]

                # Get the available moves
                available_moves = get_availables_moves(board)

                for move in available_moves:
                    row, col = move[0], move[1]
                    new_board = np.copy(board)
                    new_board[row][col] = player

                    # Create the child node
                    child_node = Node(0, new_board, player, move, self.depth)

                    enter, score = evaluate_win_game(child_node.board, child_node.player, maximizing_player, child_node.move[1])
                    if enter:
                        child_node.value = score * (self.depth + 1)
                        child_node.children = []
                        list_no_child.append(child_node)

                    parent.children.append(child_node)

                    if child_node not in list_no_child:
                        list_children.append(child_node)
                        new_list_board.append(new_board)

            list_board = new_list_board
            list_parent_node = list_children

            self.depth -= 1
            self.create_children(get_opponent_player(player), list_parent_node, list_board, maximizing_player)



class GOOD_IA:

    def __init__(self, depth_tree):
        self.depth_tree = depth_tree


    def get_best_move(self, root_node, depth, maximizing_player):
        best_score = minimax(root_node, depth, maximizing_player) # Get the best score with the minimax algorithm
        list_best_child = []

        # Check which move(s) correspond to the best score
        for child in root_node.children:
            if child.value == best_score:
                list_best_child.append(child)

        # If there is only one move
        if len(list_best_child) == 1:
            best_col = (list_best_child[0].move)[1]
        
        # If there are several moves
        else:
            # Get the best move with the static evaluation of the position (of the root_node's children)
            dico_score_move = {}
            for i in range(len(list_best_child)):
                score = score_evaluation(list_best_child[i].player, get_opponent_player(list_best_child[i].player), list_best_child[i].board, list_best_child[i].move, maximizing_player, factor_mult1=5, factor_mult2=10)
                dico_score_move[score] = (list_best_child[i].move)[1]

            best_score = max(dico_score_move.keys())
            best_col = dico_score_move[best_score]
        return best_col


    def get_move(self, board, player):

        board_copy = board.copy()

        if check_first_stroke(board_copy):
            return len(board[0]) // 2  # Best strategy to begin at the middle => Avoid to lose time to do some calculations whereas the middle is ALWAYS the best place to begin.

        # Create the tree of all possible moves
        root_node = Node(0, board_copy, get_opponent_player(player), None, self.depth_tree)
        root_node.create_children(player, [root_node], [board_copy], player)

        # Return the best column to play
        best_col = self.get_best_move(root_node, self.depth_tree, player)
        return best_col