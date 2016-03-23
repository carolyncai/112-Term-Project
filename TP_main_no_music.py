# TP - no music ver.

import pygame
from playerclass import Player
from textboxclass import Textbox
from signclass import Sign
from healptclass import HealPoint
from npcclass import NPC
from BHMode_no_music import BHMode, BHMode2, BHMode3
from SHOPMODE import ShopMode
from BHbulletclasses import Raindrop

pygame.init()

class RPG(object):
    ARROWKEYS = {pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN}
    def __init__(self):
    # this is super long omg
    # Bye Style Points...
    # but seriously though
        BHMode.init()

        self.triedToGoHome = False

        self.hasRained = False
        self.isRaining = False
        self.rain_thresh = 4000
        self.rainCount = 0
        self.max_rainCount = 60 * 60
        self.raindrops = pygame.sprite.Group()
        Raindrop.init()

        self.inBH = False
        self.BH = None
        self.BH1 = BHMode()
        #self.BH1.completed = True #!!
        self.BH2 = BHMode2()
        #self.BH2.completed = True #!!
        self.BH3 = BHMode3()
        #self.BH3.completed = True #!!
        # these comments were for testing purposes

        self.completed = False
        self.ending_thresh = 5980

        self.worldX = 0
        self.worldX_dx = 0
        self.max_worldX = 5400
        
        self.textbox = pygame.sprite.Group()
        self.textbox.add(Textbox())

        self.player = Player()
        self.playerList = pygame.sprite.Group()
        self.playerList.add(self.player)

        # add signs
        sign1 = Sign(300, ["\"Hello, I am a sign.\"",
                           "\"Here is some important information:\"",
                           "\"West: Residential area.\"",
                           "\"East: Shopping district.\"",
                           "\"I hope you found this helpful.\""])
        sign2 = Sign(550, ["(There is a sticky note on this sign.)",
                            "\"Dear Star Town citizens:\"",
                            "\"It's me! Your mayor.\"",
                            "\"Please join me in welcoming our new residents...\"",
                            "\"Tomorrow.\"",
                            "\"I don't want to miss the supermarket sale today!\""])
        sign3 = Sign(1200, ["\"It's not 'trash CAN'T '...\"",
                            "\"It's 'trash CAN' !!\"",
                            "\"So, even if you are feeling like trash...\"",
                            "\"Please, keep doing your best!!\"",
                            "\"--Sincerely, a trash enthusiast.\""])
                            # (im the trash enthusiast) 
        sign4 = Sign(2100, ["(It seems like someone has defaced this sign...)",
                            "(Now there is a picture of a cat on it.)",
                            "\"WANTED: CAT WHO KEEPS EATING MY FOOD.\"",
                            "\"Whoever you are, please stop...\""])
        sign5 = Sign(2710, ["\"Space enthusiast meeting --\"",
                            "\"Next Tuesday at 7pm.\"",
                            "\"BYOS (Bring Your Own Spaceship).\""])
        sign6 = Sign(3400, ["\"Star Town Tree:\"",
                            "\"This tree was planted to commemorate\"",
                            "\"the founding of our town.\"",
                            "\"The tree supports our citizens in many ways,\"",
                            "\"so please continue to support Star Town.\""])
        sign7 = Sign(4900, ["\"Warning: dog.\"",
                            "\"Very fluffy.\""])
        sign8 = Sign(5850, ["\"Supermarket -- just over to the right!\"",
                            "\"Don't miss all our PRICES and SELECTIONS.\""])
        self.signs = pygame.sprite.Group()
        self.signs.add(sign1, sign2, sign3, sign4, sign5, sign6, sign7, sign8)

        # add heal pts
        trash = HealPoint(rectY=180, worldX=1000, healthPts=30, 
            imageName="trash-chan.png", textDict=
            {False:["(It's a trash can.)",
                    "(You find a burger in the trash.)",
                    "(You eat the burger and recover some HEALTH.)",
                    "(How disgusting...)"],
            True:["(You ate the trash...)",
                  "(The trash is inside of you...)",
                  "(You feel like a trash can.)"]})

        tallPerson = HealPoint(rectY=0, worldX=2300, healthPts=40,
            imageName="tall.png", textDict=
            {False:["(It's an extremely tall individual.)",
                    "(For some reason, you feel very safe here.)",
                    "(You rest underneath the individual for a while...)",
                    "(Hopefully they didn't mind.)",
                    "(You recover some HEALTH.)"],
            True:["(This individual is so tall,",
                  "that you can't see beyond their legs.)",
                  "(But, at least they have great footwear.)"]})

        tree = HealPoint(rectY=0, worldX=3500, healthPts=40, 
            imageName="tree.png", textDict=
            {False:["(It's a great big tree.)",
                    "(You stop and take a break under it.)",
                    "(Suddenly, a piece of fruit falls in front of you!)",
                    "(You eat the fruit and regain some HEALTH.)",
                    "(Somewhere in the distance...)",
                    "(You sense that someone is greatly offended by this.)"],
            True:["(You stay under the tree for a little while.)",
                  "(You feel so refreshed! Mentally, that is.)"]})

        busStop = HealPoint(rectY=110, worldX=5500, healthPts=40,
            imageName="bus_stop.png", textDict=
            {False:["(It's a bus stop.)",
                    "(You haven't seen the bus all day...)",
                    "(But...)",
                    "(You're sure the bus is trying its best!!)",
                    "(Thinking of the bus increases your HEALTH.)"],
            True:["(You keep thinking about the bus...)",
                  "(But nothing else happens. Aw.)"]})

        self.healPoints = pygame.sprite.Group()
        self.healPoints.add(trash, tallPerson, tree, busStop)
      
        # add npc's
        egg = NPC(rectY=305, worldX=800, imageName="egg.png", 
            textDictM = {False:["\"Oh...hello...\"",
                                "\"I was just enjoying this nice sunlight.\"", 
                                "\"I'll get out of the way.\""]},
            textDictD={False: ["\"Do you see that trash can over there?\"",
                               "\"I saw someone throw something away",
                               "a few minutes ago.\"",
                               "\"Maybe you should check it out.\""],
                       True: ["\"The ground is all warm from the sun...\"",
                              "\"By the way, did you find anything in the trash?\""]})
        egg.hasBH = False

        toast = NPC(rectY=250, worldX=1500, imageName="toast.png", 
            textDictM = {False:["\"Hello, new neighbor!\"",
                                "\"You look hungry!\"", 
                                "\"Did you eat breakfast today?\"",
                                "\"It's important to have a balanced breakfast.\"",
                                "\"Let me help you out.\"",
                                "\"Please take the breakfast items",
                                "that I am about to throw at you.\"",
                                "\"Run into them as hard as you can, ok??\"",
                                "\"I'm sure your HEALTH will improve in no time.\"",
                                "\"Of course, it's totally safe.\"",
                                "\"There is no way this can hurt you.\"",
                                "(...)",
                                "(You hear a voice from above again...)",
                                "('Hey! Listen up!')",
                                "('Move around with the ARROW KEYS.')",
                                "('Try to dodge the projectiles!')",
                                "('If your HEART gets hit, you will lose HEALTH.')",
                                "('Hold down 'Z' to cry...')",
                                "('You will shoot tears at your opponent.')",
                                "('Crying will damage them...emotionally')",
                                "('They will leave you alone if they have low HP,)",
                                "('or if they run out of projectiles.')",
                                "('Hold down LEFT SHIFT to focus.')",
                                "('If you concentrate, you can slow your movements.')",
                                "('You will also cry harder.')",
                                "('Press 'X' to do something exciting.')",
                                "('If you distract your neighbor,')",
                                "('you can make them stop shooting momentarily.')",
                                "('You will also scare away the projectiles.')",
                                "('Finally, press 'P' to stop time.')",
                                "('It's fine to take a break.')",
                                "('OK, that's it! I hope you were paying attention!')",
                                "(...You carefully remember those instructions!)",
                                "(...)",
                                "\"Are you ready?\"",
                                "\"Here we go!\""]},
            textDictD={False: ["\"You didn't eat anything...\"",
                               "\"Do you not like food items...",
                               "...being hurled at you at high velocities?\"",
                               "\"Well...whatever works for you, I guess.\""],
                       True: ["\"Are you headed to the supermarket?\"",
                              "\"It's all the way to your right.\"",
                              "\"You can go buy some fruits there...\"",
                              "\"Even though, I gave some to you for free.\""]})
        toast.hasBH = True

        raindrop = NPC(rectY=255, worldX=1800, imageName="raindrop.png",
            textDictM = {False: ["\"Ah...I wish it was raining.\"",
                                 "\"I love the rain. It's my element.\"",
                                 "\"But I guess this weather is OK too.\"",
                                 "\"...Oh, am I in your way?\"",
                                 "\"I'll go stand a little bit to my right.\""]},
            textDictD= {False: ["\"Sometimes the weather here gets really bad.\"",
                                "\"It'll rain so hard that, if the rain hits you...\"",
                                "\"You might even lose some HEALTH!\"",
                                "\"If you wanted to go anywhere...\"",
                                "\"You would have to dodge all the rain!!\"",
                                "\"Doesn't that sound fun? Haha.\"",
                                "\"Don't worry, though.\"",
                                "\"It won't happen to you today.\"",
                                "\"It might rain a little bit, but,\"",
                                "\"a slight drizzle won't hurt you.\""],
                        True: ["\"It's good to stock up on food at home.\"",
                               "\"That way you won't have to go outside",
                               "when there's bad weather.\"",
                               "\"...\"",
                               "\"What do you mean, you never go outside anyway??\""]})
        raindrop.hasBH = False

        ufo = NPC(rectY=220, worldX=2900, imageName="ufo.png",
            textDictM = {False: ["\"...\"",
                                 "\".....\"",
                                 "\"....!\"",
                                 "\"! ! !\""]},
            textDictD= {False: ["\"Oh no...I'm sorry, are you hurt?\"",
                                "\"I was just so excited about space.\"",
                                "\"I just moved here from space, you see.\"",
                                "\"I wanted to show everyone here",
                                "how cool and pretty my home was...\"",
                                "\"So I bought a bunch of plastic stars...\"",
                                "\"But now they're all over the ground.\"",
                                "\"...whoops...\""],
                        True: ["\"...\"",
                               "\"......\"",
                               "\"...zzz...\"",
                               "(You look more closely at the UFO...)",
                               "(Oh! There is a very small cat inside.)",
                               "(The cat is taking a nap!)",
                               "(It must be nice and cozy in there.)"]})
        ufo.hasBH = True

        cat = NPC(rectY=210, worldX=3800, imageName="cat.png",
            textDictM= {False: ["\"Someone keeps eating all my Frisky Bitz.\"",
                                "\"It's not you, is it??\"",
                                "\"...\"",
                                "\"You don't look like a cat, so...\"",
                                "\"I guess it's someone else.\"",
                                "\"I mean, they pay me back for it, but still!\"",
                                "\"Now I have to go buy more all the time.\"",
                                "\"Sigh...\""]},
            textDictD= {False: ["\"...Have you noticed all the stuff on the ground?\"",
                                "\"Those star-shaped rocks...\"",
                                "\"No one knows where they came from.\"",
                                "\"Except maybe the mayor.\"",
                                "\"I've never seen them before, but...\"",
                                "\"Sometimes you'll hear their voice from above.\"",
                                "\"So, has the mayor said anything to you yet?\"",
                                "(...You hear something from above...)",
                                "('...*coughing noises*...')",
                                "('...Sorry, I choked on a chip.')",
                                "('Did you need something?')",
                                "(...no thanks...you're good...)"],
                        True:  ["\"I'll be waiting here until I run into",
                                "whoever keeps eating my food.\"",
                                "\"You should go on ahead!\"",
                                "\"The shopping district is not so far ahead.\""]})
        cat.hasBH = False

        dog = NPC(rectY=210, worldX=5200, imageName="dog.png",
            textDictM= {False: ["\"Woof!\"",
                                "\"Don't come any closer!\"",
                                "\"I decided to dig up all my chew toys.\"",
                                "\"But now I have too many...\"",
                                "\"I can't hold on to all of them...\"",
                                "\"...Oh no...\"",
                                "\"Oh no oh no oh no\"",
                                "\"Now they're dropping all over the place.\"",
                                "\"You'd better get out of the way!!\""]},
            textDictD= {False: ["\"Bark bark!\"",
                                "\"Are you ok??\"",
                                "\"I didn't mean for that to happen...\"",
                                "\"Oh no...\"",
                                "(The dog looks sad...)",
                                "(You reach out to pet the dog.)",
                                "(The dog is so fluffy and nice...)",
                                "(After being pet, the dog looks happy again!)"],
                        True:  ["(You pet the dog again.)",
                                "(The dog is so happy!!)",
                                "(Petting the dog makes you feel happy too.)"]})
        dog.hasBH = True

        self.NPCs = pygame.sprite.Group()
        self.NPCs.add(egg, toast, raindrop, ufo, cat, dog)

        self.currentSign = None
        self.currentHP = None
        self.currentNPC = None

        self.bg_ground = pygame.image.load("ground.png").convert_alpha()
        self.bg_bush = pygame.image.load("bushes.png").convert_alpha()
        self.bg_sky = pygame.image.load("sky.png").convert_alpha()
        self.bg_sun = pygame.image.load("sunlight.png").convert_alpha()
        self.bg_sun = pygame.transform.flip(self.bg_sun, True, False)
        # all the shadows were on the wrong side OOPS LOLOLOL its fixed now

    def setPlayerHealth(self, health):
        self.player.health = health

    def keyPressed(self, keyCode, modifier):
    # first part: if player is reading, advance text
        if self.player.displayingText:
            if keyCode == pygame.K_z:
                self.player.advanceText()
        elif (self.currentSign != None and self.currentSign.displayingText
            and not self.currentSign.doneReading):
            if keyCode == pygame.K_z:
                self.currentSign.advanceText()
                if self.currentSign.doneReading:
                    self.currentSign = None
        elif (self.currentHP != None and self.currentHP.displayingText 
            and not self.currentHP.doneReading):
            if keyCode == pygame.K_z:
                self.currentHP.advanceText()
                if self.currentHP.doneReading:
                    self.currentHP.healPlayer(self.player)
                    self.currentHP = None
        elif (self.currentNPC != None and self.currentNPC.displayingText 
            and not self.currentNPC.doneReading):
            if keyCode == pygame.K_z:
                self.currentNPC.advanceText()
                if self.currentNPC.doneReading:
                    if self.currentNPC.placated == False:
                        # trigger BH mode if possible
                        # otherwise move out of way
                        if self.currentNPC.hasBH:
                            if not self.BH1.completed:
                                self.BH = self.BH1
                            elif not self.BH2.completed:
                                self.BH = self.BH2 
                            elif not self.BH3.completed:
                                self.BH = self.BH3
                            self.BH.setPlayerHealth(self.player.health)
                            self.inBH = True
                        else:
                            self.currentNPC.becomeNice()
                            self.currentNPC.moveOutOfWay()
                    if self.currentNPC.placated == True:
                        self.currentNPC = None
        # second part: let player interact with stuff
        elif keyCode == pygame.K_z:
            collidedSigns = pygame.sprite.spritecollide(self.player, self.signs, False)
            collidedHPs = pygame.sprite.spritecollide(self.player, self.healPoints, False)
            collidedNPCs = pygame.sprite.spritecollide(self.player, self.NPCs, False)
            if collidedSigns != []:
                self.currentSign = collidedSigns[0]
                self.currentSign.displayingText = True
                self.currentSign.doneReading = False
            elif collidedHPs != []:
                self.currentHP = collidedHPs[0]
                self.currentHP.textToDisplay = self.currentHP.text[self.currentHP.talkedTo]
                self.currentHP.displayingText = True
                self.currentHP.doneReading = False  
            elif collidedNPCs != []:
                self.currentNPC = collidedNPCs[0]
                self.currentNPC.textToDisplay = self.currentNPC.text[self.currentNPC.talkedTo]
                self.currentNPC.displayingText = True
                self.currentNPC.doneReading = False
            self.stopMoving()
        # third part: move player
        else:
            if keyCode == pygame.K_LEFT:
                self.player.facingRight = False
                self.player.moving = True
                if (self.player.rect.x > Player.left_thresh or self.worldX <= 0):
                    self.player.changeSpeed(-1, 0)
            elif keyCode == pygame.K_RIGHT:
                self.player.facingRight = True
                self.player.moving = True
                if (self.player.rect.x < Player.right_thresh or 
                        self.worldX >= self.max_worldX):
                    self.player.changeSpeed(+1, 0)
            elif keyCode == pygame.K_UP:
                self.player.unsquish()
            elif keyCode == pygame.K_DOWN:
                self.player.squish()

    def keyReleased(self, keyCode, modifier):
        if keyCode in RPG.ARROWKEYS:
            self.stopMoving()

    def stopMoving(self):
        self.player.moving = False
        self.player.unanimate()
        self.player.dx = 0
        self.worldX_dx = 0

    def timerFired(self, dt):
        # first part: move player & scroll
        if self.player.moving:
            if self.player.facingRight and self.player.rect.x > Player.right_thresh: 
                if self.worldX >= self.max_worldX:
                    self.worldX_dx = 0
                elif self.worldX < self.max_worldX:
                    self.player.dx = 0
                    self.worldX_dx = +1*self.player.speed
            elif (not self.player.facingRight) and self.player.rect.x < Player.left_thresh: 
                if self.worldX <= 0:
                    self.worldX_dx = 0
                elif self.worldX > 0:
                    self.player.dx = 0
                    self.worldX_dx = -1*self.player.speed
        
        player_worldX = self.worldX + self.player.rect.x
        
        # do stuff if player reaches ends of map
        if player_worldX > self.ending_thresh:
            self.completed = True
        elif player_worldX < 0:
            self.triedToGoHome = True

        # make it rain
        if (player_worldX >= self.rain_thresh and not self.isRaining and 
            not self.hasRained):
            self.isRaining = True

        if self.isRaining:
            self.rainCount += 1
            self.raindrops.update(self.worldX_dx)
            if self.rainCount % 2 == 0:
                self.raindrops.add(Raindrop())
            if self.rainCount >= self.max_rainCount:
                self.isRaining = False
                self.hasRained = True

        # trigger flavor text
        if (player_worldX in Player.FLAVORTEXT and
                player_worldX not in Player.SEENTEXT):
            self.stopMoving()
            self.player.displayingText = True
            self.player.textToDisplay = Player.FLAVORTEXT[player_worldX]
            Player.SEENTEXT.add(player_worldX)

        # automatic npc interaction
        collidedNPCs = pygame.sprite.spritecollide(self.player, self.NPCs, False)
        if collidedNPCs != [] and collidedNPCs[0].placated == False:
            self.stopMoving()
            self.currentNPC = collidedNPCs[0]
            self.currentNPC.textToDisplay = self.currentNPC.text[self.currentNPC.talkedTo]
            self.currentNPC.displayingText = True
            self.currentNPC.doneReading = False        

        # update everything
        self.worldX += self.worldX_dx
        self.player.animate()
        self.playerList.update()
        self.signs.update(self.worldX)
        self.healPoints.update(self.worldX)
        self.NPCs.update(self.worldX)

    def redrawAll(self, screen):
        # draw background (parallax..whee)
        screen.blit(self.bg_sky, (0, 0), (self.worldX//2, 0, 600, 450))
        screen.blit(self.bg_bush, (0, 0), (int(self.worldX*0.75), 0, 600, 450))
        screen.blit(self.bg_ground, (0, 0), (self.worldX, 0, 600, 450))
        # draw player & other things
        self.signs.draw(screen)
        self.healPoints.draw(screen)
        self.NPCs.draw(screen)
        self.playerList.draw(screen)
        # draw more background..or..foreground??
        screen.blit(self.bg_sun, (0, 0), (self.worldX*1.2, 0, 600, 450))
        # draw rain
        self.raindrops.draw(screen)
        # draw health
        self.player.displayHealth(screen)
        # display some text
        text = None
        if self.player.displayingText:
            text = self.player.textToDisplay[self.player.text_index]
        elif self.currentSign != None and self.currentSign.displayingText:
            text = self.currentSign.text[self.currentSign.text_index]
        elif self.currentHP != None and self.currentHP.displayingText:
            text = self.currentHP.textToDisplay[self.currentHP.text_index]
        elif self.currentNPC != None and self.currentNPC.displayingText:
            text = self.currentNPC.textToDisplay[self.currentNPC.text_index]
        if text != None:
            Textbox.displayTextBox(screen, self.textbox, text)


class TitleScreen(object):
    def __init__(self):
        self.bg = pygame.image.load("titlescreen.png")
        self.inTitleScreen = True

    def keyPressed(self, keyCode, modifier):
        if keyCode == pygame.K_z:
            self.inTitleScreen = False

    def redrawAll(self, screen):
        screen.blit(self.bg, (0,0))


class Intro(object):
    def __init__(self):
        self.bg = pygame.image.load("home_cg.png")
        self.inIntro = False
        self.textbox = pygame.sprite.Group()
        self.textbox.add(Textbox())
        self.text = ["Somewhere in a small town...",
                     "Sometime in the early evening...",
                     "A simple Cube (that's you!) settles in for the night,",
                     "having just moved into a new home.",
                     "You get ready to spend some quality time...",
                     "...doing absolutely nothing.",
                     "But suddenly!",
                     "You realize something very urgent!",
                     "You don't have any food in the house!!",
                     "Oh no!!",
                     "Even though you don't want to go outside...",
                     "You start feeling a bit hungry.",
                     "You start becoming worried about your HEALTH...",
                     "So, you decide to go to the supermarket.",
                     "Being in a new town makes you a little nervous.",
                     "But you feel like you have to carry on!",
                     "You leave your home and head outside."]
        self.text_index = 0
        self.max_text_index = len(self.text) - 1

    def keyPressed(self, keyCode, modifier):
        if keyCode == pygame.K_z:
            self.text_index += 1
            if self.text_index > self.max_text_index:
                self.inIntro = False # u done

    def redrawAll(self, screen):
        screen.blit(self.bg, (0,0))
        if self.text_index <= self.max_text_index:
            Textbox.displayTextBox(screen, self.textbox, self.text[self.text_index])

class NotHome(object):
# if u try to go home before the game is over
    def __init__(self):
        self.inNotHome = False
        self.textbox = pygame.sprite.Group()
        self.textbox.add(Textbox())
        self.text = ["You're tempted to go home...",
                     "but...",
                     "You remember that you have something to do!",
                     "So, get back out there!! You can do it!!"]
        self.text_index = 0
        self.max_text_index = len(self.text) - 1

    def keyPressed(self, keyCode, modifier):
        if keyCode == pygame.K_z:
            self.text_index += 1
            if self.text_index > self.max_text_index:
                self.text_index = 0
                self.inNotHome = False 

    def redrawAll(self, screen):
        screen.fill((0,0,0))
        if self.text_index <= self.max_text_index:
            Textbox.displayTextBox(screen, self.textbox, self.text[self.text_index])

class Instructions(object):
    def __init__(self):
        self.bg = pygame.image.load("instructions.png")
        self.inInstructions = False

    def keyPressed(self, keyCode, modifier):
        if keyCode == pygame.K_z:
            self.inInstructions = False

    def redrawAll(self, screen):
        screen.blit(self.bg, (0,0))

class Ending(object):
    def __init__(self):
        self.bg = pygame.image.load("ending_cg.png")
        self.inEnding = False
        self.textbox = pygame.sprite.Group()
        self.textbox.add(Textbox())
        self.text = ["It's the supermarket!",
                     "You made it!",
                     "There are only a few minutes before closing time.",
                     "There is not much food left on the shelves...",
                     "But it looks like all the essentials are still here.",
                     "You reach out to put an item in your basket.",
                     "Suddenly...you remember...",
                     "...you don't have arms...",
                     "...or hands......",
                     "...oh...",
                     "... ... ...",
                     "After some time,",
                     "a nice employee notices your struggle.",
                     "They offer to throw some food at you.",
                     "Armed with your shopping basket, you accept!",
                     "You get ready to catch the food!"]
        self.text_index = 0
        self.max_text_index = len(self.text) - 1

    def keyPressed(self, keyCode, modifier):
        if keyCode == pygame.K_z:
            self.text_index += 1
            if self.text_index > self.max_text_index:
                self.inEnding = False

    def redrawAll(self, screen):
        screen.blit(self.bg, (0,0))
        if self.text_index <= self.max_text_index:
            Textbox.displayTextBox(screen, self.textbox, self.text[self.text_index])

class RealEnding(object):
    def __init__(self):
        self.inRealEnding = False
        self.textbox = pygame.sprite.Group()
        self.textbox.add(Textbox())
        self.text = None # temp
        self.text_index = 0
        self.max_text_index = None # temp

    def setText(self, txtList):
        self.text = txtList
        self.text += ["...",
                      "Finally, after a long day...",
                      "You can't wait to relax!",
                      "You think about how far you've come...",
                      "And all the people you've met...",
                      "Even though it's been difficult at times,",
                      "You feel like it's been a good day!",
                      "Now, it's time for you to head home!"]
        self.max_text_index = len(self.text) - 1

    def keyPressed(self, keyCode, modifier):
        if keyCode == pygame.K_z:
            self.text_index += 1
            if self.text_index > self.max_text_index:
                self.text_index = 0
                self.inRealEnding = False 

    def redrawAll(self, screen):
        screen.fill((19,24,52)) # color = same as credits page
        if self.text_index <= self.max_text_index:
            Textbox.displayTextBox(screen, self.textbox, self.text[self.text_index])

class NiceGame(object):
# from pygamegame.py, from CA Lukas Peraza, from optional Pygame lecture
    def init(self):
        self.blackScreen = pygame.image.load("black_screen.png").convert()
        self.fadeAlpha = 255
        self.fading = False
        self.mode = "titleScreen"
        self.titleScreen = TitleScreen()
        self.instructions = Instructions()
        self.intro = Intro()
        self.RPG = RPG()
        self.notHome = NotHome()
        self.ending = Ending()
        ShopMode.init()
        self.shopMode = ShopMode()
        self.realEnding = RealEnding()
        self.creditsBG = pygame.image.load("credits.png")

        #self.music_6pm = pygame.mixer.Sound("ACNL_6pm.wav")
        #self.music_shop = pygame.mixer.Sound("ACNL_re-tail.wav")
        #self.music_credits = pygame.mixer.Sound("ACNL_1am.wav")
        # ^ this is a repeat but i wanted to be able to fade it in

    def fade(self, screen):
    # fades FROM black?? but eh it looks ok so i will keep it
    # takes advantage of how redrawAll is called every frame...
        if self.fadeAlpha < 0:
            self.fading = False
            self.fadeAlpha = 255
        else:
            self.blackScreen.set_alpha(self.fadeAlpha)
            screen.blit(self.blackScreen, (0,0))
            self.fadeAlpha -= 15
       
    def keyPressed(self, keyCode, modifier):
        if self.mode == "titleScreen":
            self.titleScreen.keyPressed(keyCode, modifier)
            if self.titleScreen.inTitleScreen == False:
                self.fading = True
                self.mode = "instructions"
                self.instructions.inInstructions = True
        elif self.mode == "instructions":
            self.instructions.keyPressed(keyCode, modifier)
            if self.instructions.inInstructions == False:
                self.fading = True
                self.mode = "intro"
                self.intro.inIntro = True
        elif self.mode == "intro":
            self.intro.keyPressed(keyCode, modifier)
            if self.intro.inIntro == False:
                self.fading = True
                #pygame.mixer.music.fadeout(100)
                #self.music_6pm.play(-1, fade_ms=200)
                self.mode = "RPG"
        elif self.mode == "RPG":
            self.RPG.keyPressed(keyCode, modifier)
            if self.RPG.inBH:
                self.fading = True
                #self.music_6pm.fadeout(100)
                #self.RPG.BH.music.play(-1, fade_ms=200)
                self.mode = "BH"
        elif self.mode == "BH":
            self.RPG.BH.keyPressed(keyCode, modifier)
        elif self.mode == "NotHome":
            self.notHome.keyPressed(keyCode, modifier)
            if self.notHome.inNotHome == False:
                #whoooo ok set everything back now
                self.RPG.triedToGoHome = False
                self.RPG.player.rect.x = 30
                self.RPG.player.facingRight = True
                self.RPG.player.moving = False
                self.RPG.player.unanimate()
                self.RPG.player.dx = 0
                self.fading = True
                self.mode = "RPG"
        elif self.mode == "ending":
            self.ending.keyPressed(keyCode, modifier)
            if self.ending.inEnding == False:
                self.fading = True
                self.mode = "shop"
        elif self.mode == "shop":
            self.shopMode.keyPressed(keyCode, modifier)
        elif self.mode == "realEnding":
            self.realEnding.keyPressed(keyCode, modifier)
            if self.realEnding.inRealEnding == False:
                self.fading = True
                #self.music_shop.fadeout(100)
                #self.music_credits.play(-1, fade_ms=300)
                self.mode = "credits"


    def keyReleased(self, keyCode, modifier):
        if self.mode == "RPG":
            self.RPG.keyReleased(keyCode, modifier)
        elif self.mode == "BH":
            self.RPG.BH.keyReleased(keyCode, modifier)
        elif self.mode == "shop":
            self.shopMode.keyReleased(keyCode, modifier)

    def timerFired(self, dt):
        if self.mode == "RPG":
            self.RPG.timerFired(dt)
            if self.RPG.triedToGoHome:
                self.fading = True
                self.mode = "NotHome"
                self.notHome.inNotHome = True
            if self.RPG.completed:
                self.fading = True
                self.mode = "ending"
                #self.music_6pm.fadeout(100)
                #self.music_shop.play(-1, fade_ms=200)
                self.ending.inEnding = True
        elif self.mode == "BH":
            self.RPG.BH.timerFired(dt)
            if self.RPG.BH.completed:
                self.RPG.inBH = False
                self.RPG.setPlayerHealth(self.RPG.BH.player.health)
                self.RPG.currentNPC.becomeNice()
                self.RPG.currentNPC.moveOutOfWay()
                self.fading = True
                #self.RPG.BH.music.fadeout(100)
                #self.music_6pm.play(-1, fade_ms=200)
                self.mode = "RPG"
        elif self.mode == "shop":
            self.shopMode.timerFired(dt)
            if self.shopMode.completed:
                playermoney = self.shopMode.player_moneyLeft
                endingtxt = []
                if playermoney == 20.00:
                    endingtxt = ["Oh dear...",
                                 "It looks like you didn't buy anything.",
                                 "The supermarket is closed now.",
                                 "But, not to worry!",
                                 "You decide...",
                                 "to leave tomorrow's problems for tomorrow's you!"]
                elif playermoney > 0.00:
                    endingtxt = ["You leave the supermarket with some food.",
                                 "You even have some money left over!",
                                 "Luckily, there was a big sale today.",
                                 "Perhaps you should have bought more things?",
                                 "...you decide not to dwell on such matters."]
                else:
                    endingtxt = ["You bought a lot of food at the supermarket!",
                                 "But...",
                                 "Now you feel like you're running low on funds.",
                                 "...",
                                 "...You'll cross that bridge when the time comes.",
                                 "...Which won't be for a while, because,",
                                 "you have so much food."]
                self.realEnding.setText(endingtxt)
                self.shopMode.inShopMode = False
                self.fading = True
                self.mode = "realEnding"
                self.realEnding.inRealEnding = True


    def redrawAll(self, screen):
        if self.mode == "titleScreen":
            self.titleScreen.redrawAll(screen)
        elif self.mode == "instructions":
            self.instructions.redrawAll(screen)
        elif self.mode == "intro":
            self.intro.redrawAll(screen)
        elif self.mode == "RPG":
            self.RPG.redrawAll(screen)
        elif self.mode == "BH":
            self.RPG.BH.redrawAll(screen)
        elif self.mode == "NotHome":
            self.notHome.redrawAll(screen)
        elif self.mode == "ending":
            self.ending.redrawAll(screen)
        elif self.mode == "shop":
            self.shopMode.redrawAll(screen)
        elif self.mode == "realEnding":
            self.realEnding.redrawAll(screen)
        elif self.mode == "credits":
            screen.blit(self.creditsBG, (0,0))
        
        if self.fading == True:
            self.fade(screen)
    

    def __init__(self, width=600, height=450, fps=60, 
        title="Cube Just Wants A Quiet Life"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (0, 0, 0)
        pygame.init()

    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)
        # stores all the keys currently being held down
        self._keys = dict()
        # call game-specific initialization
        self.init()
        #pygame.mixer.music.load("ACNL_1am.wav")
        #pygame.mixer.music.play(-1)
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()

def main():
    nicegame = NiceGame()
    nicegame.run()

if __name__ == '__main__':
    main()