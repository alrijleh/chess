# pieces.py
# Contains definitions of chess pieces and functions to generate and execute moves
import unicodedata

from utils import other_color

# abstract class for chess piece
class Piece(object):
    def __init__(self, board, color):
        self.color = color
        self.board = board
        self.moved = False  # if piece has ever been moved
        self.en_passant_ready = False
        self.unicode_str = None

    def __str__(self):
        color_letter = self.color[0]
        type_letter = self.type_letter
        return f" {unicodedata.lookup(self.unicode_str)} "

    def __repr__(self):
        return self.__str__()

    # return all legal moves of a piece
    def get_moves(self, board):
        safe_moves = []
        all_movements, all_captures = self.gen_moves()
        all_moves = all_movements + all_captures

        for move in all_moves:
            if board.is_castle(move):
                king_in_check = False
                for column in range(move.origin[0], move.target[0]):
                    row = move.origin[1]
                    color = board[move.origin].color
                    if board.in_danger([column, row], color):
                        king_in_check = True
                if not king_in_check:
                    safe_moves.append(move)
            else : 
                board.try_move(move)
                if not board.in_check(self.color):
                    safe_moves.append(move)
                board.undo_move(move)
        return safe_moves


class Move(object):
    # generated by board functions
    moved_piece = None
    is_en_passant = False
    color = None
    board = None
    # optional, user set
    promote = "queen"
    message = ""

    def __init__(self, origin, target, capture=None):
        # mandatory for bot moves
        self.origin = origin
        self.target = target
        # generated by board function
        self.capture = capture

    def __str__(self):
        return f"{self.moved_piece} moving from {chr(self.origin[0]+97)}{self.origin[1] +1} to {chr(self.target[0]+97)}{self.target[1] +1}{f' capturing{self.capture}' if self.capture else ''}"

    def __repr__(self):
        return self.__str__()


# piece classes
class Rook(Piece):
    def __init__(self, board, color):
        super().__init__(board,color)
        self.type_letter = "R"
        self.unicode_str = f"{other_color(color).upper()} CHESS ROOK"

    def gen_moves(self):
        location = self.board.get_location(self)
        moves = []
        captures = []
        for y_offset in [-1, 0, 1]:
            for x_offset in [-1, 0, 1]:
                if abs(y_offset) + abs(x_offset) == 1:
                    new_location = [location[0] + x_offset, location[1] + y_offset]
                    while (
                        new_location[0] >= 0
                        and new_location[0] < 8
                        and new_location[1] >= 0
                        and new_location[1] < 8
                    ):
                        target = self.board[new_location]
                        if target is None:
                            moves.append(Move(location, new_location))
                        elif target.color != self.color:
                            captures.append(Move(location, new_location, target))
                            break
                        elif target.color == self.color:
                            break
                        new_location = [
                            new_location[0] + x_offset,
                            new_location[1] + y_offset,
                        ]
        return moves, captures


class Pawn(Piece):
    def __init__(self, board,color):
        super().__init__(board,color)
        self.type_letter = "P"
        self.unicode_str = f"{other_color(color).upper()} CHESS PAWN"

    def gen_moves(self):
        location = self.board.get_location(self)
        moves = []
        captures = []
        if self.color == "white":
            direction = 1
        elif self.color == "black":
            direction = -1

        # walk forwards
        step_location = [location[0], location[1] + 1 * direction]
        if self.board[step_location] == None:
            moves.append(Move(location, step_location))
        # two spaces from initial location
        step2_location = [location[0], location[1] + 2 * direction]
        if (
            not self.moved
            and self.board[step_location] is None
            and self.board[step2_location] is None
        ):
            moves.append(Move(location, step2_location))
        # diagonal attacks
        diagonal = {}
        en_passant_victim_loc = {}
        for i in [-1, 1]:
            diagonal[i] = [location[0] + 1 * i, location[1] + 1 * direction]
            target = self.board[diagonal[i]]
            if target is not None:
                if target.color != self.color:
                    captures.append(Move(location, diagonal[i], target))
            # en passant
            en_passant_victim_loc[i] = [location[0] + 1 * i, location[1]]
            target = self.board[en_passant_victim_loc[i]]
            if target is not None:
                if (
                    target.color != self.color
                    and target is Pawn
                    and target.en_passant_ready == True
                ):
                    move = Move(location, diagonal[i], target)
                    move.is_en_passant = True
                    captures.append(move)
        return moves, captures


