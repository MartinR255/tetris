import pygame

class Shape:
    def __init__(self, width, height, size):
        size = size + 1
        self.cube_shape = [pygame.Rect(175, -35, size, size), pygame.Rect(210, -35, size, size), 
                        pygame.Rect(175, 0, size, size), pygame.Rect(210, 0, size, size)]

        self.small_l_shape = [pygame.Rect(175, -35, size, size), pygame.Rect(210, -35, size, size), 
                        pygame.Rect(175, 0, size, size)]

        self.large_l_shape = [pygame.Rect(175, -35, size, size), pygame.Rect(175, 0, size, size), 
                        pygame.Rect(210, 0, size, size), pygame.Rect(245, 0, size, size)]

        self.z_shape = [pygame.Rect(175, -35, size, size), pygame.Rect(210, -35, size, size), 
                        pygame.Rect(210, 0, size, size), pygame.Rect(245, 0, size, size)]

        self.line_shape = [pygame.Rect(175, 0, size, size), pygame.Rect(210, 0, size, size), 
                        pygame.Rect(245, 0, size, size)]
        
        self.small_line_shape = [pygame.Rect(175, 0, size, size), pygame.Rect(210, 0, size, size)]
        
        self.pyramid_shape = [pygame.Rect(245, 0, size, size),  pygame.Rect(210, 0, size, size), 
                        pygame.Rect(175, 0, size, size), pygame.Rect(210, -35, size, size)]

        self.spin_range = pygame.Rect(175, -70, 35 * 3 + 1, 35 * 3 + 1)
        self.small_spin_range = pygame.Rect(175, -35, 35 * 2 + 1, 35 * 2 + 1)

        self.all_spin_ranges = [self.spin_range, self.small_spin_range]
        self.all_shapes = [self.cube_shape, self.small_line_shape, self.small_l_shape, self.line_shape, self.pyramid_shape, self.z_shape, self.large_l_shape]
        
        
