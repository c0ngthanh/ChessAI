from Chess import *

from agent import *

def terminate(board):
    pass
 
def simulate(game:Chess):
    print('Turn', game.getPlayerTurn())
    player0 = AgentRandom(Team.WHITE)
    # player1 = AgentRandom(Team.BLACK)

    # iterations = 2, 5 or 10
    player1 = AgentMCTS(team=Team.BLACK, iterations= 5, depth_limit= None, chess = game)
    
    # for i in range(2):
        
    # if terminate(currentState):
    #     print('Player %d win', game.getPlayerID)
    #     return
    
    if game.getPlayerTurn() == player0.getTeam():
        player0.makeMove(game)
    else:
        player1.makeMove(game)
        game.changeTurn()

    # print(game.game_over)
    if game.game_over: 
        print(game.result)
    # print('Turn: ', i)
    game.printChess()
    return game


def simulate2(game:Chess):
    player0 = AgentRandom(Team.WHITE)
    # player1 = AgentRandom(Team.BLACK)

    # iterations = 2, 5 or 10
    player1 = AgentMCTS(team=Team.BLACK, iterations= 2, depth_limit= None, chess = game)
    
    step_lim = 1000
    step = 0
    while not game.game_over and step < step_lim:  
        # if terminate(currentState):
        #     print('Player %d win', game.getPlayerID)
        #     return
        step += 1
        if game.getPlayerTurn() == Team.WHITE:
            player0.makeMove(game)
        if game.getPlayerTurn() == Team.BLACK:
            player1.makeMove(game)
        
        print('Turn: ', step)
        game.printChess()
        game.changeTurn()
    
    # print(chess.result)

# for _ in range(10):
#     chess= Chess()
#     simulate2(chess)
#     print(chess.result)   

chess= Chess()
simulate2(chess)
print(chess.result)