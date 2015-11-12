#engine.py
#contains implementation of the game

import time

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

while True:
    null = board.in_check('black')
    if not board.make_random_move('white'):
        print('white cannot make a move')
        break
    time.sleep(3)
    null = board.in_check('white')
    if not board.make_random_move('black'):
        print('black cannot make a move')
        break
    time.sleep(3)

