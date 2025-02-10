# coding: utf-8
"""
            SAE1.02 SERPIUT'O
         BUT1 Informatique 2024-2025

    Module IA.py
    Ce module implémente toutes les fonctions ainsi que l'IA de votre serpent
"""

import partie
import argparse
import client
import random
import arene
import serpent
import case

import matrice

direction_prec='X' # variable indiquant la décision précédente prise par le joueur. A mettre à jour soi-même
DIRECTIONS={"N":(-1,0),"E":(0,1),"S":(1,0),"O":(0,-1)}

####################################################################
### A partir d'ici, implémenter toutes les fonctions qui vous seront 
### utiles pour prendre vos décisions
### Toutes vos fonctions devront être documentées
####################################################################

# Complexité : O (N)

def directions_possibles(l_arene:dict,num_joueur:int)->str:
    """Renvoie les directions possible d'un joueur

    Args : 
        l_arene (dict): l'arène considéré
        num_joueur (int): le joueur considéré

    Returns:
        str : directions possibles
    """
    res=''
    mat=l_arene["matrice"]
    nb_lig=matrice.get_nb_lignes(mat)
    nb_col=matrice.get_nb_colonnes(mat)
    lig_dep,col_dep=serpent.get_liste_pos(l_arene["serpents"][num_joueur-1])[0]
    copy_arena = arene.copy_arene(l_arene)

    player_head_ligne,player_head_col = arene.get_serpent(copy_arena,num_joueur)[0]
    player_head_val = arene.get_val_boite(l_arene,player_head_ligne,player_head_col)

    for dir in 'NOSE':
        delta_lig,delta_col=DIRECTIONS[dir]
        lig_arr=lig_dep+delta_lig
        col_arr=col_dep+delta_col
        if lig_arr<0 or lig_arr>=nb_lig or col_arr<0 or col_arr>=nb_col:
            continue
        if case.est_mur(matrice.get_val(mat,lig_arr,col_arr)) and serpent.get_temps_mange_mur(l_arene["serpents"][num_joueur-1]) == 0:
            continue
        if case.get_proprietaire(matrice.get_val(mat,lig_arr,col_arr))==num_joueur:
            continue
        if player_head_val < case.get_val_boite (matrice.get_val(mat,lig_arr,col_arr)): #Si le la tête du joueur est inférieur à la boite
            continue
        res+=dir
    return res

# Complexité : O (N)

def objets_voisinage(l_arene: dict, num_joueur: int, dist_max: int) -> dict:
    """Retourne un dictionnaire indiquant pour chaque direction possible,
    les objets ou boîtes pouvant être mangés par le serpent du joueur et
    se trouvant dans le voisinage de la tête du serpent.

    Args:
        l_arene (dict): l'arène considérée.
        num_joueur (int): le numéro du joueur considéré.
        dist_max (int): le nombre de cases maximum autorisé à partir de la tête.

    Returns:
        dict: Un dictionnaire dont les clés sont des directions ("N", "S", "E", "O") et les valeurs des listes
              de triplets (distance, val_objet, prop). "distance" indique le nombre de cases jusqu'à l'objet,
              "val_objet" indique la valeur de l'objet ou de la boîte, et "prop" indique le propriétaire.
    """
    resultat = {direction: [] for direction in "NOSE"}
    queue = [] 
    visited = set()
    mat=l_arene["matrice"]
 

    tete_ligne, tete_col = arene.get_serpent(l_arene, num_joueur)[0]
    tete_val = arene.get_val_boite(l_arene, tete_ligne, tete_col)

    for direction, (delta_lig, delta_col) in DIRECTIONS.items():
        next_lig, next_col = tete_ligne + delta_lig, tete_col + delta_col
        if est_dans_arene(l_arene, next_lig, next_col):
            queue.append((next_lig, next_col, direction, 1))
            visited.add((next_lig, next_col))

    while queue:
        curr_lig, curr_col, initial_dir, distance = queue.pop(0)

        val_case = arene.get_val_boite(l_arene, curr_lig, curr_col)
        prop_case = case.get_proprietaire(matrice.get_val(mat,curr_lig,curr_col))

        if val_case != 0 and tete_val >= val_case:  
            resultat[initial_dir].append((distance, val_case, prop_case))

        if distance < dist_max:
            for delta_lig, delta_col in DIRECTIONS.values():
                next_lig, next_col = curr_lig + delta_lig, curr_col + delta_col
                if (next_lig, next_col) not in visited and est_dans_arene(l_arene, next_lig, next_col):
                    visited.add((next_lig, next_col))
                    queue.append((next_lig, next_col, initial_dir, distance + 1))

    return resultat

# Complexité : O (N)

