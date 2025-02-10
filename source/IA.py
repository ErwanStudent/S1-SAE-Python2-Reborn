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
import arene
import serpent
import matrice
import case

####################################################################
### A partir d'ici, implémenter toutes les fonctions qui vous seront 
### utiles pour prendre vos décisions
### Toutes vos fonctions devront être documentées
####################################################################

# Types de boites 
BOITE_PLUS1 = 1
BOITE_PLUS2 = 2

directions = {"N", "O", "S", "E"}
inverse_directions = {
    "N": "S",
    "O": "E",
    "S": "N",
    "E": "O"
}

def get_points_case_tri(valeur_case: int, l_arene: dict, serpent_case: dict) -> int|float:
    """Obtenir le nombre de points d'une case pour pouvoir trier selon leurs avantages dans le jeu.
    Complexité : O(1)

    Args:
        valeur_case (int): La valeur de la case (Boite +1, Surprotection, etc.)
        l_arene (dict): Le plateau de l'arène
        serpent_case (dict): La case du serpent dans l'arène

    Returns:
        int or float: Le points de la case (Plus c'est positif, mieux c'est)
    """

    serpent_points = serpent.get_points(serpent_case)
    match valeur_case:
        case arene.AJOUTE:
            return -60
        case arene.MULTIPLIE:
            return -110
        case arene.SURPUISSANCE:
            if serpent_points < abs(arene.SURPUISSANCE * 2):
                return 0
            return -3
        case arene.MANGE_MUR:
            if serpent_points < abs(arene.MANGE_MUR * 2):
                return -5
            temps_restant = serpent.get_temps_mange_mur(serpent_case)
            return -50 + temps_restant * 5
        case arene.PROTECTION:
            if serpent_points < abs(arene.PROTECTION * 2):
                return -5
            temps_restant = serpent.get_temps_protection(serpent_case)
            return -25 + temps_restant * 2.5
        case 1: # Boite +1
            queue_pos = serpent.get_queue(serpent_case)
            queue_valeur = arene.get_val_boite(l_arene, queue_pos[0], queue_pos[1])
            if queue_valeur == 1:
                return -150
            return 2
        case 2: # Boite +2
            queue_pos = serpent.get_queue(serpent_case)
            queue_valeur = arene.get_val_boite(l_arene, queue_pos[0], queue_pos[1])
            if queue_valeur <= 2:
                return -150
            return 1
        case _:
            return -valeur_case

def directions_possibles(l_arene: dict, position: tuple[int, int], num_joueur: int, bloque_boites: bool = True)->list[tuple]:
    """Indique les directions possible pour le joueur num_joueur
        c'est à dire les directions qu'il peut prendre sans se cogner dans
        un mur, sortir de l'arène ou se cogner sur une boîte trop grosse pour sa tête.
    Compléxité : O(N)

    Args:
        l_arene (dict): l'arène considérée
        position (tuple): La position du joueur
        num_joueur (int): le numéro du joueur
        bloque_boites (bool): Indique si les boites +1 ou +2 sont bloquées ou non

    Returns:
        list: Une liste de tuples avec les prochaines cordonnées possibles.
    """    

    [nb_lig, nb_col] = arene.get_dim(l_arene)

    serpent_joueur = arene.get_serpent_complet(l_arene, num_joueur)
    points_joueur = serpent.get_points(serpent_joueur)

    coords=[]
    for direction in directions:
        delta_lig,delta_col=arene.DIRECTIONS[direction]
        
        ligne_fin=position[0]+delta_lig
        colonne_fin=position[1]+delta_col
        if ligne_fin<0 or ligne_fin>=nb_lig or colonne_fin<0 or colonne_fin>=nb_col:
            continue

        if not serpent.get_temps_mange_mur(serpent_joueur) and arene.est_mur(l_arene, ligne_fin, colonne_fin):
            continue

        proprietaire = arene.get_proprietaire(l_arene, ligne_fin, colonne_fin)
        if arene.get_proprietaire(l_arene, ligne_fin, colonne_fin) == num_joueur:
            continue

        if proprietaire:
            serpent_proprietaire = arene.get_serpent_complet(l_arene, proprietaire)
            if serpent.get_temps_protection(serpent_proprietaire):
                continue

        valeur_boite = arene.get_val_boite(l_arene, ligne_fin, colonne_fin)
        case_point = arene.get_case(l_arene, ligne_fin, colonne_fin)
        if case.contient_boite(case_point):
            if valeur_boite > 0:
                tete_cordos = serpent.get_tete(serpent_joueur)
                tete_points = arene.get_val_boite(l_arene, tete_cordos[0], tete_cordos[1])

                if bloque_boites:
                    serpent_pos = serpent.get_liste_pos(serpent_joueur)
                    if tete_points >= 4 or len(serpent_pos) >= 2:
                        continue

                if valeur_boite > tete_points:
                    continue
            else:
                if abs(valeur_boite) > points_joueur:
                    continue
        coords.append((ligne_fin, colonne_fin))
    return coords

