from src.functions import *
from src.players.good_IA import GOOD_IA
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


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4")

text_surface = FONT.render("Connect 4", True, (0, 0, 0))

text_rect = text_surface.get_rect()
text_rect.center = (WIDTH // 2, SQUARE_SIZE // 2)

for x in range(text_surface.get_width()):
    
    g = x / text_surface.get_width() * 173

    for y in range(text_surface.get_height()):
        pixel_color = text_surface.get_at((x, y))
        if pixel_color != (0, 0, 0, 0):
            text_surface.set_at((x, y), (255, g, 0))


def draw_board(board):
    for row in range(ROWS):
        for col in range(COLUMNS):
            pygame.draw.rect(screen, BOARD_COLOR, (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            pygame.draw.circle(screen, (94, 120, 236), (col * SQUARE_SIZE + SQUARE_SIZE // 2 - 1.2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2 - 1.2), SQUARE_SIZE // 2 - 2)
            pygame.draw.circle(screen, (0, 29, 153), (col * SQUARE_SIZE + SQUARE_SIZE // 2 + 1.2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2 + 1.2), SQUARE_SIZE // 2 - 2)
            pygame.draw.circle(screen, BOARD_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 2.5)

            pygame.draw.circle(screen, TOKEN_COLORS[board[row][col]], (col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)

            if TOKEN_COLORS[board[row][col]] == (255, 173, 0):
                pygame.draw.circle(screen, (167, 114, 0), (col * SQUARE_SIZE + SQUARE_SIZE // 2 - 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2 - 2), SQUARE_SIZE // 2 - 10)
                pygame.draw.circle(screen, (255, 232, 182), (col * SQUARE_SIZE + SQUARE_SIZE // 2 + 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2 + 2), SQUARE_SIZE // 2 - 10)

            if TOKEN_COLORS[board[row][col]] == (254, 0, 0):
                pygame.draw.circle(screen, (166, 1, 0), (col * SQUARE_SIZE + SQUARE_SIZE // 2 - 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2 - 2), SQUARE_SIZE // 2 - 10)
                pygame.draw.circle(screen, (254, 182, 183), (col * SQUARE_SIZE + SQUARE_SIZE // 2 + 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2 + 2), SQUARE_SIZE // 2 - 10)

            pygame.draw.circle(screen, TOKEN_COLORS[board[row][col]], (col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 10.5)


def main():

    board = [[0] * COLUMNS for _ in range(ROWS)]
    current_player = 1
    game_over = False
    opponent_player = GOOD_IA(4)
    counter = 0

    while not game_over:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over and current_player == 1:
                    mouse = event.pos
                    col = mouse[0] // SQUARE_SIZE
                    availables_moves = get_availables_moves(board)
                    for move in availables_moves:
                        if col == move[1]:
                            row = move[0]
                            board[row][col] = current_player

                            if check_win(board, col, current_player):
                                print('Player 🔴 won!')
                                game_over = True
                            
                            counter += 1
                    
                    # Alterne entre les joueurs 1 et 2
                    current_player = 3 - current_player
            
            if current_player == 2:
                col = opponent_player.get_move(board, current_player)
                availables_moves = get_availables_moves(board)
                for move in availables_moves:
                    if col == move[1]:
                        row = move[0]
                        board[row][col] = current_player

                        if check_win(board, col, current_player):
                            print('Player 🔵 won!')
                            game_over = True
                            
                        counter += 1

                # Alterne entre les joueurs 2 et 1
                current_player = 3 - current_player

        screen.fill((0, 0, 0))
        draw_board(board)
        screen.blit(text_surface, text_rect)

        if counter >= 21:
            print("Draw!")
            game_over = True

        pygame.display.update()
    
    while True:
        screen.fill((0, 0, 0))
        draw_board(board)
        screen.blit(text_surface, text_rect)
        pygame.display.update()



if __name__ == "__main__":
    main()