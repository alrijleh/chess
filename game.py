#engine.py
#contains implementation of the game

import time
import random

from board import Board
from pieces import King, Queen, Rook, Bishop, Knight, Pawn

def rand_ai (board,color):
    pieces = board.get_pieces(color)    
    all_moves = []
    for piece in pieces:
        all_moves.extend( piece.get_moves(board) )
    return random.choice( all_moves ) 

board = Board()
board.setup()

print(board)
while True:
    

    board.in_checkmate('white')
    board.in_stalemate('white')
    move = rand_ai(board,'white')
    board.play_move(move)
    print(board)
    input()

    board.in_checkmate('black')
    board.in_stalemate('black')
    move = rand_ai(board,'black')
    board.play_move(move)
    print(board)
    input()

