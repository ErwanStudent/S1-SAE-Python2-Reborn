# coding: utf-8
"""
            SAE1.02 SERPIUT'O
         BUT1 Informatique 2024-2025

    Module serpent.py
    Ce module implémente l'API permettant de gérer les informations des joueurs (idenfier à leur serpent)
"""
import arene
from utils import copie_dico

def Serpent(nom_joueur:str, num_joueur:int,points:int=0,positions:list=None,tps_s:int=0,tps_p:int=0,tps_m:int=0,direction:str='N')->dict:
    """Créer un joueur avec toutes les informations le concernant.
    Compléxité : O(1)

    Args:
        nom_joueur (str): nom du joueur
        num_joueur (int): numero du joueur
        points (int, optional): nombre de points attribués au joueur. Defaults to 0.
        positions (list, optional): la liste des positions occupées par le serpent sur l'arène. Defaults to None.
        tps_s (int, optional): temps restant pour le bonus surpuissance. Defaults to 0.
        tps_p (int, optional): temps restant pour le bonus protection. Defaults to 0.
        tps_m (int, optional): temps restant pour le bonus mange-mur. Defaults to 0.
        direction (str, optional): dernière direction prise par le serpent. Defaults to 'N'.

    Returns:
        dict: une dictionnaire contenant les informations du serpent
    """

    return {
        "nom_joueur": nom_joueur,
        "num_joueur": num_joueur,
        "points": points,
        "positions": positions,
        "tps_s": tps_s,
        "tps_p": tps_p,
        "tps_m": tps_m,
        "direction": direction
    }

def get_nom(serpent:dict)->str:
    """retourne le nom du joueur associé au serpent
    Compléxité : O(1)

    Args:
        serpent (dict): le serpent considéré

    Returns:
        str: le nom du joueur associé à ce serpent
    """    
    
    return serpent["nom_joueur"]

def get_num_joueur(serpent:dict)->int:
    """retourne le numéro du joueur associé au serpent
    Compléxité : O(1)

    Args:
        serpent (dict): le serpent considéré

    Returns:
        int: le numéro du joueur associé à ce serpent
    """   
    return serpent["num_joueur"]


def get_points(serpent:dict)->int:
    """retourne le nombre de points du joueur associé au serpent
    Compléxité : O(1)

    Args:
        serpent (dict): le serpent considéré

    Returns:
        int: le nombre de points du joueur associé à ce serpent
    """   
    
    return serpent["points"]

def get_liste_pos(serpent:dict)->list:
    """retourne la liste des positions occupées par le serpent sur l'arène. La première position étant la tête du serpent
    Compléxité : O(1)

    Args:
        serpent (dict): le serpent considéré

    Returns:
        list: la liste des positions occupées par le serpent
    """
    positions = serpent.get("positions", None)
    if positions == None:
        return []
    return positions

def get_queue(serpent:dict)->[int,int]:
    """retourne la position (lig,col) de la queue du serpent dans l'arène
    Compléxité : O(1)

    Args:
        serpent (dict): le serpent considéré

    Returns:
        [int,int]: la position lig,col du la queue du serpent
    """

    positions = get_liste_pos(serpent)
    if not len(positions):
        return None   
    return positions[len(positions) - 1]

def get_derniere_direction(serpent:dict)->str:
    """retourne la dernière direction choisie par le joueur pour se déplacer
    Compléxité : O(1)

    Args:
        serpent (dict): le serpent considéré

    Returns:
        str: un des caractère N S E O
    """    
    
    return serpent["direction"]

def get_bonus(serpent:dict)->list:
    """retourne une liste contenant les bonus obtenus par le joueur
        c'est-à-dire ceux pour lesquels le temps restant est supérieur à 0
    Compléxité : O(1)

    Args:
        serpent (dict): le serpent considéré

    Returns:
        list: la liste des bonus du joueur
    """  

    bonus = []
    if get_temps_surpuissance(serpent) > 0:
        bonus.append(arene.SURPUISSANCE)
    if get_temps_protection(serpent) > 0:
        bonus.append(arene.PROTECTION)
    if get_temps_mange_mur(serpent) > 0:
        bonus.append(arene.MANGE_MUR)
    return bonus