def evaluer_direction(l_arene: dict, num_joueur: int, dist_max: int, directions_valides: dict) -> int:
    """
    Évalue une  direction donnée pour le joueur, en calculant une "valeur" basée
    sur les objets accessibles dans cette direction.

    Args:
        arene (dict): L'arène actuelle.
        num_joueur (int): Numéro du joueur.
        direction (str): Direction à évaluer ('N', 'S', 'E', 'O').
        dist_max (int): Distance maximale pour explorer dans cette direction.

    Returns:
        dict: Un dictionnaire associant la meilleure direction
    """
    tete_ligne, tete_col = arene.get_serpent(l_arene, num_joueur)[0]
    tete_val = arene.get_val_boite(l_arene, tete_ligne, tete_col)
    objets = objets_voisinage(l_arene, num_joueur, dist_max)

    dico_priorite = {}

    for direction, liste_objets in objets.items():
        if direction in directions_valides:

            for (distance, val_objet, prop_case) in liste_objets:
                dico_priorite[direction] = dico_priorite.get(direction,0) + priorite_objet(val_objet, prop_case, tete_val, num_joueur, l_arene) / distance

    
    return dico_priorite

# Complexité : O (1)

def priorite_objet(val_objet, prop_case, tete_val, num_joueur, l_arene):
    dico_priorite = {
        -5: 0,
        -4: 10,
        -3: 8,
        -2: 5,
        -1: 5,
        1: 4,
        2: 10
        }
    if prop_case == num_joueur:
        return 0

    if val_objet in dico_priorite.keys():

        return dico_priorite[val_objet]
    else: #Sinon c'est forcément un serpent
        if tete_val > val_objet: #Si la tête du joueur est plus grande que l'autre serpent
            return 5
        else:
            if serpent.get_temps_surpuissance(l_arene["serpents"][num_joueur-1]) == 0:
                return -50
            else:
                return 10

# Complexité : O (1)

def est_dans_arene(l_arene: dict, lig: int, col: int) -> bool:
    """
    Vérifie si une position donnée (ligne, colonne) est dans les limites de l'arène.

    Args:
        l_arene (dict): L'arène considérée.
        lig (int): La ligne de la position à vérifier.
        col (int): La colonne de la position à vérifier.

    Returns:
        bool: True si la position est dans l'arène, False sinon.
    """
    mat = l_arene["matrice"]
    nb_lig = matrice.get_nb_lignes(mat)
    nb_col = matrice.get_nb_colonnes(mat)

    # Vérifie si la position est dans les limites
    return 0 <= lig < nb_lig and 0 <= col < nb_col

# Complexité : O (1)

def going_back(dir: str):
    """Revoie la direction pour faire marche arrière

    Args:
        dir(str): la direction précédente

    Returns:    
        str: direction opposée de la direction précédente
    """
    backward_dir = ""

    match dir:
        case "N":
            backward_dir = "S"
        case "S":
            backward_dir = "N"
        case "O":
            backward_dir = "E"
        case "E":
            backward_dir = "O"

    return backward_dir

# Complexité : O (N)

def mon_IA_smart(num_joueur: int, la_partie: dict) -> str:
    """
    Fonction qui prend la décision du prochain coup pour le joueur de numéro `num_joueur`.

    Args:
        num_joueur (int): Numéro du joueur qui doit prendre une décision.
        la_partie (dict): Structure représentant l'état actuel de la partie.

    Returns:
        str: Une des lettres 'N', 'S', 'E' ou 'O' indiquant la direction choisie.
    """
    l_arene = partie.get_arene(la_partie)
    dist_max = 4

    directions_valides = directions_possibles(l_arene, num_joueur)
    if directions_valides == "":
        return going_back(arene.get_derniere_direction(l_arene, num_joueur))

    dico_priorite = evaluer_direction(l_arene, num_joueur, dist_max, directions_valides)
    if dico_priorite == {}:
        return random.choice(directions_valides)
    meilleur_dir = max(dico_priorite, key=dico_priorite.get)
    return meilleur_dir


if __name__=="__main__":
    parser = argparse.ArgumentParser()  
    parser.add_argument("--equipe", dest="nom_equipe", help="nom de l'équipe", type=str, default='Non fournie')
    parser.add_argument("--serveur", dest="serveur", help="serveur de jeu", type=str, default='localhost')
    parser.add_argument("--port", dest="port", help="port de connexion", type=int, default=1111)
    
    args = parser.parse_args()
    le_client=client.ClientCyber()
    le_client.creer_socket(args.serveur,args.port)
    le_client.enregistrement(args.nom_equipe,"joueur")
    ok=True
    while ok:
        ok,id_joueur,le_jeu,_=le_client.prochaine_commande()
        if ok:
            la_partie=partie.partie_from_str(le_jeu)
            actions_joueur=mon_IA_smart(int(id_joueur),la_partie)
            le_client.envoyer_commande_client(actions_joueur)
    le_client.afficher_msg("terminé")
