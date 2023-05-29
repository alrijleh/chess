from utils import *
import datetime




def date_bot(board, color):
    pieces = board.get_pieces(color)
    todays_day= datetime.datetime.today().day

    move = None
    piece_to_move = pieces[todays_day%len(pieces)]

    while move == None:
        if piece_to_move.get_moves(board):
            move = piece_to_move.get_moves(board)[todays_day%len(piece_to_move.get_moves(board))]
        else:
            # the piece we tried has no moves, what a goober. lets check what would happen for tomorrow
            todays_day += 1
            piece_to_move = pieces[(todays_day)%len(pieces)]
    return move
