import pygame

pygame.init()

GAMEFONT = pygame.font.Font("FreePixel.ttf", 20)

class Player(pygame.sprite.Sprite):
# screen is 600 width 450 height
# player motion from programarcadegames.com --> move_sprite_keyboard_smooth.py
    left_thresh = 220
    right_thresh = 270
    FLAVORTEXT = { 80:  ["(It's the start of an exciting journey!)",
                         "(...)",
                         "(...Huh? You hear a voice from above...)",
                         "('Press 'Z' to interact with objects!')"],
                   600: ["(Seems like someone is up ahead!)",
                         "(You wonder what they have to say.)"],
                   1600:["(You notice some cutlery on the ground.)",
                         "(As well as a bunch of squished fruits.)",
                         "(How sad...)"],
                   3100:["(Colorful plastic stars litter the ground.)",
                         "(You step over them carefully.)"],
                   5372: ["(You look around for the chew toys.)",
                          "(You don't see anything...)",
                          "(Maybe they all reburied themselves??)"]}
    SEENTEXT = set()

    def __init__(self, health=50):
        super(Player, self).__init__()
        self.image_R1 = pygame.image.load("cube.png").convert_alpha()
        self.image_R2 = pygame.image.load("cube_squish.png").convert_alpha()
        self.image_RS = pygame.image.load("cube_supersquish.png").convert_alpha()
        self.image_RT = pygame.image.load("cube_tall.png").convert_alpha()
        self.image_L1 = pygame.transform.flip(self.image_R1, True, False)
        self.image_L2 = pygame.transform.flip(self.image_R2, True, False)
        self.image_LS = pygame.transform.flip(self.image_RS, True, False)
        self.image_LT = pygame.transform.flip(self.image_RT, True, False)
        self.image = self.image_R1
        self.imgTXT = "r1"
        self.rect = self.image_R1.get_rect()
        # rect.x is relative to the screen! not the world
        self.rect.x = 40
        self.rect.y = 250
        self.dx = 0
        self.dy = 0
        self.facingRight = True
        self.moving = False
        self.displayingText = False
        self.textToDisplay = None # this is a list
        self.text_index = 0 # index of text line in textToDisplay
        self.speed = 2
        self.health = health
        self.max_health = 100
        self.animate_timer = 0
        self.plsanimate = 10

    def animate(self):
        if self.moving:
            self.animate_timer += 1
            if self.animate_timer == self.plsanimate:
                if self.facingRight:
                    if self.imgTXT == "r2":
                        self.imgTXT = "r1"
                        self.image = self.image_R1
                    else:
                        self.imgTXT = "r2"
                        self.image = self.image_R2
                else:
                    if self.imgTXT == "l2":
                        self.imgTXT = "l1"
                        self.image = self.image_L1
                    else:
                        self.imgTXT = "l2"
                        self.image = self.image_L2
                self.animate_timer = 0

    def unanimate(self):
        if self.facingRight:
            self.image = self.image_R1
            self.imgTXT = "r1"
        else:
            self.image = self.image_L1
            self.imgTXT = "l1"

    def squish(self):
        if self.facingRight and not self.moving:
            self.image = self.image_RS
        elif not self.facingRight and not self.moving:
            self.image = self.image_LS

    def unsquish(self):
        if self.facingRight and not self.moving:
            self.image = self.image_RT
        elif not self.facingRight and not self.moving:
            self.image = self.image_LT

    def changeSpeed(self, dx, dy):
        if dx < 0:
            self.dx -= self.speed
        elif dx > 0:
            self.dx += self.speed
    
    def update(self):
        self.rect.x += self.dx

    def heal(self, healthPts):
        self.health = min(self.health + healthPts, self.max_health)

    def displayHealth(self, screen):
        healthtxt = GAMEFONT.render("HEALTH: " + str(self.health) + "/100", 
            False, (60,54,115)) # same color as bushes in the bg
        screen.blit(healthtxt, (430, 10))

    def advanceText(self):
        self.text_index += 1
        if self.text_index == len(self.textToDisplay):
        # went through all the text
            self.displayingText = False
            self.text_index = 0