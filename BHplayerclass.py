import pygame
from BHbulletclasses import PlayerBullet

pygame.init()

GAMEFONT = pygame.font.Font("FreePixel.ttf", 20)

class BHPlayer(pygame.sprite.Sprite):
    UP_THRESH = 6 + 2
    DOWN_THRESH = 450 - 6 - 8 - 2
    LEFT_THRESH = 6 + 2
    RIGHT_THRESH = 350 - 6 - 8 - 2
    
    def __init__(self, health=80):
        PlayerBullet.init()

        super(BHPlayer, self).__init__()
        self.image = pygame.image.load("bh_p_hitbox.png").convert_alpha()
        self.sprite = pygame.image.load("bh_p_sprite.png").convert_alpha()
        self.sprite_f = pygame.image.load("bh_p_sprite_f.png").convert_alpha()
        self.sprite_inv = pygame.image.load("bh_p_sprite_inv.png").convert_alpha()
        self.sprite_f_inv = pygame.image.load("bh_p_sprite_f_inv.png").convert_alpha()
        self.spriteOffset = 6
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 175-4
        self.rect.y = 400-4
        self.cx = self.rect.x + 4
        self.cy = self.rect.y + 4
        self.dx = 0
        self.dy = 0

        self.focused = False

        self.invincible = False
        self.inv_counter = 0
        self.not_inv = 120

        self.dead = False
        self.health = health

        self.shooting = False

        self.bullets = pygame.sprite.Group()
        self.shootCounter = 0
        self.plsShoot = 8

    def changeSpeed(self, dx, dy):    
        self.dx += dx
        self.dy += dy

    def update(self):
        if self.focused:
            self.plsShoot = 6
            self.rect.x += self.dx
            if not BHPlayer.isLegal_X(self.rect.x):
                self.rect.x -= self.dx
            self.rect.y += self.dy
            if not BHPlayer.isLegal_Y(self.rect.y):
                self.rect.y -= self.dy
        else:
            self.plsShoot = 10
            self.rect.x += 2*self.dx
            if not BHPlayer.isLegal_X(self.rect.x):
                self.rect.x -= 2*self.dx
            self.rect.y += 2*self.dy
            if not BHPlayer.isLegal_Y(self.rect.y):
                self.rect.y -= 2*self.dy
        self.cx = self.rect.x + 4
        self.cy = self.rect.y + 4


    @staticmethod
    def isLegal_X(x):
        return (BHPlayer.LEFT_THRESH < x < BHPlayer.RIGHT_THRESH)

    @staticmethod
    def isLegal_Y(y):
         return (BHPlayer.UP_THRESH < y < BHPlayer.DOWN_THRESH)

    
    def shootBullets(self):
        if self.shooting:
            self.shootCounter += 1
            if self.shootCounter >= self.plsShoot:
                self.bullets.add(PlayerBullet(self.cx + 8, self.cy - 16), 
                    PlayerBullet(self.cx - 8, self.cy - 16))
                self.shootCounter = 0

    def beInvincible(self):
        if self.invincible:
            self.inv_counter += 1
            if self.inv_counter == self.not_inv:
                self.inv_counter = 0
                self.invincible = False

    def decreaseHealth(self):
        if not self.invincible:
            if self.health > 5:
                self.health -= 5
            elif self.health == 5: 
                self.health = 1
            elif self.health == 1: 
                self.health = 0 
                self.dead = True
            self.invincible = True

    def drawSprite(self, screen):
        # draws the player image over the hitbox
        if not self.invincible:
            if self.focused:
                screen.blit(self.sprite_f, 
                    (self.rect.x - self.spriteOffset, 
                    self.rect.y - self.spriteOffset))
            else:
                screen.blit(self.sprite, 
                    (self.rect.x - self.spriteOffset, 
                    self.rect.y - self.spriteOffset))
        else:
            if self.focused:
                screen.blit(self.sprite_f_inv, 
                    (self.rect.x - self.spriteOffset, 
                    self.rect.y - self.spriteOffset))
            else:
                screen.blit(self.sprite_inv, 
                    (self.rect.x - self.spriteOffset, 
                    self.rect.y - self.spriteOffset))

    def displayHealth(self, screen):
        healthtxt = GAMEFONT.render("CUBE: HP " + str(self.health) + "/100", 
            False, (255,255,255))
        screen.blit(healthtxt, (390, 20))






