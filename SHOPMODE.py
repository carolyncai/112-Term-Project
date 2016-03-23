import pygame
import random
from BHwallclass import Wall
from BHplayerclass import BHPlayer
from BHbulletclasses import FoodItem

GAMEFONT = pygame.font.Font("FreePixel.ttf", 20)

class ShopMode(object):
# hm...this is different enough from BHMode 
# that i dont think inheriting would really do anything...
# since i'd have to rewrite half the stuff anyway...

    @staticmethod
    def init():
        ShopMode.bg = pygame.image.load("bh_bg.png")
        ShopMode.sidepanel = pygame.image.load("bh_sidepanel.png")
        ShopMode.walls = pygame.sprite.Group()
        ShopMode.walls.add(Wall(-100,-100,550,-102),
            Wall(-102,-100,-100,550), 
            Wall(550,-100,452,550),
            Wall(-100,550,450,552))

    def __init__(self, playerHealth=100):
        FoodItem.init()

        self.inShopMode = False
        self.completed = False
        self.out_of_money = False # or out of time

        self.walls = ShopMode.walls

        self.bg = ShopMode.bg
        self.sidepanel = ShopMode.sidepanel

        self.player = BHPlayer(playerHealth)
        self.players = pygame.sprite.Group()
        self.players.add(self.player)

        self.player_moneyLeft = 20.00
        self.player_itemCount = {
            "MILK": 0,
            "SODA": 0,
            "CHIP": 0,
            "CEREAL": 0,
            "NOODLE": 0
        }

        self.foodItems = pygame.sprite.Group()
        self.food_xRange = range(50, 350, 50)

        self.bulletTimer = 0

        self.timer = 1
        self.timedOut = 60 * 30 # 30 seconds play time

        self.completionCounter = 0
        self.completionCount = 180

    def keyPressed(self, keyCode, modifier):
        if keyCode == pygame.K_LSHIFT:
            self.player.focused = True
        elif keyCode == pygame.K_z:
            self.player.shooting = True
        elif keyCode == pygame.K_LEFT:
            self.player.changeSpeed(-3,0)
        elif keyCode == pygame.K_RIGHT:
            self.player.changeSpeed(+3,0)
        elif keyCode == pygame.K_UP:
            self.player.changeSpeed(0,-3)
        elif keyCode == pygame.K_DOWN:
            self.player.changeSpeed(0,+3)

    def keyReleased(self, keyCode, modifier):
        if keyCode == pygame.K_LSHIFT:
            self.player.focused = False
        elif keyCode == pygame.K_z:
            self.player.shooting = False
        elif keyCode == pygame.K_LEFT:
            self.player.changeSpeed(+3,0)
        elif keyCode == pygame.K_RIGHT:
            self.player.changeSpeed(-3,0)
        elif keyCode == pygame.K_UP:
            self.player.changeSpeed(0,+3)
        elif keyCode == pygame.K_DOWN:
            self.player.changeSpeed(0,-3)

    def timerFired(self, dt):
        self.timer += 1
        if not self.out_of_money:
            self.bulletTimer += 1
            if self.bulletTimer % 20 == 0:
                self.bulletTimer = 0
                foodx = random.choice(self.food_xRange)
                self.foodItems.add(FoodItem(foodx))

            # get rid of offscreen food items & playerbullets
            pygame.sprite.groupcollide(
                    self.foodItems, self.walls, True, False)
            pygame.sprite.groupcollide(
                    self.player.bullets, self.walls, True, False)

            player_foods_collided = pygame.sprite.spritecollide(
                self.player, self.foodItems, True, pygame.sprite.collide_mask)

            for foodItem in player_foods_collided:
                foodName = foodItem.name
                self.player_itemCount[foodName] += 1
                self.player_moneyLeft = max(self.player_moneyLeft-foodItem.cost, 0)

            if self.player_moneyLeft <= 0:
                self.out_of_money = True

            if self.timer >= self.timedOut:
                self.completed = True

        elif self.out_of_money:
            self.completionCounter += 1
            if (self.completionCounter >= self.completionCount or
                self.timer >= self.timedOut):
                self.completed = True

        self.players.update()
        self.player.bullets.update()

        self.foodItems.update()

    def displayText(self, screen):
        playerHP = GAMEFONT.render("CUBE: HP Infty/100", False, (255,255,255))
        player_money = GAMEFONT.render("MONEY LEFT: %0.2f" % self.player_moneyLeft,
            False, (255,255,255))
        foodsBought = GAMEFONT.render("FOODS BOUGHT:", False, (255,255,255))
        milks = GAMEFONT.render("MILK:    %d" % self.player_itemCount["MILK"], 
            False, (255,255,255))
        sodas = GAMEFONT.render("SODA:    %d" % self.player_itemCount["SODA"], 
            False, (255,255,255))
        chisps = GAMEFONT.render("CHIPS:   %d" % self.player_itemCount["CHIP"], 
            False, (255,255,255))
        cornflakes = GAMEFONT.render("CEREAL:  %d" % self.player_itemCount["CEREAL"],
            False, (255,255,255))
        ramens = GAMEFONT.render("NOODLES: %d" % self.player_itemCount["CEREAL"],
            False, (255,255,255))
        time = (self.timedOut - self.timer) // 60
        timetxt = GAMEFONT.render(str(time), False, (255,255,255))

        screen.blit(playerHP, (390,20))
        screen.blit(player_money, (390,60))
        screen.blit(foodsBought, (390,100))
        screen.blit(milks, (390, 140))
        screen.blit(sodas, (390, 160))
        screen.blit(chisps, (390, 180))
        screen.blit(cornflakes, (390, 200))
        screen.blit(ramens, (390, 220))
        screen.blit(timetxt, (320,10))

    def redrawAll(self, screen):
        screen.blit(self.bg, (0,0))
            
        self.player.bullets.draw(screen)
        self.players.draw(screen)
        self.player.drawSprite(screen)
        self.foodItems.draw(screen)

        screen.blit(self.sidepanel, (350,0))
        self.displayText(screen)







