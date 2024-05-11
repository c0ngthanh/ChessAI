import time
import pygame
from AssetsCfg import *
from Chess import *
from agent import *
from main import *
# from Config import *
# pygame.transform.scale(pygame.image.load("Assets/white.png"),(WIDTH,HEIGHT))
white_cell = pygame.transform.scale(pygame.image.load("Assets/white.png"),(WIDTH,HEIGHT))
green_cell = pygame.transform.scale(pygame.image.load("Assets/green.png"),(WIDTH,HEIGHT))
class ChessGame():
    def __init__(self):
        pygame.init()
        self.FPS = 120
        self.fpsClock = pygame.time.Clock()
        self.DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption('Chess Game')
        self.chess = Chess()
        self.renderGame()
        self.player0 = AgentRandom(Team.WHITE)
        self.player1 = AgentMCTS(team=Team.BLACK, iterations= 2, depth_limit= None, chess = self.chess)
    def renderGame(self):
        for row in range(8):
            for column in range(8):
                if self.chess.board.board[row][column].value == CellValue.GREEN: 
                    self.DISPLAYSURF.blit(green_cell,self.chess.board.board[row][column].position)
                if self.chess.board.board[row][column].value == CellValue.WHITE: 
                    self.DISPLAYSURF.blit(white_cell,self.chess.board.board[row][column].position)
                if(self.chess.chess[row][column] != None):
                    self.DISPLAYSURF.blit(pygame.transform.scale(pygame.image.load(self.chess.chess[row][column].sprite),(WIDTH,HEIGHT)),self.chess.board.board[row][column].position)
    def simulate(self):
        print('Turn', self.chess.getPlayerTurn())
        if self.chess.getPlayerTurn() == self.player0.getTeam():
            self.player0.makeMove(self.chess)
            print(self.chess.history[-1])
            print("hehe")
        else:
            self.player1.makeMove(self.chess)
            self.chess.changeTurn()

        # print(game.game_over)
        if self.chess.game_over: 
            print(self.chess.result)
        # print('Turn: ', i)
        self.chess.printChess()
        return self.chess
    def run(self):
        # DISPLAYSURF.blit(BACKGROUND, (0, 0))
        done = False
        status = None
        while not done:
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    done = True  # Flag that we are done so we exit this loop
                # if event.type == pygame.MOUSEBUTTONDOWN:
                    # self.chess = simulate(self.chess)
                    # self.renderGame()
            time.sleep(0.01)
            if not self.chess.game_over:
                self.chess = simulate(self.chess)
                self.renderGame()
            self.fpsClock.tick(self.FPS)
            pygame.display.update()
chess= ChessGame()
chess.run()