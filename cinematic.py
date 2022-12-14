import pygame

class End_game:
    def __init__(self):
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
        self.state = "cam_trans"
        self.exp_time = (225/720)*self.screen_y
        self.cam_trans_state = 0

    def draw(self,screen,player,cargo,bg):
        if self.state == "cam_trans":
            if self.cam_trans_state < self.screen_y//2:
                screen.fill((0,0,0))
                screen.blit(bg,(0,0))
                pygame.draw.rect(screen,(0,0,0),pygame.Rect(0, self.screen_y-self.cam_trans_state, self.screen_x, self.screen_y//2))
                pygame.draw.rect(screen,(0,0,0),pygame.Rect(0, -(self.screen_y//2)+self.cam_trans_state, self.screen_x, self.screen_y//2))
                self.cam_trans_state +=4
            else:
                self.state = "drop_the_bomb"
        elif self.state == "drop_the_bomb":
            screen.fill((0,0,0))
            screen.blit(bg,(0,0))
            if self.cam_trans_state < self.screen_y//3:
                if self.time < 90:
                    self.image = self.image_list[self.time]
                self.rect.y+=2
                if self.time >self.exp_time:
                    self.state = "boum"
                screen.blit(self.image,self.rect)
                self.time+=1
            pygame.draw.rect(screen,(0,0,0),pygame.Rect(0, self.screen_y-self.cam_trans_state, self.screen_x, self.screen_y//2))
            pygame.draw.rect(screen,(0,0,0),pygame.Rect(0, -(self.screen_y//2)+self.cam_trans_state, self.screen_x, self.screen_y//2))
            self.cam_trans_state -=4
        elif self.state == "boum":
            self.image = pygame.image.load('assets/cinematic/nuke.png')
            self.image = pygame.transform.scale(self.image,(self.screen_x,self.screen_y))
            self.rect = self.image.get_rect()
            self.time+=1
            screen.blit(self.image,self.rect)
            if self.time > self.exp_time+200:
                return True

        return False
