import pygame

class Rocket(pygame.sprite.Sprite):
    def __init__(self,launcher,side):
        super().__init__()
        self.image = pygame.image.load("assets/MainShipBullet/PNGs/main_ship_rocket/MainShipR-1.png")
        self.image = pygame.transform.scale(self.image,(75,75))
        self.rect = self.image.get_rect()
        if side == "left": self.rect.y = launcher.rect.y-13
        else: self.rect.y = launcher.rect.y+36
        self.rect.x = launcher.rect.x + 40
        self.launcher = launcher
        self.speed = 10
        self.damage = 10

    def move(self):
        self.rect.x += self.speed
        if self.rect.x > 1200:
            self.launcher.all_rocket.remove(self)

    def get_damage(self):
        return self.damage

class Bullet(pygame.sprite.Sprite):
    def __init__(self,launcher,side):
        super().__init__()
        self.image = pygame.image.load("assets/MainShipBullet/PNGs/main_ship_bullet/tile000.png")
        self.rect = self.image.get_rect()
        if side == "left": self.rect.y = launcher.rect.y+13
        else: self.rect.y = launcher.rect.y+53
        self.rect.x = launcher.rect.x+17
        self.launcher = launcher
        self.speed = 25
        self.damage = 3

    def move(self):
        self.rect.x += self.speed
        if self.rect.x > 1200:
            self.launcher.all_bullet.remove(self)

    def get_damage(self):
        return self.damage

class Bullet_cargo(pygame.sprite.Sprite):
    def __init__(self,launcher,dx,dy):
        super().__init__()
        self.image = pygame.image.load("assets/MainShipBullet/PNGs/main_ship_bullet/tile000.png")
        self.image = pygame.transform.rotate(self.image,180)
        self.rect = self.image.get_rect()
        self.speed_x = launcher.rect.x
        self.speed_y = launcher.rect.x * ((launcher.rect.y-dy)/(launcher.rect.x-dx))
        self.rect.x = launcher.rect.x
        self.rect.y = launcher.rect.y
        self.damage = 1
        self.launcher = launcher

    def move(self):
        sx = self.speed_y//40;sy = self.speed_x//40
        self.rect.y -= sx
        self.rect.x -= sy
        if self.rect.x > 1200 or self.rect.x < 0:
            self.launcher.all_bullet.remove(self)
        if self.rect.y > 675 or self.rect.y < 0:
            self.launcher.all_bullet.remove(self)

    def get_damage(self):
        return self.damage

class Bullet_ally(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("assets/MainShipBullet/PNGs/main_ship_bullet/tile000.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self,screen):
        screen.blit(self.image,self.rect)

class Rocket_ally(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("assets/MainShipBullet/PNGs/main_ship_rocket/MainShipR-1.png")
        self.image = pygame.transform.scale(self.image,(75,75))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self,screen):
        screen.blit(self.image,self.rect)