def ajouter_points(serpent:dict,nb_points:int):
    """ajoute (ou enlève) des points à un serpent
    Compléxité : O(1)

    Args:
        serpent (dict): le serpent considéré
        nb_points (int): le nombre de points à ajouter (si négatif enlève des points)
    """    
    
    serpent["points"] += nb_points

def set_liste_pos(serpent:dict, tete:list):
    """Initialise la liste des positions d'un serpent
    Compléxité : O(1)

    Args:
        serpent (dict): le serpent considéré
        tete (list): la liste des positions occupées par ce serpent
    """    ""
    serpent["positions"] = tete

def set_derniere_direction(serpent:dict, direction:str):
    """Mettre à jour la dernière direction utilisée par le serpent (utile pour l'affichage)
    Compléxité : O(1)

    Args:
        serpent (dict): le serpent considéré
        direction (str): un des caractère N S E O
    """
    if direction in ["N", "S", "E", "O"]:
        serpent["direction"] = direction 

def to_str(serpent:dict)->str:
    """produit une chaine de caractères contenant les informations principales d'un serpent sour la forme
    Joueur 1 -> 143 s:0 m:4 p:0
    où Joueur 1 est le nom du joueur, après la flèche se trouve le nombre de point
    puis le temps restant de chaque bonus (supuissante, mange mur et protection)
    Compléxité : O(1)

    Args:
        serpent (dict): le serpent considéré

    Returns:
        str: la chaine de caractères donnant les informations principales d'un serpent 
    """    
    return f"{get_nom(serpent)} -> {get_points(serpent)} s:{get_temps_surpuissance(serpent)} m:{get_temps_mange_mur(serpent)} p:{get_temps_protection(serpent)}"
    

def get_temps_protection(serpent:dict)->int:
    """indique le temps restant pour le bonus protection
    Compléxité : O(1)

    Args:
        serpent (dict): le serpent considéré

    Returns:
        int: le nombre de tours restant pour ce bonus
    """    
    return serpent.get("tps_p", 0)

def get_temps_mange_mur(serpent:dict)->int:
    """indique le temps restant pour le bonus mange mur
    Compléxité : O(1)

    Args:
        serpent (dict): le serpent considéré

    Returns:
        int: le nombre de tours restant pour ce bonus
    """   
    return serpent.get("tps_m", 0)

def get_temps_surpuissance(serpent:dict)->int:
    """indique le temps restant pour le bonus surpuissance
    Compléxité : O(1)

    Args:
        serpent (dict): le serpent considéré

    Returns:
        int: le nombre de tours restant pour ce bonus
    """
    return serpent.get("tps_s", 0)   

def ajouter_temps_protection(serpent:dict, temps:int)->int:
    """ajoute du temps supplémentaire pour le bonus protection
    Compléxité : O(1)

    Args:
        serpent (dict): le serpent considéré
        temps (int): le nombre de tours à ajouter

    Returns:
        int: le nombre de tours total restant pour ce bonus
    """    
    serpent["tps_p"] = get_temps_protection(serpent) + temps

def ajouter_temps_mange_mur(serpent:dict, temps:int)->int:
    """ajoute du temps supplémentaire pour le bonus mange mur
    Compléxité : O(1)

    Args:
        serpent (dict): le serpent considéré
        temps (int): le nombre de tours à ajouter

    Returns:
        int: le nombre de tours total restant pour ce bonus
    """    
    
    serpent["tps_m"] = get_temps_mange_mur(serpent) + temps

def ajouter_temps_surpuissance(serpent:dict, temps:int)->int:
    """ajoute du temps supplémentaire pour le bonus surpuissance
    Compléxité : O(1)

    Args:
        serpent (dict): le serpent considéré
        temps (int): le nombre de tours à ajouter

    Returns:
        int: le nombre de tours total restant pour ce bonus
    """    
    serpent["tps_s"] = get_temps_surpuissance(serpent) + temps

