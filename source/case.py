# coding: utf-8
"""
            SAE1.02 SERPIUT'O
         BUT1 Informatique 2024-2025

    Module case.py
    module implémentant l'API de gestion d'une case de l'arène.
"""
from typing import Any

def Case(mur:bool, valeur:int=0, proprietaire:int=0, temps_restant:int=0) -> dict:
    """crée une case du jeu avec son contenu

    Args:
        mur (bool): indique si la case est un mur ou non
        valeur (int, optional): indique la valeur de la boite sur la case (0 indique que la case est vide). Defaults to 0.
        proprietaire (int, optional): indique à qui appartient la boite (0 pas de propriétaire). Defaults to 0.
        temps_restant (int, optional): indique le temps avant que la boite disparaisse si celle-ci n'est pas dans un serpent
        si la boite est dans serpent ce paramètre indique le temps restant avant de pouvoir fusionner la boite. Default 0.

    Returns:
        dict: une case représentée sous la forme d'un dictionnaire
    """
    return {"mur":mur,"valeur":valeur,"proprietaire":proprietaire,"temps_restant":temps_restant}

def est_mur(case:dict)->bool:
    """indique si la case est un mur ou non

    Args:
        case (dict): la case considérée

    Returns:
        bool: True si la case est un mur False sinon
    """    
    return case["mur"]

def compare(case1:dict, case2:dict)->int:
    if case1["mur"] != case2["mur"]:
        return -2
    if case1["mur"]:
        return 0
    if case1["valeur"]>case2["valeur"]:
        return 1
    if case1["valeur"]<case2["valeur"]:
        return -1
    if case1["temps_restant"]>case2["temps_restant"]:
        return 1
    if case1["temps_restant"]<case2["temps_restant"]:
        return -1
    return 0
    

def contient_boite(case:dict)->bool:
    """indique si la case contient une boite ou non

    Args:
        case (dict): la case considérée

    Returns:
        bool: True si la case contient une boite ou est un mur
    """
    if case["mur"]:
        return False
    return case["valeur"]!=0

def get_val_boite(case:dict)->int:
    """retourne la valeur de la boite de la case (0 si la case est un mur ou ne contient rien)

    Args:
        case (dict): la case considérée

    Returns:
        int: valeur de la boite contenue dans la case s'il y en a une 0 sinon
    """
    if case["mur"]:
        return 0
    return case["valeur"]

def get_proprietaire(case:dict)->int:
    """retourne le numéro du propriétaire de la boite de la case
        0 si la case est vide ou est un mur ou n'a pas de pripriétaire 

    Args:
        case (dict): la case considérée

    Returns:
        int: numéro du propriétaire de la boite contenu dans la case
    """
    if case["mur"]:
        return 0
    return case["proprietaire"]

def get_temps_restant(case:dict):
    """retourne le temps restant d'une case contenant une boite

    Args:
        case (dict): la case considérée
    Returns:
        int: le temps restant de la boite. -1 si c'est un mur
    """
    if case["mur"]:
        return -1
    return case["temps_restant"]

def get_val_temps(case:dict)->None|tuple[int,int]:
    """return un couple contenant la valeur et le temps restant de la boite

    Args:
        case (dict): la case considérée

    Returns:
        None|tuple[int,int]: None si la case est un mur, sinon la valeur et le temps restant de la boite
    """    
    if case["mur"]:
        return None
    return case["valeur"],case["temps_restant"]


def set_boite(case:dict,valeur:int,proprietaire:int,temps_restant:int)->bool:
    """positionne une boite dans la case. Retourne True si l'opération s'est bien passée et False sinon

    Args:
        case (dict): la case considérée
        valeur (int): valeur de la boite
        proprietaire (int): identifiant du propriétaire
        temps_restant (int): indique soit la durée de vie de la boite soit le temps restant avant fusion

    Returns:
        bool: True si l'opération s'est bien passée et False sinon
    """
    # if case["mur"]:
    #     return False
    case["mur"]=False
    case["valeur"]=valeur
    case["proprietaire"]=proprietaire
    case["temps_restant"]=temps_restant
    return True

def mise_jour_temps_restant(case:dict):
    """diminue de 1 le temps restant de la boite. Si le temps passe à 0 et
        que la boite n'a pas de propriétaire, la valeur passe à 0

    Args:
        case (dict): la case considérée
    """
    if case["mur"] or case["temps_restant"]==0:
        return
    case["temps_restant"]-=1
    if case["temps_restant"]==0 and case["proprietaire"]==0:
        case["valeur"]=0



def set_val_boite(case:dict,valeur:int)->bool:
    """change la valeur de la boite dans une case. Retourne True si l'opération s'est bien passée et False sinon

    Args:
        case (dict): la case considérée
        valeur (int): valeur de la boite

    Returns:
        bool: True si l'opération s'est bien passée et False sinon
    """
    if case["mur"]:
        return False
    case["valeur"]=valeur
    return True

def set_val_temps_restant_boite(case:dict,valeur:int,temps_restant:int)->bool:
    """change la valeur de la boite dans une case. Retourne True si l'opération s'est bien passée et False sinon

    Args:
        case (dict): la case considérée
        valeur (int): valeur de la boite
        temps_restant (int): temps restant avant fusion de la boite

    Returns:
        bool: True si l'opération s'est bien passée et False sinon
    """
    if case["mur"]:
        return False
    case["valeur"]=valeur
    case["temps_restant"]=temps_restant
    return True



def enlever_boite(case:dict)->None|tuple[int,int,int]:
    """Enlever la boite qui se trouve dans la case et retourne le contenu de la case,
        None si la case est un mur

    Args:
        case (dict): la case considérée

    Returns:
        None|tuple[int,int,int]: None si la case est un mur, sinon un triplet contenant la valeur et le propriétaire de la boite ainsi que le temps restant
    """
    if case["mur"]:
        return None
    val=case["valeur"]
    prop=case["proprietaire"]
    tr=case["temps_restant"]
    case["valeur"]=0
    case["proprietaire"]=0
    case["temps_restant"]=0

    return val,prop,tr

def copy_case(case:dict)->dict:
    """fait une copie de la case
    Compléxité : O(N)    

    Args:
        case (dict): la case considérée

    Returns:
        dict: la copie de la case passée en paramètre
    """ 
    return dict(case)

def est_bonus_ou_boite(case:dict)->bool:
    # Bonus
    valeur_case = get_val_boite(case)
    if valeur_case < 0:
        return True
    
    # Boite
    proprietaire = get_proprietaire(case)
    return not proprietaire and valeur_case > 0