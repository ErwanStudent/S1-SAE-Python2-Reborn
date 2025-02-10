#! /usr/bin/python3
# coding: utf-8
"""
            SAE1.02 SERPENT IUT'O
         BUT1 Informatique 2024-2025

        Module serveur.py
        Ce module contient le serveur du jeu
"""
import argparse
import random
import socket
import threading
import time

import client

import partie

JOUEUR = 1
AFFICHEUR = 2
TOUS = 3

NB_JOUEURS = 8

TEMPO=0.25

class Table_Clients(object):
    def __init__(self, nb_joueurs_max, nb_afficheur_max=5):
        self.nb_joueurs_max = nb_joueurs_max
        self.nb_afficheur_max = nb_afficheur_max
        self.nb_joueurs = 0
        self.nb_actifs = 0
        self.joueurs = []
        self.afficheurs = []
        self.reponses = {}
        self.nb_reponses = 0
        self.verrou_ajout = threading.RLock()
        self.verrou_reponses = threading.Lock()
        self.nouvelle_iteration = threading.Event()
        self.reponses_ok = threading.Event()
        self.le_jeu = None

    def ajouter_joueur(self, joueur):
        self.verrou_ajout.acquire()
        if len(self.joueurs) >= self.nb_joueurs_max:
            joueur.envoyer_refus()
            joueur.clientsocket.fermer()
            self.verrou_ajout.release()
            return -1
        self.joueurs.append(joueur)
        res=partie.ajouter_joueur(self.le_jeu,joueur.nom)
        self.nb_joueurs += 1
        self.nb_actifs += 1
        self.verrou_ajout.release()
        self.envoyer_jeu(AFFICHEUR,"Inscription de "+joueur.nom)
        return res

    def enlever_client(self, client):
        self.verrou_ajout.acquire()
        if client.type_client == JOUEUR:
            ind = self.joueurs.index(client)
            if ind != -1:
                client.clientsocket.fermer()
                self.nb_joueurs -= 1
                self.nb_actifs -= 1
                #self.joueurs.pop(ind)
                print("Joueur", client.id, "déconnecté")
        elif client.type_client == AFFICHEUR:
            ind = self.afficheurs.index(client)
            if ind != -1:
                client.clientsocket.fermer()
                self.afficheurs.pop(ind)
                print("Afficheur", client.id, "déconnecté")
        self.verrou_ajout.release()

    def ajouter_afficheur(self, afficheur):
        self.verrou_ajout.acquire()
        if len(self.afficheurs) == self.nb_afficheur_max:
            afficheur.envoyer_refus()
            afficheur.clientsocket.fermer()
            self.verrou_ajout.release()
            return -1
        self.afficheurs.append(afficheur)
        res = len(self.afficheurs)
        self.verrou_ajout.release()
        self.envoyer_jeu(AFFICHEUR)
        return res

    def envoyer_jeu(self, dest=TOUS, msg=""):
        self.verrou_ajout.acquire()
        jeu_temp = self.le_jeu
        jeu_str = partie.partie_2_str(jeu_temp)
        if dest == JOUEUR or dest == TOUS:
            for joueur in self.joueurs:
                joueur.envoyer_jeu(jeu_str,msg)
        if dest == AFFICHEUR or dest == TOUS:
            for afficheur in self.afficheurs:
                afficheur.envoyer_jeu(jeu_str,msg)    
        self.verrou_ajout.release()

    def envoyer_quit(self):
        self.verrou_ajout.acquire()
        for joueur in self.joueurs:
            joueur.envoyer_quit()
        for afficheur in self.afficheurs:
                afficheur.envoyer_quit()
        self.verrou_ajout.release()

    def envoyer_message(self, msg, dest=TOUS):
        self.verrou_ajout.acquire()
        if dest == JOUEUR or dest == TOUS:
            for joueur in self.joueurs:
                joueur.envoyer_message(msg)
        if dest == AFFICHEUR or dest == TOUS:
            for afficheur in self.afficheurs:
                afficheur.envoyer_message(msg)
        self.verrou_ajout.release()

    def commencer_nouvelle_iteration(self):
        self.nouvelle_iteration.set()

    def ajouter_reponse(self, id_joueur, msg):
        self.verrou_reponses.acquire()
        self.nouvelle_iteration.clear()
        self.reponses[id_joueur] = msg
        self.nb_reponses += 1
        if self.nb_reponses >= self.nb_actifs:
            self.reponses_ok.set()
        self.verrou_reponses.release()

    def recolter_reponses(self):
        self.reponses_ok.wait()
        self.reponses_ok.clear()
        self.verrou_reponses.acquire()
        res = self.reponses.copy()
        self.reponses = {}
        self.nb_reponses = 0
        self.verrou_reponses.release()
        return res

    def attendre_nouvelle_iteration(self):
        self.nouvelle_iteration.wait()

    def liberer_ressources(self):
        for joueur in self.joueurs:
            joueur.clientsocket.fermer()
        for afficheur in self.afficheurs:
            afficheur.clientsocket.fermer()


