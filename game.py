from distutils.dep_util import newer_group
import pygame
from player import Player
from enemy import Enemy
from effects import *
from random import randint
from cargo import Cargo
from projectile import *
import json

class Game:
    def __init__(self):
        self.player = Player()
        self.cargo = Cargo(self)
        self.all_enemy = pygame.sprite.Group()
        self.all_effect = pygame.sprite.Group()
        self.pressed = {}
    
    def spawn_enemy(self,r):
        if randint(0,r) == 1 and len(self.all_enemy) < 11:
            self.all_enemy.add(Enemy(self))

    def explosion(self,x,y):
        self.all_effect.add(Explosion(self,x,y))

    def remove_effect(self,eff):
        self.all_effect.remove(eff)

    def remove_enemy(self,en):
        self.all_enemy.remove(en)

    def spawn_cloud(self,r):
        if randint(0,r) == 1:
            self.all_effect.add(Cloud(self))

    def collision(self): #a optimiser (veryyyyy important)
        """gestion des collisions pour tous les objets"""
        for enemy in self.all_enemy:
            collide = enemy.rect.colliderect(self.player)
            if collide:
                self.player.damage(enemy.get_damage())
                enemy.destroy()
            for rocket in self.player.get_projectile("rocket"):
                collide = rocket.rect.colliderect(enemy)
                if collide:
                    self.explosion(rocket.rect.x-20,rocket.rect.y-40)
                    enemy.hit(rocket,self)
                    self.player.get_projectile("rocket").remove(rocket)
            for bullet in self.player.get_projectile("bullet"):
                collide = bullet.rect.colliderect(enemy)
                if collide:
                    enemy.hit(bullet,self)
                    self.player.get_projectile("bullet").remove(bullet)
        for rocket in self.player.get_projectile("rocket"):
            collide = self.cargo.rect.colliderect(rocket)
            if collide:
                self.explosion(rocket.rect.x-20,rocket.rect.y-40)
                self.cargo.damage(rocket.get_damage())
                self.player.get_projectile("rocket").remove(rocket)
        for bullet in self.player.get_projectile("bullet"):
            collide = self.cargo.rect.colliderect(bullet)
            if collide:
                self.cargo.damage(bullet.get_damage())
                self.player.get_projectile("bullet").remove(bullet)
        for bullet in self.cargo.machine_gun.get_bullet():
            collide = self.player.rect.colliderect(bullet)
            if collide:
                self.cargo.machine_gun.get_bullet().remove(bullet)
                self.player.damage(bullet.get_damage())

    def update_effect(self,screen):
        for effect in self.all_effect:
            effect.animation()
        self.all_effect.draw(screen)

    def clear_effect(self):
        self.all_effect = pygame.sprite.Group()
                
    def game_update(self,screen,clock):
        #update des effets
        self.update_effect(screen)
        self.spawn_cloud(75)

        #update du joueur
        self.player.hud(self,screen,clock)
        self.player.draw(screen)

        #update du cargo
        self.cargo.draw(screen,self.player)

        #spawn des enemy
        self.spawn_enemy(60)
        
        #update des enemy
        for enemy in self.all_enemy:
            self.all_enemy.draw(screen)
            enemy.move(self.player)
        self.collision()

        #gestion des touches
        if self.pressed.get(pygame.K_UP): # move key
            self.player.move("up")
        if self.pressed.get(pygame.K_DOWN):
            self.player.move("down")
        if self.pressed.get(pygame.K_RIGHT):
            self.player.move("right")
        if self.pressed.get(pygame.K_LEFT):
            self.player.move("left")
        if self.pressed.get(pygame.K_q): #fire keys
            self.player.machine_gun.fire()

