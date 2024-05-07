from Chess import *

from agent import *

def terminate(board):
    pass
 
def simulate(game:Chess):
    player0 = AgentRandom(Team.WHITE)
    player1 = AgentRandom(Team.BLACK)

    # iterations = 2, 5 or 10
    # player1 = AgentMCTS(team=Team.BLACK, iterations= 2, depth_limit= None, chess = game)
    
    # for i in range(2):
        
    # if terminate(currentState):
    #     print('Player %d win', game.getPlayerID)
    #     return
    
    if game.getPlayerTurn() == Team.WHITE:
        player0.makeMove(game)
    if game.getPlayerTurn() == Team.BLACK:
        player1.makeMove(game)
    
    # print('Turn: ', i)
    game.printChess()
    game.changeTurn()
    return game


def simulate2(game:Chess):
    player0 = AgentRandom(Team.WHITE)
    # player1 = AgentRandom(Team.BLACK)

    # iterations = 2, 5 or 10
    player1 = AgentMCTS(team=Team.BLACK, iterations= 2, depth_limit= None, chess = game)
    
    for i in range(2):  
        # if terminate(currentState):
        #     print('Player %d win', game.getPlayerID)
        #     return
        
        if game.getPlayerTurn() == Team.WHITE:
            player0.makeMove(game)
        if game.getPlayerTurn() == Team.BLACK:
            player1.makeMove(game)
        
        # print('Turn: ', i)
        game.printChess()
        game.changeTurn()

chess= Chess()
simulate2(chess)
        