class JeuThread(threading.Thread):

    def __init__(self, ecouteur, table_clients, duree, nom_partie='score.csv', map='../plan/plan1.txt'):
        super().__init__()
        self.ecouteur=ecouteur
        self.table_clients = table_clients
        self.nom_partie = nom_partie
        table_clients.le_jeu = partie.nouvelle_partie(nom_partie,duree,map)
        

    def run(self):
        # pb ici de coordination entre le start et les inscriptions
        print("On attend")
        rep=""
        while rep!="S":
            rep=input().upper()
            # if self.table_clients.nb_joueurs==NB_JOUEURS:
            #     break
            # if self.table_clients.nb_joueurs<NB_JOUEURS:
            #     print("Tous les joueurs ne sont pas inscrits\nOn attend")
            # else:
            #     print("Trop de joueurs inscrits")
            if rep=='Q':
                self.table_clients.envoyer_quit()
                self.table_clients.liberer_ressources()
                self.ecouteur.arreter()
        partie.init_boites(self.table_clients.le_jeu)
        id_joueurs=[i for i in range(1,self.table_clients.nb_joueurs+1)]
        print("C'est parti!!!")
        self.table_clients.envoyer_jeu(msg="C'est parti!!!")
        cpt = 0
        rep=''
        self.table_clients.commencer_nouvelle_iteration()
        while rep != 'Q':
            recup = self.table_clients.recolter_reponses()

            if recup != None:
                random.shuffle(id_joueurs)
                for id_joueur in id_joueurs:
                    action=recup[id_joueur]
                    if len(action)!=1: #lorsqu'un joueur est déconnecté
                        action="*"
                    msg=partie.jouer_joueur(self.table_clients.le_jeu,id_joueur,action)
                    if msg!='':
                        print(msg)
                    self.table_clients.envoyer_jeu(AFFICHEUR,msg)
                    time.sleep(TEMPO)

                partie.finir_tour(self.table_clients.le_jeu)
                if partie.est_fini(table_clients.le_jeu):
                    self.table_clients.envoyer_jeu(msg="Fin de la partie")
                    break
                self.table_clients.envoyer_jeu(msg="Fin du tour")
                self.table_clients.commencer_nouvelle_iteration()
                time.sleep(TEMPO)
                cpt += 1
        self.table_clients.envoyer_quit()
        self.table_clients.liberer_ressources()
        partie.sauver_score(table_clients.le_jeu,self.nom_partie)
        self.ecouteur.arreter()
        print("C'est fini")


