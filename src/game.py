from src.functions import *
from src.players.good_IA import GOOD_IA
from src.players.bad_IA import BAD_IA
from src.configs import *
import time

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4")


class Game:
    def __init__(self):
        self.board = [[0] * COLUMNS for _ in range(ROWS)]
        self.current_player = 1
        self.opponent_player = None

        self.game_over = False
        self.menu = True
        self.end_menu = False
        self.win = True
        self.counter = 0
    
    def draw_board(self, board):
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
    
    def reset_game(self):
        self.board = [[0] * COLUMNS for _ in range(ROWS)]
        self.current_player = 1
        self.opponent_player = None

        self.game_over = False
        self.menu = True
        self.end_menu = False
        self.win = True
        self.counter = 0

    def run(self):

        while not self.game_over:
            
            ### Events

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.game_over = True
                    pygame.quit()
                
                if event.type == pygame.KEYDOWN:
                    if self.menu or self.end_menu:
                        if event.key == pygame.K_ESCAPE:
                            self.game_over = True
                            pygame.quit()
                        elif event.key == pygame.K_1:
                            if self.menu:
                                self.menu = False
                                self.opponent_player = BAD_IA()
                            if self.end_menu:
                                self.end_menu = False
                                self.menu = True
                                self.reset_game()
                        elif event.key == pygame.K_2:
                            if self.menu:
                                self.menu = False
                                self.opponent_player = GOOD_IA(4)
                            if self.end_menu:
                                self.end_menu = False
                                self.menu = True
                                self.reset_game()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.menu and not self.game_over and self.current_player == 1:
                        mouse = event.pos
                        col = mouse[0] // SQUARE_SIZE
                        availables_moves = get_availables_moves(self.board)
                        for move in availables_moves:
                            if col == move[1]:
                                row = move[0]
                                self.board[row][col] = self.current_player

                                if check_win(self.board, col, self.current_player):
                                    self.end_menu = True
                                
                                self.counter += 1
                                screen.fill((0, 0, 0))
                                self.draw_board(self.board)
                                screen.blit(TITLE_TEXT_SURFACE, TITLE_TEXT_RECT)
                                pygame.display.update()
                                time.sleep(1)
                        
                        # Alterne entre les joueurs 1 et 2
                        self.current_player = 3 - self.current_player
            
            ### Game elements

            # Si le joueur est dans le menu
            if self.menu:
                screen.fill((0, 0, 0))
                text_y = HEIGHT // 2 - (len(MENU_TEXT) * TEXT_SPACING) // 2

                for line in MENU_TEXT:
                    text = FONT.render(line, True, (255, 255, 255))
                    text_rect = text.get_rect(center=(TEXT_X, text_y))
                    screen.blit(text, text_rect)
                    text_y += TEXT_SPACING
            
            # Si le joueur est dans le menu de fin
            elif self.end_menu:
                time.sleep(2)
                text_y = HEIGHT // 2 - 1/2 * (len(MENU_TEXT) * TEXT_SPACING) // 2

                if self.win:
                    first_line = "You are the winner!"
                elif not self.win:
                    first_line = "You are the loser!"
                else:
                    first_line = "Draw!"
                text = FONT.render(first_line, True, (255, 255, 255))
                text_rect = text.get_rect(center=(TEXT_X, text_y))
                screen.blit(text, text_rect)
                text_y += TEXT_SPACING

                for line in END_MENU_TEXT:
                    text = FONT.render(line, True, (255, 255, 255))
                    text_rect = text.get_rect(center=(TEXT_X, text_y))
                    screen.blit(text, text_rect)
                    text_y += TEXT_SPACING

            # Si le joueur est dans le jeu
            else:
                # Si c'est le tour de l'IA de jouer
                if self.current_player == 2:
                    col = self.opponent_player.get_move(self.board, self.current_player)
                    availables_moves = get_availables_moves(self.board)
                    for move in availables_moves:
                        if col == move[1]:
                            row = move[0]
                            self.board[row][col] = self.current_player

                            if check_win(self.board, col, self.current_player):
                                self.end_menu = True
                                self.win = False
                                
                            self.counter += 1

                    # Alterne entre les joueurs 2 et 1
                    self.current_player = 3 - self.current_player

                screen.fill((0, 0, 0))
                self.draw_board(self.board)
                screen.blit(TITLE_TEXT_SURFACE, TITLE_TEXT_RECT)

                if self.counter == 42:
                    self.win = None
                    self.end_menu = True

            pygame.display.update()