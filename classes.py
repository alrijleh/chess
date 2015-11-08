#Contains classes for pieces and board

class Board(object):

    def __init__ (self):
        self.matrix = [['empty' for x in range(8)] for y in range(8)]

    def __getitem__(self, index):
        return self.matrix[index]


#abstract class for chess piece
class Piece(object):

    def __init__(self, board, x, y, color):
        self.board = board #board on which the piece will be placed
        self.x = x
        self.y = y
        self.color = color
        self.type = 'unassigned'
        self.moves = []
    
    #calling for the string of a piece returns its color
    def __str__(self):
        return self.color;

#piece classes
class Pawn(Piece):
    
    def __init__(self, board, x, y, color):
        super().__init__(board, x, y, color)
        self.type = 'pawn'
        board[x][y] = self

    def gen_moves(self):
        self.moves.clear()
        if (self.color == 'white'):
            #walk forwards
            if ( str( board[self.x][self.y+1]) == 'empty' ):
                self.moves.append( (self.x, self.y+1) )
            #diagonal attacks
            if ( str( board[self.x+1][self.y+1]) == 'black' ):
                self.moves.append( (self.x+1, self.y+1) )
            if ( str( board[self.x-1][self.y+1]) == 'black' ):
                self.moves.append( (self.x+1, self.y+1) )
        if (self.color == 'black'):
            #walk forwards
            if ( str( board[self.x][self.y-1]) == 'empty' ):
                self.moves.append( (self.x, self.y-1) )
            #diagonal attacks
            if ( str( oard[self.x+1][self.y-1]) == 'white' ):
                self.moves.append( (self.x+1, self.y-1) )
            if ( str( oard[self.x-1][self.y-1]) == 'white' ):
                self.moves.append( (self.x11, self.y-1) )





#test area
board = Board()
pawn = Pawn(board, 2, 1, 'white')
block = Pawn(board, 2, 2, 'black')
victim = Pawn(board, 3, 2, 'black')
pawn.gen_moves()
print(pawn.moves)
