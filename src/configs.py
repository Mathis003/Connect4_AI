import pygame

ROWS = 6
COLUMNS = 7
SQUARE_SIZE = 100
WIDTH = COLUMNS * SQUARE_SIZE
HEIGHT = (ROWS + 1) * SQUARE_SIZE  # +1 pour la ligne supérieure où les jetons sont placés
BOARD_COLOR = (0, 42, 224)
TOKEN_COLORS = [(0, 0, 0), (254, 0, 0), (255, 173, 0)]  # Noir, Rouge et Jaune
FONT = pygame.font.Font(None, 100)