# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 02:12:30 2023

@author: mysys
"""

from tkinter import *
import socket, sys, threading
#from leServeur3 import gestionClient
#from clients3 import *

def create_fen():
    new_fen = Toplevel()
    new_fen.title('Chat en Local: Client')
    new_fen.geometry("500x50")
    
    #frame client
    frame = Frame(new_fen, bg="pink")
    frame.pack(side=BOTTOM)
    message = Label(frame, text="Ecrire le message:")
    message.pack(side=TOP)
    zSaisie = Entry(frame, 
                        font=("ink free", 20),
                        fg="black",
                        bg="khaki", 
                        width="25")
    zSaisie.pack(side=LEFT)

    envoyer = Button(frame, text='Envoyer',
                     activeforeground="black",
                     activebackground="blue")
    envoyer.pack(side=RIGHT)

    suprimer = Button(frame, text='Suprimer',
                      activeforeground="black",
                      activebackground="red")
    suprimer.pack(side=RIGHT)
    
    
def gestionClient(connexion):
        
        #Dealogue avec le client :
        nom = input("Entrez votre nom: ")
        while 1:
            msgClient=connexion.recv(1024).decode('utf8')
            if not msgClient or msgClient.upper() == "FIN":
                break
            #Ajout de l'identifiant au message
            message = "%s> %s" % (nom, msgClient)
            msg = Label(frameS, text=message).pack()
            
            #Faire suivre le message à tous les autres :
            for cle in conn_client:
                if cle != nom:
                    conn_client[cle].send(message.encode('utf8'))
                
        #Fermeture de la connexion :
        connexion.close()      #Couper la connexion (du clent) côté serveur
        del conn_client[it]        #Supprimer son entrée dans le dictionnaire
        deconnect = Label(frameS, text="Client %s déconnecté." % nom).pack()
        #Fin du thread
    

def lancer():
    host='127.0.0.1'
    port=12000
    #initialisation du serveur - Mise en place du socket:
    mySocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        mySocket.bind((host, port))
    except socket.error:
        erreur = Label(frameS, text="La liaison du socket à l'adresse choisie a échouée.").pack(side=TOP)
        print()
        sys.exit()
    pret = Label(frameS, text="Serveur prêt, en attente de requêtes ...").pack(side=TOP)
    
    mySocket.listen(5)
    
    #Attente et prise en charge des connexions demandées par les client :
    conn_client={}
    it=""
    while 1:
        connexion, adresse = mySocket.accept()
        
        #Créer un nouvel objet thread pour gérer la connexion :
        #th = ThreadClient(connexion)
        th = threading.Thread(target=(gestionClient), args=[connexion])
        th.start()
        
        #Mémoriser la connexion dans le dictionnaire :
        it = th.getName() #doit etre associer au nom
        conn_client[it]=connexion
        Thconnect = Label(frameS, text="Client %s connecté, adresse IP: %s, port %s." % (it, adresse[0], adresse[1])).pack()       
        #Dialogue avec le Client
        msgTop ="Vous êtes connecté. Envoyez vos messages."
        connexion.send(msgTop.encode('utf8'))
    
    

# Fenêtre principale #
fenetre = Tk()
fenetre.geometry('500x700')
fenetre.title('Chat en Local')

#fenetre.config()

label=Label(fenetre, text="Bienvenue dans le Chat !")
label.pack(side=TOP)

#frame serveur
frameS = Frame(fenetre, bg="aqua", bd=8, relief=SUNKEN, width="500", height="500")
frameS.pack(side=TOP)
#☺label1 = Label(frameS, text=msgLancement, command=)

clients = Button(fenetre, text="Commencer une discution", command=create_fen).pack()
serveur = Button(fenetre, text="lancer le serveur", command=lancer).pack()

fenetre.mainloop()