class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket, table_clients):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = client.ClientCyber()
        self.clientsocket.set_socket(clientsocket)
        self.table_clients = table_clients
        self.actif=True

    def maj_info_client(self, type_client, nom):
        self.nom = nom
        self.id = -1
        if type_client == "joueur":
            self.type_client = JOUEUR
            self.clientsocket.set_timeout(TEMPO+0.1) # pour gérer les clients qui plantent
        elif type_client == "afficheur":
            self.type_client = AFFICHEUR
        else:
            print("[-] Type de client inconnu")
            return False
        res = False
        if self.type_client == JOUEUR:
            self.id = table_clients.ajouter_joueur(self)
            if self.id != -1:
                print("[+] Nouveau joueur [%s] pour %s %s" %
                      (self.nom, self.ip, self.port, ))
                res = True
            else:
                print("[-] Trop de joueurs déjà enregistrés")
        elif self.type_client == AFFICHEUR:
            self.id = table_clients.ajouter_afficheur(self)
            if self.id != -1:
                print("[+] Nouvel afficheur [%s] pour %s %s" %
                      (self.nom, self.ip, self.port, ))      
                res = True
            else:
                print("[-] Trop d'afficheurs déjà enregistrés")
        return res

    def lire_commande(self):
        if not self.actif:
            self.table_clients.ajouter_reponse(self.id, "")
            return True
        try:
            la_commande = self.clientsocket.recevoir_commande_client()
        except Exception as ex:
            print(ex)
            print(self.id, "semble déconnecté")
            self.table_clients.ajouter_reponse(self.id, "")
            return True
        self.table_clients.ajouter_reponse(self.id, la_commande)
        return True

    def envoyer_quit(self):
        try:
            self.clientsocket.envoyer_quit()
        except:
            print(self.id,"est deconnecté") 
            self.table_clients.enlever_client(self)

    def envoyer_refus(self):
        try:
            self.clientsocket.envoyer_refus()
        except:
            print(self.id,"est deconnecté")    

    def envoyer_jeu(self,jeu_str,msg=""):
        if not self.actif:
            return
        try:
            self.clientsocket.envoyer_jeu(jeu_str,self.id,msg)
        except:
            print(self.id,"est deconnecté")
            self.table_clients.enlever_client(self)

    def envoyer_message(self, message):
        if not self.actif:
            return
        try:
            self.clientsocket.envoi(message)
        except:
            print(self.id, "est déconnecté")
            self.table_clients.enlever_client(self)

    def run(self):
        print("Connexion de %s %s" % (self.ip, self.port, ))
        
        type_cli, nom_cli = self.clientsocket.recevoir_enregistrement()
        if self.maj_info_client(type_cli, nom_cli):
            if self.type_client == JOUEUR:
                continuer = True
                while continuer:
                    self.table_clients.attendre_nouvelle_iteration()
                    continuer = self.lire_commande()
                print("Client déconnecté...")

class Ecouteur(threading.Thread):
    def __init__(self,serveur,port,table_clients):
        threading.Thread.__init__(self)
        self.ip=serveur
        self.port=port
        self.table_clients=table_clients
        self.ok=True

    def arreter(self):
        print("arreter")
        self.ok=False
    
    def run(self):
        tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcpsock.bind((self.ip, self.port))
        while self.ok:
            tcpsock.listen(10)
            print("En écoute...")
            (clientsocket, (ip, port)) = tcpsock.accept()
            newthread = ClientThread(self.ip, self.port, clientsocket, self.table_clients)
            newthread.start()

if __name__ == '__main__':
    print("Bienvenue dans le jeu du Serpents'O")
    parser = argparse.ArgumentParser()
    parser.add_argument("--serveur", dest="serveur", help="serveur de jeu", type=str, default='localhost')
    parser.add_argument("--port", dest="port", help="port de connexion", type=int, default=1111)
    # parser.add_argument("--empl_tournoi", dest="empl_tournoi", help="emplacement du tournoi", type=str, default='.')
    parser.add_argument("--nom_partie", dest="nom_partie", help="nom de la partie", type=str, default='score.csv')
    parser.add_argument("--duree", dest="duree", help="nombre de tours de la partie", type=int, default=150)
    parser.add_argument("--map", dest="map", help="fichier contenant la map", type=str, default='../plan/plan1.txt')
    
    args = parser.parse_args()
    table_clients = Table_Clients(NB_JOUEURS, 5)
    ecouteur=Ecouteur(args.serveur,args.port,table_clients)
    ecouteur.start()
    le_jeu = JeuThread(ecouteur,table_clients,args.duree,args.nom_partie,args.map)
    le_jeu.start()