class Bishop(Piece):
    def __init__(self, board,color):
        super().__init__(board,color)
        self.type_letter = "B"
        self.unicode_str = f"{other_color(color).upper()} CHESS BISHOP"

    def gen_moves(self):
        location = self.board.get_location(self)
        moves = []
        captures = []
        for y_offset in [-1, 1]:
            for x_offset in [-1, 1]:
                new_location = [location[0] + x_offset, location[1] + y_offset]
                while (
                    new_location[0] >= 0
                    and new_location[0] < 8
                    and new_location[1] >= 0
                    and new_location[1] < 8
                ):
                    target = self.board[new_location]
                    if target is None:
                        moves.append(Move(location, new_location))
                    elif target.color != self.color:
                        captures.append(Move(location, new_location, target))
                        break
                    elif target.color == self.color:
                        break
                    new_location = [
                        new_location[0] + x_offset,
                        new_location[1] + y_offset,
                    ]
        return moves, captures


class Queen(Piece):
    def __init__(self, board,color):
        super().__init__(board,color)
        self.type_letter = "Q"
        self.unicode_str = f"{other_color(color).upper()} CHESS QUEEN"

    def gen_moves(self):
        location = self.board.get_location(self)
        moves = []
        captures = []
        for y_offset in [-1, 0, 1]:
            for x_offset in [-1, 0, 1]:
                new_location = [location[0] + x_offset, location[1] + y_offset]
                while (
                    new_location[0] >= 0
                    and new_location[0] < 8
                    and new_location[1] >= 0
                    and new_location[1] < 8
                ):
                    if x_offset == 0 and y_offset == 0:
                        break
                    target = self.board[new_location[0], new_location[1]]
                    if target is None:
                        moves.append(Move(location, new_location))
                    elif target.color != self.color:
                        captures.append(Move(location, new_location, target))
                        break
                    elif target.color == self.color:
                        break
                    new_location = [
                        new_location[0] + x_offset,
                        new_location[1] + y_offset,
                    ]
        return moves, captures


class Knight(Piece):
    def __init__(self, board,color):
        super().__init__(board,color)
        self.type_letter = "N"
        self.unicode_str = f"{other_color(color).upper()} CHESS KNIGHT"

    def gen_moves(self):
        location = self.board.get_location(self)
        moves = []
        captures = []
        for y_offset in [-2, -1, 1, 2]:
            for x_offset in [-2, -1, 1, 2]:
                if abs(y_offset) + abs(x_offset) == 3:  # movement must be 2,1 or 1,2
                    new_location = [location[0] + x_offset, location[1] + y_offset]
                    if (
                        new_location[0] >= 0
                        and new_location[0] < 8
                        and new_location[1] >= 0
                        and new_location[1] < 8
                    ):
                        target = self.board[new_location]
                        if target is None:
                            moves.append(Move(location, new_location))
                        elif target.color != self.color:
                            captures.append(Move(location, new_location, target))
        return moves, captures


class King(Piece):
    def __init__(self, board,color):
        super().__init__(board,color)
        self.type_letter = "K"
        self.unicode_str = f"{other_color(color).upper()} CHESS KING"

    def gen_moves(self):
        location = self.board.get_location(self)
        moves = []
        captures = []
        for y_offset in [-1, 0, 1]:
            for x_offset in [-1, 0, 1]:
                new_location = [location[0] + x_offset, location[1] + y_offset]
                if (
                    new_location[0] >= 0
                    and new_location[0] < 8
                    and new_location[1] >= 0
                    and new_location[1] < 8
                ):
                    target = self.board[new_location]
                    if target is None:
                        moves.append(Move(location, new_location))
                    elif target.color != self.color:
                        captures.append(Move(location, new_location, target))
        # castling
        if self.moved is False:
            row = location[1]
            row_ahead = row + 1 if self.color == "white" else row - 1
            # right
            if self.board[7, row] is not None:
                if (
                    self.board[7, row].moved is False
                    and self.board[5, row] is None
                    and self.board[6, row] is None
                ):
                    moves.append(Move(location, [6, row]))
            # left
            if self.board[0, row] is not None:
                if (
                    self.board[0, row].moved is False
                    and self.board[1, row] is None
                    and self.board[2, row] is None
                    and self.board[3, row] is None
                ):
                    moves.append(Move(location, [2, row]))
        return moves, captures
