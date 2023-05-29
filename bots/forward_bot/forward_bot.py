from board import Board
import random
from collections import defaultdict

def forward_bot(board: Board, color):
    direction = 1 if color == 'white' else -1

    pieces_by_row = defaultdict(list)
    for piece in [piece for piece in board.get_pieces(color) if piece.get_moves(board)]:
        pieces_by_row[board.get_location(piece)[1]].append(piece)

    for row in list(pieces_by_row.keys())[::direction]:
        moves_for_row = []
        for piece in pieces_by_row[row]:
            biggest_moves = []
            biggest_diff = 0
            for move in piece.get_moves(board):
                diff = (move.target[1] - move.origin[1]) * direction
                if diff > biggest_diff and diff > 0:
                    biggest_moves = []
                    biggest_moves.append(move)
                    biggest_diff = diff
                elif diff == biggest_diff:
                    biggest_moves.append(move)
            if biggest_moves:
                moves_for_row = biggest_moves
                # print('weve got moves')
                break
        if moves_for_row:
            return random.choice(moves_for_row)
    
    # if we're here, we cant make forward progress. maybe go sideways?
    # from here,we have to go back, this is the worst
    for row in list(pieces_by_row.keys())[::direction]:
        moves_for_row = []
        for piece in pieces_by_row[row]:
            biggest_moves = []
            biggest_diff = 0
            for move in piece.get_moves(board):
                diff = (move.target[1] - move.origin[1]) * -1 *  direction
                if diff > biggest_diff and diff >= 0:
                    biggest_moves = []
                    biggest_moves.append(move)
                    biggest_diff = diff
                elif diff == biggest_diff:
                    biggest_moves.append(move)
            if biggest_moves:
                moves_for_row = biggest_moves
                break
        if moves_for_row:
            return random.choice(moves_for_row)
        
    return 'utter and complete desolation'
    
        

    

