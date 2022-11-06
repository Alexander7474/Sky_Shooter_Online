import pygame
from random import randint
from gun import Cargo_machine_gun

class Cargo(pygame.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        self.image = pygame.image.load("assets/cargo/cargo_1.png")
        self.screen_x, self.screen_y = pygame.display.get_surface().get_size()
        self.image = pygame.transform.scale(self.image,((474/1280)*self.screen_x,(184/720)*self.screen_y))
        self.rect = self.image.get_rect()
        self.rect.x = self.screen_x - (550/1280)*self.screen_x
        self.rect.y = (-100/720)*self.screen_y
        self.init_life = 500
        self.life = 500
        self.direction = "down"
        self.game = game
        self.machine_gun = Cargo_machine_gun(self)

    def respawn(self):
        """respawn le cargo"""
        self.image = pygame.image.load("assets/cargo/cargo_1.png")
        self.image = pygame.transform.scale(self.image,((474/1280)*self.screen_x,(184/720)*self.screen_y))
        self.rect.y = -100
        self.life = int(self.init_life * 1.25)
        self.init_life = self.life
        self.game.player.add_score(self.life//2)

    def draw(self,screen,player):
        """dessine le cargo"""
        screen.blit(self.image,self.rect)
        pygame.draw.rect(screen, (0,255,0), pygame.Rect(self.rect.x, self.rect.y+((200/720)*self.screen_y), ((self.life/2)/1280)*self.screen_x, (10/720)*self.screen_y))
        if self.life > 0:
            self.machine_gun.draw(screen,self,player)
            if self.direction == "down":   self.rect.y += 1
            if self.direction == "up": self.rect.y -= 1
            if self.rect.y > self.screen_y//1.8:  self.direction = "up"
            if self.rect.y < self.screen_y//3.5:  self.direction = "down"
        else:
            self.image = pygame.image.load("assets/cargo/cargo_1_down.png")
            self.image = pygame.transform.scale(self.image,((474/1280)*self.screen_x,(184/720)*self.screen_y))
            self.rect.y += 2
            self.game.explosion(self.rect.x+randint(0,int((474/1280)*self.screen_x)),self.rect.y+randint(0,int((184/720)*self.screen_y)))
        if self.rect.y >= self.screen_y+(200/720)*self.screen_y:
            self.respawn()

    def damage(self,damage):
        self.life -= damage

    def get_life(self):
        return self.life
