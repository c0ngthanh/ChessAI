from enum import Enum
MAX_ROW =8
MAX_COL =8
def unique(needList : list):
    result = []
    for i in needList:
        if i not in result:
            result.append(i)
    return result
class Chess:
    pass
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
    def __init__(self, team: Team, chess:Chess = None, row=None, col=None):
        self.team = team
        self.row = row
        self.col = col
        self.chess = chess
    def possibleMove(self):
        print("Nothing")
    def checkPossibleMove(self,row:int,col:int):
        # Return (can move, can eat)
        if(col > 7 or col < 0):
            return False
        if(row > 7 or row < 0):
            return False
        if(self.chess.chess[row][col] != None):
            if(self.chess.chess[row][col].team == self.team):
                return (False,False)
            if(self.chess.chess[row][col].team != self.team):
                return (True,True)
        return (True,False)
    def move(self,row_col):
        if(type(row_col) is tuple):
            self.chess.chess[self.row][self.col] = None
            self.row = row_col[0]
            self.col = row_col[1]
            self.chess.chess[self.row][self.col] = self
        return
    def autoCheck(self, result:list,i,j,indexI,indexJ):
        while -1< i < MAX_ROW and -1< j < MAX_COL:
            posssibleMove = self.checkPossibleMove(i+indexI,j+indexJ)
            if(type(posssibleMove)==tuple):
                if(posssibleMove[0]==False):
                    break
                else:
                    result.append((i+indexI,j+indexJ))
                    if(posssibleMove[1]==True):
                        break
            else:
                break
            i+=indexI
            j+=indexJ
        return result
class Pawn(Piece):
    def __init__(self, team: Team, chess=None, row=None, col=None):
        super().__init__(team, chess, row, col)
        self.firstMove = True
    def checkPossibleMove(self,row:int,col:int):
        if(col > 7 or col < 0):
            return False
        if(row > 7 or row < 0):
            return False
        if(self.chess.chess[row][col] != None):
            if(self.chess.chess[row][col].team == self.team):
                return False
        return True
    def checkCanEat(self,row:int,col:int):
        if(col > 7 or col < 0):
            return False
        if(row > 7 or row < 0):
            return False
        if(self.chess.chess[row][col] != None):
            if(self.chess.chess[row][col].team != self.team):
                return True
        return False
    def possibleMove(self):
        result = []
        if(self.team == Team.WHITE):
            if(self.firstMove):
                if(self.checkPossibleMove(self.row-2,self.col)):
                    result.append((self.row-2,self.col))
            if(self.checkPossibleMove(self.row-1,self.col)):
                result.append((self.row-1,self.col))
            if(self.checkCanEat(self.row-1,self.col-1)):
                result.append((self.row-1,self.col-1))
            if(self.checkCanEat(self.row-1,self.col+1)):
                result.append((self.row-1,self.col+1))
        elif(self.team == Team.BLACK):
            if(self.firstMove):
                if(self.checkPossibleMove(self.row+2,self.col)):
                    result.append((self.row+2,self.col))
            if(self.checkPossibleMove(self.row+1,self.col)):
                result.append((self.row+1,self.col))
            if(self.checkCanEat(self.row+1,self.col-1)):
                result.append((self.row+1,self.col-1))
            if(self.checkCanEat(self.row+1,self.col+1)):
                result.append((self.row+1,self.col+1))
        return result
    def move(self,row_col):
        super().move(row_col)
        self.firstMove = False
class Knight(Piece):
    def __init__(self, team: Team, chess=None, row=None, col=None):
        super().__init__(team, chess, row, col)
    def checkAndAppend(self,result:list,row:int,col:int):
        posssibleMove = self.checkPossibleMove(row,col)
        if(type(posssibleMove)==tuple):
            if(posssibleMove[0]==True):
                result.append((row,col))
        return result
    def possibleMove(self):
        result = []
        self.checkAndAppend(result,self.row-2,self.col+1)
        self.checkAndAppend(result,self.row-2,self.col-1)
        self.checkAndAppend(result,self.row+2,self.col+1)
        self.checkAndAppend(result,self.row+2,self.col-1)
        self.checkAndAppend(result,self.row-1,self.col-2)
        self.checkAndAppend(result,self.row+1,self.col-2)
        self.checkAndAppend(result,self.row-1,self.col+2)
        self.checkAndAppend(result,self.row+1,self.col+2)
        return unique(result)
class Bishop(Piece):
    def __init__(self, team: Team, chess=None, row=None, col=None):
        super().__init__(team, chess, row, col)
    def possibleMove(self):
        result = []
        self.autoCheck(result,self.row,self.col,1,1)
        self.autoCheck(result,self.row,self.col,1,-1)
        self.autoCheck(result,self.row,self.col,-1,1)
        self.autoCheck(result,self.row,self.col,-1,-1)
        return unique(result)
