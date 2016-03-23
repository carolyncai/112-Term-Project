import pygame

pygame.init()

GAMEFONT = pygame.font.Font("FreePixel.ttf", 20)

class Textbox(pygame.sprite.Sprite): 
    def __init__(self):
        super(Textbox, self).__init__()
        self.image = pygame.image.load("textbox.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 350

    # i didnt realize u could call a class method within a class...whoops
    # whatever thats ok
    @staticmethod
    def displayText(screen, words):
        text = GAMEFONT.render(words, False, (255,255,255))
        txtRect = text.get_rect()
        txtRect.x = 40
        txtRect.y = 390
        screen.blit(text, txtRect)

    @staticmethod
    def displayTextBox(screen, txtBoxGrp, words):
        txtBoxGrp.draw(screen)
        Textbox.displayText(screen, words)
