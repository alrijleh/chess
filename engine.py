#engine.py
#contains implementation of the game

from board import Board
from pieces import King, Queen, Rook, Bishop, Knight, Pawn

#setup board
board = Board()
for x in range(8) :
    Pawn(board, x, 1, 'white')
    Pawn(board, x, 6, 'black')

for color in ['white', 'black']:
    if   color == 'white': y = 0
    elif color == 'black': y = 7

    Rook(board, 0, y, color)
    Rook(board, 7, y, color)

    Knight(board, 1, y, color)
    Knight(board, 6, y, color)

    Bishop(board, 2, y, color)
    Bishop(board, 5, y, color)

    Queen(board, 3, y, color)
    King(board, 4, y, color)


#piece = board.random_piece('white')
#move = piece.random_move()
#piece.move(move)
#board.draw()