def fabriquer_calque(l_arene:dict, num_joueur: int, position_depart: tuple[int, int], bloque_boite = True) -> dict:
    """Fabriquer le calque pour une position de départ.
    Compléxité : O(N**2)

    Args:
        l_arene (dict): L'arène du jeu
        num_joueur (int): Le numéro du joueur
        position_depart (tuple[int, int]): La position de départ du joueur
        bloque_boite (bool, optional): Indique si les boites +1 ou +2 sont bloquées ou non. Defaults to True.

    Returns:
        dict: La matrice du calque.
    """

    (nb_lignes, nb_colonnes) = arene.get_dim(l_arene)
    matrice_calque = matrice.Matrice(nb_lignes, nb_colonnes)

    cpt = 0
    matrice.set_val(matrice_calque, position_depart[0], position_depart[1], cpt)
    
    voisins_temp = set()
    points_a_verifier = { position_depart }
    while len(points_a_verifier):
        cpt += 1
        for point in points_a_verifier:
            voisins_point = directions_possibles(l_arene, point, num_joueur, bloque_boite)
            for voisin in voisins_point:
                if (matrice.get_val(matrice_calque, voisin[0], voisin[1]) == None):
                    matrice.set_val(matrice_calque, voisin[0], voisin[1], cpt)
                    voisins_temp.add(voisin)
        points_a_verifier = voisins_temp.copy()
        voisins_temp = set()
    return matrice_calque

def fabriquer_chemin(l_arene: dict, num_joueur: int, position_depart: tuple[int, int], position_arrivee: tuple[int, int], bloque_boites: bool = True) -> list|None:
    """Fabriquer le chemin d'une position de départ à une position d'arrivée.
    Complexité : O(N**2)
    
    Args:
        l_arene (dict): L'arène du jeu
        num_joueur (int): Le numéro du joueur
        position_depart (tuple[int, int]): La position de départ du joueur
        position_arrivee (tuple[int, int]): La position d'arrivée voulu.
        bloque_boites (bool, optional): Indique si les boites +1 ou +2 sont bloquées ou non. Defaults to True.

    Returns:
        list or none: Le chemin entre les deux points.
    """    
    
    if position_depart == position_arrivee:
        return []

    mat_calque = fabriquer_calque(l_arene, num_joueur, position_depart, bloque_boites)

    chemin = [position_arrivee]
    cpt = matrice.get_val(mat_calque, position_arrivee[0], position_arrivee[1])
    if cpt == None:
        return None     
    
    cpt -= 1
    voisin = position_arrivee
    while cpt != 0:
        i = 0
        trouve = False
        voisins_points = directions_possibles(l_arene, voisin, num_joueur, bloque_boites)
        while not trouve and i < len(voisins_points):
            (x, y) = voisins_points[i]
            if matrice.get_val(mat_calque, x, y) == cpt:
                voisin = voisins_points[i]
                chemin.append(voisin)

                cpt -= 1
                trouve = True
            else:
                i += 1
    return chemin

def get_coordinates(position_depart: tuple[int, int], position_arrivee: tuple[int, int]) -> str|None:
    """Obtenir la direction entre deux points
    Complexité : O(N)

    Args:
        position_depart (tuple[int, int]): La position de départ
        position_arrivee (tuple[int, int]): La position d'arrivée

    Returns:
        str or None: La direction entre les deux points ou None si invalide
    """

    for direction in "NSEO":
        (y_direction, x_direction) = arene.DIRECTIONS[direction]
        if position_arrivee[0] - y_direction == position_depart[0] and position_arrivee[1] - x_direction == position_depart[1]:
            return direction
    return None

