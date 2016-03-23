# no music ver.

import pygame
from BHwallclass import Wall
from BHplayerclass import BHPlayer
from BHenemyclass import BHEnemy, Toast, UFO, Dog

BLACK = (0,0,0)
WHITE = (255,255,255)
GAMEFONT = pygame.font.Font("FreePixel.ttf", 20)

class BHMode(object):

    @staticmethod
    def init():
        BHMode.gameOverScreen = pygame.image.load("gameOverScreen.png")
        BHMode.blackScreen = pygame.image.load("black_screen.png").convert()
        BHMode.bg = pygame.image.load("bh_bg.png")
        BHMode.sidepanel = pygame.image.load("bh_sidepanel.png")
        BHMode.walls = pygame.sprite.Group()
        BHMode.walls.add(Wall(-100,-100,550,-102),
            Wall(-102,-100,-100,550), 
            Wall(550,-100,452,550),
            Wall(-100,550,450,552))
        # 4 walls...my current jam.....

    def __init__(self, playerHealth=50):
        #self.music = pygame.mixer.Sound("ACNL_8am.wav")
        self.gameOverScreen = BHMode.gameOverScreen
        self.gameOver = False
        self.wait_until_game_over = 0

        self.paused = False

        self.completed = False
        
        self.walls = BHMode.walls

        self.bg = BHMode.bg
        self.sidepanel = BHMode.sidepanel

        self.player = BHPlayer(playerHealth)
        self.playerList = pygame.sprite.Group()
        self.playerList.add(self.player)

        self.bombsLeft = 4

        self.enemy = Toast(name="TOAST", imageName="bh_toast.png", 
            rectX=350//2-40, height=80, width=80, health=800, attacks=5,
            moveList = [(128,54),(114,32),(146,58),(124,40),(140,50),
                        (134,46),(140,60),(120,34),(152,60),(126,48)],
            movingAttacks=[5])
        self.enemies = pygame.sprite.Group()
        self.enemies.add(self.enemy)

        self.completionCounter = 0
        self.completionCount = 180

        self.blackScreen = BHMode.blackScreen
        self.fadeAlpha = 255
        self.fading = False

    def fade(self, screen):
    # ahaha its the same fade from the main....but....
    # since im switching modes IN here.....
    # hhhhaha.....
        if self.fadeAlpha < 0:
            self.fading = False
            self.fadeAlpha = 255
        else:
            self.blackScreen.set_alpha(self.fadeAlpha)
            screen.blit(self.blackScreen, (0,0))
            self.fadeAlpha -= 15

    def setPlayerHealth(self, health):
        self.player.health = health

    def keyPressed(self, keyCode, modifier):
        if not self.gameOver:
            if not self.paused:
                if keyCode == pygame.K_LSHIFT:
                    self.player.focused = True
                elif keyCode == pygame.K_z:
                    self.player.shooting = True
                elif keyCode == pygame.K_x:
                    self.bomb()
                elif keyCode == pygame.K_LEFT:
                    self.player.changeSpeed(-3,0)
                elif keyCode == pygame.K_RIGHT:
                    self.player.changeSpeed(+3,0)
                elif keyCode == pygame.K_UP:
                    self.player.changeSpeed(0,-3)
                elif keyCode == pygame.K_DOWN:
                    self.player.changeSpeed(0,+3)
                elif keyCode == pygame.K_p:
                    self.paused = True
                    self.player.focused = False
                    self.player.shooting = False
            elif self.paused:
                if keyCode == pygame.K_p:
                    self.paused = False
        else:
            if keyCode == pygame.K_z:
                self.__init__()
                self.fading = True

    def keyReleased(self, keyCode, modifier):
        if not self.gameOver and not self.paused:
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

    def bomb(self):
        if self.bombsLeft > 0:
            self.enemy.bullets.empty()
            self.bombsLeft -= 1

    def timerFired(self, dt):
        if not self.paused:
            if not self.player.dead:
                # check if player ran into enemy
                player_enemy_collided = pygame.sprite.groupcollide(
                    self.playerList, self.enemies, False, False, 
                    pygame.sprite.collide_mask)
                
                if player_enemy_collided != {}:
                    self.player.decreaseHealth()

                # get rid of offscreen bullets
                pygame.sprite.groupcollide(
                    self.enemy.bullets, self.walls, True, False)
                pygame.sprite.groupcollide(
                    self.player.bullets, self.walls, True, False)

                # check if player ran into bullets
                player_bullets_collided = pygame.sprite.spritecollide(
                    self.player, self.enemy.bullets, False, pygame.sprite.collide_mask)

                if player_bullets_collided != []:
                    self.player.decreaseHealth()

                # check if player shot enemy
                enemy_bullets_collided = pygame.sprite.spritecollide(
                    self.enemy, self.player.bullets, True)

                for hit in enemy_bullets_collided:
                    self.enemy.decreaseHealth()

                # make everyone shoot
                self.enemy.shootBullets(self.player.cx, self.player.cy)
                self.player.shootBullets()

                # update some stuff
                self.player.beInvincible()
                self.playerList.update()
                self.player.bullets.update()

                self.enemies.update()
                self.enemy.bullets.update()

                if self.enemy.dead:
                    self.completionCounter += 1
                    if self.completionCounter == self.completionCount:
                        self.completed = True

            elif self.player.dead and not self.gameOver: 
            # pause the screen
                self.wait_until_game_over += 1
                if self.wait_until_game_over >= 60:
                    self.fading = True
                    self.gameOver = True

    def displayInstructions(self, screen):
        txt1 = GAMEFONT.render("ARROW KEYS: move", 
            False, (255,255,255))
        screen.blit(txt1, (390, 200))
        txt2 = GAMEFONT.render("SHIFT: focus", 
            False, (255,255,255))
        screen.blit(txt2, (390, 220))
        txt3 = GAMEFONT.render("Z: shoot", 
            False, (255,255,255))
        screen.blit(txt3, (390, 240))
        if self.bombsLeft > 0:
            txt4 = GAMEFONT.render("X: bomb (%d left)" % self.bombsLeft, 
                False, (255,255,255))
            screen.blit(txt4, (390, 260))
        pausetxt = GAMEFONT.render("P: pause", 
            False, (255,255,255))
        screen.blit(pausetxt, (390, 280))
        if self.paused:
            isPausedTxt = GAMEFONT.render("****PAUSED****", 
            False, (255,255,255))
            screen.blit(isPausedTxt, (400, 400))

    def redrawAll(self, screen):
        if not self.gameOver:
            screen.blit(self.bg, (0,0))
            
            self.enemies.draw(screen)
            self.player.bullets.draw(screen)
            self.playerList.draw(screen)
            self.player.drawSprite(screen)
            self.enemy.bullets.draw(screen)
            
            screen.blit(self.sidepanel, (350,0))
            self.player.displayHealth(screen)
            self.enemy.displayHealth(screen)
            self.enemy.displayTimeLeft(screen)
            self.displayInstructions(screen)
        else:
            screen.blit(self.gameOverScreen, (0,0))

        if self.fading:
            self.fade(screen)

