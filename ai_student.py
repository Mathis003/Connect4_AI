import numpy as np

class Node:

    # Class that represent a node of the tree

    def __init__(self, value, board, player, move):
        # Attributes of the node
        self.value = value
        self.board = board
        self.move = move
        self.player = player  # Player that played the move right now

        # Attributes of the tree (to create it)
        self.depth = 4
        self.children = []  # CREATE ALL THE TREE ! => Recursive function

    def create_children(self, player, list_parent_node, list_board, maximizing_player):
        if self.depth == 0:  # If we reach the maximum depth, we stop
            return
        else:  # Else, we create the children

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
                    new_board = np.copy(board) # Copy the board
                    new_board[row][col] = player

                    child_node = Node(0, new_board, player, move)  # Create the child node

                    enter, score = evaluate_win_game(child_node.board, child_node.player, maximizing_player, child_node.move[0], child_node.move[1])
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
            # Recursive call function
            self.create_children(get_opponent_player(player), list_parent_node, list_board, maximizing_player)


def evaluate_win_game(board, player, maximizing_player, row, col):
    # Check if the player wins the game
    if check_connect4(board, player, row, col):
        if player == maximizing_player:
            return True, 1000000  # The maximizing player wins
        else:
            return True, -1000000  # The minimizing player wins

    return False, 0  # No one wins


def evaluate_score(opponent_player, board, move, factor_mult):
    # This function evaluates the score of the move given in argument
    total_score = 0
    row, col = move[0], move[1]

    for j in range(-1, 2, 2): # For each direction
        count = 0
        for i in range(3):
            try:
                if board[row][col + j * i] == opponent_player:
                    count += 1
                else:
                    break
            except:
                break

        total_score += count * factor_mult

    for j in range(-1, 2, 2):  # For each direction
        count = 0
        for i in range(3):
            try:
                if board[row + j * i][col] == opponent_player:
                    count += 1
                else:
                    break
            except:
                break

        total_score += count * factor_mult

    for j in range(-1, 2, 2):  # For each direction
        count = 0
        for i in range(3):
            try:
                if board[row + j * i][col + j * i] == opponent_player:
                    count += 1
                else:
                    break
            except:
                break

        total_score += count * factor_mult

    for j in range(-1, 2, 2):  # For each direction
        count = 0
        for i in range(3):
            try:
                if board[row - j * i][col + j * i] == opponent_player:
                    count += 1
                else:
                    break
            except:
                break

        total_score += count * factor_mult

    return total_score


def evaluate_position(move):
    # This function evaluates the position of the board

    # Check the possible moves to do a connect4 for each tile => 1 point by connect4 possible
    list_score_pos = [[3, 4, 5, 7, 5, 4, 3],
                      [4, 6, 8, 10, 8, 6, 4],
                      [5, 8, 11, 13, 11, 8, 5],
                      [5, 8, 11, 13, 11, 8, 5],
                      [4, 6, 8, 10, 8, 6, 4],
                      [3, 4, 5, 7, 5, 4, 3]]

    score = list_score_pos[move[0]][move[1]]

    return 80 * score


def score_evaluation(player, opponent_player, board, move, maximizing_player, factor_mult1, factor_mult2):
    # This function evaluates the score of the board

    score = evaluate_score(opponent_player, board, move, factor_mult1) + evaluate_score(player, board, move, factor_mult2) + evaluate_position(move)

    if player != maximizing_player:
        return -score

    return score


def minimax(root_node, depth, maximizing_player):
    # This function is the minimax algorithm

    if depth == 0: # If we reach the maximum depth
        if root_node.value == 0:
            # Return the static evaluation of the position
            root_node.value += score_evaluation(root_node.player, get_opponent_player(root_node.player), root_node.board, root_node.move, maximizing_player, factor_mult1=5, factor_mult2=10)
        return root_node.value
    else:
        if root_node.children == []:
            return root_node.value

    # If it's the maximizing player
    if root_node.player != maximizing_player:
        max_eval = -np.inf
        for child in root_node.children:
            eval = minimax(child, depth - 1, maximizing_player) # Recursive call
            max_eval = max(max_eval, eval)
        root_node.value = max_eval # Update the value of the node
        return max_eval

    # If it's the minimizing player
    else:
        min_eval = np.inf
        for child in root_node.children:
            eval = minimax(child, depth - 1, maximizing_player) # Recursive call
            min_eval = min(min_eval, eval)
        root_node.value = min_eval # Update the value of the node
        return min_eval


def choose_best_score_with_move(root_node, depth, maximizing_player):
    # This function chooses the best move to do
    best_score = minimax(root_node, depth, maximizing_player) # Get the best score with the minimax algorithm
    list_best_child = []

    # Check which move(s) correspond to the best score
    for child in root_node.children:
        if child.value == best_score:
            list_best_child.append(child)

    # If there is only one move
    if len(list_best_child) == 1:
        return (list_best_child[0].move)[1]
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


def get_availables_moves(board):
    # This function returns the available moves

    # Get the available columns
    first_row = board[0]
    available_col = []
    for i in range(len(first_row)):
        if first_row[i] == 0:
            available_col.append(i)

    # Get the available moves (with row!)
    available_moves = []
    for col in available_col:
        for i in reversed(range(6)):
            if board[i][col] == 0:
                available_moves.append([i, col])
                break

    return available_moves


def check_connect4(board, player, row, col):
    # COPY/PASTE OF THE FUNCTION PROVIDED IN CONNECT4.PY
    # This function checks if the player wins the game => return True if he does, False otherwise.

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
    # This function returns the opponent player of the player given in argument.
    if player == 1:
        return 2
    else:
        return 1

def check_first_stroke(board):
    # This function checks if the board is empty (sum of all the elements of the board = 0)
    # If it is, it returns True, False otherwise.
    np_board = board.copy()
    if np.sum(np_board) == 0:
        return True
    return False

def ai_student(board, player):
    # This function is the AI that choose the best move. At least, he tries to :)

    board_copy = board.copy()

    if check_first_stroke(board_copy):
        return len(board[0]) // 2  # Best strategy to begin at the middle => Avoid to lose time to do some calculations whereas the middle is ALWAYS the best place to begin.

    # Too long for a depth greater than 6
    depth_tree = 4  # Depth of the tree (the number of "moves's floors" that the AI can foresee to do)

    # Create the tree of all possible moves
    root_node = Node(0, board_copy, get_opponent_player(player), None)
    root_node.create_children(player, [root_node], [board_copy], player)

    # Return the best column to play
    best_col = choose_best_score_with_move(root_node, depth_tree, player)
    return best_col