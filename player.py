import pygame

from gun import Rocket_launcher
from gun import Machine_gun

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/mainShip/PNGs/ship.png")
        w, h = pygame.display.get_surface().get_size()
        self.image = pygame.transform.scale(self.image,((100/1200)*w,(100/675)*h))
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 100
        self.speed = 5
        self.life = 100
        self.score = 0
        self.rocket_launcher = Rocket_launcher(self)
        self.machine_gun = Machine_gun(self)
        self.font = pygame.font.SysFont('Comic Sans MS', 30)


    def move(self,direct):
        #deplacement du joueur
        if self.rect.x > -50:
            if direct == "left": self.rect.x -= self.speed
        if self.rect.x < 1150:
            if direct == "right": self.rect.x += self.speed
        if direct == "up": self.rect.y -= self.speed
        if direct == "down": self.rect.y += self.speed
        #deplacement de l'autre cote de la fenetre sui depassement
        if self.rect.y < -50: self.rect.y = 625
        if self.rect.y > 625: self.rect.y = -50

    def get_projectile(self,type):
        if type == "rocket":
            return self.rocket_launcher.get_rocket()
        elif type == "bullet":
            return self.machine_gun.get_bullet()

    def draw_projectile(self,screen):
        for bullet in self.machine_gun.get_bullet():
            bullet.move()
        for rocket in self.rocket_launcher.get_rocket():
            rocket.move()
        self.machine_gun.get_bullet().draw(screen)
        self.rocket_launcher.get_rocket().draw(screen)

    def draw(self,screen):
        self.machine_gun.draw(screen,self)
        self.rocket_launcher.draw(screen,self)
        if self.rocket_launcher.get_state() == True:
            self.rocket_launcher.launcher()
        screen.blit(self.image,self.rect)
        self.draw_projectile(screen)

    def hud(self,game,screen,clock):
        text_life = self.font.render(str("life:" + str(self.life)), False, (255, 255, 255))
        screen.blit(text_life, (0,635))
        text_score = self.font.render(str("score:" + str(self.score)), False, (255, 255, 255))
        screen.blit(text_score, (1000,635))
        if self.rocket_launcher.get_timer() == 0:
            pygame.draw.circle(screen,(0,255,0),(15,615), 10, 0)
        else:
            if self.rocket_launcher.get_timer() <= 255:
                pygame.draw.circle(screen,(255,self.rocket_launcher.get_timer(),0),(15,615), 10, 0)
            else:
                self.rocket_launcher.rearms()
        text_fps = self.font.render(str(round(clock.get_fps(),1)), False,(255,255,255))
        screen.blit(text_fps,(0,0))
        text_cargo_life = self.font.render(str(game.cargo.get_life()), False, (255,255,255))
        screen.blit(text_cargo_life,(1000,450))

    def get_life(self):
        return self.life

    def damage(self,damage):
        self.life -= damage

    def add_score(self,add):
        self.score+=add
