import random
from utils import *
from pieces import *

class Smart_piece(Piece):
    def __init__(self, piece):
        self.color = piece.color
        self.board = piece.board
        self.value = piece.value

        self.attacker = None

class Smart_move(Move):
    def __init__(self,move):
        #current move
        self.origin = move.origin
        self.target = move.target
        self.moved_piece = move.moved_piece
        self.capture = move.capture

        #result of move
        self.is_check = False
        self.danger_list = list() #format: thier_target, their attacker
        self.enemey_could_check = False
        self.enemy_possible_move_count = 0
        
def fouad_bot(board,color):
    all_moves = board.possible_moves(color)
    my_moves = list()

    for basic_move in all_moves:
        my_move = Smart_move(basic_move)
        my_moves.append(my_move)
        board.try_move(my_move)
        if board.in_check(other_color(color)):
            my_move.is_check = True

        enemy_moves = board.possible_moves(other_color(color))
        my_move.enemy_possible_move_count = len(enemy_moves)
        #for enemy_move in enemy_moves:
        #    if enemy_move.capture is not None:
        #        pass

        #    board.try_move(enemy_move)
        #    if board.in_check(color):
        #        my_move.enemy_could_check = True

        #    board.undo_move(enemy_move)
        board.undo_move(my_move)
    
    sorted_move_list = sorted(my_moves, key=lambda x: x.enemy_possible_move_count)
    move = sorted_move_list[0]
    move.message = f"enemy can make {move.enemy_possible_move_count} moves"
    return move