class Game_Online:
    def __init__(self):
        self.player = Player()
        self.cargo = Cargo(self)
        self.all_enemy = pygame.sprite.Group()
        self.all_effect = pygame.sprite.Group()
        self.pressed = {}

    def update_effect(self,screen):
        for effect in self.all_effect:
            effect.animation()
        self.all_effect.draw(screen)

    def explosion(self,x,y):
        self.all_effect.add(Explosion(self,x,y))

    def remove_effect(self,eff):
        self.all_effect.remove(eff)

    def collision(self): #a optimiser (veryyyyy important)
        """gestion des collisions pour tous les objets"""
        for enemy in self.all_enemy:
            collide = enemy.rect.colliderect(self.player)
            if collide:
                self.player.damage(enemy.get_damage())
                enemy.destroy()
            for rocket in self.player.get_projectile("rocket"):
                collide = rocket.rect.colliderect(enemy)
                if collide:
                    self.explosion(rocket.rect.x-20,rocket.rect.y-40)
                    enemy.hit(rocket,self)
                    self.player.get_projectile("rocket").remove(rocket)
            for bullet in self.player.get_projectile("bullet"):
                collide = bullet.rect.colliderect(enemy)
                if collide:
                    enemy.hit(bullet,self)
                    self.player.get_projectile("bullet").remove(bullet)
        for rocket in self.player.get_projectile("rocket"):
            collide = self.cargo.rect.colliderect(rocket)
            if collide:
                self.explosion(rocket.rect.x-20,rocket.rect.y-40)
                self.cargo.damage(rocket.get_damage())
                self.player.get_projectile("rocket").remove(rocket)
        for bullet in self.player.get_projectile("bullet"):
            collide = self.cargo.rect.colliderect(bullet)
            if collide:
                self.cargo.damage(bullet.get_damage())
                self.player.get_projectile("bullet").remove(bullet)
        for bullet in self.cargo.machine_gun.get_bullet():
            collide = self.player.rect.colliderect(bullet)
            if collide:
                self.cargo.machine_gun.get_bullet().remove(bullet)
                self.player.damage(bullet.get_damage())

    def game_update(self,screen,clock,list_ally,player_number,dict_game):
        #update du cargo
        self.cargo.draw(screen,self.player)
        self.cargo.life = dict_game["cargo_life"]

        #update des effets
        self.update_effect(screen)

        self.collision()

        #update du joueur
        self.player.hud(self,screen,clock)
        self.player.draw(screen)

        bullet_ally = pygame.sprite.Group()
        rocket_ally = pygame.sprite.Group()

        for i in range(len(list_ally)):
            if i != int(player_number):
                list_ally[i].rect.x = dict_game['players']['player'+str(i)]["coo"][0]
                list_ally[i].rect.y = dict_game['players']['player'+str(i)]["coo"][1]
                list_ally[i].draw(screen)
                for ib in dict_game['players']['player'+str(i)]['bullets']:
                    bullet_ally.add(Bullet_ally(ib[0],ib[1]))
                for ir in dict_game['players']['player'+str(i)]['rockets']:
                    rocket_ally.add(Rocket_ally(ir[0],ir[1]))

        for bullet in bullet_ally:
            bullet.draw(screen)
        for rocket in rocket_ally:
            rocket.draw(screen)

        #gestion des touches
        if self.pressed.get(pygame.K_UP): # move key
            self.player.move("up")
        if self.pressed.get(pygame.K_DOWN):
            self.player.move("down")
        if self.pressed.get(pygame.K_RIGHT):
            self.player.move("right")
        if self.pressed.get(pygame.K_LEFT):
            self.player.move("left")
        if self.pressed.get(pygame.K_q): #fire keys
            self.player.machine_gun.fire()

        bl = []
        for bullet in self.player.machine_gun.all_bullet:
            bl.append((bullet.rect.x,bullet.rect.y))
        dict_game['players']['player'+str(player_number)]["bullets"] = bl
        rl = []
        for rocket in self.player.rocket_launcher.all_rocket:
            rl.append((rocket.rect.x,rocket.rect.y))
        dict_game['players']['player'+str(player_number)]["rockets"] = rl
        dict_game["cargo_life"] = self.cargo.get_life()

        dict_game["players"]["player"+player_number]["coo"] = (self.player.rect.x,self.player.rect.y)
        return json.dumps(dict_game)