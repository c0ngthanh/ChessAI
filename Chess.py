from enum import Enum
from Enums import *
from agent import Agent
# from AssetsCfg import *
from Config import *
from Checkmate import Checkmate
from pieces import *
import random
import copy
MAX_COL = 8

def GetWorldPosition(row:int,col:int):
    return (OFFSET[0]+(MARGIN + WIDTH) * col + MARGIN, OFFSET[1]+(MARGIN + HEIGHT) * row + MARGIN)

class CellValue(Enum):
    WHITE = 0
    GREEN= 1

# Cell and Board for draw game, dont touch
class Cell:
    def __init__(self, value: CellValue, row: int, col: int):
        self.value = value
        self.row = row
        self.col = col
        self.position = GetWorldPosition(row,col)
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
                    self.board[i].append(Cell(CellValue.GREEN, i, j))

class Chess:
    def __init__(self):
        self.black_List = []
        self.white_List = []
        self.initChess()
        self.board = Board()
        self.playerTurn = Team.WHITE #white move first
        self.result = None # the result of the game
        self.game_over = False # game is still ongoing
        self.white_King : King = self.chess[7][4]
        self.black_King : King = self.chess[0][4]
        self.history = []
        # if (player0.__class__.__name__ == 'AgentMCTS'):
        #     player0.init_root(self.chess)
        # if (player1.__class__.__name__ == 'AgentMCTS'):
        #     player1.init_root(self.chess)
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
    def addChess(self, piece: Piece, row: int, col:int):
        self.chess[row][col] = piece
        piece.row = row
        piece.col = col
        piece.chess = self
        if(piece.team == Team.WHITE):
            self.white_List.append(piece)
        elif(piece.team == Team.BLACK):
            self.black_List.append(piece)
    def checkAfterMove(self):
        self.black_King.possibleMove()     
        self.white_King.possibleMove()
    def SetGameOver(self, team: Team = None):
        # required team win, if not team = None, result - draw
        self.game_over = True 
        if team == None:
            # self.white_King.gameResult = GameResult.DRAW
            # self.black_King.gameResult = GameResult.DRAW
            self.result = GameResult.DRAW
            
        elif team == Team.WHITE:
            # self.white_King.gameResult = GameResult.WHITELOSE
            # self.black_King.gameResult = GameResult.WHITEWIN
            self.result = GameResult.WHITELOSE
            
        elif team == Team.BLACK:
            # self.white_King.gameResult = GameResult.WHITEWIN
            # self.black_King.gameResult = GameResult.WHITELOSE
            self.result = GameResult.WHITEWIN
    def printChess(self):
        for i in range(8):
            for j in range(8):
                chess_obj = self.chess[i][j]
                if(chess_obj!= None):
                    if chess_obj.__class__.__name__ == 'King':
                        if(chess_obj.team == Team.WHITE):
                            print("V_W", end=" ", flush=True)
                        else:
                            print("V_B", end=" ", flush=True)
                    else:
                        if(chess_obj.team == Team.WHITE):
                            print(chess_obj.__class__.__name__[0] +"_W", end=" ", flush=True)
                        else:
                            print(chess_obj.__class__.__name__[0]+"_B", end=" ", flush=True)
                else:
                    print("___", end=" ", flush=True)
            print()
        print()

    def possible_move(self):
        moves = []
        for i in range(8):
            for j in range(8):
                if(self.chess[i][j] == None): continue
                if self.playerTurn == self.chess[i][j].team:
                    for move in self.chess[i][j].possibleMove():
                        moves.append(move)
        return moves


    def getPlayerTurn(self):
        return self.playerTurn
    
    def getCurrentBoard(self):
        return self.chess
    
    def changeTurn(self):
        self.playerTurn = Team.WHITE if self.playerTurn == Team.BLACK else Team.BLACK

    def isGameOver(self):
        return self.game_over
    
    def makeRandomMove(self):
        flag = True
        x, y, i, j = 0, 0, 0, 0
        while flag:
            # choose a random piece
            i = random.randint(0,7)
            j = random.randint(0,7)
            if(self.chess[i][j] == None): continue
            if self.chess[i][j].team != self.playerTurn: continue
            candidateMove = self.chess[i][j].possibleMove()
            

            # choose a random possible move
            if (candidateMove != []):
                selectedMove = random.choice(candidateMove)
                x, y = selectedMove
                self.chess[i][j].move(selectedMove)
                flag= False
            
        #change turn
        self.changeTurn()
        
        #update history
        self.history.append((i, j, x, y))

    def makeMoveFromTuple(self, move: tuple):
        print('move', move)
        i,j,x,y = move
        self.chess[i][j].move((x,y))
        #change turn

    def __deepcopy1__(self):
        deep = Chess()
        deep.black_List = copy.deepcopy(self.black_List)
        deep.white_List = self.white_List 
        deep.chess = self.chess
        deep.board = self.board 
        deep.playerTurn = self.playerTurn 
        deep.result = self.result
        deep.game_over = self.game_over
        deep.white_King = self.white_King 
        deep.black_King = self.black_King 
        deep.history = self.history
        return deep
