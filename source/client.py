# coding: utf-8
"""
            SAE1.02 SERPIUT'O
         BUT1 Informatique 2024-2025

        Module client.py
        Ce module implémente le protocole de communication entre
        le serveur et les clients (joueurs et affichage)
"""
import socket
import select
import random
import json

class Client():
    def __init__(self, fin_de_message="\0", taille_chunk=8192):
        self.taille_chunk = taille_chunk
        self.fin_de_message = fin_de_message
        self.id_client = random.randint(1, 1000)
        self.reserve = ''

    def creer_socket(self, ip="", port=1111):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))
        

    def set_socket(self, la_socket):
        self.socket = la_socket

    def afficher_msg(self, msg, complement=""):
        print("["+str(self.id_client)+"] =>", msg, complement)

    def reception(self,timeout=-1):
        # on vérifie que la réserve ne contient pas déjà le message
        ind_0 = self.reserve.find(self.fin_de_message)
        if ind_0 != -1:
            msg = self.reserve[:ind_0]
            self.reserve = self.reserve[ind_0+1:]
        else:  # si la réserve ne contient pas le message complet on recopie la réserve dans le message
            msg = self.reserve
            self.reserve = ''
            ok = False
            while not ok:  # on lit sur la socket jusqu'à obtenir un message contenant le caractère '\0'
                try:
                    if timeout!=-1:
                        ready = select.select([self.socket], [], [], timeout)
                    else:
                        ready=[True]
                    if ready[0]:
                        #print("ready")
                        msg_brut = self.socket.recv(self.taille_chunk)
                    else:
                        print("not ready")
                        raise OSError
                except OSError as exc:
                    self.afficher_msg("probleme de timeout",str(exc))
                    return ""
                if len(msg_brut) == 0:
                    self.afficher_msg("le serveur semble déconnecté")
                    return ""
                msg_comp = msg_brut.decode("utf-8")
                ind_0 = msg_comp.find(self.fin_de_message)
                if ind_0 != -1:  # le message recu contient un caractère '\0'
                    ok = True
                    # on met tout ce qui est avant le '\0' dans le message
                    msg += msg_comp[:ind_0]
                    # et le reste dans la réserve
                    self.reserve = msg_comp[ind_0+1:]
                else:
                    msg += msg_comp
        return msg

    def envoi(self, msg):
        # envoi d'un message auquel on ajoute le caractère '\0' pour repérer les fins de message
        if self.socket.send((msg+'\0').encode()) == 0:
            self.afficher_msg("le serveur semble planté")
            raise RuntimeError("Serveur inaccessible")

    def fermer(self):
        self.socket.close()


TYPE_JOUEUR = "joueur"
TYPE_AFFICHEUR = "afficheur"
TYPE_SERVEUR = "serveur"


class ClientCyber(Client):
    def __init__(self, fin_de_message="\0", taille_chunk=8192, separateur=";",timeout=-1):
        super().__init__(fin_de_message=fin_de_message, taille_chunk=taille_chunk)
        self.type_client = None
        self.nom_client = None
        self.separateur = separateur
        self.timeout = timeout

    def set_timeout(self,timeout):
        self.timeout=timeout

    def enregistrement(self, nom_client, type_client):
        self.nom_client = nom_client.replace(
            self.separateur, "_", -1).replace("\n", "_")
        self.type_client = type_client
        self.envoi(type_client+self.separateur+self.nom_client)

    def prochaine_commande(self):
        msg = self.reception()
        if msg is None:
            self.afficher_msg("Le serveur semble déconnecté")
            return False, 0, True, "Le serveur semble déconnecté"
       # traitement du message
        fin_entete = msg.find('\n')
        commande = msg[:fin_entete]
        if commande == "quit":
            self.afficher_msg("le jeu se termine")
            return False, 0, True,"le jeu se termine"
        if commande == "refused":
            self.afficher_msg("la connection a été refusée")
            return False, 0, True,"la connection a été refusée"
        try:
            cmd, num_joueur = commande.split(self.separateur)
            if cmd != 'jeu':
                raise Exception()
        except:
            self.afficher_msg("commande jeu mal formée", commande)
            return False, 0, False, "commande jeu mal formée"
        le_jeu = None
        try:
            fin_msg=msg.find('\n',fin_entete+1)
            le_message=msg[fin_entete+1:fin_msg]
            le_jeu = msg[fin_msg+1:]
        except Exception as ex:
            print(ex)
            self.afficher_msg("le jeu n'est pas correctement encodé")
            return False, num_joueur, False, "le jeu n'est pas correctement encodé"
        return True, num_joueur, le_jeu, le_message

    def envoyer_quit(self):
        self.envoi("quit\n")

    def envoyer_refus(self):
        self.envoi("refused\n")

    def envoyer_jeu(self, jeu_str, num_joueur,msg=""):
        self.envoi("jeu"+self.separateur+str(num_joueur)+'\n'+msg+'\n'+jeu_str)

    def envoyer_commande_client(self, commande):
        self.envoi(commande)

    def recevoir_commande_client(self):
        return self.reception(self.timeout)

    def recevoir_enregistrement(self):
        msg = self.reception()
        type_client, nom_client = msg.split(self.separateur)
        return type_client, nom_client
