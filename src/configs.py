import pygame

pygame.init()

ROWS = 6
COLUMNS = 7
SQUARE_SIZE = 100
WIDTH = COLUMNS * SQUARE_SIZE
HEIGHT = (ROWS + 1) * SQUARE_SIZE  # +1 pour la ligne supérieure où les jetons sont placés
BOARD_COLOR = (0, 42, 224)
TOKEN_COLORS = [(0, 0, 0), (254, 0, 0), (255, 173, 0)]  # Noir, Rouge et Jaune
FONT = pygame.font.Font(None, 100)

MENU_TEXT = [
    "Menu",
    "Jouer contre une IA:",
    "1. IA Nulle",
    "2. IA Forte",
    "Appuyez sur 1 ou 2",
    "pour choisir,",
    "ESC pour quitter."
]

END_MENU_TEXT = [
    "Appuyez sur 1",
    "pour rejouer,",
    "ESC pour quitter."
]

# Positionnement des textes
TEXT_SPACING = 80
TEXT_X = WIDTH // 2
TEXT_Y = HEIGHT // 2 - (len(MENU_TEXT) * TEXT_SPACING) // 2

TITLE_TEXT_SURFACE = FONT.render("Connect 4", True, (0, 0, 0))
TITLE_TEXT_RECT = TITLE_TEXT_SURFACE.get_rect()
TITLE_TEXT_RECT.center = (WIDTH // 2, SQUARE_SIZE // 2)

for x in range(TITLE_TEXT_SURFACE.get_width()):
    
    g = x / TITLE_TEXT_SURFACE.get_width() * 173

    for y in range(TITLE_TEXT_SURFACE.get_height()):
        pixel_color = TITLE_TEXT_SURFACE.get_at((x, y))
        if pixel_color != (0, 0, 0, 0):
            TITLE_TEXT_SURFACE.set_at((x, y), (255, g, 0))