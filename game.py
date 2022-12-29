# engine.py
# contains implementation of the game

import time

from board import Board
from pieces import King, Queen, Rook, Bishop, Knight, Pawn

from bots.randombot.randombot import randombot


if __name__ == "__main__":
    board = Board()
    board.setup()

    print(board)
    while True:
        board.in_checkmate("white")
        board.in_stalemate("white")
        move = randombot(board, "white")
        board.play_move(move)
        print(board)
        input()

        board.in_checkmate("black")
        board.in_stalemate("black")
        move = randombot(board, "black")
        board.play_move(move)
        print(board)
        input()
