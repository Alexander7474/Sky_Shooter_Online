import pygame
from random import randint
from game import *
import socket
import json

#pygame init
pygame.init()
pygame.font.init()

#initialisation des objets
screen_x = 1200
screen_y = 675
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()
bg = pygame.image.load('assets/bg/bg.png')
bg = pygame.transform.scale(bg,(3840,screen_y))
my_font = pygame.font.SysFont('Comic Sans MS', 30)

def menu():
    """menu du jeu"""
    try:
        file = open('score.txt', "r")
        score = file.read().split(":")
        best_score = score[1]
        file.close()
    except:
        best_score = "No best score"

    selected = 2
    text_button = ["Options","Online mode","Solo mode"]
    list_button = []
    for i in range(len(text_button)): list_button.append(my_font.render(text_button[i], False, (0, 0, 0)))
    coo_button = [((screen_x-list_button[0].get_width())//2,screen_y//1.5),
                ((screen_x-list_button[1].get_width())//2,screen_y//1.7),
                ((screen_x-list_button[2].get_width())//2,screen_y//2)]

    title_text = my_font.render("Sky Shooter", False, (0,0,0))
    best_score_text = my_font.render("Best score: "+best_score, False, (0,0,0))

    online_addr_select = False
    text = ''
    len_box = 140
    input_box = pygame.Rect((screen_x-len_box)//2,screen_y//2,len_box,32)

    running = True
    while running:

        screen.blit(bg,(0,0))
        if not online_addr_select:
            list_button[selected] = my_font.render(text_button[selected], False, (0, 255, 0))

            for i in range(len(list_button)):
                if i != selected: list_button[i] = my_font.render(text_button[i], False, (0, 0, 0))
                screen.blit(list_button[i], coo_button[i])

            screen.blit(title_text, ((screen_x-title_text.get_width())//2,screen_y//3.1))
            screen.blit(best_score_text, ((screen_x-best_score_text.get_width())//2,screen_y//2.8))

        else:
            txt_surface = my_font.render(text, True, (0,0,0))
            screen.blit(txt_surface, ((screen_x-len_box)//2, screen_y//2))
            pygame.draw.rect(screen, (0,0,0), input_box, 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if online_addr_select:
                    if event.key == pygame.K_RETURN:
                        print(text)
                        running = False;online_game(text)
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                if event.key == pygame.K_RETURN:
                    if selected == 2:
                        running = False;solo_game()
                    if selected == 1:
                        online_addr_select = True
                if event.key == pygame.K_UP:
                    if selected < len(list_button)-1: selected+=1
                    else: selected = 0
                if event.key == pygame.K_DOWN:
                    if selected > 0: selected-=1
                    else: selected = len(list_button)-1

        pygame.display.update()

def end_game(game):
    """fin de jeu"""
    game.clear_effect()
    for i in range(700):
        game.explosion(randint(0,1150),randint(0,625))
        game.update_effect(screen)
        text_title = my_font.render("Fin de Partie", False, (255, 255, 255))
        screen.blit(text_title, ((screen_x-text_title.get_width())/2,screen_y//2))
        pygame.display.update()
        #block the fps to 60
        clock.tick(60)
    try:
        file = open('score.txt', "r")
        score = file.read().split(":")
        score = int(score[1])
        file.close()
    except:
        score = 0
    if score < game.player.score:
        file = open('score.txt','w')
        file.write('score:'+str(game.player.score))
        file.close()
    menu()

def solo_game():
    """partie solo"""
    game = Game()
    running = True
    bg_x=0
    while running:
        #screen gestion
        screen.fill((0,0,0))

        #background
        bg_x-=5
        if bg_x < -3840:
            bg_x = 0
        screen.blit(bg,(bg_x,0))
        screen.blit(bg,(bg_x+3840,0))

        #update de la game
        game.game_update(screen,clock)

        #fin de game
        if game.player.get_life() <= 0: running=False;end_game(game)

        #gestion des events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            #detection des touches
            elif event.type == pygame.KEYDOWN:
                game.pressed[event.key] = True
                if event.key == pygame.K_w:
                    if game.player.rocket_launcher.get_state() == False:
                        game.player.rocket_launcher.launcher()
                if event.key == pygame.K_ESCAPE:
                    exit()
            elif event.type == pygame.KEYUP:
                game.pressed[event.key] = False
                if event.key == pygame.K_q:
                    game.player.machine_gun.stop_fire()

        pygame.display.update()
        #block the fps to 60
        clock.tick(60)

def online_game(addr):
    try:
        for i in addr.split("."):
            if int(i) > 255:
                menu()
    except:
        menu()
    server = socket.socket()
    server.connect((addr,5555))
    game = Game_Online()
    valid = "200"

    bg_x = 0

    msg = server.recv(1024).decode()
    print("matricule du client: "+msg)
    player_number = msg.split(',')[0]
    n_of_player = msg.split(',')[1]
    server.send(valid.encode())
    list_ally = []
    for i in range(int(n_of_player)):
        list_ally.append(Player())

    running = True
    while running:
        #screen gestion
        screen.fill((0,0,0))

        #background
        bg_x-=5
        if bg_x < -3840:
            bg_x = 0
        screen.blit(bg,(bg_x,0))
        screen.blit(bg,(bg_x+3840,0))

        dict_game = server.recv(1024).decode()
        dict_game = json.loads(dict_game)
        dict_game = game.game_update(screen,clock,list_ally,player_number,dict_game)

        #gestion des events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            #detection des touches
            elif event.type == pygame.KEYDOWN:
                game.pressed[event.key] = True
                if event.key == pygame.K_w:
                    if game.player.rocket_launcher.get_state() == False:
                        game.player.rocket_launcher.launcher()
                if event.key == pygame.K_ESCAPE:
                    exit()
            elif event.type == pygame.KEYUP:
                game.pressed[event.key] = False
                if event.key == pygame.K_q:
                    game.player.machine_gun.stop_fire()

        server.send(dict_game.encode())

        pygame.display.update()
        #block the fps to 60
        clock.tick(60)


    pygame.display.update()
    clock.tick(60)

if __name__ == '__main__':
    menu()
