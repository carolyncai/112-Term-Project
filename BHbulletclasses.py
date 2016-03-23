import pygame
import random, math

pygame.init()

class PlayerBullet(pygame.sprite.Sprite):
# blue squares that move upwards
    SIZE = 4
    COLOR = (144,180,212)
    
    @staticmethod
    def init():
        PlayerBullet.image = pygame.Surface(
            (PlayerBullet.SIZE, PlayerBullet.SIZE))
        PlayerBullet.image.fill(PlayerBullet.COLOR)

    def __init__(self, cx, cy):
        super(PlayerBullet, self).__init__()

        self.image = PlayerBullet.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect.x = cx - PlayerBullet.SIZE//2
        self.rect.y = cy - PlayerBullet.SIZE//2

        self.dy = 8

    def update(self):
        self.rect.y -= self.dy


class ForkBullet(pygame.sprite.Sprite):
# fall down from top.   
    @staticmethod
    def init():
        fork1 = pygame.image.load("bh_fork.png").convert_alpha()
        fork2 = pygame.transform.flip(fork1, True, False)
        ForkBullet.images = [fork1, fork2]
    
    def __init__(self):
        super(ForkBullet, self).__init__()
        self.image = random.choice(ForkBullet.images)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 330)
        self.rect.y = -10
        self.dy = random.randint(2, 4)

    def update(self):
        self.rect.y += self.dy


class KnifeBullet(pygame.sprite.Sprite):
# these follow the player ...with the naive angular movement oh well   
    @staticmethod
    def init():
        knife1 = pygame.image.load("bh_knife.png").convert_alpha()
        knife2 = pygame.transform.flip(knife1, True, False)
        KnifeBullet.images = [knife1, knife2]
    
    def __init__(self, playerX, playerY, side):
        super(KnifeBullet, self).__init__()
        x = 50 if side == "left" else 300
        y = -10

        self.dy = random.randint(4, 6)
        self.dx = math.atan((playerX - x) / (playerY - y))
        self.dx /= (math.pi/2)
        self.dx *= self.dy

        angle = math.atan(self.dx / self.dy) * (180 / math.pi)
        self.image = random.choice(KnifeBullet.images)
        self.image = pygame.transform.rotate(self.image, angle)

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy


class OrangeBullet(pygame.sprite.Sprite):
# these sweep across screen
    @staticmethod
    def init():
        slice1 = pygame.image.load("bh_orange.png").convert_alpha()
        slice2 = pygame.transform.flip(slice1, True, False)
        OrangeBullet.images = [slice1, slice2]

    def __init__(self, orientation, direction, 
        startX=None, startY=None, speed=3):
        super(OrangeBullet, self).__init__()
        self.image = random.choice(OrangeBullet.images)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        if orientation == "horizontal":
            if direction == "right":
                self.rect.x = -30
                self.dx = speed
            elif direction == "left":
                self.rect.x = 350
                self.dx = -1 * speed
            self.rect.y = random.randint(10, 410) if startY == None else startY
            self.dy = 0
        elif orientation == "vertical":
            if direction == "up":
                self.rect.y = 450
                self.dy = -1 * speed
            elif direction == "down":
                self.rect.y = -30
                self.dy = speed
            self.rect.x = random.randint(10, 310) if startX == None else startX
            self.dx = 0

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

class CircularBullet(pygame.sprite.Sprite):
# bullets that go at an angle...in a circle
# superclass for some bullet types.
    def __init__(self, cx, cy):
        super(CircularBullet, self).__init__()
        # self.image is set
        # self.angle is set
        # self.speed is set
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        w, h = self.image.get_size()
        self.rect.x = cx - w // 2
        self.rect.y = cy - h // 2
        self.tempx = self.rect.x
        self.tempy = self.rect.y
        # fixed the angle issue!!!
        # rect.x and rect.y round every time u update them
        # but tempx and tempy wont do that so it's all good

        self.dx = self.speed * math.cos(math.radians(self.angle))
        self.dy = self.speed * math.sin(math.radians(self.angle))

    def update(self):
        self.tempx += self.dx
        self.tempy += self.dy
        self.rect.x = self.tempx
        self.rect.y = self.tempy


