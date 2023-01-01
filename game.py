#call this file to run the game

from board import Board
from utils import other_color

#bots
from bots.randombot.randombot import *
from bots.bot_fouad import fouad_bot
from simpbot import simpbot


def run_game():
    board = Board()
    board.setup()
    print(board)

    color = "white"
    while not board.in_checkmate(color) and not board.in_stalemate(color):
        if color == "white":
            move = randombot(board, color)
        elif color == "black":
            move = fouad_bot(board, color)
        move.color = color
        board.play_move(move, color)
        #input()
        print(board)
        color = other_color(color)

    if not board.in_stalemate(color):
        return other_color(color)
    else:
        print("you both suck")
        return None


if __name__ == "__main__":
    x = 0
    bookie = {"black": 0, "white": 0, None: 0}
    while x < 10:
        winner = run_game()
        bookie[winner] += 1
        x += 1

    print(bookie)
