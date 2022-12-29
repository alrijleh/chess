# engine.py
# contains implementation of the game

import time

from board import Board
from pieces import King, Queen, Rook, Bishop, Knight, Pawn

from bots.randombot.randombot import randombot
from utils import other_color


if __name__ == "__main__":
    board = Board()
    board.setup()
    print(board)

    color = 'white'
    while not board.in_checkmate(color) and not board.in_stalemate(color):
        if color == 'white':
            move = randombot(board, color)
        elif color == 'black':
            move = randombot(board, color)
        board.play_move(move)
        print(board)
        #input()
        color = other_color(color)