class StrawberryBullet(CircularBullet):
    @staticmethod
    def init():
        StrawberryBullet.image = pygame.image.load("bh_strawberry.png").convert_alpha()

    def __init__(self, cx, cy, angle):
    # angle is in degrees
        pygame.sprite.Sprite.__init__(self)
        self.angle = angle
        self.speed = 6
        self.baseImage = StrawberryBullet.image
        self.image = pygame.transform.rotate(self.baseImage, -1 * self.angle)
        super().__init__(cx, cy)


class AppleBullet(pygame.sprite.Sprite):
# follows player 
    @staticmethod
    def init():
        AppleBullet.image = pygame.image.load("bh_apple.png").convert_alpha()

    def __init__(self, cx, cy, playerX, playerY):
    # if i were to inherit this...then wouldnt the images and masks and rects
    # be messed up... :o
    # angle is in degrees
        super(AppleBullet, self).__init__()
        self.image = AppleBullet.image
        
        self.dy = 5
       
        self.dx = math.atan((playerX - cx) / (playerY - cy))
        self.dx /= (math.pi/2)
        self.dx *= self.dy

        angle = math.atan(self.dx / self.dy) * (180 / math.pi) 
        self.image = pygame.transform.rotate(self.image, angle)

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        w, h = self.image.get_size()
        self.rect.x = cx - w / 2
        self.rect.y = cy - h / 2
        self.tempx = self.rect.x
        self.tempy = self.rect.y
    
    def update(self):
        self.tempx += self.dx
        self.tempy += self.dy
        self.rect.x = self.tempx
        self.rect.y = self.tempy

class LittleStarBullet(pygame.sprite.Sprite):
# spin in a circle
    @staticmethod
    def init():
        LittleStarBullet.images = []
        for starNum in range(0,7):
            imgName = "bh_little_star%d.png" % starNum
            img = pygame.image.load(imgName).convert_alpha()
            LittleStarBullet.images.append(img)

    def __init__(self, cx, cy, angle=0, speed=3):
    # angle is in degrees
        super(LittleStarBullet, self).__init__()
        self.image = random.choice(LittleStarBullet.images)
        self.baseImage = self.image.copy()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.cx = cx
        self.cy = cy
        self.tempcx = self.cx
        self.tempcy = self.cy
        w, h = self.image.get_size()
        self.rect.x = self.cx - w/2
        self.rect.y = self.cy - h/2

        self.speed = speed

        self.angle = angle
        self.dx = self.speed * math.cos(math.radians(self.angle))
        self.dy = self.speed * math.sin(math.radians(self.angle))

    def updateRect(self):
        # update the object's rect attribute with the new x,y coordinates
        # from 112 pygame lecture online examples (Lukas Peraza)
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.cx - w / 2, self.cy - h / 2, w, h)

    def update(self):
        self.angle = (self.angle + 2) % 360
        self.image = pygame.transform.rotate(self.baseImage, self.angle)
        self.mask = pygame.mask.from_surface(self.image)
        
        self.tempcx += self.dx
        self.tempcy += self.dy
        self.cx = self.tempcx
        self.cy = self.tempcy
        self.updateRect()

class BigStarBullet(pygame.sprite.Sprite):
# falls down to where player is then explodes into little stars
    @staticmethod
    def init():
        BigStarBullet.images = []
        for starNum in range(0,7):
            imgName = "bh_big_star%d.png" % starNum
            img = pygame.image.load(imgName).convert_alpha()
            BigStarBullet.images.append(img)

    def __init__(self, startX, endY):
    # angle is in degrees
        super(BigStarBullet, self).__init__()
        self.image = random.choice(BigStarBullet.images)
        self.baseImage = self.image.copy()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = startX - 25
        self.rect.y = 0

        self.angle = 0

        self.endY = endY
        self.cx = startX
        self.cy = self.rect.y + 25

        self.speed = 6

        self.dead = False

    def updateRect(self):
        # update the object's rect attribute with the new x,y coordinates
        # from 112 pygame lecture online examples (Lukas Peraza)
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.cx - w / 2, self.cy - h / 2, w, h)

    def update(self):
        self.angle = (self.angle + 10) % 360
        self.image = pygame.transform.rotate(self.baseImage, self.angle)
        self.mask = pygame.mask.from_surface(self.image)
        
        self.cy += self.speed
        self.updateRect()

        if self.cy >= self.endY and not self.dead:
            self.dead = True
        elif self.cy >= self.endY and self.dead:
            self.kill()

