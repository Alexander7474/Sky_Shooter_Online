import pygame
from random import randint
from game import *
import socket
import json

#pygame init
pygame.init()
pygame.font.init()

#initialisation des variables principales
#recupérations des infos de la config
def config():
    """fonction qui créé les variables global en fonction du fichier config.txt"""
    global CONFIG
    global SCREEN_X
    global SCREEN_Y
    global FPS
    global SOUND_VOLUME
    global SOLO_SCORE
    global screen
    global clock
    global bg
    global my_font
    file = open('config.txt', "r");CONFIG = file.read().split("\n");file.close()
    SCREEN_X = int(CONFIG[1].split(':')[1].split('x')[0])
    SCREEN_Y = int(CONFIG[1].split(':')[1].split('x')[1])
    FPS = int(CONFIG[3].split(':')[1])
    SOUND_VOLUME = int(CONFIG[2].split(':')[1])
    SOLO_SCORE = int(CONFIG[0].split(':')[1])
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    clock = pygame.time.Clock()
    bg = pygame.image.load('assets/bg/bg.png')
    bg = pygame.transform.scale(bg,((3840/1280)*SCREEN_X,SCREEN_Y))
    my_font = pygame.font.SysFont('Comic Sans MS', 30)

def main_menu():
    """fonction qui affiche le menu principale"""
    config()
    selected = 0
    text_button = ["Solo mode","Online mode","Options","Quitter"]
    list_button = []
    for i in range(len(text_button)): list_button.append(my_font.render(text_button[i], False, (0, 0, 0)))
    coo_button = [((SCREEN_X-list_button[0].get_width())//2,SCREEN_Y//2),
                ((SCREEN_X-list_button[1].get_width())//2,SCREEN_Y//1.85),
                ((SCREEN_X-list_button[2].get_width())//2,SCREEN_Y//1.7),
                ((SCREEN_X-list_button[3].get_width())//2,SCREEN_Y//1.55)]

    title_text = my_font.render("Sky Shooter", False, (0,0,0))
    best_score_text = my_font.render("Best score: "+str(SOLO_SCORE), False, (0,0,0))

    online_addr_select = False
    text = ''
    len_box = 140
    input_box = pygame.Rect((SCREEN_X-len_box)//2,SCREEN_Y//2,len_box,32)

    running = True
    while running:
        screen.blit(bg,(0,0))
        if not online_addr_select:
            list_button[selected] = my_font.render(text_button[selected], False, (0, 255, 0))
            for i in range(len(list_button)):
                if i != selected: list_button[i] = my_font.render(text_button[i], False, (0, 0, 0))
                screen.blit(list_button[i], coo_button[i])
            screen.blit(title_text, ((SCREEN_X-title_text.get_width())//2,SCREEN_Y//3.1))
            screen.blit(best_score_text, ((SCREEN_X-best_score_text.get_width())//2,SCREEN_Y//2.8))
        else:
            txt_surface = my_font.render(text, True, (0,0,0))
            screen.blit(txt_surface, ((SCREEN_X-len_box)//2, SCREEN_Y//2))
            pygame.draw.rect(screen, (0,0,0), input_box, 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if online_addr_select:
                    if event.key == pygame.K_RETURN:
                        co_text = my_font.render("En attente de réponse du "+text, False, (0,0,0))
                        screen.blit(co_text, ((SCREEN_X-co_text.get_width())//2,SCREEN_Y//2.5))
                        pygame.display.update()
                        running = False;online_game(text)
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        online_addr_select = False
                    else:
                        text += event.unicode
                if event.key == pygame.K_RETURN:
                    if selected == 0:
                        running = False;solo_game()
                    if selected == 1:
                        online_addr_select = True
                    if selected == 2:
                        running = False;option_menu()
                    if selected == 3:
                        exit()
                if event.key == pygame.K_UP:
                    if selected > 0: selected-=1
                    else: selected = len(list_button)-1
                if event.key == pygame.K_DOWN:
                    if selected < len(list_button)-1: selected+=1
                    else: selected = 0

        pygame.display.update()

def option_menu():
    """fonction qui affiche le menu des options"""
    title_text = my_font.render("Sky Shooter", False, (0,0,0))
    res = ["640x360","800x450","960x540","1024x576","1280x720","1366x768","1600x900","1920x1080","2048x1152","2560x1440","2880x1620","3200x1800","3840x2160"]
    volume = SOUND_VOLUME
    fps_limit = FPS

    selected = 0
    selected_res = 0
    for i in range(len(res)):
        if res[i] == CONFIG[1].split(':')[1]:
            selected_res = i

    text_button = ["Résolution: "+res[selected_res],"Volume: "+str(volume),"Fps limite: "+str(fps_limit),"Touches","Retour et appliquer"]
    list_button = []
    for i in range(len(text_button)): list_button.append(my_font.render(text_button[i], False, (0, 0, 0)))
    coo_button = [((SCREEN_X-list_button[0].get_width())//2,SCREEN_Y//2),
                ((SCREEN_X-list_button[1].get_width())//2,SCREEN_Y//1.85),
                ((SCREEN_X-list_button[2].get_width())//2,SCREEN_Y//1.7),
                ((SCREEN_X-list_button[3].get_width())//2,SCREEN_Y//1.55),
                ((SCREEN_X-list_button[4].get_width())//2,SCREEN_Y//1.40)]

    running = True
    while running:
        screen.blit(bg,(0,0))
        list_button[selected] = my_font.render(text_button[selected], False, (0, 255, 0))
        for i in range(len(list_button)):
            if i != selected: list_button[i] = my_font.render(text_button[i], False, (0, 0, 0))
            screen.blit(list_button[i], coo_button[i])
        text_button[0] = "Résolution: "+res[selected_res]
        text_button[1] = "Volume: "+str(volume)
        text_button[2] = "Fps limite: "+str(fps_limit)

        screen.blit(title_text, ((SCREEN_X-title_text.get_width())//2,SCREEN_Y//3.1))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if selected == 4:
                        file = open('config.txt','w')
                        CONFIG[1] = "screen:"+str(res[selected_res])
                        CONFIG[2] = "volume:"+str(volume)
                        CONFIG[3] = "fps:"+str(fps_limit)
                        new_config = ""
                        for co in CONFIG: new_config += co+"\n"
                        file.write(new_config)
                        file.close()
                        running = False;main_menu()
                    if selected == 3:
                        running = False;touches_menu()
                if event.key == pygame.K_UP:
                    if selected > 0: selected-=1
                    else: selected = len(list_button)-1
                if event.key == pygame.K_DOWN:
                    if selected < len(list_button)-1: selected+=1
                    else: selected = 0
                if event.key == pygame.K_LEFT:
                    if selected == 0:
                        if selected_res > 0: selected_res-=1
                        else: selected_res = len(res)-1
                    elif selected == 1:
                        if volume > 0: volume-=1
                        else: volume = 100
                    elif selected == 2:
                        if fps_limit > 15: fps_limit-=1
                        else: fps_limit = 120
                if event.key == pygame.K_RIGHT:
                    if selected == 0:
                        if selected_res < len(res)-1: selected_res+=1
                        else: selected_res = 0
                    elif selected == 1:
                        if volume < 100: volume+=1
                        else: volume = 0
                    elif selected == 2:
                        if fps_limit < 120: fps_limit+=1
                        else: fps_limit = 15
                if event.key == pygame.K_ESCAPE:
                    running = False;main_menu()

        pygame.display.update()

def touches_menu():
    screen.blit(bg,(0,0))
    running = True
    title_text = my_font.render("Sky Shooter", False, (0,0,0))
    up_text = my_font.render("Haut:UpArrow", False, (0,0,0))
    middle_text = my_font.render("Gauche:LeftArrow Droite:RightArrow", False, (0,0,0))
    down_text = my_font.render("Bas:DownArrow", False, (0,0,0))
    missile_text = my_font.render("Tirer avec les missiles:W", False, (0,0,0))
    mgun_text = my_font.render("Tirer avec le machine gun:Q", False, (0,0,0))
    while running:
        screen.blit(title_text, ((SCREEN_X-title_text.get_width())//2,SCREEN_Y//3.1))
        screen.blit(up_text, ((SCREEN_X-up_text.get_width())//2,SCREEN_Y//2.1))
        screen.blit(middle_text, ((SCREEN_X-middle_text.get_width())//2,SCREEN_Y//2))
        screen.blit(down_text, ((SCREEN_X-down_text.get_width())//2,SCREEN_Y//1.9))
        screen.blit(missile_text, ((SCREEN_X-missile_text.get_width())//2,SCREEN_Y//1.7))
        screen.blit(mgun_text, ((SCREEN_X-mgun_text.get_width())//2,SCREEN_Y//1.6))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False;option_menu()
        pygame.display.update()

def end_game(game):
    """fonction de fin jeu qui modifie les scores"""
    game.clear_effect()
    for i in range(500):
        if randint(0,1) == 0: game.explosion(randint(0-50,SCREEN_X),randint(0-50,SCREEN_Y))
        game.update_effect(screen)
        text_title = my_font.render("Fin de Partie", False, (255, 255, 255))
        screen.blit(text_title, ((SCREEN_X-text_title.get_width())/2,SCREEN_Y//2))
        pygame.display.update()
        #block the fps to 60
        clock.tick(FPS)
    if SOLO_SCORE < game.player.get_score():
        file = open('config.txt','w')
        CONFIG[0] = "score:"+str(game.player.get_score())
        new_config = ""
        for i in CONFIG: new_config += i+"\n"
        file.write(new_config)
        file.close()
    main_menu()

def solo_game():
    """fonction qui gère une partie solo"""
    game = Game()
    running = True
    bg_x=0
    while running:
        #screen gestion
        screen.fill((0,0,0))

        #background
        bg_x-=(5/1280)*SCREEN_X
        if bg_x < -(3840/1280)*SCREEN_X:
            bg_x = 0
        screen.blit(bg,(bg_x,0))
        screen.blit(bg,(bg_x+(3840/1280)*SCREEN_X,0))

        #update de la game
        game.game_update(screen,clock)

        #fin de game
        if game.player.get_life() < 0: running=False;end_game(game)

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
                    running = False
                    main_menu()
            elif event.type == pygame.KEYUP:
                game.pressed[event.key] = False
                if event.key == pygame.K_q:
                    game.player.machine_gun.stop_fire()

        pygame.display.update()
        #block the fps
        clock.tick(FPS)

def online_game(addr):
    """fonction qui gère la partie multijoueur et la communication avec le serveur"""
    #verification de la validité de l'adresse saisie
    try:
        for i in addr.split("."):
            if int(i) > 255:
                main_menu()
    except:
        print("Adresse entré non valide")
        main_menu()
    server = socket.socket()
    #tentatie de connexion
    try:server.connect((addr,5555))
    except:
        print("Serveur injoiniable, vérifier connexion")
        running = False
        main_menu()
    game = Game_Online()
    valid = "200"
    bg_x = 0
    #reception du matricule
    try:msg = server.recv(1024).decode()
    except:
        print("Impossible de recevoir le matricule")
        running = False
        main_menu()
    #envoie du code 200 pour valider la reception du matricule
    try:server.send(valid.encode())
    except:
        print("Serveur injoiniable, vérifier connexion")
        running = False
        main_menu()
    print("matricule du client: "+msg)
    player_number = msg.split(',')[0]
    n_of_player = msg.split(',')[1]
    list_ally = []
    #creation de la liste d'alliés
    for i in range(int(n_of_player)):
        list_ally.append(Player())

    running = True
    while running:
        #screen gestion
        screen.fill((0,0,0))

        #background
        bg_x-=(5/1280)*SCREEN_X
        if bg_x < -(3840/1280)*SCREEN_X:
            bg_x = 0
        screen.blit(bg,(bg_x,0))
        screen.blit(bg,(bg_x+(3840/1280)*SCREEN_X,0))

        try:
            dict_game = server.recv(1024).decode()
            dict_game = json.loads(dict_game)
        except:
            print("Impossible de recevoir les données de jeu")
            running = False
            main_menu()
        dict_game = game.game_update(screen,clock,list_ally,player_number,dict_game)
        if dict_game == "end":
            running = False;end_game(game)

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
                    running = False
                    main_menu()
            elif event.type == pygame.KEYUP:
                game.pressed[event.key] = False
                if event.key == pygame.K_q:
                    game.player.machine_gun.stop_fire()

        try:
            server.send(dict_game.encode())
        except:
            print("Impossible d'envoyer les données de jeu")
            running = False
            main_menu()

        pygame.display.update()
        #block the fps
        clock.tick(FPS)

    pygame.display.update()
    clock.tick(60)

if __name__ == '__main__':
    main_menu()
