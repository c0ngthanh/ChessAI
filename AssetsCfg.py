import pygame
WHITE = (256,244,228)
GREEN = (8,116,52)
WIDTH = 50
HEIGHT = 50
WINDOWWIDTH = 1000
WINDOWHEIGHT = 1000
OFFSET = [300,200]
MARGIN = 2
# bulb_img = pygame.transform.scale(pygame.image.load("game/Assets/bulb.jpg"),(WIDTH,HEIGHT))
# red_bulb_img = pygame.transform.scale(pygame.image.load("game/Assets/redbulb.jpg"),(WIDTH,HEIGHT))
# black_cell = pygame.transform.scale(pygame.image.load("game/Assets/black_cell.png"),(WIDTH,HEIGHT))
white_cell = pygame.transform.scale(pygame.image.load("Assets/white.png"),(WIDTH,HEIGHT))
green_cell = pygame.transform.scale(pygame.image.load("Assets/green.png"),(WIDTH,HEIGHT))

white_bishop = pygame.transform.scale(pygame.image.load("Assets/white_bishop.png"),(WIDTH,HEIGHT))
white_king = pygame.transform.scale(pygame.image.load("Assets/white_king.png"),(WIDTH,HEIGHT))
white_knight = pygame.transform.scale(pygame.image.load("Assets/white_knight.png"),(WIDTH,HEIGHT))
white_pawn = pygame.transform.scale(pygame.image.load("Assets/white_pawn.png"),(WIDTH,HEIGHT))
white_queen = pygame.transform.scale(pygame.image.load("Assets/white_queen.png"),(WIDTH,HEIGHT))
white_rook = pygame.transform.scale(pygame.image.load("Assets/white_rook.png"),(WIDTH,HEIGHT))
green_bishop = pygame.transform.scale(pygame.image.load("Assets/black_bishop.png"),(WIDTH,HEIGHT))
green_king = pygame.transform.scale(pygame.image.load("Assets/black_king.png"),(WIDTH,HEIGHT))
green_knight = pygame.transform.scale(pygame.image.load("Assets/black_knight.png"),(WIDTH,HEIGHT))
green_pawn = pygame.transform.scale(pygame.image.load("Assets/black_pawn.png"),(WIDTH,HEIGHT))
green_queen = pygame.transform.scale(pygame.image.load("Assets/black_queen.png"),(WIDTH,HEIGHT))
green_rook = pygame.transform.scale(pygame.image.load("Assets/black_rook.png"),(WIDTH,HEIGHT))
