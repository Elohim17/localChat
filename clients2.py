# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 16:05:52 2023

@author: mysys
"""


import socket, sys
import threading

host='127.0.0.1'
port=12000

##      _Nos classes:       ##
## -Pour gérer les emissions et la recption
## -des messages en parallèle
      

def ThreadReception(connexion):
        while 1:
            msg_recu = connexion.recv(1024).decode('utf8')
            print("*"+msg_recu+"*")
            if msg_recu == "" or msg_recu.upper() == "FIN":
                break
        #Le thread <receptiion> se termine ici.
        #On force la fermeture du thread <emission>
        #th_E._stop()
        #print("Client arrêté. Connexion interrompu.")
        #connexion.close()
        


def ThreadEmission(connexion):
        while 1:
            msg_emi=input("écrit: ")
            connexion.send(msg_emi.encode('utf8'))
      


###         _Programme Principal_       ###
    #Creation du socket
connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Connexion du client au serveur
try:
    connexion.connect((host, port))
except socket.error :
    print("La connexion a échouée.")
    sys.exit()
print("Connexion établie avec le serveur.")
#name = input("Entrez votre nom: ")

#Dialogue avec le serveur: on lance deux threads pour gérer
#independamment l'emission et la reception des messages.
th_E = threading.Thread(target=(ThreadEmission), args=[connexion])
th_R = threading.Thread(target=(ThreadReception), args=[connexion])
th_E.start()
th_R.start()

th_E.join()
th_R.join()

print("Client arrêté. Connexion interrompu.")
connexion.close()
