import random
from utils import *


def randombot(board, color):
    return random.choice(board.possible_moves(color))

def randombot2(board, color):
    taking_moves = list()
    for move in board.possible_moves(color):
        if move.capture is not None:
            taking_moves.append(move)
    if taking_moves:
        return random.choice(taking_moves)
    else:
        return random.choice(board.possible_moves(color))

def randombot_plus(board, color):
    my_moves = board.possible_moves(color)
    their_moves = board.possible_moves(other_color(color))

    thier_capturing_moves = [move for move in their_moves if move.capture is not None]
    my_capturing_moves    = [move for move in my_moves    if move.capture is not None]
    
    threatened_pieces = [board[move.target] for move in thier_capturing_moves ]

    for piece in threatened_pieces:
        escape_moves = piece.get_moves() 
        for move in escape_moves:
            if move.capture is not None:
                return move
        if escape_moves:
            return random.choice(escape_moves)
    if my_capturing_moves:
        return random.choice(my_capturing_moves)
    return random.choice(my_moves)
