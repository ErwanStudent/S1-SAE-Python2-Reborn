# coding: utf-8
"""
            SAE1.02 SERPIUT'O
         BUT1 Informatique 2024-2025

        Module partie.py
        Ce module implémente l'API permettant de gérer une partie
"""
import arene
from utils import copie_dico

def Partie(nom_partie:str, duree_totale:int,temps_restant:int,arene:dict)-> dict:
    """Créer une nouvelle partie où l'arene a déjà été créée

    Args:
        nom_partie (str): nom de la partie 
        duree_totale (int): durée totale de la partie en nombre de tours
        temps_restant (int): nombre de tours restants pour la partie
        arene (dict): arene où se joue la partie

    Returns:
        dict: retourne un dictionnaire contenant les informations de la partie
    """    
    return {"nom_partie":nom_partie, "duree_totale":duree_totale,"temps_restant":temps_restant,
            "arene":arene}

def nouvelle_partie(nom_partie:str, duree_totale:int,nom_fic_plan:str):
    """Créer une nouvelle partie à partir d'un plan d'arene fourni sous forme d'un fichier texte.
        La partie n'aura pas de joueur et ne sera pas commencée

    Args:
        nom_partie (str): nom de la partie
        duree_totale (int): durée totale de la partie
        nom_fic_plan (str): nom du fichier texte contenant le plan

    Returns:
        dict: un dictionnaire contenant les informations de la partie
    """    
    return {"nom_partie":nom_partie, "duree_totale":duree_totale,"temps_restant":duree_totale,
            "arene":arene.set_plan_from_fic(nom_fic_plan)}

def get_nom_partie(partie:dict)->str:
    """retourne le nom d'une partie

    Args:
        partie (dict): la partie considérée

    Returns:
        str: le nom de la partie
    """    
    return partie["nom_partie"]

def get_duree_totale(partie:dict)->int:
    """retourne la durée totale d'une partie

    Args:
        partie (dict): la partie considérée

    Returns:
        int: le nombre de tours total partie
    """    
    return partie["duree_totale"]

def get_temps_restant(partie:dict)->int:
    """retourne le nombre de tours restant d'une partie

    Args:
        partie (dict): la partie considérée

    Returns:
        int:le nombre de tours restant de la partie
    """    
    return partie["temps_restant"]

def get_arene(partie:dict)->dict:
    """retourne l'arene dans laquelle se joue une partie

    Args:
        partie (dict): la partie considérée

    Returns:
        dict: l'arene dans laquelle se joue la partie
    """    
    return partie["arene"]

def get_nb_joueurs(partie:dict)->int:
    """retourne le nombre de joueurs participants à la partie

    Args:
        partie (dict): la partie considérée

    Returns:
        int: le nombre de joueurs inscrits à cette partie
    """    
    return arene.get_nb_joueurs(partie["arene"])

def ajouter_joueur(partie:dict, nom_joueur:str)->int:
    """Permet d'inscrire un nouveau joueur à la partie

    Args:
        partie (dict): La partie considérée
        nom_joueur (str): le nom du joueur qui s'incrit

    Returns:
        int: le numéro identifiant le joueur dans la partie
    """    
    return arene.ajouter_joueur(partie["arene"],nom_joueur)

def init_boites(partie:dict):
    """Ajoute autant de boites qu'il y de joueur sur l'arène

    Args:
        partie (dict): la partie considérée
    """    
    arene.ajouter_des_boites_ou_bonus(get_arene(partie),1,2,get_nb_joueurs(partie))

def maj_temps(partie:dict)->int:
    """Décrémente de 1 le temps restant d'une partie sans descendre en dessous de 0

    Args:
        partie (dict): la partie considérée

    Returns:
        int: le nombre de tours restants de la partie
    """    
    if partie["temps_restant"]>0:
        partie["temps_restant"]-=1
    return partie["temps_restant"]

def jouer_joueur(partie:dict,joueur:int,direction:str)->str:
    """Execute les actions liées à déplacement du joueur indiqué dans la direction indiquée

    Args:
        partie (dict): la partie considérée
        joueur (int): le numéro du joueur 
        direction (str): la direction choisie par le joueur

    Returns:
        str: un message indiquant les conséquences du déplacement
    """    
    return arene.deplacer_joueur(partie["arene"],joueur,direction)

def finir_tour(partie:dict):
    """Exécute les mises à jour du jeu après que chaque joueur ait effectuer son déplacement
        - fusion des boites des serpents
        - mise à jour des durées de vie des boites
        - ajout de nouvelles boites
        - ajout de nouveaux bonus
        - mise à jour du temps restant de la partie

    Args:
        partie (dict): La partie considérée
    """    
    larene=partie["arene"]
    arene.fusionner_boites_ex(larene)
    arene.mise_a_jour_temps(larene)
    arene.ajouter_des_boites_ou_bonus(larene,1,2,4)
    arene.ajouter_des_boites_ou_bonus(larene,-5,-1,2)
    maj_temps(partie)

def sauver_score(partie:dict,nom_fic:str):
    """sauvegarde du score de la partie dans un fichier texte

    Args:
        partie (dict): la partie considérée
        nom_fic (str): le nom du fichier où sauvegarder le score
    """     
    arene.sauver_score(partie["arene"],nom_fic)

def est_fini(partie:dict)->bool:
    """permet de savoir si une partie est terminée ou non

    Args:
        partie (dict): la partie considérée

    Returns:
        bool: un booléean à True si la partie est terminée et False sinon
    """    
    return partie["temps_restant"]<=0

def partie_2_str(partie:dict,sep=";")->str:
    """sérialise une partie sous la forme d'une chaine de caractères

    Args:
        partie (dict):  la partie considérée
        sep (str, optional): le caractère séparteur des infos d'une partie. Defaults to ";".

    Returns:
        str: une chaine de caractères permettant de connaitre toutes les informations de la partie
    """    
    res=partie["nom_partie"]+sep+str(partie["duree_totale"])+sep+str(partie["temps_restant"])+'\n'
    res+=arene.arene_2_str(partie["arene"])
    return res

def partie_from_str(la_chaine:str,sep=";") ->dict:
    """Crée à partir une chaine de caractères au bon format, une partie

    Args:
        la_chaine (str): la chaine de carectères décrivant la partie
        sep (str, optional): le caractère séparateur utilisé pour délimiter les informations. Defaults to ";".

    Returns:
        dict: la partie reconstituée
    """    
    ligne1=la_chaine.find("\n")
    nom_partie,duree_totale,temps_restant=la_chaine[:ligne1].split(sep)
    duree_totale=int(duree_totale)
    temps_restant=int(temps_restant)
    larene=arene.arene_from_str(la_chaine[ligne1+1:])
    return {"nom_partie":nom_partie, "duree_totale":duree_totale,"temps_restant":temps_restant,
            "arene":larene}

def copy_partie(partie:dict)->dict:
    """ recopie complètement une partie
    Compléxité : O(N)**n    

    Args:
        partie (dict): la partie considérée

    Returns:
        dict: la recopie de la partie passée en paramètres
    """
    return copie_dico(partie)