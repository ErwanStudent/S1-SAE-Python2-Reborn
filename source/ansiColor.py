# -*- coding: utf-8 -*-
"""
            SAE1.02 SERPIUT'O
         BUT1 Informatique 2024-2025

   Module ansi.py 
   ~~~~~~~~~~~~~~~
   
   Petit script permettant un affichage coloré dans une console en utilisant le code ANSI. 
"""

fin='\x1b[0m'
NOIR=0
ROUGE=1
VERT=2
JAUNE=3
BLEU=4
VIOLET=5
CYAN=6
GRIS=7
NORMAL=9
AUCUN=0
GRAS=1
ITALIQUE=3
SOULIGNE=4

def clearscreen():
     """
     permet d'effacer l'écran
     """
     print("\x1b[2J",end='')

def pcouleur(texte,couleurCar=9,couleurFond=9,style=0):
     """
     permet d'afficher un texte en couleur avec un style éventuel
     paramètres:
         texte: la chaine de caractères à afficher
         couleurCar: un entier indiquant la couleur des caractères (blanc par défaut)
         couleurFond: un entier indiquant la couleur du fond (noir par défaut)
         style: un entier indiquant le style de la police (gras, italique etc.)
     """
     print("\x1b["+str(style)+";"+str(30+couleurCar)+";"+str(40+couleurFond)+"m"+str(texte)+fin,sep='',end='')
