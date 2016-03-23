import pygame

pygame.init()

class HealPoint(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
    #kwargs has: rectY, worldX, healthPts, imageName, textDict
        super(HealPoint, self).__init__()
        self.image = pygame.image.load(kwargs["imageName"]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0 # this will change
        self.rect.y = kwargs["rectY"]
        self.worldX = kwargs["worldX"] # this is set

        self.healthPts = kwargs["healthPts"]

        self.talkedTo = False
        self.healed = False
        self.displayingText = False
        self.doneReading = False
        self.text = kwargs["textDict"]
        self.textToDisplay = None
        self.text_index = 0

    def update(self, world_worldX):
        self.rect.x = self.worldX - world_worldX

    def healPlayer(self, playerObj):
        if not self.healed:
            playerObj.heal(self.healthPts)
            self.healed = True

    def advanceText(self):
        self.text_index += 1
        if self.text_index == len(self.textToDisplay):
        # went through all the text
            self.displayingText = False
            self.doneReading = True
            self.text_index = 0
            self.talkedTo = True