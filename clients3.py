# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 11:33:47 2023

@author: mysys
"""

import socket, sys
import threading

host='127.0.0.1'
port=12000

def Reception(connexion):
        while 1:
            msg_recu = connexion.recv(1024).decode('utf8')
            print("*"+msg_recu+"*")
            if msg_recu == "" or msg_recu.upper() == "FIN":
                break
        
        #th_E._stop()
        #print("Client arrêté. Connexion interrompu.")
        #connexion.close()
        


def Emission(connexion):
        while 1:
            msg_emi=input("écrire: ")
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
th_E = threading.Thread(target=(Emission), args=[connexion])
th_R = threading.Thread(target=(Reception), args=[connexion])
th_E.start()
th_R.start()

th_R.join()
#th_E._stop()

print("Client arrêté. Connexion interrompu.")
connexion.close()
