# Simps for the enemy queen
# Will do it's best to sacrifice its pieves to her
# True sacrifice is putting piece for queen unprotected
# Weak sacrifice is putting piece for queen protected
# Safe moves do not take the queen
# once surrendering is implemented it will give up if no safe moves

import random
from pieces import King, Queen, Rook, Bishop, Knight, Pawn
import math


def simpbot(board, color):
    my_moves = board.possible_moves(color)

    her_color = "white"
    if color == "white":
        her_color = "black"

    her_pieces = board.get_pieces(her_color)

    her_moves = []
    her_locs = []
    for piece in her_pieces:
        if isinstance(piece, Queen):
            her_moves.extend(piece.get_moves(board))
            her_locs.append(board.get_location(piece))

    if not her_moves:
        return random.choice(board.possible_moves(color))

    her_move_locs = []
    for move in her_moves:
        her_move_locs.append(move.target)

    my_sacrifice_moves = []
    for move in my_moves:
        if move.target in her_move_locs:
            my_sacrifice_moves.append(move)

    if my_sacrifice_moves:
        my_sacrifice_moves = sorted(
            my_sacrifice_moves,
            key=lambda x: min([math.dist(x.target, i) for i in her_locs]),
        )
        true_sacrifices = []
        for sacrifice_move in my_sacrifice_moves:
            true_sacrifice = True
            for move in my_moves:
                if move != sacrifice_move:
                    if move.target == sacrifice_move.target:
                        true_sacrifice = False
            if true_sacrifice:
                true_sacrifices.append(sacrifice_move)

        new_true_sacrifices = []
        if true_sacrifices:
            for move in true_sacrifices:
                if move.origin not in her_move_locs:
                    new_true_sacrifices.append(move)
        my_new_sacrifice_moves = []
        for move in my_sacrifice_moves:
            if move.origin not in her_move_locs:
                my_new_sacrifice_moves.append(move)

        if new_true_sacrifices:
            return random.choice(new_true_sacrifices)
        if my_new_sacrifice_moves:
            return random.choice(my_new_sacrifice_moves)
        if true_sacrifices:
            return random.choice(true_sacrifices)
        if my_sacrifice_moves:
            return random.choice(my_sacrifice_moves)

    safe_moves = []
    for move in my_moves:
        if move.target not in her_locs:
            safe_moves.append(move)
    if safe_moves:
        return random.choice(safe_moves)

    return random.choice(board.possible_moves(color))
