# ¡Crea tu propio juego de disparos!

from pygame import *
from time import time as t
from random import randint
from math import sin

init()

window = display.set_mode((700, 500))
fps = 60
running = True
clock = time.Clock()

# clase padre para otros objetos
class GameSprite(sprite.Sprite):
    # constructor de clase
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # llamamos al constructor de la clase (Sprite):
        sprite.Sprite.__init__(self)

        # cada objeto debe almacenar una propiedad image
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # cada objeto debe almacenar la propiedad rect en la cual está inscrito
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # método que dibuja al personaje en la ventana
    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

backgroundImg = image.load("galaxy.jpg")
backgroundImg = transform.scale(backgroundImg, (700, 500))

class Bullet(GameSprite):
     def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)

# clase del jugador principal
class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)

        self.direction = 0
        self.aPressed = False
        self.dPressed = False
        self.velocity = 0
        self.displayImg = self.image
        self.shootCD = 1
        self.shootTimer = t()
        self.canShoot = True

    def simulate(self):

        change = self.direction * self.speed

        self.velocity *= 0.99

        self.velocity += change * (1/ 60)

        self.rect.x += self.direction + self.velocity

        if self.rect.x < 150:
            self.rect.x = 150

        if self.rect.x > 500:
            self.rect.x = 500

        self.displayImg = transform.rotozoom(self.image, -self.velocity * 2, 1)

    def processInputs(self):

        self.direction = 0

        if self.aPressed:
            self.direction -= 1
        if self.dPressed:
            self.direction += 1

    def update(self):
        window.blit(self.displayImg, (self.rect.x, self.rect.y))

class Game():
    def __init__(self, playerInstance):

        self.enemies = sprite.Group()
        self.bullets = sprite.Group()

        self.font = font.Font(None, 80)
        self.RIPFONT = font.Font(None, 160)
        self.plr = playerInstance

        # gamerules
        self.enemiesCanSpawn = True
        self.showUI = True
        self.running = True

        # game settings
        self.enemyClock = t()
        self.spawnCooldown = 1.25
        self.maxSpawnable = 1
        self.baseSpeed = 0
        self.loseClock = t()
        self.deathMessage = None

        # game stats
        self.killed = 0
        self.failed = 0
        self.lost = False

    def showStats(self):
        if self.showUI == False : return

        lavoided = self.font.render(str(self.killed), True, (0, 100, 255))
        lfailed = self.font.render(str(self.failed), True, (255, 50, 10))

        window.blit(lavoided, (275, 50))
        window.blit(lfailed, (100+275, 50))
    
    def displayLoss(self):

        deathMessages = ["RIP.", "ggs.", "EZ.", "LOL."]

        if not self.deathMessage:
            self.deathMessage = deathMessages[randint(0, len(deathMessages)-1)]
        
        lRIP = self.RIPFONT.render(self.deathMessage, True, (255, 0, 0))
        lRIP = transform.rotozoom(lRIP, -sin(t()) * 15, 1)

        window.blit(lRIP, (250, 200 + (sin(t()) * 100)))

    def simulate(self, plr):

        if not running: return

        if self.enemiesCanSpawn == True:
            if t() - self.enemyClock >= self.spawnCooldown + randint(-250, 1000) / 1000:
                self.enemyClock = t()

                for i in range(randint(1, self.maxSpawnable)):
                    e = Enemy("ufo.png", 700 / 2 + randint(-200, 150), -60, 100, 50, randint(500, 3000) / 1000 + self.baseSpeed)
                    self.enemies.add(e)

        for enemy in self.enemies:
            enemy.rect.y += enemy.speed

            if enemy.rect.y > 500:
                enemy.kill()
                self.failed += 1
            else:
                if plr.rect.colliderect(enemy.rect) == True and not self.lost:
                    self.lost = True
                    self.maxSpawnable = 5
                    self.baseSpeed = 10
                    self.loseClock = t()
                    self.deathMessage = None

        for bullet in self.bullets:
            bullet.rect.y -= bullet.speed

            if bullet.rect.y < -50:
                bullet.kill()
            else:
                for enemy in self.enemies:
                    if bullet.rect.colliderect(enemy.rect) == True:

                        enemy.kill()
                        bullet.kill()

                        self.killed += 1

        if self.lost:
            self.displayLoss()

            if t() - self.loseClock >= 3.5:

                self.baseSpeed = 0
                self.maxSpawnable = 1
                self.lost = False
                self.killed = 0
                self.failed = 0

                self.bullets.empty()
                self.enemies.empty()

                plr.velocity = 0
                plr.rect.x = 700 / 2 - 50

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)

plr = Player("rocket.png", 700/2 - 50, 500-100, 80, 100, 9)
game = Game(plr)

while running:

    window.blit(backgroundImg, (0,0))

    for e in event.get():
        if e.type == QUIT:
            quit()
            exit(0)
        if e.type == KEYDOWN:
            if e.key == K_a:
                plr.aPressed = True
            if e.key == K_d:
                plr.dPressed = True
        elif e.type == KEYUP:
            if e.key == K_a:
                plr.aPressed = False
            if e.key == K_d:
                plr.dPressed = False
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == BUTTON_LEFT:
                
                if game.lost: break
                if plr.canShoot == False and t() - plr.shootTimer < plr.shootCD: break

                plr.shootTimer = t()
                plr.canShoot = False

                b = Bullet("bullet.png", plr.rect.x + (25 / 2), plr.rect.y, 50, 50, 5)
                shootSFX = mixer.Sound("fire.ogg")
                shootSFX.play()

                game.bullets.add(b)

    game.simulate(plr)
    game.showStats()

    plr.processInputs()
    plr.simulate()
    game.bullets.draw(window)

    if not game.lost:
        plr.update()

    game.enemies.draw(window)

    display.update()
    clock.tick(fps)