import pygame
from AssetsCfg import *
from Chess import *
from agent import *

class ChessGame():
    def __init__(self):
        pygame.init()
        self.FPS = 120
        self.fpsClock = pygame.time.Clock()
        self.DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption('Chess Game')
        # BACKGROUND = pygame.image.load('tent_game/Assets/bg.png')
        # BACKGROUND = pygame.transform.scale(BACKGROUND, (WINDOWWIDTH, WINDOWHEIGHT))
        # self.font = pygame.font.Font('arial.ttf', 20)
        self.chess = Chess(AgentRandom(Team.WHITE),AgentRandom(Team.WHITE))
        self.renderGame()
    def renderGame(self):
        for row in range(8):
            for column in range(8):
                # pygame.draw.rect(self.DISPLAYSURF,
                #             WHITE,
                #             [grid.grid[row][column].position[0],
                #             grid.grid[row][column].position[1],
                #             WIDTH,
                #             HEIGHT])
                if self.chess.board.board[row][column].value == CellValue.GREEN: 
                    self.DISPLAYSURF.blit(green_cell,self.chess.board.board[row][column].position)
                if self.chess.board.board[row][column].value == CellValue.WHITE: 
                    self.DISPLAYSURF.blit(white_cell,self.chess.board.board[row][column].position)
                if(self.chess.chess[row][column] != None):
                    self.DISPLAYSURF.blit(self.chess.chess[row][column].sprite,self.chess.board.board[row][column].position)
    def run(self):
        # DISPLAYSURF.blit(BACKGROUND, (0, 0))
        done = False
        status = None
        while not done:
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    done = True  # Flag that we are done so we exit this loop
            self.fpsClock.tick(self.FPS)
            pygame.display.update()
chess= ChessGame()
chess.run()