def maj_temps(serpent:dict):
    """Décrémente les temps restant pour les bonus de ce serpent
    Attention les temps ne peuvent pas être négatif
    Compléxité : O(1)

    Args:
        serpent (dict): le serpent considéré
    """    
    if get_temps_surpuissance(serpent) > 0:
        ajouter_temps_surpuissance(serpent, -1)
    
    if get_temps_protection(serpent) > 0:
        ajouter_temps_protection(serpent, -1)
            
    if get_temps_mange_mur(serpent) > 0:
        ajouter_temps_mange_mur(serpent, -1)
    

def serpent_2_str(serpent:dict, sep=";")->str:
    """Sérialise un serpent sous la forme d'une chaine de caractères
    contenant 2 lignes.
    nom_j;num_j;nb_point;tps_surpuissance;tps_mange_mur;tps_protection;direction
    lig1;col1;lig2;col2;...
    La première ligne donne les informations autres que la liste des positions du serpent
    la deuxième ligne donné la liste des position du serpent en commençant par la tête
    Compléxité : O(N) + O(P) => O(M)

    Args:
        serpent (dict): le serpent considéré
        sep (str, optional): le caractère séparant les informations du serpent. Defaults to ";".

    Returns:
        str: la chaine de caractères contenant les toutes informations du serpent
    """
    informations_serpent = []
    for element in ["nom_joueur", "num_joueur", "points", "tps_s", "tps_m", "tps_p", "direction"]:
        informations_serpent.append(str(serpent[element]))

    informations_positions = []
    for (ligne, colonne) in get_liste_pos(serpent):
        informations_positions.append(str(ligne))
        informations_positions.append(str(colonne))

    res = sep.join(informations_serpent) + "\n" + sep.join(informations_positions) + "\n"
    return res

def serpent_from_str(la_chaine, sep=";")->dict:
    """Reconstruit un serpent à partir d'une chaine de caractères
       telle que celle produite par la fonction précédente
    Compléxité : O(N/2)

    Args:
        la_chaine (_type_): la chaine de caractères contenant les informations du serpent
        sep (str, optional): le caractère servant à séparer les informations du serpent. Defaults to ";".

    Returns:
        dict: Le serpent représenté dans la chaine de caractères
    """
    infos_brut = la_chaine.split("\n")
    
    info_serpent = infos_brut[0]
    info_positions = infos_brut[1]
    [nom_j,num_j,nb_point,tps_surpuissance,tps_mange_mur,tps_protection, direction] = info_serpent.split(sep)

    positions = []
    positions_brut = info_positions.split(";")
    for i in range(1, len(positions_brut), 2):
        ligne = positions_brut[i -1]
        colonne = positions_brut[i]
        
        positions.append((int(ligne), int(colonne)))

    if not len(positions):
        positions = None

    return Serpent(nom_j, int(num_j), int(nb_point), positions, int(tps_surpuissance), int(tps_protection), int(tps_mange_mur), direction)

def copy_serpent(serpent:dict)->dict:
    """fait une copie du serpent passer en paramètres
    Attention à bien faire une copie de la liste des positions
    Compléxité : O(N)**n    

    Args:
        serpent (dict): le serpent à recopier

    Returns:
        dict: la copie du serpent passé en paramètres
    """
    return copie_dico(serpent)

def get_tete(serpent:dict)->[int,int]:
    """retourne la position (lig,col) de la queue du serpent dans l'arène
    Compléxité : O(1)

    Args:
        serpent (dict): le serpent considéré

    Returns:
        [int,int]: la position lig,col du la queue du serpent
    """

    positions = get_liste_pos(serpent)
    if not len(positions):
        return None   
    return positions[0]

def set_points(serpent:dict,nb_points:int):
    """Défini  des points à un serpent
    Compléxité : O(1)

    Args:
        serpent (dict): le serpent considéré
        nb_points (int): le nombre de points à définir
    """    
    
    serpent["points"] = nb_points