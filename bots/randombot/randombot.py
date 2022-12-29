import random

def randombot(board, color):
    return random.choice(board.possible_moves(color))