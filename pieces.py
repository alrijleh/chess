#pieces.py
#Contains definitions of chess pieces and functions to generate and execute moves

#abstract class for chess piece
class Piece(object):

    def __init__(self, board, x, y, color):
        self.board = board #board on which the piece will be placed
        self.x = x
        self.y = y
        self.color = color
        self.type = 'unassigned'
        self.moves = []
        self.status = 'alive'

        self.board[x][y] = self
        if color == 'white': self.board.white.append(self)
        if color == 'black': self.board.black.append(self)
    
    #calling for the string of a piece returns its color
    def __str__(self):
        return self.color;

    #move the piece to previously validated location tuple
    def move(self, location):
        x = 0
        y = 1
        origin = self.board[self.x][self.y]
        target = self.board[location[x]][location[y]]
        if origin is target: raise ValueError('Cannot move a piece to itself', self.color, self.type, location[x], location[y])
        if ( str(target) != 'empty' ):
            target.status = 'dead'
            self.board.captured.append(target)
            try:
                self.board.white.remove(target)
                self.board.black.remove(target)
            except ValueError:
                pass
        self.board[location[x]][location[y]] = origin
        self.board[self.x][self.y] = 'empty'
        self.x = location[x]
        self.y = location[y]


#piece classes
class Pawn(Piece):
    
    def __init__(self, board, x, y, color):
        super().__init__(board, x, y, color)
        self.type = 'pawn'

    def gen_moves(self):
        self.moves.clear()
        if self.color == 'white':
            #walk forwards
            if str( self.board[self.x][self.y+1]) == 'empty':
                self.moves.append( (self.x, self.y+1) )
            #two spaces from initial location
            if str( self.board[self.x][self.y+2]) == 'empty' and self.y == 1:
                self.moves.append( (self.x, self.y+2) )
            #diagonal attacks
            if str( self.board[self.x+1][self.y+1]) == 'black':
                self.moves.append( (self.x+1, self.y+1) )
            if str( self.board[self.x-1][self.y+1]) == 'black':
                self.moves.append( (self.x-1, self.y+1) )

        elif self.color == 'black':
            #walk forwards
            if str( self.board[self.x][self.y-1]) == 'empty':
                self.moves.append( (self.x, self.y-1) )
            #two spaces from initial location
            if str( self.board[self.x][self.y-2]) == 'empty' and self.y == 6:
                self.moves.append( (self.x, self.y-2) )
            #diagonal attacks
            if str( self.board[self.x+1][self.y-1]) == 'white':
                self.moves.append( (self.x+1, self.y-1) )
            if str( self.board[self.x-1][self.y-1]) == 'white':
                self.moves.append( (self.x-1, self.y-1) )

class Rook(Piece):

    def __init__(self, board, x, y, color):
        super().__init__(board, x, y, color)
        self.type = 'rook'

    def gen_moves(self):
        x = 0
        y = 1
        self.moves.clear()
        for y_offset in [-1,0,1]:
            for x_offset in [-1,0,1]:
                if (x_offset + y_offset) % 2 != 0: #only one coordinate is changing
                    location = (self.x + x_offset, self.y + y_offset)
                    while (location[x] >= 0 and location[x] < 8 and location[y] >= 0 and location[y] < 8):
                        target = self.board[location[x]][location[y]]
                        if str(target) == 'empty':
                            self.moves.append( location )
                        elif target.color != self.color:
                            self.moves.append( location )
                            break
                        elif target.color == self.color:
                            break
                        location = (location[x] + x_offset, location[y] + y_offset)

class Bishop(Piece):

    def __init__(self, board, x, y, color):
        super().__init__(board, x, y, color)
        self.type = 'bishop'

    def gen_moves(self):
        x = 0
        y = 1
        self.moves.clear()
        for y_offset in [-1,1]:
            for x_offset in [-1,1]:
                location = (self.x + x_offset, self.y + y_offset)
                while (location[x] >= 0 and location[x] < 8 and location[y] >= 0 and location[y] < 8):
                    target = self.board[location[x]][location[y]]
                    if str(target) == 'empty':
                        self.moves.append( location )
                    elif target.color != self.color:
                        self.moves.append( location )
                        break
                    elif target.color == self.color:
                        break
                    location = (location[x] + x_offset, location[y] + y_offset)

class Queen(Piece):

    def __init__(self, board, x, y, color):
        super().__init__(board, x, y, color)
        self.type = 'queen'

    def gen_moves(self):
        x = 0
        y = 1
        self.moves.clear()
        for y_offset in [-1,0,1]:
            for x_offset in [-1,0,1]:
                location = (self.x + x_offset, self.y + y_offset)
                while (location[x] >= 0 and location[x] < 8 and location[y] >= 0 and location[y] < 8):
                    target = self.board[location[x]][location[y]]
                    if str(target) == 'empty':
                        self.moves.append( location )
                    elif target.color != self.color:
                        self.moves.append( location )
                        break
                    elif target.color == self.color:
                        break
                    location = (location[x] + x_offset, location[y] + y_offset)

class Knight(Piece):

    def __init__(self, board, x, y, color):
        super().__init__(board, x, y, color)
        self.type = 'knight'

    def gen_moves(self):
        x = 0
        y = 1
        self.moves.clear()
        for y_offset in [-2,-1,1,2]:
            for x_offset in [-2,-1,1,2]:
                if (x_offset + y_offset) % 2 != 0: #movement must be 2,1 or 1,2
                    location = (self.x + x_offset, self.y + y_offset)
                    if (location[x] >= 0 and location[x] < 8 and location[y] >= 0 and location[y] < 8):
                        target = self.board[location[x]][location[y]]
                        if str(target) == 'empty':
                            self.moves.append( location )
                        elif target.color != self.color:
                            self.moves.append( location )

class King(Piece):

    def __init__(self, board, x, y, color):
        super().__init__(board, x, y, color)
        self.type = 'king'

    def gen_moves(self):
        x = 0
        y = 1
        self.moves.clear()
        for y_offset in [-1,0,1]:
            for x_offset in [-1,0,1]:
                location = (self.x + x_offset, self.y + y_offset)
                if (location[x] >= 0 and location[x] < 8 and location[y] >= 0 and location[y] < 8):
                    target = self.board[location[x]][location[y]]
                    if str(target) == 'empty':
                        self.moves.append( location )
                    elif target.color != self.color:
                        self.moves.append( location )
