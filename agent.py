from collections import deque
import random
import math
import copy

class Agent:
    def __init__(self, team):
        self.team = team

    def getTeam(self):
        return self.team


class AgentRandom(Agent):
    def __init__(self, team):
        Agent.__init__(self,team)

    def randomMove(self, chess):
        flag = True
        while flag:
            # choose a random piece
            i = random.randint(0,7)
            j = random.randint(0,7)
            if(chess[i][j] == None): continue

            candidateMove = chess[i][j].possibleMove()

            # choose a random possible move
            if (candidateMove != []):
                selectedMove = random.choice(candidateMove)
                chess[i][j].move(selectedMove)
                flag= False


class MCTSNode:
    def __init__(self, chess, parent, move, alpha = -float("inf"),beta = float("inf")):
        self.chess= chess
        self.parent = parent
        self.move = move
        self.children = []
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

class AgentMCTS(Agent):
    def __init__(self, chess, iterations: int, depth_limit: int, exploration_constant: float = math.sqrt(2)):
        self.interations =  iterations
        self.chess = chess
        self.exploration_constant = exploration_constant
        self.depth_limit = depth_limit
        self.root = MCTSNode(chess)
        self.hashtable = {}
        self.current_node = self.root

    def set_current_node(self, chess):
        # set current node to the one similar to the given chess
        for child in self.current_node.children:
            if child.chess == chess:
                self.current_node = child
                return
        
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            if node.chess == chess and node != self.root and node != self.current_node:
                self.current_node = node
                return
            queue.extend(node.children)
        if not self.current_node.chess == chess:
            self.current_node= MCTSNode(chess)

    def _selection(self, node:MCTSNode, depth: int):
        while not node.chess.check_game_over():
            if node.not_fully_expanded():
                return node
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
            next_chess.play_random_move()
        except Checkmate:
            return node
        new_node = MCTSNode(next_chess, parent = node, alpha=node.alpha, beta = node.beta, move  = None)
        node.children.append(new_node)
        return new_node
    
    def _simulation(self, node:MCTSNode) -> int:
        chess = copy.deepcopy(node.chess)
        while not chess.game_over:
            try:
                chess.play_random_move()
            except Checkmate:
                return chess.result
        return chess.result
    
    def _backpropagate(self, node: MCTSNode, result: int):
        while node is not None:
            node.visits+=1
            node.wins+=result
            node = node.parent
  
    def selectMove(self, chess):
        self.set_current_node(chess)

        for _ in range(self.interations):
            node = self._selection(self.current_node, 0)
            try:
                if node.not_fully_expanded():
                    node = self._expand()
            except Exception: 
                pass
            result = self._simulation(node)
            self._backpropagate(node, result)
        best_child = max(self.current_node.children, key = lambda x: x.ucb1(self.exploration_constant))
        self.current_node = best_child
        return best_child.move

