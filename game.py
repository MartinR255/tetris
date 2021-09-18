import pygame
from shape import Shape
from random import randrange
import os

class Game:
    def __init__(self, width, height, size, FPS):
        self.width = width
        self.height = height
        self.size = size
        self.grid_columns = (self.width - self.size) / 12
       
        self.FPS = FPS
        self.timer = 0

        ###restart tab
        self.restart_tab = pygame.image.load(os.path.join('images', 'restart_tab.png'))
        self.restart_button = pygame.Rect(150, 300, 165, 45)

        self.score = 0
        self.level = 1
        self.active = True
        self.moving = False
        self.obj = None
        self.obj_cl = None
        self.obj_locked = []
        self.obj_locked_cl = []
        self.next_level = [80]
        self.raise_new_level = 80

        #colors
        self.WHITE = (255, 255, 255)
        self.LIGHT_RED = (255, 77, 77)
        self.LIGHT_BLUE = (51, 133, 255)
        self.LIGHT_GREEN = (0, 230, 115)
        self.LIGHT_YELLOW = (230, 230, 0)
        self.LIGHT_ORANGE = (255, 166, 77)
        self.PURPLE = (136, 77, 255)
        self.colors = [self.LIGHT_RED, self.LIGHT_BLUE, self.LIGHT_GREEN, self.LIGHT_YELLOW, self.PURPLE, self.LIGHT_ORANGE]

        pygame.font.init()
        self.myfont = pygame.font.SysFont('Oswald', 35)
        self.score_text = self.myfont.render(f'SCORE:{self.score}', False, self.WHITE)
        self.level_text = self.myfont.render(f'LEVEL:{self.level}', False, self.WHITE)
        

    def movement(self, keypressed):
        self.timer += self.FPS
        self.create_new_shape()
        self.check_for_full_lines()

        if self.timer % 42 == 0:
            self.turn_obj(keypressed)

        if self.timer % 36 == 0:
            self.move_side_to_side(keypressed)

        ###change speed if down key is being pressed
        if keypressed[pygame.K_DOWN]:
            self.timer = self.FPS * 30

        if self.timer == self.FPS * 30:
            self.timer = 0
            self.move_down(keypressed)
        
        
    def create_new_shape(self):
        if not(self.moving):
            self.moving = True
            self.shapes = Shape(self.width, self.height, self.size)
            self.obj_type = randrange(7)
            self.obj = self.shapes.all_shapes[self.obj_type]

            ###choosing box for spin range
            if self.obj_type in [1, 2]:
                self.obj_spin_range = self.shapes.all_spin_ranges[1]
                self.range_num = 2 #spin range width and height
            else:
                self.obj_spin_range = self.shapes.all_spin_ranges[0]
                self.range_num = 3 

            self.obj_cl = self.colors[randrange(6)]
            self.direct = 0


    def move_down(self, keypressed):
        ###creates one move ahead
        next_move = []
        for i in self.obj:
            next_move.append(pygame.Rect(i.x, i.y + self.size, self.size + 1, self.size + 1))

        ###check for collision with other pieces
        if self.collision(next_move):
            self.moving = False
            self.obj_locked_cl.append(self.obj_cl)
            self.obj_locked.append([j for j in self.obj])
            return

        ###check for bottom
        for i in self.obj:
            if i.y + self.size > self.height - self.size:
                self.moving = False
                self.obj_locked_cl.append(self.obj_cl)
                self.obj_locked.append([j for j in self.obj])
                break   
        
        if self.moving:      
            for i in self.obj:
                i.y += self.size
            self.obj_spin_range.y += self.size

    
    def turn_obj(self, keypressed):
        if (keypressed[pygame.K_UP] and self.obj_type != 0 and 
            self.obj_spin_range.x + self.size * self.range_num <= self.width - self.size and 
            self.obj_spin_range.x >= self.size and 
            self.obj_spin_range.y + self.size * self.range_num < self.height - self.size):

            if self.direct == 4:
                self.direct = 0
                
            x = self.obj_spin_range.x
            y = self.obj_spin_range.y
            middle_pos = [0, 0, 0, 0]
            center = [0]

            if self.obj_type > 2:
                corners_pos = [(x + self.size * 2, y + self.size * 2), (x, y + self.size * 2),
                                    (x, y), (x + self.size * 2, y)]
                center = [(x + self.size, y + self.size)] 
            else:
                corners_pos = [(x + self.size, y + self.size), (x, y + self.size), (x, y), (x + self.size, y)]
            
            middle_pos = [(x + self.size, y + self.size * 2), (x, y + self.size), 
                                    (x + self.size, y), (x + self.size  * 2, y + self.size)]
    
            for i in range(self.direct):
                corners_pos.append(corners_pos.pop(0))
                middle_pos.append(middle_pos.pop(0))

            can_turn = []
            for i in self.obj:
                if (i.x, i.y) in corners_pos:
                    corners_pos.append(corners_pos.pop(0))
                    next_x =  corners_pos[0][0]
                    next_y = corners_pos[0][1]
                    next_move = [pygame.Rect(next_x, next_y + self.size, self.size + 1, self.size + 1)]
                    if not(self.collision(next_move)):
                        can_turn.append((next_x, next_y))
                   
                elif (i.x, i.y) in middle_pos:
                    middle_pos.append(middle_pos.pop(0)) 
                    next_x = middle_pos[0][0]
                    next_y = middle_pos[0][1]
                    next_move = [pygame.Rect(next_x, next_y + self.size, self.size + 1, self.size + 1)]
                    if not(self.collision(next_move)):
                        can_turn.append((next_x, next_y))
                        
                elif (i.x, i.y) in center:
                    next_x = center[0][0]
                    next_y = center[0][1]
                    next_move = [pygame.Rect(next_x, next_y + self.size, self.size + 1, self.size + 1)]
                    if not(self.collision(next_move)):
                        can_turn.append((center[0][0], center[0][1]))
                    
            if len(can_turn) == len(self.obj):
                for i, j in zip(self.obj, can_turn):
                    i.x = j[0]
                    i.y = j[1]
                self.direct += 1    


    def collision(self, next_move):
        for i in next_move:
            for obj in self.obj_locked:
                if i in obj:
                    return True
        return False
                    

    def move_side_to_side(self, keypressed):
        if keypressed[pygame.K_RIGHT]:
            ###creates one block ahead down and also to right
            next_move = []
            for i, j in zip(self.obj, self.obj):
                next_move.append(pygame.Rect(i.x + self.size, i.y + self.size, self.size + 1, self.size + 1))
                next_move.append(pygame.Rect(i.x + self.size, i.y, self.size + 1, self.size + 1))
            if self.collision(next_move):
                return

            ###check collision with sides
            for i in self.obj:
                if i.x + self.size >= self.width - self.size:
                    return
            for i in self.obj:
                i.x += self.size
            self.obj_spin_range.x += self.size

        elif keypressed[pygame.K_LEFT]:
            ###creates one block ahead down and also to left side
            next_move = []
            for i, j in zip(self.obj, self.obj):
                next_move.append(pygame.Rect(i.x - self.size, i.y + self.size, self.size + 1, self.size + 1))
                next_move.append(pygame.Rect(i.x - self.size, i.y, self.size + 1, self.size + 1))
            if self.collision(next_move):
                return

            ###check collision with sides
            for i in self.obj:
                if i.x - self.size < self.size:
                    return
            for i in self.obj:
                i.x -= self.size
            self.obj_spin_range.x -= self.size

    
    def check_for_full_lines(self):
        num_of_full_lines = 0
        add = 0
        for line in range(self.height - self.size * 2 + 1, 0, -self.size):
            position = []
            for col in range(self.size, self.width - self.size, self.size):
                for obj in self.obj_locked:
                    for i in obj:
                        if (i.x, i.y) == (col, line):
                            position.append((i.x, i.y))
                        if i.y < self.size:
                            self.active = False
        
            if len(position) == 11:
                num_of_full_lines += 1
                for i in range(11):
                    self.delete_square(position)
                self.move_grid_down(line)

        add += 20 * num_of_full_lines
        self.score += add
        self.score_text = self.myfont.render(f'SCORE:{self.score}', False, self.WHITE)
        if self.score >= self.next_level[self.level - 1]:
            self.next_level.append(self.next_level[self.level - 1] + self.raise_new_level)
            self.level += 1
            self.raise_new_level += 20
        self.level_text = self.myfont.render(f'LEVEL:{self.level}', False, self.WHITE)

                
    ###deletes one square and then stop
    def delete_square(self, position):
        for pos, obj in enumerate(self.obj_locked):
            for i in obj:
                if (i.x, i.y) in position:
                    self.obj_locked[pos].remove(i)
                    return


    ###moves grid down after full lines have been deleted
    def move_grid_down(self, move_from):
        for obj in self.obj_locked:
            for i in obj:
                if i.y < move_from:
                    i.y += self.size

                       

            