def objets_voisinage(l_arene:dict, num_joueur:int, dist_max:int, objets_ignores = set()):
    """Obtenir les objets dans le voisinage du joueur.
    Complexité : O(N**2)

    Args:
        l_arene (dict): L'arène du jeu
        num_joueur (int): Le numéro de joueur
        dist_max (int): La distance max des objets pris en compte
        objets_ignores (set, optional): Les objets non pris en compte. Defaults to set().

    Returns:
        list[tuple]: La liste des objets pris en compte.
    """

    arene_copie = arene.copy_arene(l_arene)

    (nb_lignes, nb_colonnes) = arene.get_dim(l_arene)
    matrice_calque = matrice.Matrice(nb_lignes, nb_colonnes)

    serpent_joueur = arene.get_serpent_complet(l_arene, num_joueur)
    position_tete = serpent.get_tete(serpent_joueur)

    cpt = 0
    objets = []
    matrice.set_val(matrice_calque, position_tete[0], position_tete[1], cpt)

    voisins_temp = set()
    points_a_verifier = { position_tete }
    while len(points_a_verifier) and cpt < dist_max:
        cpt += 1
        for (y_point, x_point) in points_a_verifier:
            voisins_point = directions_possibles(arene_copie, (y_point, x_point), num_joueur)
            for voisin in voisins_point:
                voisin_case = arene.get_case(arene_copie,voisin[0],voisin[1])
                valeur_case = case.get_val_boite(voisin_case)
                
                if matrice.get_val(matrice_calque, voisin[0], voisin[1]) == None:
                    if case.est_bonus_ou_boite(voisin_case):
                        if not valeur_case in objets_ignores:
                            temps_restant = case.get_temps_restant(voisin_case)
                            if cpt <= dist_max and temps_restant >= cpt:
                                if not est_cul_de_sac(arene_copie, voisin, num_joueur):
                                    proprietaire = case.get_proprietaire(voisin_case)
                                    objets.append((cpt, valeur_case, proprietaire, voisin))
                    else:
                        proprietaire = case.get_proprietaire(voisin_case)
                        if proprietaire and proprietaire != num_joueur:
                            if cpt <= 3:
                                objets.append((cpt, valeur_case * 3, proprietaire, voisin))

                    voisins_temp.add(voisin)
                    matrice.set_val(matrice_calque, voisin[0], voisin[1], cpt)

        arene.mise_a_jour_temps(arene_copie)
        arene.fusionner_boites_ex(arene_copie)

        points_a_verifier = voisins_temp.copy()
        voisins_temp = set()
    return objets

def trier_objets(objets: list[tuple], l_arene:dict, serpent_case: dict):
    """Trier les objets selon leur importance dans le jeu.
    Complexité : O(NlogN)

    Args:
        objets (list[tuple]): Les objets à proximités.
        l_arene (dict): L'arène du jeu
        serpent_case (dict): Les données du serpent du joueur.

    Returns:
        list[tuple]: Les objets remis dans l'ordre suivant leur importance.
    """

    def critere(objet):
        (distance, valeur_case, _proprietaire, _position) = objet
        return distance * 0.5 + get_points_case_tri(valeur_case, l_arene, serpent_case) * 0.5
    return sorted(objets, key=critere)

def obtenir_chemin_adequat(l_arene: dict, num_joueur: int, position: tuple[int, int], serpent_case: dict, bloque_boites: bool = True):
    """Obtenir le chemin le plus adéquat selon la position du joueur. 
    Complexité O(N**2)
    
    Args:
        l_arene (dict): L'arène du jeu
        num_joueur (int): Le numéro du joueur
        position (tuple[int, int]): La position du joueur
        serpent_case (dict): Les données du serpent du joueur.
        bloque_boites (bool, optional): Indique si les boites +1 ou +2 sont bloquées ou non. Defaults to True.
    """

    def tri_case_vide(case_valide):
        return get_points_case_tri(case_valide[1], l_arene, serpent_case)

    cases_valides = []
    diections_chemin = directions_possibles(l_arene, position, num_joueur, bloque_boites)
    for direction_chemin in diections_chemin:
        case_position = arene.get_case(l_arene, direction_chemin[0], direction_chemin[1])
        if not est_cul_de_sac(l_arene, direction_chemin, num_joueur):
            valeur_case = case.get_val_boite(case_position)
            proprietaire = case.get_proprietaire(case_position)

            cases_valides.append((1, valeur_case, proprietaire, direction_chemin))

    if not len(cases_valides):
        return None

    cases_tries = sorted(cases_valides, key=tri_case_vide)
    return cases_tries[0]

