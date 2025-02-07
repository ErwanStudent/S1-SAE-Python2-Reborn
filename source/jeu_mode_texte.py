#! /usr/bin/python3
# coding: utf-8
"""
            SAE1.02 SERPIUT'O
         BUT1 Informatique 2024-2025

    Module jeu_mode_texte.py
    Ce module implémente le jeu en mode texte ce qui permet de faire des tests simplement
    python3 jeu_mode_texte.py --help
"""
import argparse
import time
import random
import arene
import partie
import IA

# Si vous souhaitez tester plusieurs IA, vous pouvez changer le
# le nom de la fonction d'IA utilisée pour chaque joueur (par défaut IA.mon_IA)
les_IA={1:IA.mon_IA,2:IA.mon_IA,3:IA.mon_IA,4:IA.mon_IA}

if __name__ == '__main__': 
    print("Bienvenue dans le jeu du SerpIUT'O")

    parser = argparse.ArgumentParser()
    parser.add_argument("--nom_partie", dest="nom_partie", help="nom de la partie", type=str, default='score.csv')
    parser.add_argument("--duree", dest="duree", help="nombre de tours de la partie", type=int, default=150)
    parser.add_argument("--map", dest="map", help="fichier contenant la map", type=str, default='../plan/plan1.txt')
    parser.add_argument("--nb_joueurs", dest="nb_joueurs", help="indique le nombre de joueurs de la partie", type=int, default=4)
    parser.add_argument("--tempo", dest="tempo",help="indique le temps en secondes de temporisation entre chaque affichage", type=float, default=0.5)
    parser.add_argument("--debug", help="permet de faire dérouler la partie pas à pas", action='store_true')
    args = parser.parse_args()
    la_partie=partie.nouvelle_partie(args.nom_partie, args.duree, args.map)
    nb_joueurs=min(4,args.nb_joueurs)
    print("inscription de",nb_joueurs,"a la partie")
    for num in range(nb_joueurs):
        partie.ajouter_joueur(la_partie,"Joueur "+str(num+1))
    l_arene=partie.get_arene(la_partie)
    arene.ajouter_des_boites_ou_bonus(l_arene,1,2,args.nb_joueurs)
    arene.afficher_arene(l_arene)
    print("partie:",partie.get_nom_partie(la_partie),"duree totale:",partie.get_duree_totale(la_partie),
          "duree restante:",partie.get_temps_restant(la_partie))
    rep=input("Q pour quitter, ENTREE pour continuer ").upper()
    liste_num_joueurs=[nj for nj in range(1,partie.get_nb_joueurs(la_partie)+1)]
    while not partie.est_fini(la_partie) and rep!='Q':
        choix={}
        for nj in range(1,partie.get_nb_joueurs(la_partie)+1):
            choix[nj]=les_IA[nj](nj,la_partie)
        random.shuffle(liste_num_joueurs)
        for nj in liste_num_joueurs:
            msg=partie.jouer_joueur(la_partie,nj,choix[nj])
            arene.afficher_arene(l_arene)
            print("partie:",partie.get_nom_partie(la_partie),"duree totale:",partie.get_duree_totale(la_partie),
                "duree restante:",partie.get_temps_restant(la_partie))
            print("Le joueur",nj,"s'est déplacé vers",choix[nj])
            print(msg)
            if args.debug:
                rep=input("ENTREE pour continuer ").upper()
            else:
                time.sleep(args.tempo)
        partie.finir_tour(la_partie)
        arene.afficher_arene(l_arene)
        print("partie:",partie.get_nom_partie(la_partie),"duree totale:",partie.get_duree_totale(la_partie),
                "duree restante:",partie.get_temps_restant(la_partie))
        print("fin du tour\n")
        if args.debug:     
            rep=input("Q pour quitter, ENTREE pour continuer ").upper()
        else:
            time.sleep(args.tempo)

    print("Partie terminée")
