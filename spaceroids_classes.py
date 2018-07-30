import pygame
from pygame.locals import Rect, K_a, K_d, KEYDOWN, KEYUP, K_LEFT, K_RIGHT, K_w, K_UP
from pygame.locals import JOYAXISMOTION, JOYBUTTONDOWN
from math import sqrt
from random import randint

class Cenario(object):
    def __init__(self):
        self.image_background = pygame.image.load('bg.jpg')
        self.player1 = Player(50, 420, 64, 64, "Nave 1 Left.png", "Nave 1 Right.png", "Nave 1.png")
        self.player2 = Player(500, 420, 64, 64, "Nave 2 Left.png", "Nave 2 Right.png", "Nave 2.png")
        self.bullets = []
        self.asteroids = []
        self.asteroid_time = 600
        self.bulletSound = pygame.mixer.Sound('bullet.wav')

        self.music = pygame.mixer.music.load('music.mp3')
        pygame.mixer.music.play(-1)

        self.font = pygame.font.SysFont("Arial", 32, False, False)

    def restart(self):
        self.player1.score = 0
        self.player2.score = 0
        self.player1.lives = 1
        self.player2.lives = 1
        self.player1.tempo_asteroid = 0
        self.player2.tempo_asteroid = 0
        self.asteroids = []

    def produce_shoot(self, player):
        if player.can_shoot() and len(self.bullets) < 4:
            bullet = Projetil(player, 4, (0, 255, 0))
            self.bullets.append(bullet)
            self.bulletSound.play()

    #Drawing on screen stuff
    def draw(self, scr):
        scr.blit(self.image_background, (0, 0)) #background

        #player draw bullet
        for bullet in self.bullets:
            bullet.draw(scr)

        #player asteroids draw
        for asteroid in self.asteroids:
            asteroid.draw(scr)

        #players draw
        self.player1.draw(scr)
        self.player2.draw(scr)

        img_pontos1 = self.font.render("Pontos : "+ str(self.player1.score), True, (255, 255, 0))
        img_pontos2 = self.font.render("Pontos : " + str(self.player2.score), True, (255, 255, 0))

        scr.blit(img_pontos1, (50, 50))
        scr.blit(img_pontos2, (450, 50))

    def update(self):
        # player updates
        self.player1.update()
        self.player2.update()

        #player limits
        if self.player1.rect.x + 6 < 0:
            self.player1.rect.x += 6
        elif self.player1.rect.x + 6 > 280:
            self.player1.rect.x -= 6

        if self.player2.rect.x + 6 < 320:
            self.player2.rect.x += 6
        elif self.player2.rect.x + 6 > 600:
            self.player2.rect.x -= 6

        # player bullets
        for bullet in self.bullets:
            if bullet.y > 0:
                bullet.y -= bullet.vel
            else:
                self.bullets.pop(self.bullets.index(bullet))

        #asteroids players
        for asteroid in self.asteroids:
            if asteroid.y < 480:
                asteroid.update()
            else:
                self.asteroids.pop(self.asteroids.index(asteroid))
                asteroid.owner.lives -= 1

        #asteroids player 1 collision
        for asteroid in self.asteroids:
            for bullet in self.bullets:
                dx = abs(bullet.x - asteroid.x)
                dy = abs(bullet.y - asteroid.y)
                d = sqrt((dx ** 2) + (dy ** 2) // 1)
                if d < (asteroid.raio + bullet.raio):
                    self.asteroids.pop(self.asteroids.index(asteroid))
                    self.bullets.pop(self.bullets.index(bullet))
                    asteroid.owner.score += 1

        if self.player1.tempo_asteroid > 30 and self.player1.lives > 0:
            if len(self.asteroids) < 10:
                self.asteroids.append(Enemy(self.player1, randint(40, 280), 0, 20,  (0, 255, 255)))
                self.player1.tempo_asteroid = 0

        if self.player2.tempo_asteroid > 30 and self.player2.lives > 0:
            if len(self.asteroids) < 10:
                self.asteroids.append(Enemy(self.player2, randint(360, 600), 0, 20,  (255, 0, 255)))
                self.player2.tempo_asteroid = 0


    def processa_evento(self, evento):
        if evento.type == KEYDOWN:
            if evento.key == K_a:
                self.player1.move(-6)
            elif evento.key == K_d:
                self.player1.move(6)
            elif evento.key == K_w:
                self.produce_shoot(self.player1)
            elif evento.key == K_LEFT:
                self.player2.move(-6)
            elif evento.key == K_RIGHT:
                self.player2.move(6)
            elif evento.key == K_UP:
                self.produce_shoot(self.player2)

        elif evento.type == KEYUP:
            if evento.key == K_a:
                self.player1.move(0)
            elif evento.key == K_d:
                self.player1.move(0)
            elif evento.key == K_LEFT:
                self.player2.move(0)
            elif evento.key == K_RIGHT:
                self.player2.move(0)
				
        elif evento.type == JOYAXISMOTION:
            if evento.joy == 0 and evento.axis == 0:
                self.player1.move(evento.value * 6)
            elif evento.joy == 1 and evento.axis == 0:
                self.player2.move(evento.value * 6)
        elif evento.type == JOYBUTTONDOWN:
            if evento.joy == 0 and evento.button == 1:
                self.produce_shoot(self.player1)
            elif evento.joy == 1 and evento.button == 1:
                self.produce_shoot(self.player2)

				
class Player(object):
    def __init__(self, x, y, w, h, img_left, img_right, img_center):
        self.rect = Rect(x, y, w, h)
        self.velX = 0
        self.tempo_recarga = 0
        self.tempo_asteroid = 0
        self.score = 0
        self.lives = 1
        self.img_right = pygame.image.load(img_right)
        self.img_left = pygame.image.load(img_left)
        self.img_center = pygame.image.load(img_center)
        self.image = self.img_center

    def draw(self, scr):
        # sprite player1
        if self.lives > 0:
            scr.blit(self.image, self.rect.topleft)

    def move(self, vel):
        self.velX = vel

    def update(self):
        # player 1 movement limits
        if self.lives > 0:
            self.tempo_recarga += 1
            self.tempo_asteroid += 1
            self.rect.x += self.velX
            if self.velX < 0:
                self.image =  self.img_left
            elif self.velX > 0:
                self.image = self.img_right
            else:
                self.image = self.img_center

    def reset_charge(self):
        self.tempo_recarga = 0

    def can_shoot(self):
        return self.tempo_recarga > 10 and self.lives > 0


class Enemy (object):
    #asteroide1 = [pygame.image.load('')]
    #asteroide2 = [pygame.image.load('')]

    def __init__(self, player_origem, x, y, raio, cor):
        self.owner = player_origem
        self.ast = pygame.image.load('asteroid.png')
        self.x = x
        self.y = y
        self.raio = raio
        self.cor = cor
        self.vel = 3
        self.etype = 0

    def update(self):
        self.y += self.vel

    def draw(self, scr):
        #pygame.draw.circle(scr, self.cor, (self.x, self.y), self.raio)
        scr.blit(self.ast, (self.x - 20, self.y - 20))


class Projetil(object):
    def __init__(self, player_origem, raio, cor):
        self.owner = player_origem
        self.x = self.owner.rect.x + round(self.owner.rect.w / 2)
        self.y = self.owner.rect.y
        self.raio = raio
        self.cor = cor
        self.vel = 8

    def draw(self, scr):
        pygame.draw.circle(scr, self.cor, (self.x, self.y), self.raio)
       # pygame.blit(tiro, (self.x, self.y))