class Rook(Piece):
    def __init__(self, team: Team, chess=None, row=None, col=None):
        super().__init__(team, chess, row, col)
        self.firstMove = True
    def possibleMove(self):
        result = []
        self.autoCheck(result,self.row,self.col,1,0)
        self.autoCheck(result,self.row,self.col,-1,0)
        self.autoCheck(result,self.row,self.col,0,1)
        self.autoCheck(result,self.row,self.col,0,-1)
        return unique(result)
    def move(self,row_col):
        super().move(row_col)
        self.firstMove = False
class Vua(Piece):
    def __init__(self, team: Team, chess=None, row=None, col=None):
        super().__init__(team, chess, row, col)
        self.firstMove = True
    def autoCheck(self, result:list,i,j,indexI,indexJ):
        posssibleMove = self.checkPossibleMove(i+indexI,j+indexJ)
        if(type(posssibleMove)==tuple):
            if(posssibleMove[0]==True):
                result.append((i+indexI,j+indexJ))
        return result
    def possibleMove(self):
        result = []
        self.autoCheck(result,self.row,self.col,1,1)
        self.autoCheck(result,self.row,self.col,1,-1)
        self.autoCheck(result,self.row,self.col,-1,1)
        self.autoCheck(result,self.row,self.col,-1,-1)
        self.autoCheck(result,self.row,self.col,1,0)
        self.autoCheck(result,self.row,self.col,-1,0)
        self.autoCheck(result,self.row,self.col,0,1)
        self.autoCheck(result,self.row,self.col,0,-1)
        ###########################
        if(self.firstMove):
            self.checkCastle(result,0)
            self.checkCastle(result,7)
        return unique(result)
    def move(self,row_col):
        if(type(row_col) is tuple):
            if(type(row_col[0]) is int):
                self.chess.chess[self.row][self.col] = None
                self.row = row_col[0]
                self.col = row_col[1]
                self.chess.chess[self.row][self.col] = self
            else:
                row_col[0](row_col[1])
        self.firstMove = False
        return
    def Castle(self,col):
        print("Nhap thanh " + (self.row,self.col) + " " +  col)
    def checkCastle(self,result:list, col: int):
        if(self.chess.chess[self.row][col] == None):
            return
        if(self.chess.chess[self.row][col].firstMove):
            if(self.col > col):
                for i in range(col+1,self.col):
                    if(self.chess.chess[self.row][i] != None):
                        return
            else:
                for i in range(self.col+1,col):
                    if(self.chess.chess[self.row][i] != None):
                        return
        result.append((self.Castle, col))
        return result
class Queen(Piece):
    def __init__(self, team: Team, chess=None, row=None, col=None):
        super().__init__(team, chess, row, col)
    def possibleMove(self):
        result = []
        self.autoCheck(result,self.row,self.col,1,1)
        self.autoCheck(result,self.row,self.col,1,-1)
        self.autoCheck(result,self.row,self.col,-1,1)
        self.autoCheck(result,self.row,self.col,-1,-1)
        self.autoCheck(result,self.row,self.col,1,0)
        self.autoCheck(result,self.row,self.col,-1,0)
        self.autoCheck(result,self.row,self.col,0,1)
        self.autoCheck(result,self.row,self.col,0,-1)
        return unique(result)
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
        self.addChess(Vua(Team.BLACK),0,4)
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
        self.addChess(Vua(Team.WHITE),7,4)
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
        piece.chess = self
    def printChess(self):
        for i in range(8):
            for j in range(8):
                if(self.chess[i][j]!= None):
                    if(self.chess[i][j].team == Team.WHITE):
                        print(self.chess[i][j].__class__.__name__[0]+"_W", end=" ", flush=True)
                    else:
                        print(self.chess[i][j].__class__.__name__[0]+"_B", end=" ", flush=True)
                else:
                    print("___", end=" ", flush=True)
            print()
chess = Chess()
chess.printChess()
chess.chess[0][1].move((5,3))
chess.chess[0][2].move((5,3))
chess.chess[0][3].move((5,3))
chess.chess[0][5].move((5,3))
chess.chess[0][6].move((5,3))
chess.chess[7][1].move((5,3))
chess.chess[7][2].move((5,3))
chess.chess[7][3].move((5,3))
chess.chess[7][5].move((5,3))
chess.chess[7][6].move((5,3))
chess.printChess()
print(chess.chess[7][4].possibleMove())