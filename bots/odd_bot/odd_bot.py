from board import Board
from collections import defaultdict
import random

def look_for_moves_to_odd(pieces: list, board):
    moves_to_make = []
    for piece in pieces:
        piece_moves = piece.get_moves(board)
        for move in piece_moves:
            if move.target[0] % 2 == 1:
                moves_to_make.append(move)
    if moves_to_make:
        return random.choice(moves_to_make)
    return None

def get_random_move(pieces: list, board):
    moves_to_make = []
    for piece in pieces:
        moves_to_make.extend(piece.get_moves(board))
    if moves_to_make:
        return random.choice(moves_to_make)
    return None
        
def odd_bot(board: Board, color):
    pieces_by_column = defaultdict(list)
    # sort pieces with available moves based on their current column
    for piece in [piece for piece in board.get_pieces(color) if piece.get_moves(board)]:
        pieces_by_column[board.get_location(piece)[0]].append(piece)

    even_pieces = []
    odd_pieces = []
    # sort pieces based on whether they're on an odd or even column
    for column, pieces in pieces_by_column.items():
        if column % 2 == 1:
            odd_pieces.extend(pieces)
        else:
            even_pieces.extend(pieces)

    # look for an even column'd piece that can move to an odd column
    # if we can't do that, look for an even column'd piece with a different move
    # if we can't do that, look for an odd piece that can move to another odd position
    # if we can't do that, move an odd piece to a gross even position
    move = look_for_moves_to_odd(even_pieces, board)
    if move is None:
        move = get_random_move(even_pieces, board)
    if move is None:
        move = look_for_moves_to_odd(odd_pieces, board)
    if move is None:
        move = get_random_move(odd_pieces, board)
    return move


   