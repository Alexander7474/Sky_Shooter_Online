import pygame
from random import randint

class Enemy(pygame.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        self.image_list = []
        for i in range(4):
            img = pygame.image.load("assets/enemy/enemy1/enemy-00"+str(i)+".png")
            w, h = pygame.display.get_surface().get_size()
            img = pygame.transform.scale(img,((80/1200)*w,(80/675)*h))
            self.image_list.append(img)
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        self.rect.x = 1200
        self.rect.y = randint(0,650)
        self.game = game
        self.damage = 5
        self.life = 10

    def move(self,player):
        x=(self.rect.x - player.rect.x)/40
        y=(self.rect.y - player.rect.y-40)/40
        self.rect.x-=x
        self.rect.y-=y

    def hit(self,projectile,game):
        self.life -= projectile.get_damage()
        if self.life < 1:
            self.destroy()
        elif self.life < 4:
            self.image = self.image_list[3]
        elif self.life < 6:
            self.image = self.image_list[2]
        elif self.life < 8:
            self.image = self.image_list[1]
        game.player.add_score(projectile.damage)

    def destroy(self):
        self.game.remove_enemy(self)
        self.game.explosion(self.rect.x,self.rect.y)

    def get_damage(self):
        return self.damage

    def get_life(self):
        return self.life

class Enemy_ally(pygame.sprite.Sprite):
    def __init__(self,x,y,life):
        super().__init__()
        self.image = pygame.image.load("assets/enemy/enemy1/enemy-001.png")
        self.image = pygame.transform.scale(self.image,(80,80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.life = life

    def draw(self,screen):
        screen.blit(self.image,self.rect)
