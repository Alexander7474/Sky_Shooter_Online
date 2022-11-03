import pygame
from random import randint
from gun import Cargo_machine_gun

class Cargo(pygame.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        self.image = pygame.image.load("assets/cargo/cargo_1.png")
        self.w, self.h = pygame.display.get_surface().get_size()
        self.image = pygame.transform.scale(self.image,(((237*2)/1200)*self.w,((92*2)/675)*self.h))
        self.rect = self.image.get_rect()
        self.rect.x = 690
        self.rect.y = -100
        self.init_life = 500
        self.life = 500
        self.way = "down"
        self.game = game
        self.machine_gun = Cargo_machine_gun(self)

    def respawn(self):
        self.image = pygame.image.load("assets/cargo/cargo_1.png")
        self.image = pygame.transform.scale(self.image,(((237*2)/1200)*self.w,((92*2)/675)*self.h))
        self.rect.y = -100
        self.life = int(self.init_life * 1.25)
        self.init_life = self.life
        self.game.player.add_score(self.life//2)

    def draw(self,screen,player):
        screen.blit(self.image,self.rect)
        """dessine le cargo"""
        if self.life > 0:
            self.machine_gun.draw(screen,self,player)
            if self.way == "down":   self.rect.y += 1
            if self.way == "up": self.rect.y -= 1
            if self.rect.y > 300:  self.way = "up"
            if self.rect.y < 200:  self.way = "down"
        else:
            self.image = pygame.image.load("assets/cargo/cargo_1_down.png")
            self.image = pygame.transform.scale(self.image,(((237*2)/1200)*self.w,((92*2)/675)*self.h))
            self.rect.y += 2
            self.game.explosion(self.rect.x+randint(0,((237*2)/1200)*self.w),self.rect.y+randint(0,((92*2)/675)*self.h))
        if self.rect.y >= 750:
            self.respawn()

    def damage(self,damage):
        self.life -= damage
    
    def get_life(self):
        return self.life