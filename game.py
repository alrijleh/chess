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
        if board.in_checkmate("white") or board.in_stalemate("white"):
            # cleanup code post game
            exit(0)

        move = randombot(board, "white")
        board.play_move(move)
        print(board)

        if board.in_checkmate("black") or board.in_stalemate("black"):
            # clean up code post game
            exit(0)
        move = randombot(board, "black")
        board.play_move(move)
        print(board)
