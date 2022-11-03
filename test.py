import pygame
from game import *
from projectile import *

pygame.init()
pygame.display.set_mode((1200,675))
game = pygame.sprite.Group()
list = [2,5,6,7]
list1 = [2,8,6,31]
print(list+list1)