def est_cul_de_sac(l_arene:dict, position: tuple[int, int], num_joueur: int) -> bool:
    """Vérifie si une position est un cul-de-sac.
    Complexité : O(N**2)

    Args:
        l_arene (dict): L'arène du jeu.
        position (tuple[int, int]): La position du joueur.
        num_joueur (int): Le numéro du joueur

    Returns:
        bool: Indique si oui ou non la position est un cul-de-sac.
    """

    serpent_pos = arene.get_serpent(l_arene, num_joueur)
    if len(serpent_pos) == 1 and arene.get_val_boite(l_arene, position[0], position[1]) < 0:
        return False
    
    arene_copie = arene.copy_arene(l_arene)

    points_verifies = set()
    points_a_verifier = { position }
    while len(points_a_verifier):
        for point in points_a_verifier.copy():
            points_verifies.add(point)
            directions_point = directions_possibles(arene_copie, point, num_joueur)
            if len(directions_point) >= 2:
                return False

            points_a_verifier.remove(point)
            points_a_verifier = set(directions_point).difference(points_verifies)
        arene.fusionner_boites_ex(l_arene)
        arene.mise_a_jour_temps(arene_copie)
    return True

def obtenir_prochaine_direction(l_arene: dict, num_joueur: int, la_partie: dict) -> str:
    """Obtenir la prochaine direction de l'IA.
    Complexité : O(N**2)

    Args:
        l_arene (dict): L'arène
        num_joueur (int): Le numéro du joueur
        la_partie (dict): La partie

    Returns:
        str: La direction de l'IA.
    """

    chemin = None
    serpent_joueur = arene.get_serpent_complet(l_arene, num_joueur)
    position = serpent.get_tete(serpent_joueur)

    objets_ignores = set()
    if arene.get_val_boite(l_arene, position[0], position[1]) > 1:
        objets_ignores.add(BOITE_PLUS1)

    if len(serpent.get_liste_pos(serpent_joueur)) >= 2 or arene.get_val_boite(l_arene, position[0], position[1]) >= 2:
        objets_ignores.add(BOITE_PLUS2)


    objet = None
    max_distance = 10
    objets = objets_voisinage(l_arene, num_joueur, max_distance, objets_ignores)
    if len(objets):
        objets_tries = trier_objets(objets, l_arene, serpent_joueur)

        objet = objets_tries[0]
        chemin = fabriquer_chemin(l_arene, num_joueur, position, objet[3])

    taille_serpent = len(serpent.get_liste_pos(serpent_joueur))
    if taille_serpent >= 2:
        tour_restant = partie.get_temps_restant(la_partie)
        if (objet and objet[0] > tour_restant) or taille_serpent > 3:
            queue = serpent.get_queue(serpent_joueur)
            queue_valeur = arene.get_val_boite(l_arene, queue[0], queue[1])
            tete_valeur = arene.get_val_boite(l_arene, position[0], position[1])
            if (taille_serpent >= 3 and (tete_valeur / 2) > queue_valeur) or queue_valeur == tete_valeur:
                cur_dir = serpent.get_derniere_direction(serpent_joueur)
                return inverse_directions[cur_dir]

    if not chemin:
        deplacement = obtenir_chemin_adequat(l_arene, num_joueur, position, serpent_joueur, False)
        if deplacement:
            print("secours")
            chemin = fabriquer_chemin(l_arene, num_joueur, position, deplacement[3], False)

    if not chemin:
        print("miam miam")
        cur_dir = serpent.get_derniere_direction(serpent_joueur)
        return inverse_directions[cur_dir]
    return get_coordinates(position, chemin[len(chemin) - 1])

def mon_IA2(num_joueur:int, la_partie:dict)->str:
    """Lancement de l'IA.
    Complexité : O(N**2)

    Args:
        num_joueur (int): Le numéro du joueur
        la_partie (dict): La partie

    Returns:
        str: La direction de l'IA
    """

    arene_partie = partie.get_arene(la_partie)
    return obtenir_prochaine_direction(arene_partie, num_joueur, la_partie)               
 
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
            actions_joueur=mon_IA2(int(id_joueur),la_partie)
            le_client.envoyer_commande_client(actions_joueur)
    le_client.afficher_msg("terminé")