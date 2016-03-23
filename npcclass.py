import pygame

pygame.init()

class NPC(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        #kwargs has: rectY, worldX, imageName, textDictM, textDictD
        super(NPC, self).__init__()
        self.hasBH = False

        self.image = pygame.image.load(kwargs["imageName"]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 650 # set this in update
        self.rect.y = kwargs["rectY"]
        self.worldX = kwargs["worldX"]

        self.talkedTo = False
        self.placated = False
        self.movedOutOfWay = False
        
        self.displayingText = False
        self.doneReading = False
        self.mean_text = kwargs["textDictM"]
        self.docile_text = kwargs["textDictD"]
        self.text = self.mean_text
        self.textToDisplay = None
        self.text_index = 0

    def update(self, world_worldX):
        self.rect.x = self.worldX - world_worldX

    def advanceText(self):
        self.text_index += 1
        if self.text_index == len(self.textToDisplay):
        # went through all the text
            self.displayingText = False
            self.doneReading = True
            self.text_index = 0
            if self.placated:
                self.talkedTo = True

    def becomeNice(self):
        self.placated = True
        self.text = self.docile_text

    def moveOutOfWay(self):
        if self.movedOutOfWay == False:
            self.rect.y -= 20
            self.movedOutOfWay = True

