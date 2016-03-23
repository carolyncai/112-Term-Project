import pygame

pygame.init()

class Sign(pygame.sprite.Sprite):
    def __init__(self, worldX, textList):
        super(Sign, self).__init__()
        self.image = pygame.image.load("sign.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0 # temp value, this changes in update...
        self.rect.y = 230
        self.worldX = worldX # set this for each sign

        self.displayingText = False
        self.doneReading = False
        self.text = textList
        self.text_index = 0

    def update(self, world_worldX):
        self.rect.x = self.worldX - world_worldX

    def advanceText(self):
        self.text_index += 1
        if self.text_index == len(self.text):
        # went through all the text
            self.displayingText = False
            self.doneReading = True
            self.text_index = 0