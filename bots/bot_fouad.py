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
    #result of move
    is_check = False
    is_checkmate = False
    is_stalemate = False
    enemey_could_check = False
    enemy_move_list = list()
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

        
def fouad_bot(board,color):
    my_basic_moves = board.possible_moves(color)
    my_moves = [Smart_move(move) for move in my_basic_moves]

    for my_move in my_moves:

        #try move and enemy response
        board.try_move(my_move)
        their_basic_moves = board.possible_moves(other_color(color))
        my_move.enemy_move_list = [Smart_move(move) for move in their_basic_moves]
        my_move.enemy_possible_move_count = len(my_move.enemy_move_list)

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
        if my_move.is_checkmate:
            return my_move

    non_stalemate_moves = [move for move in my_moves if not move.is_stalemate]

    highest_move_gain = max( [move.material_gain for move in non_stalemate_moves] )
    highest_gain_moves = [move for move in my_moves if move.material_gain == highest_move_gain]

    least_enemy_possible_moves = min( [move.enemy_possible_move_count for move in highest_gain_moves] )
    least_enemy_possible_moves_moves = [move for move in my_moves if move.enemy_possible_move_count == least_enemy_possible_moves]

    move = random.choice(least_enemy_possible_moves_moves)
    move.message = f"material gain: {move.material_gain}, number of enemy responses: {move.enemy_possible_move_count}"
    return move
