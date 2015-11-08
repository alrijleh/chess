#engine.py
#contains implementation of the game

from board import Board
from pieces import King, Queen, Rook, Bishop, Knight, Pawn

#test
board = Board()
queen = Queen(board,2,2,'white')
