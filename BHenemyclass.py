import pygame
import random, math
from BHbulletclasses import ForkBullet, KnifeBullet, OrangeBullet
from BHbulletclasses import StrawberryBullet, AppleBullet
from BHbulletclasses import LittleStarBullet, BigStarBullet
from BHbulletclasses import ShootingStarBullet, LaserBullet
from BHbulletclasses import BoneBullet, LittleBoneBullet, BigBoneBullet
from BHbulletclasses import TennisBallBullet

pygame.init()
GAMEFONT = pygame.font.Font("FreePixel.ttf", 20)

class BHEnemy(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
    # kwargs has: name, imageName, rectX, width, height, 
    # health, attacks, moveList, movingAttacks
        super(BHEnemy, self).__init__()

        self.name = kwargs["name"]
        self.image = pygame.image.load(kwargs["imageName"]).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = kwargs["rectX"]
        self.rect.y = 50
        self.tempx = self.rect.x
        self.tempy = self.rect.y
        self.width = kwargs["width"]
        self.height = kwargs["height"]
        self.cx = self.rect.x + self.width//2
        self.cy = self.rect.y + self.height//2

        self.dx = 0
        self.dy = 0

        self.bullets = pygame.sprite.Group()

        self.max_health = kwargs["health"]
        self.health = self.max_health
        self.health_lost = 0
        
        self.dead = False

        self.attackMode = 1
        self.attackTimer = 0
        self.totalAttacks = kwargs["attacks"]
        self.switchAttacks = 120 // self.totalAttacks * 60
        # ^ makes each enemy have total ~2 mins fight time

        self.bulletTimer = 0

        self.fps = 60
        self.moving = False
        self.movingAttacks = kwargs["movingAttacks"]
        self.moveList = kwargs["moveList"]
        self.moveListIndex = 0
        self.nextSpot = self.moveList[self.moveListIndex]
        self.moveCounter = 0
        self.time_to_move = 60

    def changeAttacks(self):
        self.health_lost = 0
        self.attackMode += 1
        self.attackTimer = 1

        if self.attackMode > self.totalAttacks:
            self.dead = True
        
        if self.attackMode in self.movingAttacks:
            self.moving = True
        else:
            self.moving = False

    def decreaseHealth(self):
        if not self.dead:
            self.health -= 1
            self.health_lost += 1

        if self.health_lost == self.max_health // self.totalAttacks:
            self.changeAttacks()
        
        if self.health == 0:
            self.dead = True

    def update(self):
        self.attackTimer += 1
        
        if self.attackTimer > self.switchAttacks:
            self.changeAttacks()

        self.bulletTimer += 1

        # move around
        if self.moving:
            self.moveCounter += 1    
            if self.moveCounter == self.time_to_move:
                self.moveCounter = 0
                self.goTo(self.nextSpot)
                self.moveListIndex += 1
                if self.moveListIndex == len(self.moveList):
                    self.moveListIndex = 0
                self.nextSpot = self.moveList[self.moveListIndex]
            self.tempx += self.dx
            self.tempy += self.dy
            self.rect.x = self.tempx
            self.rect.y = self.tempy
            self.cx = self.rect.x + self.width//2
            self.cy = self.rect.y + self.height//2

    def goTo(self, spot):
    # set dx and dy if moving
        x = spot[0]
        y = spot[1]
        self.dx = (x - self.rect.x) / self.fps
        self.dy = (y - self.rect.y) / self.fps

    def displayHealth(self, screen):
        healthtxt = GAMEFONT.render(self.name + ": HP " + 
            str(self.health) + "/" + str(self.max_health), 
            False, (255,255,255))
        screen.blit(healthtxt, (390, 40))

    def displayTimeLeft(self, screen):
        if not self.dead:
            timetxt = GAMEFONT.render(
                str((self.switchAttacks-self.attackTimer)//60), 
                False, (255,255,255))
            screen.blit(timetxt, (320, 10))

class Toast(BHEnemy):
    def __init__(self, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(**kwargs)
        ForkBullet.init()
        KnifeBullet.init()
        OrangeBullet.init()
        StrawberryBullet.init()
        AppleBullet.init()

        self.spiral_angle = 0
        self.spiral_Dtheta = 25
        # for attack #6

    def shootBullets(self, playerX, playerY):
        if self.attackTimer > 120: 
            if self.attackMode == 1:
                if self.bulletTimer % 20 == 0:
                    self.bulletTimer = 0
                    self.bullets.add(ForkBullet())
            elif self.attackMode == 2:
                if self.bulletTimer % 20 == 0:
                     self.bullets.add(ForkBullet())
                if self.bulletTimer % 40 == 0:
                    self.bulletTimer = 0
                    self.bullets.add(KnifeBullet(playerX, playerY, "left"), 
                        KnifeBullet(playerX, playerY, "right"))
            elif self.attackMode == 3:
                if self.bulletTimer % 20 == 0:
                    self.bulletTimer = 0
                    dir1 = random.choice(["left", "right"])
                    dir2 = random.choice(["up", "down"])
                    self.bullets.add(OrangeBullet("horizontal", dir1),
                        OrangeBullet("vertical", dir2))
            elif self.attackMode == 4:
                if self.bulletTimer % 45 == 0:
                    self.bullets.add(AppleBullet(self.cx, self.cy, playerX, playerY),
                        AppleBullet(self.cx, self.cy, playerX + 100, playerY),
                        AppleBullet(self.cx, self.cy, playerX - 100, playerY))
                if self.bulletTimer % 90 == 0:
                    self.bulletTimer = 0
                    dir1 = random.choice(["left", "right"])
                    self.bullets.add(OrangeBullet("horizontal", dir1, None, playerY, 1))
            elif self.attackMode == 5:
                if self.bulletTimer % 15 == 0:
                    for angle in range(self.spiral_angle, self.spiral_angle + 360, 30):
                        self.bullets.add(StrawberryBullet(self.cx, self.cy, angle%360))
                    self.spiral_angle = (self.spiral_angle+self.spiral_Dtheta) % 360
                if self.bulletTimer % 30 == 0:
                    self.bulletTimer = 0
                    self.bullets.add(OrangeBullet("vertical", "down", playerX))

class UFO(BHEnemy):
    def __init__(self, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(**kwargs)

        LittleStarBullet.init()
        BigStarBullet.init()
        ShootingStarBullet.init()
        LaserBullet.init()

        self.bigStarBullets = pygame.sprite.Group()
        
        self.ss_startAngle = 0
        self.ss_dthetas = [45, 60, 72, 90]
        # for attack #2

        self.g_startAngle = 0
        self.g_dtheta = 5
        # for attack #3
        # g stands for..galaxy lol

        self.cspiral_startAngle = 0
        self.cspiral_distance = 100
        # for attack #4

    def shootBullets(self, playerX, playerY):
        if self.attackTimer > 120:
            if self.attackMode == 1:
                if self.bulletTimer % 45 == 0:
                    self.bulletTimer = 0
                    newBullet = BigStarBullet(playerX, playerY)
                    self.bigStarBullets.add(newBullet)
                    self.bullets.add(newBullet)
                for star in self.bigStarBullets:
                    if star.dead == True:
                        for angle in range(0, 360, 30):
                            self.bullets.add(LittleStarBullet(star.cx, star.cy, 
                                angle))
            elif self.attackMode == 2:
                if self.bulletTimer % 75 == 0:
                    self.bulletTimer = 0
                    dtheta = random.choice(self.ss_dthetas)
                    for angle in range(self.ss_startAngle,self.ss_startAngle+360,dtheta):
                        self.bullets.add(ShootingStarBullet(playerX, playerY, angle))
                    self.ss_startAngle = (self.ss_startAngle + 30) % 360
            elif self.attackMode == 3:
                if self.bulletTimer % 12 == 0:
                    for starAngle in range(self.g_startAngle, self.g_startAngle+360,12):
                        self.bullets.add(LittleStarBullet(self.cx, self.cy, starAngle))
                    self.g_startAngle = (self.g_startAngle + self.g_dtheta) % 360
                if self.bulletTimer % 36 == 0:
                    self.bulletTimer = 0
                    for angle in range(self.g_startAngle+90, self.g_startAngle+180,15):
                        self.bullets.add(LaserBullet(self.cx, self.cy, angle))
                    for angle in range(self.g_startAngle+270, self.g_startAngle+360,15):
                        self.bullets.add(LaserBullet(self.cx, self.cy, angle))
            elif self.attackMode == 4:
            # this attack pattern was..not what i intended...
            # but its cool so im keeping it lol
                if self.bulletTimer % 8 == 0:
                    self.bulletTimer = 0
                    for angle in range(self.cspiral_startAngle, self.cspiral_startAngle + 360, 15):
                        cx = self.cx + math.cos(math.radians(angle))*self.cspiral_distance
                        cy = self.cy - math.sin(math.radians(angle))*self.cspiral_distance
                        self.bullets.add(LittleStarBullet(cx, cy, angle, 2))
                    self.cspiral_startAngle = (self.cspiral_startAngle + 6) % 360

class Dog(BHEnemy):
    def __init__(self, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(**kwargs)

        BoneBullet.init()
        LittleBoneBullet.init()
        BigBoneBullet.init()
        TennisBallBullet.init()

        self.startAngle = 0
        self.tennisBallDir = 1

        self.switchAttacks = 90 // self.totalAttacks * 60
        # make this level a little shorter since theres only 2 attacks

        self.boneTimer = 30
        self.decayRate = 0.95 # for boneTimer
        self.smallBoneFreq = [15,20,30,36,45,60]

    def shootBullets(self, playerX, playerY):
        if self.attackTimer > 120:
            if self.attackMode == 1:
                if self.bulletTimer >= self.boneTimer:
                    self.bulletTimer = 0
                    for angle in range(self.startAngle, self.startAngle+360, 10):
                        self.bullets.add(BoneBullet(self.cx, self.cy, angle))
                    self.bulletTimer = round(self.bulletTimer*self.decayRate)
                if self.bulletTimer % 30 == 0:
                    dtheta = random.choice(self.smallBoneFreq)
                    speed = random.randint(1, 5)
                    for angle in range(
                        self.startAngle, self.startAngle+360, dtheta):
                        self.bullets.add(LittleBoneBullet(self.cx, self.cy, angle, speed))
                    self.startAngle = (self.startAngle + 5) % 360   
            elif self.attackMode == 2:
                if self.bulletTimer % 6 == 0:
                    for angle in range(
                        self.startAngle, self.startAngle+360, 45):
                        self.bullets.add(BigBoneBullet(self.cx, self.cy, angle))
                    self.startAngle = (self.startAngle + 2) % 360
                if self.bulletTimer % 60 == 0:
                    self.bulletTimer = 0
                    for angle in range(0, 360, 30):
                        self.bullets.add(TennisBallBullet(self.cx, self.cy, 
                            angle, self.tennisBallDir))
                    self.tennisBallDir *= -1
                 
            


    