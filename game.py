# engine.py
# contains implementation of the game

import time

from board import Board
from pieces import King, Queen, Rook, Bishop, Knight, Pawn

from bots.randombot.randombot import *
from utils import other_color


def run_game():
    board = Board()
    board.setup()
    print(board)

    color = "white"
    while not board.in_checkmate(color) and not board.in_stalemate(color):
        if color == "white":
            move = randombot2(board, color)
        elif color == "black":
            move = randombot_plus(board, color)
        move.color = color
        board.play_move(move, color)
        print(board)
        # input()
        color = other_color(color)

    if not board.in_stalemate(color):
        return other_color(color)
    else:
        return None


if __name__ == "__main__":
    x = 0
    bookie = {"black": 0, "white": 0, None: 0}
    while x < 10:
        winner = run_game()
        bookie[winner] += 1
        x += 1

    print(bookie)
