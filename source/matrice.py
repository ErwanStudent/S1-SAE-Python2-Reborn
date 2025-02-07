# coding: utf-8
"""
            SAE1.02 SERPIUT'O
         BUT1 Informatique 2024-2025

    Module matrice.py
    Ce module implémente l'API de gestion des matrices 2D
"""
from typing import Any

def Matrice(nb_lig:int, nb_col:int) -> dict:
    """créer une matrice 2D avec nb_lig lignes et nb_col colonnes. 
        Toutes les cases sont initialisées à None

    Args:
        nb_lig (int): le nombre de lignes
        nb_col (int): le nombre de colonnes

    Returns:
        dict: la matrice avec la représentation que vous avez choisie
    """
    mat:dict=dict()
    for lig in range(nb_lig):
        for col in range(nb_col):
            mat[(lig,col)]=None
    return {"nb_lig":nb_lig,"nb_col":nb_col,"valeurs":mat}

def get_val(mat:dict,lig:int,col:int) -> Any:
    """Retourne la valeur de la case de la matrice qui se trouve en lig,col
        si la ligne ou la colonne n'existent pas la fonction lèvera une exception

    Args:
        mat (dict): la matrice considérée
        lig (int): le numéro de la ligne de la case recherchée
        col (int): le numéro de la colonne de la case recherchée

    Returns:
        Any: la valeur de la case recherchée
    """    
    return mat["valeurs"][(lig,col)]

def set_val(mat:dict,lig:int,col:int,val:Any) -> None:
    """Stocke la valeur val dans la case de la matrice qui se trouve en lig,col
        si la ligne ou la colonne n'existent pas la fonction lèvera une exception

    Args:
        mat (dict): la matrice considérée
        lig (int): le numéro de la ligne de la case recherchée
        col (int): le numéro de la colonne de la case recherchée
        val (Any): la valeur à stocker
    """    
    mat["valeurs"][(lig,col)]=val

def get_nb_lignes(mat:dict)-> int:
    """retourne le nombre de lignes de la matrice

    Args:
        mat (dict): la matrice considérée

    Returns:
        int: le nombre de lignes de la matrice
    """    
    return mat["nb_lig"]


def get_nb_colonnes(mat:dict)-> int:
    """retourne le nombre de colonnes de la matrice

    Args:
        mat (dict): la matrice considérée

    Returns:
        int: le nombre de colonnes de la matrice
    """    
    return mat["nb_col"]

def get_dim(matrice:dict)->[int,int]:
    """retourne les dimensions de la matrice sous la forme d'un tuple (nb_lig,nb_col)

    Args:
        matrice (dict): la matrice considérée

    Returns:
        [int,int]:la paire (nb_lig,nb_col)
    """    
    return matrice["nb_lig"],matrice["nb_col"]

def affiche_ligne_separatrice(matrice: dict, taille_cellule:int=4)->None:
    """Affiche une ligne séparatrice en fonction de la taille des cellules

    Args:
        matrice (dict): la matrice à afficher
        taille_cellule (int, optional): taille des cases en nombre de caractères. Defaults to 4.
    """
    print()
    for _ in range(get_nb_colonnes(matrice) + 1):
        print('-'*taille_cellule+'+', end='')
    print()


def affiche(matrice:dict, taille_cellule:int=4)->None:
    """Affiche une matrice en prenant en utilisant taille_cellule caractères pour chaque case de la matrice

    Args:
        matrice (dict): la matrice à afficher
        taille_cellule (int, optional): taille des cases en nombre de caractères. Defaults to 4.
    """    
    nb_colonnes = get_nb_colonnes(matrice)
    nb_lignes = get_nb_lignes(matrice)
    print(' '*taille_cellule+'|', end='')
    for i in range(nb_colonnes):
        print(str(i).center(taille_cellule) + '|', end='')
    affiche_ligne_separatrice(matrice, taille_cellule)
    for i in range(nb_lignes):
        print(str(i).rjust(taille_cellule) + '|', end='')
        for j in range(nb_colonnes):
            print(str(get_val(matrice, i, j)).rjust(taille_cellule) + '|', end='')
        affiche_ligne_separatrice(matrice, taille_cellule)
    print()
