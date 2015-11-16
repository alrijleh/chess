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


#game loop
#  checking if a color is in check generates the other's moves
#  could be changed for performace gain
while True:
    null = board.in_check('black')
    if board.make_random_move('white'):
        print ('white moves: ' + board.move_list[-1])
    else:
        if board.in_check('white'): print('checkmate - black wins')
        else: print ('draw')
        break
    time.sleep(3)

    null = board.in_check('white')
    if board.make_random_move('black'):
        print ('black moves: ' + board.move_list[-1])
    else:
        if board.in_check('black'): print('checkmate - white wins')
        else: print ('draw')
        break
    time.sleep(3)

