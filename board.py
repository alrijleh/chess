#board.py
#contains chess board and structures containing pieces

import random
import time

class Board(object):

    def __init__ (self):
        self.matrix = [['empty' for x in range(8)] for y in range(8)] #physical board
        self.white = []    #contains all living white pieces
        self.black = []    #contains all living black pieces
        self.captured = [] #contains all captured pieces
        self.errors = []   #contains pieces inconsistance data - should be empty

        random.seed(self,time.time()) #generate random seed

    #allow indexing directly into matrix
    def __getitem__(self, index):
        if (index < 0): return 'invalid'
        if (index > 7): return 'invalid'
        return self.matrix[index]

    #returns a list of inconsistancies found in data
    def sanity_check(self):
        zombie = [piece for piece in self.white + self.black if not piece.alive]
        buried_alive = [piece for piece in self.captured if piece.alive]
        location_mismatch = [piece for piece in self.white + self.black if not self.matrix[piece.x][piece.y] == piece]

        for piece in zombie: piece.error += 'zombie '
        for piece in buried_alive: piece.error += 'buried_alive '
        for piece in location_mismatch: piece.error += 'location_mismatch '

        self.errors = zombie+buried_alive+location_mismatch

    #printing the board onscreen
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
