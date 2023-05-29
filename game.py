#call this file to run the game

from board import Board
from utils import other_color
import argparse

#bots
from bots.randombot.randombot import *
from bots.bot_fouad import fouad_bot
from simpbot import simpbot
from bots.date_bot.date_bot import date_bot
from bots.odd_bot.odd_bot import odd_bot
from bots.forward_bot.forward_bot import forward_bot

bot_list = {
    'simpbot': simpbot,
    'fouad_bot': fouad_bot,
    'randombot': randombot,
    'date_bot': date_bot,
    'odd_bot': odd_bot,
    'forward_bot': forward_bot
}


def run_game(white: str, black: str):

    white_bot = bot_list[white]
    black_bot = bot_list[black]
    board = Board()
    board.setup()
    print(board)

    color = "white"
    while not board.in_checkmate(color) and not board.in_stalemate(color):
        if color == "white":
            move = white_bot(board, color)
        elif color == "black":
            move = black_bot(board, color)
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

def get_args():
    parser = argparse.ArgumentParser(description='Get the bots!')
    parser.add_argument('-white_bot_name', '-w', type=str, help='the name of the bot to use for white')
    parser.add_argument('-black_bot_name', '-b', type=str, help='the name of the bot to use for black')
    parser.add_argument('-number_of_games', '-n', type=int, help='the number of games to play', default=10)
    args = parser.parse_args()
    bot_choices = list(bot_list.keys())
    if args.white_bot_name in bot_list.keys() and args.black_bot_name in bot_choices:
        white_bot_name = args.white_bot_name
        black_bot_name = args.black_bot_name
    else:
        choices = 'Your bot choices are:\nPlease choose a bot for white and black\n'
        for i in range(len(bot_choices)):
            choices += f'{i}: {bot_choices[i]}\n'
        print(choices)
        white_bot_choice = int(input('Number of white bot choice:\n'))
        black_bot_choice = int(input('Number of black bot choice:\n'))

        white_bot_name = bot_choices[white_bot_choice]
        black_bot_name = bot_choices[black_bot_choice]

    return {
        'white_bot_name': white_bot_name,
        'black_bot_name': black_bot_name,
        'number_of_games': args.number_of_games
    }

if __name__ == "__main__":
    input_args = get_args()

    x = 0
    bookie = {"black": 0, "white": 0, None: 0}
    while x < input_args['number_of_games']:
        winner = run_game(white=input_args['white_bot_name'], black=input_args['black_bot_name'])
        bookie[winner] += 1
        x += 1

    print(bookie)
