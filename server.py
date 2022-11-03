import pygame
import socket
from player import Player
from enemy import Enemy
from effects import *
from cargo import Cargo
import json
from random import randint

pygame.init()

s = socket.socket()
port = 5555
s.bind(('',port))
s.listen(5)

number_client = int(input("Combien de joueur(s) sur ce serveur ?: "))
dict_client = {}

for i in range(number_client):
  dict_client['client'+str(i)], dict_client['addr'+str(i)] = s.accept()
  print ('Got connection from', dict_client['addr'+str(i)])

dict_game = {"players": {}}
for i in range(number_client): dict_game['players']['player'+str(i)] = {"life": 100, "coo": (100,100), "bullets": [],"rockets": [], "enemys": []}
dict_game['cargo_life'] = 500
dict_game['nuages'] = []

for i in range(number_client):
  msg = str(i)+','+str(number_client)
  dict_client['client'+str(i)].send(msg.encode())
  code = dict_client['client'+str(i)].recv(1024).decode()
  if code == "200":
    print("client n"+str(i)+" a pris connaissance de son matricule")
  else:
    print("erreur")

dict_game_se = json.dumps(dict_game)
for i in range(number_client):
  dict_client['client'+str(i)].send(dict_game_se.encode())

running = True
while running:
  #update des infos selon les autres joueurs
  dict_game["bullets"] = []
  damage_cargo = 0
  for i in range(number_client):
    new_dict_game = json.loads(dict_client['client'+str(i)].recv(1024).decode())
    dict_game['players']['player'+str(i)]["coo"] = new_dict_game['players']['player'+str(i)]["coo"]
    dict_game['players']['player'+str(i)]["bullets"] = new_dict_game['players']['player'+str(i)]["bullets"]
    dict_game['players']['player'+str(i)]["rockets"] = new_dict_game['players']['player'+str(i)]["rockets"]
    dict_game['players']['player'+str(i)]["enemys"] = new_dict_game['players']['player'+str(i)]["enemys"]
    damage_cargo += dict_game['cargo_life']-new_dict_game['cargo_life']
  dict_game['cargo_life'] -= damage_cargo

  if randint(0,20) == 0:
      pn = str(randint(0,number_client-1))
      if len(dict_game['players']['player'+pn]["enemys"]) < 5:
          dict_game['players']['player'+pn]["enemys"].append({"life":10,"coo":(1200,randint(0,675)),"spawned":False})

  dict_game_se = json.dumps(dict_game)
  for i in range(number_client):
    dict_client['client'+str(i)].send(dict_game_se.encode())
