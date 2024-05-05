from collections import deque
import random
import math
import copy
from Checkmate import Checkmate
from Enums import *
import dill
import pickle

class Agent:
    def __init__(self, team):
        self.team = team

    def getTeam(self):
        return self.team


class AgentRandom(Agent):
    def __init__(self, team):
        Agent.__init__(self,team)

    def makeMove(self, game):
        chess = game.getCurrentBoard()
        flag = True
        while flag:
            # choose a random piece
            i = random.randint(0,7)
            j = random.randint(0,7)
            if(chess[i][j] == None): continue
            if chess[i][j].team != self.team: continue
            candidateMove = chess[i][j].possibleMove()
            

            # choose a random possible move
            if (candidateMove != []):
                selectedMove = random.choice(candidateMove)
                print(selectedMove)
                chess[i][j].move(selectedMove)
                flag= False


class MCTSNode:
    def __init__(self, chess, parent= None, move= None, alpha = -float("inf"),beta = float("inf")):
        self.chess = chess #state of node is chess
        self.parent = parent
        self.move = move #move to get to current node(state) from parent
        self.children = [] #possible states from current state
        self.visits = 0 
        self.wins = 0
        self.alpha = alpha
        self.beta = beta

    def not_fully_expanded(self) -> bool:
        # check if node has been fully expanded
        return len(self.children) < len(self.chess.possible_move())
    
    def ucb1(self, exploration_constant:float) -> float:
        if self.visits == 0:
            return float('inf')
        return self.wins / self.visits + exploration_constant * math.sqrt(math.log(self.parent.visits) / self.visits)
    
    def setChess(self,chess):
        self.chess = chess

class AgentMCTS(Agent):
    def __init__(self, chess, team, iterations: int, depth_limit: int, exploration_constant: float = math.sqrt(2)):
        Agent.__init__(self,team)
        self.interations =  iterations
        self.chess = chess
        self.exploration_constant = exploration_constant
        self.depth_limit = depth_limit
        self.root = MCTSNode(chess)
        self.hashtable = {}
        self.current_node = self.root
    
    def init_root(self, chess):
        # dump code so i need to create extra init
        self.chess = chess
        self.root = MCTSNode(chess)

    def set_current_node(self, chess):
        # set current node to the one similar to the given chess
        for child in self.current_node.children:
            if child.chess == chess:
                self.current_node = child
                print('set current node')
                self.current_node.chess.printChess()
                return
        
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            if node.chess == chess and node != self.root and node != self.current_node:
                self.current_node = node
                print('set current node 2')
                self.current_node.chess.printChess()
                return
            queue.extend(node.children)

        if not self.current_node.chess == chess:
            self.current_node= MCTSNode(chess)
            print('set current node 3')
            self.current_node.chess.printChess()

    def _selection(self, node:MCTSNode, depth: int):
        while not node.chess.isGameOver(): #if game is not over yet
            #select node which is not fully expanded
            if node.not_fully_expanded(): 
                return node
            #return current node if reach depth limit
            if self.depth_limit and depth >= self.depth_limit:
                return node
            
            children = node.children
            children = [child for child in children if child.alpha <= node.beta]
            if len(children) == 0:
                return node
            node = max(children, key = lambda x: x.ucb1(self.exploration_constant))
            depth += 1
        return node
    
    def _expand(self, node:MCTSNode) -> MCTSNode:
        next_chess = copy.deepcopy(node.chess)
        try:
            next_chess.makeRandomMove()
        except Checkmate:
            return node
        new_node = MCTSNode(next_chess, parent = node, alpha=node.alpha, beta = node.beta, move  = next_chess.history[-1])
        node.children.append(new_node)
        return new_node
    
    def _simulation(self, node:MCTSNode) -> int:
        print('simulation')
        copychess = copy.deepcopy(node.chess)
        while not copychess.game_over:
            try:
                copychess.makeRandomMove()
            except Checkmate:
                return copychess.result
        return copychess.result
    
    def _backpropagate(self, node: MCTSNode, result: GameResult):
        # score = 0.5 if draw, score = 1 if win and 0 if lose
        score = 0
        if result == GameResult.DRAW:
            score = 0.5
        if result == GameResult.WHITEWIN and self.team == Team.WHITE:
            score = 1
        if result == GameResult.WHITELOSE and self.team == Team.BLACK:
            score = 1
        while node is not None:
            node.visits+=1
            node.wins+=score
            node = node.parent
  
    def makeMove(self, chess):
        self.set_current_node(chess)
        
        for _ in range(self.interations):
            node = self._selection(self.current_node, 0)
            result = 0
            try:
                if node.not_fully_expanded():
                    node = self._expand()
            except Exception: 
                pass

            try:
                result = self._simulation(node)

            except Exception: 
                pass
            self._backpropagate(node, result)
        best_child = max(self.current_node.children, key = lambda x: x.ucb1(self.exploration_constant), default=0)
        if (type(best_child) is not int):
            print(best_child.move)

