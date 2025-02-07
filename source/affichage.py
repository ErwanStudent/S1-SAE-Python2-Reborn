#! /usr/bin/python3
# coding: utf-8
"""
            SAE1.02 SERPENT IUT'O
         BUT1 Informatique 2024-2025

        Module affichage.py
        Ce module permet d'afficher l'arene en mode client serveur 
"""
import pygame
import argparse
import os
import sys
import threading
import client
import partie
import arene
import serpent


ECHELLE=1
GRAND=""
PARTIES_SERPENT={"tete_N":(0,0), "tete_E":(0,ECHELLE*16), "tete_S":(0,ECHELLE*32), "tete_O":(0,ECHELLE*48),
                 "queue_N":(ECHELLE*16,0), "queue_E":(ECHELLE*16,ECHELLE*16), "queue_S":(ECHELLE*16,ECHELLE*32), "queue_O":(ECHELLE*16,ECHELLE*48),
                 "corps_EN":(ECHELLE*32,0), "corps_ES":(ECHELLE*32,ECHELLE*16), "corps_OS":(ECHELLE*32,ECHELLE*32), "corps_ON":(ECHELLE*32,ECHELLE*48),
                 "corps_NE":(ECHELLE*32,0), "corps_SE":(ECHELLE*32,ECHELLE*16), "corps_SO":(ECHELLE*32,ECHELLE*32), "corps_NO":(ECHELLE*32,ECHELLE*48),
                  "corps_NS":(ECHELLE*48,0), "corps_EO":(ECHELLE*48,ECHELLE*16), "corps_SN":(ECHELLE*48,0), "corps_OE":(ECHELLE*48,ECHELLE*16) }
