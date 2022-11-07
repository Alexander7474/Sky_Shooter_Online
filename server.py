import pygame
import socket
from effects import *
import json
from random import randint
import sys

pygame.init()
s = socket.socket()
port = 5555
s.bind(('',port))
s.listen(5)

def main():
    number_client = ""
    while type(number_client) != int:
        try:
            number_client = int(input("Combien de joueur(s) sur ce serveur ?(0 ou 1 pour quitter): "))
        except:
            print("Entrer un entier")
    if number_client == 0 or number_client == 1:
        print('Adios')
        sys.exit(1)
    print('En attente de la connexion des clients')
    dict_client = {}

    for i in range(number_client): 
        dict_client['client'+str(i)], dict_client['addr'+str(i)] = s.accept()
        print ('Connexion depuis', dict_client['addr'+str(i)], 'client n'+str(i))

    dict_game = {"players": {}}
    for i in range(number_client): dict_game['players']['player'+str(i)] = {"life": 100, "coo": (100,100), "bullets": [],"rockets": [], "enemys": [], "score": 0}
    dict_game['cargo_life'] = 500
    dict_game['nuages'] = []

    for i in range(number_client):
        try:
            msg = str(i)+','+str(number_client)
            dict_client['client'+str(i)].send(msg.encode())
            code = dict_client['client'+str(i)].recv(1024).decode()
            if code == "200":
                print("client n"+str(i)+" a pris connaissance de son matricule")
            else:
                print("erreur code invalide avec le client n"+str(i))
                print('redémarrage du serveur')
                main()
        except:
            print("erreur avec le client n"+str(i)+" lors de la prise de matricule")
            print('redémarrage du serveur')
            main()

    dict_game_se = json.dumps(dict_game)
    for i in range(number_client):
        try:
            dict_client['client'+str(i)].send(dict_game_se.encode())
        except:
            print('le client n'+str(i)+' ne répond pas')
            print('redémarrage du serveur')
            main()

    running = True
    while running:
        #update des infos selon les autres joueurs
        dict_game["bullets"] = []
        damage_cargo = 0
        for i in range(number_client):
            try:
                new_dict_game = json.loads(dict_client['client'+str(i)].recv(1024).decode())
            except:
                print('impossible de récupérer les données joueur avec le client n'+str(i))
                print('redémarrage du serveur')
                main()
            dict_game['players']['player'+str(i)] = new_dict_game['players']['player'+str(i)]
            damage_cargo += dict_game['cargo_life']-new_dict_game['cargo_life']
        dict_game['cargo_life'] -= damage_cargo

        if randint(0,20) == 0:
            pn = str(randint(0,number_client-1))
            if len(dict_game['players']['player'+pn]["enemys"]) < 5:
                dict_game['players']['player'+pn]["enemys"].append({"life":10,"coo":(1280,randint(0,720)),"spawned":False})

        dict_game_se = json.dumps(dict_game)
        for i in range(number_client):
            try:
                dict_client['client'+str(i)].send(dict_game_se.encode())
            except:
                print('le client n'+str(i)+' ne répond plus')
                print('redémarrage du serveur')
                main()

if __name__ == '__main__':
    main()
