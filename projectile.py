import pygame

class Rocket(pygame.sprite.Sprite):
    def __init__(self,launcher,side):
        super().__init__()
        self.image = pygame.image.load("assets/MainShipBullet/PNGs/main_ship_rocket/MainShipR-1.png")
        self.screen_x, self.screen_y = pygame.display.get_surface().get_size()
        self.image = pygame.transform.scale(self.image,((75/1280)*self.screen_x,(75/720)*self.screen_y))
        self.rect = self.image.get_rect()
        if side == "left": self.rect.y = launcher.rect.y-(13/720)*self.screen_y
        else: self.rect.y = launcher.rect.y+(36/720)*self.screen_y
        self.rect.x = launcher.rect.x + (40/1280)*self.screen_x
        self.launcher = launcher
        self.speed = (10/1280)*self.screen_x
        self.damage = 10

    def move(self):
        self.rect.x += self.speed
        if self.rect.x > self.screen_x:
            self.launcher.all_rocket.remove(self)

    def get_damage(self):
        return self.damage

class Bullet(pygame.sprite.Sprite):
    def __init__(self,launcher,side):
        super().__init__()
        self.image = pygame.image.load("assets/MainShipBullet/PNGs/main_ship_bullet/tile000.png")
        self.screen_x, self.screen_y = pygame.display.get_surface().get_size()
        self.image = pygame.transform.scale(self.image,((32/1280)*self.screen_x,(32/720)*self.screen_y))
        self.rect = self.image.get_rect()
        if side == "left": self.rect.y = launcher.rect.y+(13/720)*self.screen_y
        else: self.rect.y = launcher.rect.y+(53/720)*self.screen_y
        self.rect.x = launcher.rect.x+(17/1280)*self.screen_x
        self.launcher = launcher
        self.speed = (25/1280)*self.screen_x
        self.damage = 3

    def move(self):
        self.rect.x += self.speed
        if self.rect.x > self.screen_x:
            self.launcher.all_bullet.remove(self)

    def get_damage(self):
        return self.damage

class Bullet_cargo(pygame.sprite.Sprite):
    def __init__(self,launcher,dx,dy):
        super().__init__()
        self.image = pygame.image.load("assets/MainShipBullet/PNGs/main_ship_bullet/tile003.png")
        self.screen_x, self.screen_y = pygame.display.get_surface().get_size()
        self.image = pygame.transform.scale(self.image,((32/1280)*self.screen_x,(32/720)*self.screen_y))
        self.rect = self.image.get_rect()
        self.speed_x = launcher.rect.x
        self.speed_y = launcher.rect.x * ((launcher.rect.y-dy)/(launcher.rect.x-dx))
        self.speed_y = self.speed_y//40
        self.speed_x = self.speed_x//40
        self.rect.x = launcher.rect.x
        self.rect.y = launcher.rect.y
        self.damage = 1
        self.launcher = launcher

    def move(self):
        self.rect.y -= self.speed_y
        self.rect.x -= self.speed_x
        if self.rect.x > self.screen_x or self.rect.x < 0:
            self.launcher.all_bullet.remove(self)
        if self.rect.y > self.screen_y or self.rect.y < 0:
            self.launcher.all_bullet.remove(self)

    def get_damage(self):
        return self.damage

class Bullet_ally(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("assets/MainShipBullet/PNGs/main_ship_bullet/tile000.png")
        self.screen_x, self.screen_y = pygame.display.get_surface().get_size()
        self.image = pygame.transform.scale(self.image,((32/1280)*self.screen_x,(32/720)*self.screen_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.damage = 3

    def draw(self,screen):
        screen.blit(self.image,self.rect)

    def get_damage(self):
        return self.damage

class Rocket_ally(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("assets/MainShipBullet/PNGs/main_ship_rocket/MainShipR-1.png")
        self.screen_x, self.screen_y = pygame.display.get_surface().get_size()
        self.image = pygame.transform.scale(self.image,((75/1280)*self.screen_x,(75/720)*self.screen_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.damage = 10

    def draw(self,screen):
        screen.blit(self.image,self.rect)

    def get_damage(self):
        return self.damage
