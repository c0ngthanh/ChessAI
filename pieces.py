from enum import Enum
from Enums import *
from agent import Agent
from AssetsCfg import *
from Checkmate import Checkmate
import random

MAX_ROW =8
MAX_COL =8
def unique(needList : list):
    result = []
    for i in needList:
        if i not in result:
            result.append(i)
    return result

class Piece:
    def __init__(self, team: Team, chess = None, row=None, col=None):
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
    def getOpponentsTeamList(self):
        if(self.team == Team.WHITE):
            return self.chess.black_List
        else:
            return self.chess.white_List
    def move(self,row_col):
        if(type(row_col) is tuple):
            if(self.chess.chess[row_col[0]][row_col[1]] != None and self.chess.chess[row_col[0]][row_col[1]].team != self.team):
                res : list = self.getOpponentsTeamList()
                res.remove(self.chess.chess[row_col[0]][row_col[1]])
            self.chess.chess[self.row][self.col] = None
            self.row = row_col[0]
            self.col = row_col[1]
            self.chess.chess[self.row][self.col] = self
            self.chess.checkAfterMove()
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
        if(self.team == Team.BLACK):
            self.sprite = green_pawn
        else:
            self.sprite = white_pawn
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
    def possibleEat(self):
        result = []
        if(self.team == Team.WHITE):
            result.append((self.row-1,self.col-1))
            result.append((self.row-1,self.col+1))
        elif(self.team == Team.BLACK):
            result.append((self.row+1,self.col-1))
            result.append((self.row+1,self.col+1))
        return result
    def move(self,row_col):
        super().move(row_col)
        self.firstMove = False
class Knight(Piece):
    def __init__(self, team: Team, chess=None, row=None, col=None):
        super().__init__(team, chess, row, col)
        if(self.team == Team.BLACK):
            self.sprite = green_knight
        else:
            self.sprite = white_knight
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
        if(self.team == Team.BLACK):
            self.sprite = green_bishop
        else:
            self.sprite = white_bishop
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
        if(self.team == Team.BLACK):
            self.sprite = green_rook
        else:
            self.sprite = white_rook
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
class King(Piece):
    def __init__(self, team: Team, chess=None, row=None, col=None):
        super().__init__(team, chess, row, col)
        self.firstMove = True
        self.check = False
        if(self.team == Team.BLACK):
            self.sprite = green_king
        else:
            self.sprite = white_king
        self.gameResult = None
    def autoCheck(self, result:list,i,j,indexI,indexJ):
        posssibleMove = self.checkPossibleMove(i+indexI,j+indexJ)
        if(type(posssibleMove)==tuple):
            if(posssibleMove[0]==True):
                result.append((i+indexI,j+indexJ))
        return result
    def checkKingPossibleMove(self,result:list):
        opponentsList : list = self.getOpponentsTeamList()
        self.check = False
        for i in opponentsList:
            if(type(i) == King):
                continue
            if(type(i) == Pawn):
                if(len(i.possibleEat()) != 0):
                    for j in result:
                        if j in i.possibleEat():
                            result.remove(j)
                    if (self.row,self.col) in i.possibleEat():
                        print("CHIEU NE")
                        self.check = True
                        raise Checkmate(f'{self.team} checkmate')
            else:
                if(len(i.possibleMove()) != 0):
                    for j in result:
                        if j in i.possibleMove():
                            result.remove(j)
                    if (self.row,self.col) in i.possibleMove():
                        print("CHIEU NE")
                        self.check = True
                        raise Checkmate(f'{self.team} checkmate')
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
        result = unique(result)
        result = self.checkKingPossibleMove(result)
        if(result == [] and self.check):
            self.gameResult = GameResult.WHITELOSE
            if(self.team == Team.BLACK):
                self.chess.white_King.gameResult = GameResult.WHITEWIN
            else:
                self.chess.black_King.gameResult = GameResult.WHITEWIN
        return result
    def move(self,row_col):
        if(type(row_col) is tuple):
            if(type(row_col[0]) is int):
                if(self.chess.chess[row_col[0]][row_col[1]] != None and self.chess.chess[row_col[0]][row_col[1]].team != self.team):
                    res : list = super().getOpponentsTeamList()
                    res.remove(self.chess.chess[row_col[0]][row_col[1]])
                self.chess.chess[self.row][self.col] = None
                self.row = row_col[0]
                self.col = row_col[1]
                self.chess.chess[self.row][self.col] = self
            else:
                row_col[0](row_col[1])
        self.firstMove = False
        self.chess.checkAfterMove()
        return
    def Castle(self,col):
        if(col == 0):
            self.move((self.row,self.col-2))
            self.chess.chess[self.row][col].move((self.row,self.col+1))
        elif(col ==7):
            self.move((self.row,self.col+2))
            self.chess.chess[self.row][col].move((self.row,self.col-1))
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
        if(self.team == Team.BLACK):
            self.sprite = green_queen
        else:
            self.sprite = white_queen
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

