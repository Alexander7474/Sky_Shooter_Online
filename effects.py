import pygame
from random import randint

class Explosion(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        super().__init__()
        self.image_list = []
        screen_x, screen_y = pygame.display.get_surface().get_size()
        for i in range(10):
            img = pygame.image.load("assets/explosion/tile00"+str(i)+".png")
            img = pygame.transform.scale(img,((96/1280)*screen_x,(96/720)*screen_y))
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
        self.screen_x, self.screen_y = pygame.display.get_surface().get_size()
        for i in range(1):
            img = pygame.image.load("assets/bg/cloud-00"+str(i)+(".png"))
            img = pygame.transform.scale(img,((250/1280)*self.screen_x,(125/720)*self.screen_y))
            self.image_list.append(img)
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        self.rect.x = pygame.display.get_surface().get_size()[0]
        self.rect.y = randint(0,self.screen_y//1.5)
        self.speed = (7/1280)*self.screen_x
        self.game = game

    def animation(self):
        """animation des nuages"""
        self.rect.x -= self.speed
        if self.rect.x < (-250/1280)*self.screen_x:
            self.game.remove_effect(self)
