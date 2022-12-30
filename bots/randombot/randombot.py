import random


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
