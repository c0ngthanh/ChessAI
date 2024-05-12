

import random
import copy
from Chess import Chess
from Enums import Team
from pieces import Pawn, Rook, Knight, Bishop, Queen, King


def reverse_array(array):
    return array[::-1]

pawn_eval_white = [
    [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
    [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
    [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
    [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
    [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
    [0.5,  1.0,  1.0, -2.0, -2.0,  1.0,  1.0,  0.5],
    [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
]

pawn_eval_black = reverse_array(pawn_eval_white)

knight_eval = [
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
    [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
    [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
    [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
    [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
    [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
    [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
]

bishop_eval_white = [
    [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
    [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [-1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
    [-1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
    [-1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
    [-1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
    [-1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
    [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
]

bishop_eval_black = reverse_array(bishop_eval_white)

rook_eval_white = [
    [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [  0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [  0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
]

rook_eval_black = reverse_array(rook_eval_white)

eval_queen = [
    [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
    [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [ -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [  0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [ -1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
]

king_eval_white = [
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
    [ -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
    [  2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0 ],
    [  2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0 ]
]

king_eval_black = reverse_array(king_eval_white)


class Agent:
    def __init__(self, team):
        self.team = team

    def getTeam(self):
        return self.team

class MinimaxAgent(Agent):
    def __init__(self, team, level=1):
        Agent.__init__(self, team)
        if level == 1:
            self.depth = 1
        elif level == 2:
            self.depth = 2
        elif level == 3:
            self.depth = 3
        elif level == 4:
            self.depth = 4

    def get_absolute_value(self, piece, is_white, x, y):
        if type(piece) == Pawn:
            return 10 + (pawn_eval_white[y][x] if is_white else pawn_eval_black[y][x])
        elif type(piece) == Rook:
            return 50 + (rook_eval_white[y][x] if is_white else rook_eval_black[y][x])
        elif type(piece) == Knight:
            return 30 + knight_eval[y][x]
        elif type(piece) == Bishop:
            return 30 + (bishop_eval_white[y][x] if is_white else bishop_eval_black[y][x])
        elif type(piece) == Queen:
            return 90 + eval_queen[y][x]
        elif type(piece) == King:
            return 900 + (king_eval_white[y][x] if is_white else king_eval_black[y][x])
        raise Exception("Unknown piece type: " + piece.type)
        
    def get_piece_value(self, piece, x, y):
        if piece is None:
            return 0
        absolute_value = self.get_absolute_value(piece, piece.team == self.team, x, y)
        return absolute_value if piece.team == self.team else -absolute_value
        
    def evaluate_board(self, board):
        total_evaluation = 0
        for i in range(8):
            for j in range(8):
                total_evaluation += self.get_piece_value(board[i][j], i, j)
        return total_evaluation
    
    def minimax(self, board, depth, is_maximizing):
        if depth == 0:
            return self.evaluate_board(board), None
        
        if is_maximizing:
            max_eval = float('-inf')
            best_move = None
            for i in range(8):
                for j in range(8):
                    if board[i][j] is None:
                        continue
                    # else:
                        # print(board[i][j])
                    if type(board[i][j]) == None:
                        continue
                    # else: 
                        # print(type(board[i][j]))
                    if board[i][j].team != self.team:
                        continue
                    candidateMove = board[i][j].possibleMove()
                    if candidateMove == []:
                        continue
                    for move in candidateMove:
                        if(type(move[0])!= int):
                            continue
                        clone_board = copy.deepcopy(board)
                        clone_board[i][j].move(move)
                        eval, _ = self.minimax(clone_board, depth - 1, False)
                        if eval > max_eval:
                            max_eval = eval
                            best_move = (i, j, move)
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for i in range(8):
                for j in range(8):
                    if board[i][j] is None:
                        continue
                    # else:
                        # print(board[i][j])
                    if type(board[i][j]) == None:
                        continue
                    # else: 
                        # print(type(board[i][j])) 
                    if board[i][j].team == self.team:
                        continue
                    candidateMove = board[i][j].possibleMove()
                    if candidateMove == []:
                        continue
                    for move in candidateMove:
                        if(type(move[0])!= int):
                            continue
                        clone_board = copy.deepcopy(board)
                        clone_board[i][j].move(move)
                        eval, _ = self.minimax(clone_board, depth - 1, True)
                        min_eval = min(min_eval, eval)
                        if eval < min_eval:
                            min_eval = eval
                            best_move = (i, j, move)
            return min_eval, best_move
    
    def get_move(self, board):
        _, best_move = self.minimax(board, self.depth, True)
        return best_move
    def printChess(self,abc):
        for i in range(8):
            for j in range(8):
                chess_obj = abc[i][j]
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
    def makeMove(self, game: Chess):
        current_board : Chess = game.getCurrentBoard()
        # print("Current")
        # self.printChess(current_board)
        clone_board = copy.deepcopy(current_board)
        best_move = self.get_move(clone_board)
        # print(best_move)
        # if(current_board[best_move[0]][best_move[1]] == None):
            # print("huhu")
        current_board[best_move[0]][best_move[1]].move(best_move[2])
        print(f"Move made by MinimaxAgent: ({best_move[0]}, {best_move[1]}) -> ({best_move[2]})"), 
        
        
