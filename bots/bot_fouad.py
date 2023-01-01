import random
import copy
from utils import *
from pieces import *

class Smart_piece(Piece):
    def __init__(self, piece):
        self.color = piece.color
        self.board = piece.board
        self.value = piece.value

        self.attacker = None

class Smart_move(Move):
    #result of move
    is_check = False
    is_checkmate = False
    is_stalemate = False
    enemey_could_check = False
    enemy_move_list = list()
    my_next_move_list = list()
    enemy_posible_move_count = 0
    my_next_posible_move_count = 0
    capture_value = 0
    material_gain = 0

    def __init__(self,move):
        #current move
        self.origin = move.origin
        self.target = move.target
        self.moved_piece = move.moved_piece
        self.capture = move.capture
    
    def get_capture_value(self):
        value = 0
        if self.capture is not None:
            match get_name(self.capture):
                case "Pawn":
                    value  = 1
                case "Knight":
                    value  = 3
                case "Bishop":
                    value  = 3
                case "Rook":
                    value  = 5
                case "Queen":
                    value  = 10
        return value

def get_name(obj):
    return obj.__class__.__name__
    
def score_board(board,color):
    pieces = board.get_pieces(color)
    piece_score = sum( [piece.value for piece in pieces] )
    return piece_score

def get_max(list, attribute):
    value = max( [getattr(item,attribute) for item in list] )
    return [item for item in list if getattr(item,attribute) == value]

def get_min(list, attribute):
    value = min( [getattr(item,attribute) for item in list] )
    return [item for item in list if getattr(item,attribute) == value]

        
def fouad_bot(true_board,color):

    board = copy.copy(true_board)
    my_moves = [Smart_move(move) for move in board.possible_moves(color)]

    for my_move in my_moves:

        #try move and enemy response
        board.try_move(my_move)
        my_move.enemy_move_list   = [Smart_move(move) for move in board.possible_moves(other_color(color))]
        my_move.my_next_move_list = [Smart_move(move) for move in board.possible_moves(color)]
        my_move.enemy_possible_move_count = len(my_move.enemy_move_list)
        my_move.my_approx_next_move_count = len(my_move.enemy_move_list)

        if len(my_move.enemy_move_list) == 0:
            if board.in_check(other_color(color)):
                my_move.is_checkmate = True
            if not board.in_check(other_color(color)):
                my_move.is_stalemate = True
        else:
            #material gain
            for their_move in my_move.enemy_move_list:
                their_move.capture_value = their_move.get_capture_value()
            their_capture_value = max( [their_move.capture_value for their_move in my_move.enemy_move_list] )
            my_capture_value    = my_move.get_capture_value()
            my_move.material_gain  = my_capture_value - their_capture_value

        board.undo_move(my_move)
    del board

    for move in my_moves:
        if my_move.is_checkmate:
            return move

    non_stalemate_moves = [move for move in my_moves if not move.is_stalemate]

    moves = get_max(non_stalemate_moves, "material_gain")
    moves = get_min(moves, "enemy_possible_move_count") 
    moves = get_max(moves, "my_next_posible_move_count")

    move = random.choice(moves)
    if not true_board.move_is_legal(move,color):
        print("illegal move selected")
        print(move)
        exit()

    move.message = f"material gain: {move.material_gain}, number of viable moves: {len(moves)}"
    return move
