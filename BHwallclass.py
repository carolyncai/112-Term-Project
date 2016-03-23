import pygame

pygame.init()

class Wall(pygame.sprite.Sprite): 
# just a wall...
# if a bullet hits the wall it will die
# that way there aren't 10 million offscreen bullets
    def __init__(self, x0, y0, x1, y1):
        super(Wall, self).__init__()
        width = abs(int(x1 - x0))
        height = abs(int(y1 - y0))
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x0
        self.rect.y = y0


