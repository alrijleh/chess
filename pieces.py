#pieces.py
#Contains definitions of chess pieces and functions to generate and execute moves

import time
import random
import copy

#abstract class for chess piece
class Piece(object):

    def __init__(self, board, x, y, color):
        self.board = board
        self.x = x
        self.y = y
        self.color = color
        self.type = 'unassigned'
        self.moves = []
        self.alive = True
        self.touched = False
        self.error = ''

        #update the board with the new piece
        self.board[x][y] = self
        if color == 'white': self.board.white.append(self)
        if color == 'black': self.board.black.append(self)

        random.seed(self,time.time())
    
    #calling for the string of a piece returns its color
    def __str__(self):
        return self.color

    #pick and execute a valid move
    #recursive - needs self.moves as argument
    #initial call should be: pick_move(self.moves)
    def pick_move(self, move_list):
        if move_list:
            local_board = copy.deepcopy(self.board)
            move = random.choice(move_list)
            move_list.remove(move)
            self.move(local_board, move, False)
            if local_board.in_check(self.color):
                pick_move(move_list)
            else:
                self.move(self.board, move)
                self.board.draw()
                return True
        return False

    #move self to previously validated location tuple
    #optional arguments allow function to be called without altering true data
    def move(self, board, location, update_data=True):
        x = 0
        y = 1
        origin = board[self.x][self.y]
        target = board[location[x]][location[y]]
        
        #error checking
        if self == 'empty':
            error_message = 'Origin location is empty'
            self.error += error_message
            raise ValueError(error_message, self, location[x], location[y])
        if target == 'invalid':
            error_message = 'Move destination out of range'
            self.error += error_message
            raise ValueError(error_message, self, location[x], location[y])
        if origin is target:
            error_message = 'Cannot move a piece to itself'
            self.error += error_message
            raise ValueError(error_message, self, location[x], location[y])

        if update_data:
            #update board data
            if ( str(target) != 'empty' ):
                target.alive = False
                board.captured.append(target)
                if   target in board.white: board.white.remove(target)
                elif target in board.black: board.black.remove(target)
            board[location[x]][location[y]] = origin
            board[self.x][self.y] = 'empty'

            #update self data
            self.touched = True
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
            if str( self.board[self.x][self.y+2]) == 'empty' and not self.touched:
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
            if str( self.board[self.x][self.y-2]) == 'empty' and not self.touched:
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

