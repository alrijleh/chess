#Contains classes for pieces and board

class Board(object):

    def __init__ (self):
        self.matrix = [['empty' for x in range(8)] for y in range(8)]
        self.captured = []

    def __getitem__(self, index):
        if (index < 0): return 'invalid'
        if (index > 7): return 'invalid'
        return self.matrix[index]

    def draw(self):
        width = 8*3 + 8 + 1
        hieght = 8 + 9
        line = '\n' + '_' * width + '\n'
        output = line
        for y in range(7,-1,-1):
            output += '|'
            for x in range(8):
                target = self.matrix[x][y]
                #if space is empty
                if type(target) is str:
                    output += '   '
                #if occupied by piece
                else:
                    #print color
                    if target.color == 'white': output += 'w '
                    elif target.color == 'black': output += 'b '
                    #print piece type
                    if target.type == 'king': output += 'K'
                    if target.type == 'queen': output += 'Q'
                    if target.type == 'rook': output += 'R'
                    if target.type == 'bishop': output += 'B'
                    if target.type == 'knight': output += 'N'
                    if target.type == 'pawn': output += 'P'
                output += '|'
            output += line
        print(output)




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
    
    #calling for the string of a piece returns its color
    def __str__(self):
        return self.color;

    #move the piece to previously validated location tuple
    def move(self, location):
        x = 0
        y = 1
        origin = self.board[self.x][self.y]
        target = self.board[location[x]][location[y]]
        if ( str(target) != 'empty' ):
            target.status = 'dead'
            self.board.captured.append(target)
        target = self
        origin = "empty"


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
        self.moves.clear()
        #postive horizantal
        x = self.x + 1
        while (x < 8):
            target = self.board[x][self.y]
            if str(target) == 'empty':
                self.moves.append( (x, self.y) )
            elif target.color != self.color:
                self.moves.append( (x, self.y) )
                break
            elif target.color == self.color:
                break
            x += 1
        #negative horizantal
        x = self.x - 1
        while (x >= 0):
            target = self.board[x][self.y]
            if str(target) == 'empty':
                self.moves.append( (x, self.y) )
            elif target.color != self.color:
                self.moves.append( (x, self.y) )
                break
            elif target.color == self.color:
                break
            x -= 1
        #postive vertical
        y = self.y + 1
        while (y < 8):
            target = self.board[self.x][y]
            if str(target) == 'empty':
                self.moves.append( (self.x, y) )
            elif target.color != self.color:
                self.moves.append( (self.x, y) )
                break
            elif target.color == self.color:
                break
            y += 1
        #negative vertical
        y = self.y - 1
        while (y >= 0):
            target = self.board[self.x][y]
            if str(target) == 'empty':
                self.moves.append( (self.x, y) )
            elif target.color != self.color:
                self.moves.append( (self.x, y) )
                break
            elif target.color == self.color:
                break
            y -= 1


#test area
board = Board()
rook = Rook(board, 0,0,'white')
pawn = Pawn(board, 0, 2, 'white')
black = Pawn(board, 3, 0, 'black')
pawn.gen_moves()
