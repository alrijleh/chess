# board.py
# contains chess board and structures containing pieces

from pieces import *

from utils import other_color


class Board(object):
    def __init__(self):
        self.matrix = [[None for x in range(8)] for y in range(8)]  # physical board

        self.capture_list = list()
        self.move_list = list()
        self.move_log = list()

    # allow indexing directly into matrix
    def __getitem__(self, location):
        x = location[0]
        y = location[1]
        if x < 0 or y < 0 or x > 7 or y > 7:
            return None
        else:
            return self.matrix[x][y]

    def __setitem__(self, location, value):
        x = location[0]
        y = location[1]
        if x < 0 or y < 0 or x > 7 or y > 7:
            return None
        else:
            self.matrix[x][y] = value

    def get_pieces(self, color):
        piece_list = []
        for row in self.matrix:
            for item in row:
                if item is not None:
                    if item.color == color:
                        piece_list.append(item)
        return piece_list

    def get_location(self, piece):
        for x in range(8):
            for y in range(8):
                if self[x, y] == piece:
                    return [x, y]

    def in_danger(self, location, color):
        enemy_pieces = self.get_pieces(other_color(color))
        for piece in enemy_pieces:
            moves, captures = piece.gen_moves()
            for capture_move in captures:
                if capture_move.target == location:
                    return True
        return False

    def in_check(self, color):
        friendly_pieces = self.get_pieces(color)
        king = [piece for piece in friendly_pieces if isinstance(piece, King)]
        king_location = self.get_location(king[0])
        return self.in_danger(king_location, color)

    def is_castle(self, move):
        moved_piece = self[move.origin]
        if isinstance(moved_piece, King) and abs(move.origin[0] - move.target[0]) > 1:
            return True
        else:
            return False

    def move_is_legal(self, move, color):
        moved_piece = self[move.origin]
        if moved_piece is None:
            print("no piece found")
            return False
        piece_color = moved_piece.color
        if color != piece_color:
            print("moving enemy piece")
            return False
        is_legal = False
        for possible_move in self.possible_moves(color):
            if move.origin == possible_move.origin and move.target == possible_move.target:
                is_legal = True
        if is_legal:
            return True
        else:
            print("requested move not legal")
            return False

    def play_move(self, move, color):
        moved_piece = self[move.origin]
        capture = self[move.target]

        if not self.move_is_legal(move, color):
            print("illegal move bucko")
            print(f"{color} tried {move}")
            print(self.possible_moves(color))
            exit(-1)

        move.capture = self[move.target]
        move.moved_piece = self[move.origin]
        move.board = self

        moved_piece.moved = True
        self.move_list.append(move)
        if capture is not None:
            self.capture_list.append(capture)

        # set the flag for en passant
        for piece in self.get_pieces(move.color):
            piece.en_passant_ready = False
        if isinstance(piece, Pawn):
            if abs(move.origin[1] - move.target[1]) == 2:
                piece.en_passant_ready = True

        # move rook if castling
        if self.is_castle(move):
            move.is_castle = True
            row = move.origin[0]
            # castle right
            if move.target[0] == 6:
                rook = self[7, row]
                self[7, row] = None
                self[5, row] = rook
            # castle right
            if move.target[0] == 2:
                rook = self[0, row]
                self[0, row] = None
                self[5, row] = rook

        # pawn promotion
        if isinstance(moved_piece, Pawn):
            if move.target[1] in {0, 7}:
                print(self)
                print("test")
                self[move.origin] = None
                if move.promote == "knight":
                    self[move.target] = Knight(self,move.color)
                else:
                    self[move.target] = Queen(self,move.color)
                return

        # basic move handling
        self[move.target] = moved_piece
        self[move.origin] = None

    def try_move(self, move):
        moved_piece = self[move.origin]
        self[move.target] = moved_piece
        self[move.origin] = None

    def undo_move(self, move):
        moved_piece = self[move.target]
        self[move.origin] = moved_piece
        self[move.target] = move.capture

    def in_checkmate(self, color):
        if self.in_check(color):
            if self.possible_moves(color):
                return False
            print("get rekt " + color)
            return True

    def in_stalemate(self, color):
        if len(self.get_pieces("black") + self.get_pieces("white")) <= 2:
            return True
        if len(self.move_list) > 500:
            return True
        if not self.in_check(color):
            if self.possible_moves(color):
                return False
            return True

    def setup(self):
        for x in range(8):
            self[x, 1] = Pawn(self,"white")
            self[x, 6] = Pawn(self,"black")

        for color in ["white", "black"]:
            if color == "white":
                y = 0
            elif color == "black":
                y = 7

            self[0, y] = Rook(self,color)
            self[7, y] = Rook(self,color)

            self[1, y] = Knight(self,color)
            self[6, y] = Knight(self,color)

            self[2, y] = Bishop(self,color)
            self[5, y] = Bishop(self,color)

            self[3, y] = Queen(self,color)
            self[4, y] = King(self,color)

    def clear_line(self, n=21):
        LINE_UP = "\033[1A"
        LINE_CLEAR = "\x1b[2K"
        for i in range(n):
            print(LINE_UP, end=LINE_CLEAR)

    def possible_moves(self, color):
        all_moves = []
        pieces = self.get_pieces(color)
        for piece in pieces:
            all_moves.extend(piece.get_moves(self))
        return all_moves

    # printing the board onscreen
    def __str__(self):
        self.clear_line()
        width = 8 * 3 + 8 + 1
        hieght = 8 + 9
        line = "\n" + "   " + "_" * width

        if self.move_list:
            move = self.move_list[-1]
            move_text = f"  {move}"
            message = f"   {move.color}: {move.message}" if move.message else ""
        else:
            message = ""
            move_text = ""
        capture_message_dict = {"black": "", "white": ""}
        if self.capture_list:
            for color in ["black", "white"]:
                capture_list = list(
                    filter(lambda x: x.color == color, self.capture_list)
                )
                capture_message = f"   {color} casualties: " + "".join(
                    str(x) for x in capture_list
                )
                capture_message_dict.update({color: capture_message})
        turn_number_text = f"   Turn:{len(self.move_list)}"

        output = f"{line}\n"
        for y in range(7, -1, -1):
            output += " " + str(y + 1) + " |"
            for x in range(8):
                piece = self.matrix[x][y]
                if piece is None:
                    output += "   "
                else:
                    output += str(piece)
                output += "|"
                if x == 7:
                    if y == 7:
                        output += move_text
                    if y == 6:
                        output += message
                    if y == 3:
                        output += capture_message_dict["white"]
                    if y == 2:
                        output += capture_message_dict["black"]
                    if y == 0:
                        output += turn_number_text
            output += f"{line}\n"
        output += "     a   b   c   d   e   f   g   h"
        return output
