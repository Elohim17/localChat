# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 15:29:06 2023

@author: mysys
"""


#Définition d'un serveur réseau gérant un système de CHAT simplifié.
#Utilise les threads pour gérer les connexions en parallèle

host='127.0.0.1'
port=12000

import socket, sys, threading

def ThreadClient(connexion):
        
        #Dealogue avec le client :
        nom = input("Entrez votre nom: ")
        while 1:
            msgClient=connexion.recv(1024).decode('utf8')
            if not msgClient or msgClient.upper() == "FIN":
                break
            #Ajout de l'identifiant au message
            message = "%s> %s" % (nom, msgClient)
            print(message)
            
            #Faire suivre le message à tous les autres :
            for cle in conn_client:
                if cle != nom:
                    conn_client[cle].send(message.encode('utf8'))
                
        #Fermeture de la connexion :
        connexion.close()      #Couper la connexion (du clent) côté serveur
        del conn_client[connexion]        #Supprimer son entrée dans le dictionnaire
        print("Client %s déconnecté." % nom)
        #Fin du thread

#initialisation du serveur - Mise en place du socket:
mySocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    mySocket.bind((host, port))
except socket.error:
    print("La liaison du socket à l'adresse choisie a échouée.")
    sys.exit()
print("Serveur prêt, en attente de requêtes ...")
mySocket.listen(5)

#Attente et prise en charge des connexions demandées par les client :
conn_client={}
while 1:
    connexion, adresse = mySocket.accept()
    
    #Créer un nouvel objet thread pour gérer la connexion :
    #th = ThreadClient(connexion)
    th = threading.Thread(target=(ThreadClient), args=[connexion])
    th.start()
    
    #Mémoriser la connexion dans le dictionnaire :
    it = th.getName()
    conn_client[it]=connexion
    print("Client %s connecté, adresse IP: %s, port %s." % (it, adresse[0], adresse[1]))
    
    #Dialogue avec le Client
    msg ="Vous êtes connecté. Envoyez vos messages."
    connexion.send(msg.encode('utf8'))
    
    th.join()
    
    #Fermeture de la connexion :
    connexion.close()      #Couper la connexion (du clent) côté serveur
    del conn_client[connexion]        #Supprimer son entrée dans le dictionnaire
    print("Client %s déconnecté." % nom)
    #Fin du thread