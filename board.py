#board.py
#contains chess board and structures containing pieces

from pieces import *

def other_color(color):
    if color == 'white': return 'black'
    if color == 'black': return 'white'

class Board(object):

    def __init__ (self):
        self.matrix = [[None for x in range(8)] for y in range(8)] #physical board

        self.capture_list = []
        self.move_list =[] #list of moves in human-readable chess notation
        self.move_count = 0 #count of moves made

    #allow indexing directly into matrix
    def __getitem__(self, location):
        x = location[0]
        y = location[1]
        if (x<0 or y<0 or x>7 or y>7): return None
        else: return self.matrix[x][y]

    def __setitem__(self, location, value):
        x = location[0]
        y = location[1]
        if (x<0 or y<0 or x>7 or y>7): return None
        else: self.matrix[x][y] = value

    def get_pieces(self,color):
        piece_list = []
        for row in self.matrix:
            for item in row:
                if item is not None:
                    if item.color == color:
                        piece_list.append(item)
        return piece_list

    def get_location(self,piece):
        for x in range(8):
            for y in range(8):
                if self[x,y] == piece:
                    return [x,y]

    def in_danger(self,location,color):
        enemy_pieces = self.get_pieces(other_color(color))
        for piece in enemy_pieces:
            moves,captures = piece.gen_moves(self)
            for capture_move in captures:
                if capture_move.dest == location:
                    return True
        return False

    def in_check(self, color):
        friendly_pieces = self.get_pieces(color)
        king = [piece for piece in friendly_pieces if isinstance(piece, King)]
        king_location = self.get_location( king[0] )
        return self.in_danger(king_location, color)

    def is_castle(self,move):
        moved_piece   = self[move.origin]
        if isinstance(moved_piece, King) and abs(move.origin[0] - move.dest[0]) > 1:
            return True
        else:
            return False

    def play_move(self,move,commit=True):
        moved_piece   = self[move.origin]
        capture = self[move.dest]

        #only run these when a move is played - not while testing for check
        if commit is True:
            #test output
            print( str(moved_piece) + str(move) )

            moved_piece.moved = True
            self.capture_list.append( capture )

            #set the flag for en passant
            color = moved_piece.color
            for piece in self.get_pieces(color):
                piece.en_passant_ready = False 
            if isinstance(piece, Pawn):
                if abs(move.origin[1] - move.dest[1]) == 2:
                    piece.en_passant_ready = True

            #move rook if castling
            if self.is_castle(move):
                row = move.origin[0]
                #castle right
                if move.dest[0] == 6:
                   rook = self[7,row]
                   self[7,row] = None
                   self[5,row] = rook
                #castle right
                if move.dest[0] == 2:
                   rook = self[0,row]
                   self[0,row] = None
                   self[5,row] = rook

            #pawn promotion
            if isinstance(moved_piece, Pawn):
                if move.dest[1] in {0,7}:
                    self[move.origin] = None
                    if move.promote == 'knight':
                        self[move.dest] = Knight(color)
                    else:
                        self[move.dest] = Queen(color)
                    return

        #normal move handling
        self[move.dest] = moved_piece
        self[move.origin] = None

    def undo_move(self,move):
        moved_piece = self[move.dest]
        self[move.origin] = moved_piece
        self[move.dest] = move.capture

    def in_checkmate(self,color):
        if self.in_check(color):
            pieces = self.get_pieces(color)    
            for piece in pieces:
                moves = piece.get_moves(self)
                if moves:
                    return False
            print('get rekt ' + color)
            return True

    def in_stalemate(self,color):
        if not self.in_check(color):
            pieces = self.get_pieces(color)    
            for piece in pieces:
                moves = piece.get_moves(self)
                if moves:
                    return False
            print('you both suck')
            return True

    def setup(self):
        for x in range(8) :
            self[x,1] = Pawn('white')
            self[x,6] = Pawn('black')
        
        for color in ['white', 'black']:
            if   color == 'white': y = 0
            elif color == 'black': y = 7
        
            self[0,y] = Rook(color)
            self[7,y] = Rook(color)
        
            self[1,y] = Knight(color)
            self[6,y] = Knight(color)
        
            self[2,y] = Bishop(color)
            self[5,y] = Bishop(color)
        
            self[3,y] = Queen(color)
            self[4,y] = King(color)

    #printing the board onscreen
    def __str__ (self):
        width = 8*3 + 8 + 1
        hieght = 8 + 9
        line = '\n' + '   ' + '_' * width + '\n'
        output = line
        for y in range(7,-1,-1):
            output += ' ' + str(y+1) + ' |'
            for x in range(8):
                piece = self.matrix[x][y]
                #if space is empty
                if piece is None:
                    output += '   '
                #if occupied by piece
                else:
                    output += str(piece)
                output += '|'
            output += line
        output += '     a   b   c   d   e   f   g   h'
        return output

        #move_text = type_text + capture_text + chr(self.x + 97) + str(self.y + 1)
