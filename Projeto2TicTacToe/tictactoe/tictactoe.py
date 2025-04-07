"""
Tic Tac Toe Player
"""
import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    qtd_de_x = 0;
    qtd_de_o = 0;
    for i in board:
        for j in i:
            if j == 'X':
                qtd_de_x += 1
            elif j == "O":
                qtd_de_o += 1
            else:
                continue
            
    if qtd_de_x <= qtd_de_o:
        return X
    else: 
        return O
    
    raise NotImplementedError


def actions(board):
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))  # <-- Corrigido aqui
    return actions


def result(board, action):
    i, j = action
    if board[i][j] != EMPTY:
        raise Exception("Invalid move")
    
    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    for player in [X, O]:
        for row in board:
            if all(cell == player for cell in row):
                return player    
    
        for col in range(3):
            if all(player == board[row][col] for row in range(3)):
                return player
            
        if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
            return player

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    winnerOfTheGame = winner(board)
    if winnerOfTheGame == O or winnerOfTheGame == X:
        return True
    
    for i in board:
        for j in i:
            if j == EMPTY: 
                return False
    return True;
    


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    winnerOfTheGame = winner(board)
    if winnerOfTheGame == X:
        return 1;
    if winnerOfTheGame == O:
        return -1;
    return 0;
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board): return None
    
    if player(board) == X:
        best_value = -10000
        best_action = None
        possibleMoves = actions(board)
        for action in possibleMoves:
            newBoard = result(board, action)
            value = min_value(newBoard)
            if value > best_value:
                best_value = value
                best_action = action
        return best_action
    
    else:
        best_value = 10000
        best_action = None
        possibleMoves = actions(board)
        for action in possibleMoves:
            newBoard = result(board, action)
            value = max_value(newBoard)
            if value < best_value:
                best_value = value
                best_action = action
        return best_action
    
    
    raise NotImplementedError

def min_value(board):
    
    if terminal(board): 
        return utility(board)
    
    value = 10000
    possible_actions = actions(board)
    
    for action in possible_actions:
        value = min(value, max_value(result(board, action)))
    return value
    
def max_value(board):
    
    if terminal(board): 
        return utility(board)
    
    value = -10000
    possible_actions = actions(board)
    
    for action in possible_actions:
        value = max(value, min_value(result(board, action)))
    return value
    
    

    
