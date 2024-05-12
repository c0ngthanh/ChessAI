from enum import Enum
from Enums import *
from agent import Agent
from AssetsCfg import *
from Config import *
from Checkmate import Checkmate
import random
# from Chess import *


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

    def getPos(self):
        return self.row,self.col
    
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
    def getOurTeamList(self):
        if(self.team == Team.BLACK):
            return self.chess.black_List
        else:
            return self.chess.white_List
    def move(self,row_col):
        if(type(row_col) is tuple):
            if(self.chess.chess[row_col[0]][row_col[1]] != None and self.chess.chess[row_col[0]][row_col[1]].team != self.team):
                if(type(self.chess.chess[row_col[0]][row_col[1]]) == King):
                    self.chess.SetGameOver(self.chess.chess[row_col[0]][row_col[1]].team)
                    raise Checkmate(f'{self.team} checkmate')
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
                if(self.checkPossibleMove(self.row-2,self.col) and self.chess.chess[self.row-1][self.col] == None):
                    result.append((self.row-2,self.col))
            if(self.checkPossibleMove(self.row-1,self.col)):
                result.append((self.row-1,self.col))
            if(self.checkCanEat(self.row-1,self.col-1)):
                result.append((self.row-1,self.col-1))
            if(self.checkCanEat(self.row-1,self.col+1)):
                result.append((self.row-1,self.col+1))
        elif(self.team == Team.BLACK):
            if(self.firstMove):
                if(self.checkPossibleMove(self.row+2,self.col) and self.chess.chess[self.row+1][self.col] == None):
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
        if self.team == Team.WHITE:
            if(self.row == 0):
                self.Update(Queen)
        else:
            if(self.row == 7):
                self.Update(Queen)
    def Update(self, pieceClass):
        self.getOurTeamList().remove(self)
        self.chess.addChess(pieceClass(self.team),self.row,self.col)
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
        self.isCheck : Piece = None
        self.help = []
        self.firstCheck = True
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
    def GetCellBetweenCheckAndKing(self):
        # Tính toán các ô giữa thằng chiếu và vua
        result = []
        if(type(self.isCheck) == Knight):
            result.append((self.isCheck.row,self.isCheck.col))
        elif(self.col == self.isCheck.col):
            a = range(self.isCheck.row,self.row) if  self.isCheck.row<self.row else range(self.row+1,self.isCheck.row+1)
            for i in a:
                result.append((i,self.col))
        elif(self.row == self.isCheck.row):
            a = range(self.isCheck.col,self.col) if  self.isCheck.col<self.col else range(self.col+1,self.isCheck.col+1)
            for i in a:
                result.append((self.row,i))
        else:
            a = self.row - self.isCheck.row
            b = self.col - self.isCheck.col
            for i in range(1,abs(a)+1):
                result.append((self.row - i*a/abs(a),self.col - i*b/abs(b)))
        return result
    def checkKingPossibleMove(self,result:list):
        self.chess.chess[self.row][self.col] = None
        opponentsList : list = self.getOpponentsTeamList()
        self.check = False
        self.isCheck = None
        for i in opponentsList:
            if(type(i) == King):
                continue
            if(type(i) == Pawn):
                if(len(i.possibleEat()) != 0):
                    for j in result:
                        if j in i.possibleEat():
                            result.remove(j)
                        if type(j[0]) != int:
                            if (self.GetKingPosAfterCastle(j[1])) in i.possibleEat():
                                result.remove(j)
                    if (self.row,self.col) in i.possibleEat():
                        self.check = True
                        self.firstCheck = False
                        self.isCheck = i
                        # self.chess.game_over = True
                        # raise Checkmate(f'{self.team} checkmate')
            else:
                possmove = i.possibleMove()
                removeList = []
                if(len(possmove) != 0):
                    for j in result:
                        if j in possmove:
                            removeList.append(j)
                        if type(j[0]) != int:
                            if (self.GetKingPosAfterCastle(j[1])) in possmove:
                                result.remove(j)
                    for j in removeList:
                        result.remove(j)
                    if (self.row,self.col) in possmove:
                        self.check = True
                        self.firstCheck = False
                        self.isCheck = i
                        # self.chess.game_over = True
                        # raise Checkmate(f'{self.team} checkmate')
        self.chess.chess[self.row][self.col] = self
        return result
    def GetOpponentKing(self):
        if(self.team == Team.WHITE):
            return self.chess.black_King
        else:
            return self.chess.white_King
    def KvsK(self, result):
        if(self.chess.playerTurn != self.team):
            return result
        opponentKing = self.GetOpponentKing()
        aroundKing = []
        opponentKing.autoCheck(aroundKing,opponentKing.row,opponentKing.col,1,1)
        opponentKing.autoCheck(aroundKing,opponentKing.row,opponentKing.col,1,-1)
        opponentKing.autoCheck(aroundKing,opponentKing.row,opponentKing.col,-1,1)
        opponentKing.autoCheck(aroundKing,opponentKing.row,opponentKing.col,-1,-1)
        opponentKing.autoCheck(aroundKing,opponentKing.row,opponentKing.col,1,0)
        opponentKing.autoCheck(aroundKing,opponentKing.row,opponentKing.col,-1,0)
        opponentKing.autoCheck(aroundKing,opponentKing.row,opponentKing.col,0,1)
        opponentKing.autoCheck(aroundKing,opponentKing.row,opponentKing.col,0,-1)
        for i in result:
            if i in aroundKing:
                result.remove(i)
        return result
    def GetKingPosAfterCastle(self, col):
        if col == 0:
            return (self.row, 2)
        if col == 7:
            return (self.row, 6)
    def possibleMove(self):
        result = []
        self.help = []
        self.autoCheck(result,self.row,self.col,1,1)
        self.autoCheck(result,self.row,self.col,1,-1)
        self.autoCheck(result,self.row,self.col,-1,1)
        self.autoCheck(result,self.row,self.col,-1,-1)
        self.autoCheck(result,self.row,self.col,1,0)
        self.autoCheck(result,self.row,self.col,-1,0)
        self.autoCheck(result,self.row,self.col,0,1)
        self.autoCheck(result,self.row,self.col,0,-1)
        ###########################
        if self.firstMove and self.firstCheck:
            self.checkCastle(result,0)
            self.checkCastle(result,7)
        result = unique(result)
        result = self.checkKingPossibleMove(result)
        result = self.KvsK(result)

        if(self.check):
            gameOver = True
            ourTeam : list = self.getOurTeamList()
            moveList = self.GetCellBetweenCheckAndKing()
            for i in ourTeam:
                if type(i) == King:
                    continue
                for j in moveList:
                    if j in i.possibleMove():
                        gameOver = False
                        # (i,j) tuple i Piece , j (row,colum)
                        self.help.append((i,j))
            if(gameOver and result == []):
                self.chess.SetGameOver(self.team)
                # raise Checkmate(f'{self.team} checkmate')
        elif(result == [] and not self.check):
            canMove = False
            ourTeam : list = self.getOurTeamList()
            for i in ourTeam:
                if type(i) == King:
                    continue
                if i.possibleMove() != []:
                    canMove = True
                    break
            if not canMove:
                self.chess.SetGameOver()
        return result
    def move(self,row_col):
        if(type(row_col) is tuple):
            if(type(row_col[0]) is int):
                if(self.chess.chess[row_col[0]][row_col[1]] != None and self.chess.chess[row_col[0]][row_col[1]].team != self.team):
                    if(type(self.chess.chess[row_col[0]][row_col[1]]) == King):
                        self.chess.SetGameOver(self.chess.chess[row_col[0]][row_col[1]].team)
                        # raise Checkmate(f'{self.team} checkmate')
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
        # print("Nhap thanh ")
        # print(self.team)
        # print(col)
        # print(self.possibleMove())
        # print(self.row,self.col)
        # print(self.firstCheck,self.firstMove)
        if(col == 0):
            self.move((self.row,self.col-2))
            self.chess.chess[self.row][col].move((self.row,self.col+1))
        elif(col ==7):
            self.move((self.row,self.col+2))
            self.chess.chess[self.row][col].move((self.row,self.col-1))
        self.firstMove = False
    def checkCastle(self,result:list, col: int):
        if(self.chess.chess[self.row][col] == None or type(self.chess.chess[self.row][col]) != Rook):
            return
        if(self.chess.chess[self.row][col].firstMove):
            if(self.col > col):
                for i in range(col+1,self.col):
                    if(self.chess.chess[self.row][i] != None):
                        return result
            else:
                for i in range(self.col+1,col):
                    # print(self.chess.chess[self.row][i])
                    if(self.chess.chess[self.row][i] != None):
                        return result
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