class ShootingStarBullet(pygame.sprite.Sprite):
# circles around player then moves toward them
    @staticmethod
    def init():
        ShootingStarBullet.image = pygame.image.load("bh_shootingstar.png").convert_alpha()

    def __init__(self, player_cx, player_cy, angle):
        super(ShootingStarBullet, self).__init__()
        self.angle = angle
        self.baseImage = ShootingStarBullet.image
        self.image = pygame.transform.rotate(self.baseImage, self.angle)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.player_cx = player_cx
        self.player_cy = player_cy
        self.dist_from_player = 100
        self.cx = player_cx + math.cos(math.radians(self.angle))*self.dist_from_player
        self.cy = player_cy - math.sin(math.radians(self.angle))*self.dist_from_player
        self.tempcx = self.cx
        self.tempcy = self.cy 

        self.dtheta = 2
        self.rotationCounter = 0
        self.stop_rotating = 30

        w, h = self.image.get_size()
        self.rect.x = self.cx - w / 2
        self.rect.y = self.cy - h / 2
        self.tempx = self.rect.x
        self.tempy = self.rect.y

        self.speed = 4

    def updateRect(self):
        # update the object's rect attribute with the new x,y coordinates
        # from 112 pygame lecture online examples (Lukas Peraza)
        # should prob have inherited this but ohhh well
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.cx - w / 2, self.cy - h / 2, w, h)

    def update(self):
        if self.rotationCounter < self.stop_rotating:
            self.rotationCounter += 1
            self.dist_from_player += 1
            self.angle += self.dtheta
            self.tempcx = self.player_cx + math.cos(math.radians(self.angle))*self.dist_from_player
            self.tempcy = self.player_cy - math.sin(math.radians(self.angle))*self.dist_from_player
            self.cx = self.tempcx
            self.cy = self.tempcy
            self.image = pygame.transform.rotate(self.baseImage, self.angle)
            self.mask = pygame.mask.from_surface(self.image)
            self.updateRect()
        elif self.rotationCounter == self.stop_rotating:
            self.rotationCounter += 1
            self.dx = -1 * self.speed * math.cos(math.radians(self.angle))
            self.dy = +1 * self.speed * math.sin(math.radians(self.angle))
            self.tempx = self.rect.x
            self.tempy = self.rect.y
        else:
            self.tempx += self.dx
            self.tempy += self.dy
            self.rect.x = self.tempx
            self.rect.y = self.tempy
        

