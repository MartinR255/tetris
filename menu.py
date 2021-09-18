import pygame
import os

class Menu:
    def __init__(self):
        self.line_rect = pygame.Rect(10, 10, 435, 574)
        self.start_button = pygame.Rect(127.5, 350, 200, 50)
        self.start_img = pygame.image.load(os.path.join('images', 'start_button.png'))
        self.logo = pygame.image.load(os.path.join('images', 'logo.png'))
        