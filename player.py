import pygame

from gun import Rocket_launcher
from gun import Machine_gun

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/mainShip/PNGs/ship.png")
        self.screen_x, self.screen_y = pygame.display.get_surface().get_size()
        self.image = pygame.transform.scale(self.image,((100/1280)*self.screen_x,(100/720)*self.screen_y))
        self.rect = self.image.get_rect()
        self.rect.x = self.screen_x//4
        self.rect.y = self.screen_y//2
        self.speed = (5/1280)*self.screen_x
        self.life = 100
        self.score = 0
        self.rocket_launcher = Rocket_launcher(self)
        self.machine_gun = Machine_gun(self)
        self.font = pygame.font.SysFont('Comic Sans MS', 30)


    def move(self,direct):
        #deplacement du joueur
        if self.rect.x > (-50/1280)*self.screen_x:
            if direct == "left": self.rect.x -= self.speed
        if self.rect.x < self.screen_x+(80/1280)+self.screen_x:
            if direct == "right": self.rect.x += self.speed
        if direct == "up": self.rect.y -= self.speed
        if direct == "down": self.rect.y += self.speed
        #deplacement de l'autre cote de la fenetre sui depassement
        if self.rect.y < (-80/720)*self.screen_y: self.rect.y = self.screen_y-(-20/720)*self.screen_y
        if self.rect.y > self.screen_y-(-20/720)*self.screen_y: self.rect.y = (-80/720)*self.screen_y

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
        text_life = self.font.render(str("Life:" + str(self.life)), False, (255, 255, 255))
        screen.blit(text_life, (0,self.screen_y-20))
        text_score = self.font.render(str("Score:" + str(self.score)), False, (255, 255, 255))
        screen.blit(text_score, (self.screen_x-200,self.screen_y-20))
        if self.rocket_launcher.get_timer() == 0:
            pygame.draw.circle(screen,(0,255,0),(10,self.screen_y-40), 10, 0)
        else:
            if self.rocket_launcher.get_timer() <= 255:
                pygame.draw.circle(screen,(255,self.rocket_launcher.get_timer(),0),(10,self.screen_y-40), 10, 0)
            else:
                self.rocket_launcher.rearms()
        text_fps = self.font.render(str(round(clock.get_fps(),1)), False,(255,255,255))
        screen.blit(text_fps,(0,0))
        text_cargo_life = self.font.render("Cargo life:"+str(game.cargo.get_life()), False, (255,255,255))
        screen.blit(text_cargo_life,(self.screen_x-200,self.screen_y-40))

    def get_life(self):
        return self.life

    def damage(self,damage):
        self.life -= damage

    def add_score(self,add):
        self.score+=add

    def get_score(self):
        return self.score