class SpiralBullet(pygame.sprite.Sprite):
# bullets that spiral around.
# superclass for some bullet types.
    def __init__(self, centerX, centerY):
        super(SpiralBullet, self).__init__()
        # self.angle, self.dtheta, self.speed, self.image, self.baseImage 
        # are set
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.centerx = centerX
        self.centery = centerY
        # point around which this thing orbits

        self.cx = self.centerx
        self.cy = self.centery
        self.tempcx = self.cx
        self.tempcy = self.cy

        w, h = self.image.get_size()
        self.rect.x = self.cx - w/2
        self.rect.y = self.cy - h/2

        self.radius = 0

    def updateRect(self):
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.cx - w / 2, self.cy - h / 2, w, h)

    def update(self):
        self.angle += self.dtheta
        self.radius += self.speed
        self.tempcx = self.centerx + math.cos(math.radians(self.angle))*self.radius
        self.tempcy = self.centery - math.sin(math.radians(self.angle))*self.radius
        self.cx = self.tempcx
        self.cy = self.tempcy
        self.image = pygame.transform.rotate(self.baseImage, self.angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.updateRect()


class LaserBullet(SpiralBullet):
# spirals
    @staticmethod
    def init():
        LaserBullet.image = pygame.image.load("bh_laser.png").convert_alpha()

    def __init__(self, centerX, centerY, angle):
        pygame.sprite.Sprite.__init__(self)
        self.angle = angle
        self.dtheta = 0.2
        self.speed = random.randint(2,4)
        self.baseImage = LaserBullet.image
        self.image = pygame.transform.rotate(self.baseImage,self.angle)
        super().__init__(centerX, centerY)
        

class LittleBoneBullet(CircularBullet):
# just circular
    @staticmethod
    def init():
        LittleBoneBullet.image = pygame.image.load("bh_tinybone.png").convert_alpha()

    def __init__(self, cx, cy, angle, speed=2):
        pygame.sprite.Sprite.__init__(self)
        self.angle = angle
        self.speed = speed
        self.image = pygame.transform.rotate(LittleBoneBullet.image, -1 * self.angle)
        super().__init__(cx, cy)
        

class BigBoneBullet(CircularBullet):
# same as little bone
    @staticmethod
    def init():
        BigBoneBullet.image = pygame.image.load("bh_bigbone.png").convert_alpha()

    def __init__(self, cx, cy, angle, speed=8):
        pygame.sprite.Sprite.__init__(self)
        self.angle = angle
        self.image = pygame.transform.rotate(BigBoneBullet.image, -1*self.angle)
        self.speed = speed
        super().__init__(cx, cy)


class BoneBullet(pygame.sprite.Sprite):
# moves forward then backward..in a circle
    @staticmethod
    def init():
        BoneBullet.image = pygame.image.load("bh_bone.png").convert_alpha()

    def __init__(self, cx, cy, angle):
        super(BoneBullet, self).__init__()
        self.angle = angle
        self.image = pygame.transform.rotate(BoneBullet.image, -1*self.angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        w, h = self.image.get_size()
        self.rect.x = cx - w/2
        self.rect.y = cy - h/2
        self.tempx = self.rect.x
        self.tempy = self.rect.y

        self.moveCount = 0
        self.moveBackwards = 20

        self.speed = 3
        self.dx = self.speed * math.cos(math.radians(self.angle))
        self.dy = self.speed * math.sin(math.radians(self.angle))

    def move(self):
        self.tempx += self.dx
        self.tempy += self.dy
        self.rect.x = self.tempx
        self.rect.y = self.tempy

    def update(self):
        if self.moveCount < self.moveBackwards:
            self.moveCount += 1
            self.move()
        elif self.moveCount == self.moveBackwards:
            self.moveCount += 1
            self.dx *= -1
            self.dy *= -1
        else:
            self.move()

class TennisBallBullet(SpiralBullet):
# spirals
    @staticmethod
    def init():
        TennisBallBullet.image = pygame.image.load("bh_tennisball.png").convert_alpha()

    def __init__(self, centerX, centerY, angle, direction):
    # direction = direction of rotation = + or - 1
        pygame.sprite.Sprite.__init__(self)
        self.angle = angle
        self.dtheta = 1 * direction
        self.speed = 1
        self.image = pygame.transform.rotate(TennisBallBullet.image,self.angle)
        self.baseImage = self.image.copy()
        super().__init__(centerX, centerY)


class FoodItem(pygame.sprite.Sprite):
# falls straight down
    @staticmethod
    def init():
    # there are several types of food items.
     FoodItem.itemNames = ["MILK", "SODA", "CHIP", "CEREAL", "NOODLE"]
     milk = pygame.image.load("shop_milk.png").convert_alpha()
     soda = pygame.image.load("shop_soda.png").convert_alpha()
     chisp = pygame.image.load("shop_chip.png").convert_alpha()
     cereal = pygame.image.load("shop_cereal.png").convert_alpha()
     noodle = pygame.image.load("shop_ramen.png").convert_alpha()
     FoodItem.itemInfo = { # "itemname": [image, cost]
        "MILK": [milk, 0.50],
        "SODA": [soda, 0.75],
        "CHIP": [chisp, 0.25],
        "CEREAL": [cereal, 1.00],
        "NOODLE": [noodle, 0.50]
        }

    def __init__(self, cx):
        super(FoodItem, self).__init__()
        self.name = random.choice(FoodItem.itemNames)
        self.image = FoodItem.itemInfo[self.name][0]
        self.cost = FoodItem.itemInfo[self.name][1]
        self.rect = self.image.get_rect()
        width, height = self.image.get_size()
        self.rect.x = cx - width/2
        self.rect.y = 0 - height

        self.dy = random.randint(3,8)

    def update(self):
        self.rect.y += self.dy

class Raindrop(pygame.sprite.Sprite):
# for use in RPG mode when its raining
    @staticmethod
    def init():
        Raindrop.image = pygame.image.load("actual_raindrop.png").convert_alpha()
        Raindrop.x_choices = range(0, 600, 10)

    def __init__(self):
        super(Raindrop, self).__init__()
        self.image = Raindrop.image
        self.rect = self.image.get_rect()
        self.rect.x = random.choice(Raindrop.x_choices)
        self.rect.y = -20
        self.dy = 6
        self.endY = random.randint(450-150-20, 450-20-10)

    def update(self, worldX_dx):
        self.rect.y += self.dy
        self.rect.x -= worldX_dx
        if self.rect.y >= self.endY:
            self.kill()






