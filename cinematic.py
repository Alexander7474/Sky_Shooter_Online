import pygame

class End_game:
    def __init__(self,cargo):
        self.time = 0
        self.screen_x,self.screen_y = pygame.display.get_surface().get_size()
        self.image_list = []
        for i in range(90):
            img = pygame.image.load("assets/cinematic/fatman.png")
            img = pygame.transform.scale(img,((100/1280)*self.screen_x,(55/720)*self.screen_y))
            img = pygame.transform.rotate(img,i)
            self.image_list.append(img)
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        self.rect.x = (self.screen_x-((100/1280)*self.screen_x))//2
        self.rect.y = self.screen_y//4
        self.cargo_speed_x = (cargo.rect.x-(self.screen_x/2))//60
        self.cargo_speed_y = (cargo.rect.y-((100/720)*self.screen_y))//60
        self.state = "cargo_move"
        self.exp_time = (450/720)*self.screen_y

    def draw(self,screen,cargo):
        if self.state == "cargo_move":
            if cargo.rect.x != self.screen_x/2 and cargo.rect.y != (100/720)*self.screen_y:
                cargo.rect.x-=self.cargo_speed_x
                cargo.rect.y-=self.cargo_speed_y
                screen.blit(cargo.image,cargo.rect)
            else:
                self.state = "drop_the_bomb"
        elif self.state == "drop_the_bomb":
            if self.time < 90:
                self.image = self.image_list[self.time]
            if self.time >90:
                self.rect.y+=1
            if self.time >self.exp_time:
                self.state = "boum"
            screen.blit(self.image,self.rect)
            screen.blit(cargo.image,cargo.rect)
            self.time+=1
        elif self.state == "boum":
            self.image = pygame.image.load('assets/cinematic/nuke.png')
            self.image = pygame.transform.scale(self.image,(self.screen_x,self.screen_y))
            self.rect = self.image.get_rect()
            self.time+=1
            screen.blit(self.image,self.rect)
            if self.time > self.exp_time+200:
                return True

        return False
