import pygame
from random import randint

class Explosion(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        super().__init__()
        self.image_list = []
        for i in range(10):
            img = pygame.image.load("assets/explosion/tile00"+str(i)+".png")
            self.image_list.append(img)
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game
        self.time = 0

    def animation(self):
        """animation de l'explosion"""
        if self.time %4==0:
            if self.time < 9*4: self.image = self.image_list[self.time//4]
            else: self.game.remove_effect(self)
        self.time += 1

class Cloud(pygame.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        self.image_list = []
        for i in range(1):
            img = pygame.image.load("assets/bg/cloud-00"+str(i)+(".png"))
            img = pygame.transform.scale(img,(250,125))
            self.image_list.append(img)
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        self.rect.x = pygame.display.get_surface().get_size()[0]
        self.rect.y = randint(0,350)
        self.speed = 7
        self.game = game

    def animation(self):
        """animation des nuages"""
        self.rect.x -= self.speed
        if self.rect.x < -250:
            self.game.remove_effect(self)