DIRECTION_FROM_DELTA={(1,0):"N",(0,-1):"E",(-1,0):"S",(0,1):"O"}
class JeuGraphique(object):
    """Classe simple d'affichage d'une case."""

    def __init__(self, lecteur_jeu, titre="SerpIUT'O", size=(1600, 1000),
                 couleur=(209, 238, 238),
                 prefixe_image="../img"):
        """Method docstring."""
        self.lecteur_jeu=lecteur_jeu
        self.partie,message_info=lecteur_jeu.get_partie()
        self.arene=partie.get_arene(self.partie)
        self.nb_lignes,self.nb_colonnes=arene.get_dim(self.arene)
        self.sauve = False
        self.liste_msg_info=[message_info]
        self.taille_max_msg_info=10
        self.fini = False
        self.couleur_texte = couleur
        self.titre = titre
        self.images_snakes = {}
        self.images_objets = {}
        self.surf_objets = {}
        self.surf_snakes={}
        self.surf_mini_snakes={}
        self.icone = None
        self.hauteur = 0
        self.largeur = 0
        self.delta = 24
        self.finh = 0
        self.finl = 0
        self.taille_font = 12
        self.surf_snakes={}
        self.surf_snakes_echelle={}
        self.get_images(prefixe_image)
        self.path_font=pygame.font.match_font("Arial",True)
        pygame.init()
        pygame.display.set_icon(self.icone)
        pygame.display.set_mode(size, pygame.RESIZABLE | pygame.DOUBLEBUF)
        pygame.display.set_caption(titre)
        self.surface = pygame.display.get_surface()
        self.maj_parametres()

    def get_images(self, prefixe_image="../img"):
        if os.path.isfile(os.path.join(prefixe_image, 'mur.png')):
            mur = pygame.image.load(os.path.join(prefixe_image, 'mur.png'))
            self.mur=pygame.transform.smoothscale(mur, (ECHELLE*16,ECHELLE*16))
            self.mur_echelle=pygame.transform.smoothscale(mur,(self.delta,self.delta))
            print('mur.png')
        else:
            self.mur = None
        codage="1234"
        for code in codage:
            if os.path.isfile(os.path.join(prefixe_image, 'Snake' + code + GRAND+'.png')):
                s = pygame.image.load(os.path.join(prefixe_image, 'Snake' + code + GRAND + '.png'))
                print('Snake' + code + '.png')
            else:
                s = None
            self.images_snakes[int(code)]=s
            parties={}
            echelles={}
            for partie,coord in PARTIES_SERPENT.items():
                parties[partie]=s.subsurface((coord[1],coord[0],ECHELLE*16,ECHELLE*16))
                echelles[partie]=pygame.transform.smoothscale(parties[partie],(self.delta,self.delta))
            self.surf_snakes[int(code)]=parties
            self.surf_snakes_echelle[int(code)]=echelles
        for ind in range(-6,3):
            if os.path.isfile(os.path.join(prefixe_image, 'tresor' + str(ind)+'.png')):
                self.images_objets[ind] = pygame.image.load(os.path.join(prefixe_image, 'tresor' + str(ind)+ '.png'))
                self.surf_objets[ind]=pygame.transform.smoothscale(self.images_objets[ind],(self.delta*2//3,self.delta*2//3))
                print('tresor' + str(ind)+ '.png')
            
        # lecture du logo de l'IUT'O
        icone_img = pygame.image.load(os.path.join(prefixe_image, 'logo.png'))
        self.icone = pygame.transform.smoothscale(icone_img, (50, 50))

    def maj_surfaces(self,dico_entree,dico_sortie, taille):
        for (cle,img) in dico_entree.items():
            dico_sortie[cle]=pygame.transform.smoothscale(img, (taille, taille))
    
    def maj_parametres(self):
        """
        permet de mettre à jour les paramètres d'affichage en cas de redimensionnement de la fenêtre
        """
        self.surface = pygame.display.get_surface()
        self.hauteur = self.surface.get_height()
        self.largeur = self.surface.get_width()
        deltav=2*self.hauteur//(3*self.nb_lignes)
        deltah=2*self.largeur//(3*self.nb_colonnes)
        self.delta = min(deltah,deltav)
        self.taille_font = self.delta// 2
        for i in range(1,5):
            self.maj_surfaces(self.surf_snakes[i],self.surf_snakes_echelle[i],self.delta)
            smini=pygame.Surface((self.delta*3,self.delta))
            smini.blit(self.surf_snakes_echelle[i]["queue_E"],(0,0))
            smini.blit(self.surf_snakes_echelle[i]["corps_OE"],(self.delta,0))
            smini.blit(self.surf_snakes_echelle[i]["tete_E"],(2*self.delta,0))
            self.surf_mini_snakes[i]=smini
        self.maj_surfaces(self.images_objets,self.surf_objets,self.delta//2)
        self.mur_echelle=pygame.transform.smoothscale(self.mur,(self.delta,self.delta))
        self.font = pygame.font.Font(self.path_font, self.taille_font)
        
    def dessiner_partie_serpent(self,nom_partie,num_joueur,lig,col,val=1):
    
        self.surface.blit(self.surf_snakes_echelle[num_joueur][nom_partie],(col*self.delta+self.delta//2,lig*self.delta+self.delta//2))
        # écrire la valeur des boites!
        texte = self.font.render(str(val), True, (255,255,255))
        textpos = texte.get_rect()
        dec_haut=(self.delta-texte.get_height())//2
        dec_larg=(self.delta-texte.get_width())//2
        textpos.y = lig*self.delta+self.delta//2+dec_haut
        textpos.x = col*self.delta+self.delta//2+dec_larg
        self.surface.blit(texte, textpos)


    def dessiner_serpent(self,num_joueur,serpent,direction):
        lig,col=serpent[0]
        self.dessiner_partie_serpent("tete_"+direction,num_joueur,lig,col,arene.get_val_boite(self.arene,lig,col))
        dir_prec=direction
        ind=1
        while ind<len(serpent)-1:
            lig,col=serpent[ind]
            lig_suiv,col_suiv=serpent[ind+1]
            delta_lig=lig-lig_suiv
            delta_col=col-col_suiv
            dir_suiv=DIRECTION_FROM_DELTA[(delta_lig,delta_col)]
            self.dessiner_partie_serpent("corps_"+dir_prec+dir_suiv,num_joueur,lig,col,arene.get_val_boite(self.arene,lig,col))
            dir_prec=DIRECTION_FROM_DELTA[(-delta_lig,-delta_col)]
            ind+=1
        if len(serpent)>1:
            lig,col=serpent[-1]
            self.dessiner_partie_serpent("queue_"+dir_prec,num_joueur,lig,col,arene.get_val_boite(self.arene,lig,col))

    def dessiner_plan(self):
        self.surface.fill((0,0,0))
        pygame.draw.rect(self.surface,(207,108,33),(0,0,(self.nb_colonnes+1)*(self.delta),
                                                 (self.nb_lignes+1)*(self.delta)),self.delta//2,10)
        for lig in range(self.nb_lignes):
            for col in range(self.nb_colonnes):
                if arene.est_mur(self.arene,lig,col):
                    self.surface.blit(self.mur_echelle,(col*self.delta+self.delta//2,lig*self.delta+self.delta//2))
                else:
                    val=arene.get_val_boite(self.arene,lig,col)
                    if val<0:
                        self.surface.blit(self.surf_objets[val],
                                      (col*self.delta+self.delta//2+self.delta//6,lig*self.delta+self.delta//2+self.delta//6))
                    elif val>0 and arene.get_proprietaire(self.arene,lig,col)==0:
                        self.surface.blit(self.surf_objets[val],
                                      (col*self.delta+self.delta//2+self.delta//6,lig*self.delta+self.delta//2+self.delta//6))

        for i in range(1,arene.get_nb_joueurs(self.arene)+1):
            self.dessiner_serpent(i,arene.get_serpent(self.arene,i),arene.get_derniere_direction(self.arene,i))
        self.affiche_joueurs(5)
          
    def affiche_message(self, ligne, texte, images=[], couleur=None):
        """
        affiche un message en mode graphique à l'écran
        """
        posx=(self.nb_colonnes+1)*self.delta+self.delta//2+30
        posy=ligne*self.delta+20

        if couleur is None:
            couleur = self.couleur_texte
        liste_textes = texte.split('@img@')
        for msg in liste_textes:
            if msg != '':
                texte = self.font.render(msg, True, couleur)
                textpos = texte.get_rect()
                textpos.y = posy
                textpos.x = posx
                self.surface.blit(texte, textpos)
                posx += textpos.width
            if images != []:
                surface = pygame.transform.smoothscale(images.pop(0),
                                                       (round(self.taille_font * 1.5), round(self.taille_font * 1.5)))
                debuty = posy - (self.taille_font // 2)
                self.surface.blit(surface, (posx, debuty))
                posx += surface.get_width()

    def affiche_joueurs(self, ligne, couleur=None):
        if couleur is None:
            couleur = self.couleur_texte
        posx=(self.nb_colonnes+1)*self.delta+self.delta//2+30
        posy=ligne*self.delta+20

        classement = arene.classement(self.arene)
        for le_serpent in classement:
            nom = serpent.get_nom(le_serpent)
            points = serpent.get_points(le_serpent)
            contenu = "{} {}"
            surfp = self.surf_mini_snakes[serpent.get_num_joueur(le_serpent)]
            self.surface.blit(surfp, (posx, posy ))
            nb_obj=-1
            for un_obj in serpent.get_bonus(le_serpent):
               self.surface.blit(self.surf_objets[un_obj],(posx-self.delta//2,posy+(nb_obj*self.delta//2)))
               nb_obj+=1
            texte = self.font.render(
                contenu.format(nom[:15].ljust(15), str(points).rjust(5)), True,
                couleur)
            textpos = texte.get_rect()
            textpos.y = posy+self.delta//4
            textpos.x = posx + surfp.get_width()+10
            self.surface.blit(texte, textpos)
            textpos.x += texte.get_width()
            textpos.y = posy - self.delta // 3
            # self.surface.blit(surfo, textpos)
            posy += self.delta+10# texte.get_height() * 2

    def affiche_message_info(self, num_ligne=10):
        """
        affiche un message d'information aux joueurs
        """
        for msg in self.liste_msg_info:
            self.affiche_message(num_ligne, msg,[])
            num_ligne+=1
        #pygame.display.flip()

    def affiche_info(self):
        
        efface=pygame.Surface((11*self.delta,self.nb_lignes*self.delta))
        self.surface.blit(efface,(self.delta*(self.nb_colonnes+1),2))

        if partie.est_fini(self.partie):
            self.affiche_message(2, "La partie est terminée")
        nb_tours = partie.get_temps_restant(self.partie)
        pluriel = "s"
        if nb_tours <= 1:
            pluriel = ""
        self.affiche_message(3, "il reste " + str(nb_tours) + " tour" + pluriel + " de jeu", [])
        self.affiche_joueurs(5)
        self.affiche_message_info()
        #pygame.display.flip()
        
    def demarrer(self):
        pygame.display.flip()
        pygame.time.set_timer(pygame.USEREVENT + 1, 50)
        en_cours = False
        sauver = False
        clock = pygame.time.Clock()
        self.dessiner_plan()
        while (True):
            ev = pygame.event.wait()
            if ev.type == pygame.QUIT:
                break
            if ev.type == pygame.KEYDOWN:
                if ev.__dict__["unicode"].upper()=='Q':
                    break
            if ev.type == pygame.VIDEORESIZE:
                self.maj_parametres()
                self.dessiner_plan()
                pygame.display.flip()
            if ev.type == pygame.USEREVENT + 1:
                la_partie,msg=self.lecteur_jeu.get_partie()
                if la_partie is not None:
                    self.partie=la_partie
                    self.liste_msg_info.insert(0,msg)
                    if len(self.liste_msg_info)>self.taille_max_msg_info:
                        self.liste_msg_info.pop()
                    self.arene=partie.get_arene(la_partie)
                self.dessiner_plan()
                self.affiche_info()
                #self.affiche_message_info()
                pygame.display.flip()
        pygame.quit()


class LecteurThread(threading.Thread):
    def __init__(self,serveur="",port=1111):
        super().__init__()
        self.client=client.ClientCyber()
        self.client.creer_socket(serveur,port)
        self.client.enregistrement("affichage principal","afficheur")
        self.ok=True
        self.verrou=threading.Lock()
        ok,_,la_partie,msg=self.client.prochaine_commande()
        if not ok:
            sys.exit(0)
        self.partie=partie.partie_from_str(la_partie)
        self.msg=msg
        self.change=True

    def get_partie(self):
        self.verrou.acquire()
        res=None
        msg=""
        if self.change:
            res=self.partie
            msg=self.msg
            self.change=False
        self.verrou.release()
        return res,msg

    def lire_partie(self):
        ok,_,la_partie,msg=self.client.prochaine_commande()
        if not ok:
            self.ok=ok
            return None,"Le serveur a envoyé une partie invalide"
        self.verrou.acquire()
        self.partie=partie.partie_from_str(la_partie)
        self.arene=partie.get_arene(self.partie)
        self.msg=msg
        self.change=True
        self.verrou.release()
    
    def arreter(self):
        self.ok=False

    def run(self):
        while self.ok:
            self.lire_partie()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()  
    parser.add_argument("--nom_partie", dest="nom_partie", help="nom de la partie", type=str, default='Non fournie')
    parser.add_argument("--serveur", dest="serveur", help="serveur de jeu", type=str, default='localhost')
    parser.add_argument("--port", dest="port", help="port de connexion", type=int, default=1111)
    args = parser.parse_args()
    print("Bienvenue dans le jeu de SerpIUT'O")
    id_joueur=1
    lecteur=LecteurThread(args.serveur,args.port)
    lecteur.start()
    jg=JeuGraphique(lecteur,titre=args.nom_partie)
    jg.demarrer()
    lecteur.arreter()
