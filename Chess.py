from enum import Enum


class CellValue(Enum):
    WHITE = 0
    BLACK = 1
class Team(Enum):
    WHITE = 0
    BLACK = 1
# Cell and Board for draw game, dont touch
class Cell:
    def __init__(self, value: CellValue, row: int, col: int):
        self.value = value
        self.row = row
        self.col = col
class Board:
    def __init__(self):
        # Color for the board
        self.board = []
        for i in range(8):
            self.board.append([])
            for j in range(8):
                if((i+j)%2 ==0):
                    self.board[i].append(Cell(CellValue.WHITE, i, j))
                else:
                    self.board[i].append(Cell(CellValue.BLACK, i, j))
class Piece:
    def __init__(self, team: Team, row=None, col=None):
        self.team = team
        self.row = row
        self.col = col
    def possibleMove(self):
        pass
class Pawn(Piece):
    def __init__(self, team: Team, row=None, col=None):
        super().__init__(team, row, col)
class Knight(Piece):
    def __init__(self, team: Team, row=None, col=None):
        super().__init__(team, row, col)
class Bishop(Piece):
    def __init__(self, team: Team, row=None, col=None):
        super().__init__(team, row, col)
class Rook(Piece):
    def __init__(self, team: Team, row=None, col=None):
        super().__init__(team, row, col)
class Queen(Piece):
    def __init__(self, team: Team, row=None, col=None):
        super().__init__(team, row, col)
class King(Piece):
    def __init__(self, team: Team, row=None, col=None):
        super().__init__(team, row, col)
    
class Chess:
    def __init__(self):
        self.initChess()
        self.board = Board()
    def initChess(self):
        self.chess = []
        for i in range(8):
            self.chess.append([])
            for j in range(8):
                self.chess[i].append(None)
        # Init Black
        self.addChess(Rook(Team.BLACK),0,0)
        self.addChess(Knight(Team.BLACK),0,1)
        self.addChess(Bishop(Team.BLACK),0,2)
        self.addChess(Queen(Team.BLACK),0,3)
        self.addChess(King(Team.BLACK),0,4)
        self.addChess(Bishop(Team.BLACK),0,5)
        self.addChess(Knight(Team.BLACK),0,6)
        self.addChess(Rook(Team.BLACK),0,7)
        # Init Black Pawn
        self.addChess(Pawn(Team.BLACK),1,0)
        self.addChess(Pawn(Team.BLACK),1,1)
        self.addChess(Pawn(Team.BLACK),1,2)
        self.addChess(Pawn(Team.BLACK),1,3)
        self.addChess(Pawn(Team.BLACK),1,4)
        self.addChess(Pawn(Team.BLACK),1,5)
        self.addChess(Pawn(Team.BLACK),1,6)
        self.addChess(Pawn(Team.BLACK),1,7)
        # Init White
        self.addChess(Rook(Team.WHITE),7,0)
        self.addChess(Knight(Team.WHITE),7,1)
        self.addChess(Bishop(Team.WHITE),7,2)
        self.addChess(Queen(Team.WHITE),7,3)
        self.addChess(King(Team.WHITE),7,4)
        self.addChess(Bishop(Team.WHITE),7,5)
        self.addChess(Knight(Team.WHITE),7,6)
        self.addChess(Rook(Team.WHITE),7,7)
        # Init WHITE Pawn
        self.addChess(Pawn(Team.WHITE),6,0)
        self.addChess(Pawn(Team.WHITE),6,1)
        self.addChess(Pawn(Team.WHITE),6,2)
        self.addChess(Pawn(Team.WHITE),6,3)
        self.addChess(Pawn(Team.WHITE),6,4)
        self.addChess(Pawn(Team.WHITE),6,5)
        self.addChess(Pawn(Team.WHITE),6,6)
        self.addChess(Pawn(Team.WHITE),6,7)
    def addChess(self,piece: Piece, row: int, col:int):
        piece
        self.chess[row][col] = piece
        piece.row = row
        piece.col = col
    def printChess(self):
        for i in range(8):
            for j in range(8):
                if(self.chess[i][j]!= None):
                    print(self.chess[i][j].__class__.__name__, end=" ", flush=True)
                else:
                    print(self.chess[i][j], end=" ", flush=True)
            print()
chess = Chess()
chess.printChess()