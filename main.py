import pygame
from game import Game
from menu import Menu

class Program:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 455, 594
        self.size = 35
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("TETRIS")

        self.DARK_GREY = (38, 38, 38)
        self.WHITE = (255, 255, 255)

        self.in_menu = True
        self.in_game = False

        self.FPS = 60
        self.menu = Menu()
        self.main()


    def create_game(self):
        self.menu = None
        self.in_menu = False
        self.in_game = True
        self.game = Game(self.WIDTH, self.HEIGHT, self.size, self.FPS)


    def check_click(self, mouse_pos):
        if self.in_menu:
            if self.menu.start_button.collidepoint(mouse_pos):
                self.create_game()
        elif self.in_game and not(self.game.active):
            if self.game.restart_button.collidepoint(mouse_pos):
                self.game = Game(self.WIDTH, self.HEIGHT, self.size, self.FPS)


    def draw_window(self):
        self.WIN.fill(self.DARK_GREY)
        if self.in_menu:
            pygame.draw.rect(self.WIN, self.WHITE, self.menu.line_rect, 2)
            self.WIN.blit(self.menu.logo, (0, 200))
            self.WIN.blit(self.menu.start_img, (127.5, 350))

        elif self.in_game:
            self.WIN.blit(self.game.score_text, (40, 565))
            self.WIN.blit(self.game.level_text, (300, 565))

            ###grid
            for i in range(1, self.WIDTH // 13 - 1):
                pygame.draw.line(self.WIN, self.WHITE, (self.size * i, self.size), (self.size * i, self.HEIGHT - self.size), 1)
            for i in range(1, self.HEIGHT // 18 - 1):
                pygame.draw.line(self.WIN, self.WHITE, (self.size, self.size * i), (self.WIDTH - self.size, self.size * i), 1)

            ###pieces
            for i in self.game.obj:
                if i.y >= self.size:
                    pygame.draw.rect(self.WIN, self.game.obj_cl, i)
                    pygame.draw.rect(self.WIN, self.WHITE, i, 1)
            
            for obj, color in zip(self.game.obj_locked, self.game.obj_locked_cl):
                for j in obj:
                    pygame.draw.rect(self.WIN, color, j)
                    pygame.draw.rect(self.WIN, self.WHITE, j, 1)
            
            if not(self.game.active):
                self.WIN.blit(self.game.restart_tab, (78, 223))
    
        pygame.display.update()


    def main(self):
        clock = pygame.time.Clock()
        run = True
        
        while run:
            clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_click(event.pos)

            if self.in_game and self.game.active:
                self.game.movement(pygame.key.get_pressed())
            self.draw_window()

        pygame.quit()

Program()