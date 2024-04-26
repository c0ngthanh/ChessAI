from Chess import *

from agent import *

def terminate(board):
    pass

def simulate():
    player0 = AgentRandom(Team.WHITE)
    player1 = AgentRandom(Team.BLACK)

    game = Chess(player0, player1)
    for _ in range(1):
        currentState = game.getCurrentBoard()
        game.printChess()
        
        # if terminate(currentState):
        #     print('Player %d win', game.getPlayerID)
        #     return
        
        if game.getPlayerTurn() == 0:
            game.player0.randomMove(currentState)

        game.printChess()
        

if __name__ == "__main__":
    simulate()
        