class BHMode2(BHMode):
# same but im setting the enemy to be something else
    def __init__(self):
        super().__init__()
        #self.music = pygame.mixer.Sound("ACNL_dreamsuite.wav")
        self.bombsLeft = 6
        self.enemy = UFO(name="UFO", imageName="bh_ufo.png", 
            rectX=350//2-75, height=80, width=150, health=800, attacks=4,
            moveList=[(150,70),(100,100),(80,50),(110,60),(140,40),
                      (40,70),(60,60),(100,100),(30,110),(120,60)], 
            movingAttacks=[3,4])
        self.enemies = pygame.sprite.Group()
        self.enemies.add(self.enemy)

class BHMode3(BHMode):
    def __init__(self):
        super().__init__()
        #self.music = pygame.mixer.Sound("ACNL_4am.wav")
        self.bombsLeft = 6
        self.enemy = Dog(name="DOG", imageName="bh_dog.png",
            rectX=350//2-135//2, height=120, width=135, health=800, attacks=2,
            moveList=[(0,0)], movingAttacks=[])
        # put in middle of screen
        self.enemy.rect.y = 150
        self.enemy.tempy = self.enemy.rect.y
        self.enemy.cy = self.enemy.rect.y + self.enemy.height//2
        self.enemies = pygame.sprite.Group()
        self.enemies.add(self.enemy)



