import pygame
import math
from random import randint
from projectile import *

class Rocket_launcher(pygame.sprite.Sprite):
    def __init__(self,player):
        super().__init__()
        self.image_list = []
        for i in range(17):
            if i < 10: img = pygame.image.load("assets/MainShipWeapon/PNGs/missile-launcher/tile00"+str(i)+".png")
            else: img = pygame.image.load("assets/MainShipWeapon/PNGs/missile-launcher/tile0"+str(i)+".png")
            screen_x, screen_y = pygame.display.get_surface().get_size()
            img = pygame.transform.scale(img,((100/1280)*screen_x,(100/720)*screen_y))
            self.image_list.append(img)
        self.image = self.image_list[0]
        self.all_rocket = pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        self.side = 0
        self.launch_state = False
        self.launch_n = 0
        self.anim_time = 0
        self.timer = 0

    def launcher(self):
        if self.anim_time %3==0:
            if self.launch_n <17:
                self.launch_state = True
                self.image = self.image_list[self.launch_n]
                if self.launch_n%2 == 0 and self.launch_n > 0 and self.launch_n < 14:
                    if self.side%2 == 0:self.all_rocket.add(Rocket(self,"left"))
                    else:self.all_rocket.add(Rocket(self,"right"))
                    self.side += 1
                self.launch_n += 1
        self.anim_time += 1
        self.timer+=1

    def draw(self,screen,player):
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        screen.blit(self.image,self.rect)

    def rearms(self):
        self.side = 0
        self.launch_state = False
        self.launch_n = 0
        self.anim_time = 0
        self.timer = 0
        self.image = self.image_list[0]

    def get_rocket(self):
        return self.all_rocket

    def get_state(self):
        return self.launch_state

    def get_timer(self):
        return self.timer

    def reset_timer(self):
        self.timer = 0

class Machine_gun(pygame.sprite.Sprite):
    def __init__(self,player):
        super().__init__()
        self.image_list = []
        for i in range(7):
            img = pygame.image.load("assets/MainShipWeapon/PNGs/machine-gun/tile00"+str(i)+".png")
            screen_x, screen_y = pygame.display.get_surface().get_size()
            img = pygame.transform.scale(img,((100/1280)*screen_x,(100/720)*screen_y))
            self.image_list.append(img)
        self.image = self.image_list[0]
        self.all_bullet = pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        self.sound = pygame.mixer.Sound("assets/song_effect/gunshot/bullet_shot.mp3")
        self.time = 0

    def fire(self):
        if self.time == 1:
            self.all_bullet.add(Bullet(self,"left"))
            self.sound.play()
        if self.time == 2:
            self.all_bullet.add(Bullet(self,"right"))
            self.sound.play()
        t_n = self.time%7
        self.image = self.image_list[t_n]
        if self.time > 6:
            self.time = 0
        self.time += 1

    def stop_fire(self):
        self.image = self.image_list[0]

    def draw(self,screen,player):
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        screen.blit(self.image,self.rect)

    def get_bullet(self):
        return self.all_bullet

class Cargo_machine_gun(pygame.sprite.Sprite):
    def __init__(self,cargo):
        super().__init__()
        self.image = pygame.image.load("assets/cargo/gun/machine_gun.png")
        self.screen_x, self.screen_y = pygame.display.get_surface().get_size()
        self.image = pygame.transform.scale(self.image,(((13*2)/1280)*self.screen_x,((13*2)/720)*self.screen_y))
        self.rect = self.image.get_rect()
        self.rect.x = cargo.rect.x
        self.rect.y = cargo.rect.y
        self.image_list = []
        for i in range (1,361):
            self.image_list.append(pygame.transform.rotate(self.image,i))
        self.all_bullet = pygame.sprite.Group()
        self.shoot_time = randint(80,280)
        self.time = 0
        self.brrrt1 = pygame.mixer.Sound("assets/song_effect/gunshot/brrrt1.mp3")
        self.brrrt2 = pygame.mixer.Sound("assets/song_effect/gunshot/brrrt2.mp3")

    def draw_projectiles(self,screen):
        """dessine les projectiles des guns cargo"""
        for bullet in self.all_bullet:
            bullet.move()
        self.all_bullet.draw(screen)

    def draw(self,screen,cargo,player):
        """met a jour le machine gun du cargo puis le dessine"""
        if self.time == self.shoot_time-40:
            if randint(0,1) == 0:self.brrrt1.play()
            else:self.brrrt2.play()
        if self.time >= self.shoot_time-40:
            self.fire(player)
        if self.time >= self.shoot_time:
            self.time = 0;self.shoot_time = randint(80,280)
        self.draw_projectiles(screen)
        x = (self.rect.x-player.rect.x)
        y = (self.rect.y-player.rect.y)
        if player.rect.x < self.rect.x-10:
            if y > 0:
                arctan = 90-math.degrees(math.atan(x/y))
                self.image = self.image_list[359-int(arctan)]
            elif y < 0:
                arctan = 90-math.degrees(math.atan(x/y))
                self.image = self.image_list[180-int(arctan)]
        self.rect.x = cargo.rect.x +((65/1280)*self.screen_x)
        self.rect.y = cargo.rect.y +((132/720)*self.screen_y)
        screen.blit(self.image,self.rect)
        self.time+=1

    def get_bullet(self):
        return self.all_bullet

    def fire(self,player):
        """tirer en direction d'un joueur"""
        if player.rect.x < self.rect.x-10:
            self.all_bullet.add(Bullet_cargo(self,player.rect.x,player.rect.y))
