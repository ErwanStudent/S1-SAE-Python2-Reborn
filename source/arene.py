# coding: utf-8
"""
            SAE1.02 SERPIUT'O
         BUT1 Informatique 2024-2025

    Module arene.py
    Ce module implémente l'API permettant de gérer l'arène du jeu
"""
import serpent
import matrice
import case
import random
import ansiColor
import operator
from utils import copie_dico

TEMPS_BOITE=10
TEMPS_FUSION=8
TEMPS_BONUS=10
MALUS=-10
DIRECTIONS={"N":(-1,0),"E":(0,1),"S":(1,0),"O":(0,-1)}

# les differents types de bonus
AJOUTE=-1
MULTIPLIE=-2
SURPUISSANCE=-3
MANGE_MUR=-4
PROTECTION=-5

# traduction des bonus en caractères
BONUS={AJOUTE:'+', # ajoute une boite de la même valeur que la queue du serpent
       MULTIPLIE:'*', # multiplie par 2 la plus petite boite du serpent
       MANGE_MUR:'/', # Permet de manger les murs (en perdant des points)
       SURPUISSANCE:"-", # Permet de manger des boites + grosse que la tête pendant la durée de vie du bonus
       PROTECTION:'%'  # protège le serpent pendant la durée de vie du bonus
       }

def Arene(nb_lig:int,nb_col:int,noms_participants:list[str])->dict:
    """Créer une arène avec un plateau de nb_lig lignes et nb_col colonnes pour nb_joueurs joueurs

    Args:
        nb_lig (int): le nombre de lignes de l'arène
        nb_col (int): le nombre de colonnes de l'arène
        noms_participants (list[str]): la liste des noms des participants

    Returns:
        dict: le dictionnaire que vous aurez choisi pour représenter cette arène
    """
    serpents=[]
    coul=1
    for nom in noms_participants:
        serpents.append(serpent.Serpent(nom,coul))
        coul+=1

    mat= matrice.Matrice(nb_lig,nb_col)
    return {"matrice":mat,"nb_joueurs":len(serpents),"serpents":serpents}

def set_plan_from_fic(nom_fic:str)->dict|None:
    """charge un plan d'arène à partir d'un fichier texte

    Args:
        nom_fic (str): nom du fichier de plan

    Returns:
        dict|None: retourne l'arène si tout s'est bien passé et None sinon
    """
    with open(nom_fic) as fic:
        plan=fic.read()
    fin_ligne1=plan.find('\n')
    nb_lig,nb_col=plan[:fin_ligne1].split(",")
    nb_ligi=int(nb_lig)
    nb_coli=int(nb_col)
    fin=len(plan)
    if plan.endswith('\n'):
        fin=len(plan)-1
    arene=Arene(nb_ligi,nb_coli,[])
    set_plan(arene,plan[fin_ligne1+1:fin])
    return arene

def set_plan(arene:dict,plan:str)->bool:
    """pose les murs dans l'arène en fonction du plan fourni sous forme d'une chaine de caractères
        contenant des 'X' pour les murs et des ' ' pour les couloirs. Les lignes sont séparées pas des '\n'
        Exemple de plan pour une arène de 4 lignes 13 colonnes
        xx   xx xx xx
        xx x     x  x
        x  x   x    x
        xxxxxxxxxxxxx
        Si le plan n'est pas correct la fonction retourne False et l'arène est dans un état indéterminé

    Args:
        arene (dict): l'arène à créer
        plan (str): la chaine de caractères définissant le plan de l'arène
    
    Returns:
        bool: True si l'opération s'est bien passée et False sinon.
    """
    liste=plan.split('\n')
    mat=arene["matrice"]
    nb_col=matrice.get_nb_colonnes(mat)
    if len(liste)!=matrice.get_nb_lignes(mat):
        return False
    for i in range(len(liste)):
        j=0
        for car in liste[i]:
            if j>=nb_col:
                return False
            if car=='X':
                matrice.set_val(mat,i,j,case.Case(True))
            elif car==' ':
                matrice.set_val(mat,i,j,case.Case(False))
            else:
                return False
            j+=1
        if j!=nb_col:
            return False
    return True

def get_dim(arene:dict)->[int,int]:
    """return les dimensions de l'arène sous la forme (nb_lignes,nb_colonnes)

    Args:
        arene (dict): l'arène considérée

    Returns:
        [int,int]: le nombre de lignes et de colonnes de l'arène
    """    
    return matrice.get_dim(arene["matrice"])

def get_nb_joueurs(arene:dict)->int:
    """retourne le nombre de joueurs présents sur l'arène

    Args:
        arene (dict): l'arène considérée

    Returns:
        int: le nombre de joueurs enregistrés
    """    
    return arene["nb_joueurs"]

def est_mur(arene:dict,lig:int,col:int)->bool:
    """indique si la case de l'arene qui se situe à la position lig,col est un mur

    Args:
        arene (dict): l'arène considérée
        lig (int): le numéro de la ligne de l'arène
        col (int): le numéro de la colonne de l'arène

    Returns:
        bool: True si la case de l'arène est un mur et False sinon
    """    
    return case.est_mur(matrice.get_val(arene["matrice"],lig,col))

def est_bonus(arene:dict,lig:int,col:int)->bool:
    """indique si la case de l'arene qui se situe à la position lig,col contient un bonus

    Args:
        arene (dict): l'arène considérée
        lig (int): le numéro de la ligne de l'arène
        col (int): le numéro de la colonne de l'arène

    Returns:
        bool: True si la case de l'arène contient un trésor et False sinon
    """    
    return case.get_val_boite(matrice.get_val(arene["matrice"],lig,col))<0

def get_val_boite(arene:dict,lig:int,col:int)->int:
    """Permet de connaitre la valeur de la boite qui se trouve sur la case lig,col de l'arene.
        0 indique qu'il n'y a pas de boite

    Args:
        arene (dict): l'arene considérée
        lig (int): le numéro de la ligne de l'arène
        col (int): le numéro de la colonne de l'arène

    Returns:
        int: valeur de la boite qui se trouve sur la case lig,col de l'arene
    """    
    return case.get_val_boite(matrice.get_val(arene["matrice"],lig,col))

def get_proprietaire(arene:dict, lig:int, col:int)->int:
    """Permet de connaitre le propriétaire de la boite qui se trouve sur la case lig,col de l'arene.
        0 indique qu'il n'y a pas de propriétaire

    Args:
        arene (dict): l'arene considérée
        lig (int): le numéro de la ligne de l'arène
        col (int): le numéro de la colonne de l'arène

    Returns:
        int: valeur du propriétaire de la boite qui se trouve sur la case lig,col de l'arene
    """
    return case.get_proprietaire(matrice.get_val(arene["matrice"],lig,col))

def get_serpent(arene:dict,num_joueur:int)->list:
    """Retourne le serpent (la liste des positions de ce serpent) du joueur passé en paramètre

    Args:
        arene (dict): l'arène considérée
        num_joueur (int): le numéro du joueur dont on veut le serpent

    Returns:
        list: la liste des positions occupées par le serpent du joueur
    """    
    return serpent.get_liste_pos(arene["serpents"][num_joueur-1])

def get_derniere_direction(arene:dict,num_joueur:int)->str:
    """Retourne l'orientation relative des deux dernières boites du serpent du joueur passé en paramètre

    Args:
        arene (dict): l'arène considérée
        num_joueur (int): le numéro du joueur dont on veut le serpent

    Returns:
        str: une des lettres N O S E indiquant orientation relative des deux dernières boites
    """   
    return serpent.get_derniere_direction(arene["serpents"][num_joueur-1])
                            
def classement(arene:dict)->list:
    """
        retourne la liste classée suivant le nombre de points accumulés par chaque joueur

    Args:
        arene (dict): l'arene considérée

    Returns:
        list: la liste classées des serpents des joueurs présents sur l'arène
    """    
    return sorted(arene["serpents"],key=lambda s:-serpent.get_points(s))

def ajouter_joueur(arene:dict,nom_joueur:str)->int:
    """ajoute un nouveau joueur sur l'arène

    Args:
        arene (dict): l'arène considérée
        nom_joueur (str): le nom du joueur à ajouter

    Returns:
        int: l'identifiant du joueur qui vient d'être ajouté
    """    
    nb_j=arene["nb_joueurs"]+1
    arene["serpents"].append(serpent.Serpent(nom_joueur,nb_j))
    lig,col=choisir_case_vide(arene)
    init_joueur(arene,nb_j,lig,col)
    arene["nb_joueurs"]=nb_j
    return nb_j

def init_joueur(arene:dict,num_joueur:int,lig:int,col:int)->bool:
    """initialise un joueur en position lig,col.
        Si la case n'est pas libre ou est un mur la fonction retourne False et ne fait rien

    Args:
        arene (dict): l'arène considérée
        num_joueur (int): le numéro du joueur à initialiser_
        lig (int): numéro de la ligne où poser le joueur_
        col (int): numéro de la colonne où poser le joueur

    Returns:
        bool: True si la case était libre, False sinon
    """
    mat=arene["matrice"]
    la_case=matrice.get_val(mat,lig,col)
    if case.est_mur(la_case) or case.contient_boite(la_case):
        return False
    case.set_boite(la_case,1,num_joueur,TEMPS_FUSION)
    serpent.set_liste_pos(arene["serpents"][num_joueur-1],[(lig,col)])
    return True

def choisir_case_vide(arene:dict)->tuple[int,int]:
    """Choisi aléatoirement une case vide de l'arène

    Args:
        arene (dict): l'arène considérée

    Returns:
        tuple[int,int]: la paire (lig,col) donnant les coordonnées de la case choisie
    """
    fini=False
    mat=arene["matrice"]
    nb_lig=matrice.get_nb_lignes(mat)
    nb_col=matrice.get_nb_colonnes(mat)
    while not fini:
        lig=random.randint(0,nb_lig-1)
        col=random.randint(0,nb_col-1)
        la_case=matrice.get_val(mat,lig,col)
        fini=not case.est_mur(la_case) and not case.contient_boite(la_case)
    return lig,col

def placer_les_joueurs(arene:dict)->None:
    """place les joueurs de manière aléatoire sur l'arène

    Args:
        arene (dict): l'arène considérée
    """
    for i in range(arene["nb_joueurs"]):
        lig,col=choisir_case_vide(arene)
        init_joueur(arene,i+1,lig,col)

def ajouter_boite(arene:dict,valeur:int,lig:int,col:int)-> bool:
    """ajouter une boite en lig,col de l'arène. la valeur de 
        la boite est donnée en paramètres

    Args:
        arene (dict): l'arène considérée
        valeur (int): valeur de la boite
        lig (int): numéro de la ligne où poser la boite
        col (int): numéro de la colonne où poser la boite

    Returns:
        bool: False si la case est un mur ou si elle contenait déjà une boite
    """
    mat=arene["matrice"]
    la_case=matrice.get_val(mat,lig,col)
    if case.est_mur(la_case) or case.contient_boite(la_case):
        return False
    case.set_boite(la_case,valeur,0,TEMPS_BOITE)
    return True

def ajouter_des_boites_ou_bonus(arene:dict,val_min:int=1, val_max:int=2,nb_boites:int=4):
    """Ajoute des boites ou des bonus dans des cases vides

    Args:
        arene (dict): arène où poser des boites
        val_min (int, optional): valeur minimale des boites posées. Defaults to -5.
        val_max (int, optional): valeur maximale des boites posées. Defaults to 4.
        nb_boites (int, optional): nombre de boites à poser. Defaults to 4.
    """    
    for i in range(nb_boites):
        val_boite=random.randint(val_min,val_max)
        lig,col=choisir_case_vide(arene)
        ajouter_boite(arene,val_boite,lig,col)

def mise_a_jour_temps(arene:dict)->None:
    """Met à jour le temps de toutes les boites de l'arène

    Args:
        arene (dict): l'arène considérée
    """
    mat=arene["matrice"]
    for lig in range(matrice.get_nb_lignes(mat)):
        for col in range(matrice.get_nb_colonnes(mat)):
            case.mise_jour_temps_restant(matrice.get_val(mat,lig,col))
    for serp in arene["serpents"]:
        serpent.maj_temps(serp)


def decaler_queue(arene:dict,serpent:list,i_debut:int)->None:
    """Decale la queue du serpent à partir de l'indice i_debut

    Args:
        arene (dict): l'arène dans laquelle se trouve le serpent
        serpent (list): le serpent à décaler
        i_debut (int): l'indice de début de décalage
    """
    mat=arene["matrice"]
    for i in range(i_debut,len(serpent)-1):
        la_case=matrice.get_val(mat,serpent[i+1][0],serpent[i+1][1])
        matrice.set_val(mat,serpent[i][0],serpent[i][1],la_case)
    lig,col=serpent.pop()
    matrice.set_val(mat,lig,col,case.Case(False))

def mult_div_serpent(arene:dict,serpent:list, num_joueur:int, operation:str):
    """multiplie ou divise toutes les boites d'un serpent par 2
        Les boites qui étaient à 1 disparaissent

    Args:
        arene (dict): L'arène où se trouve le serpent
        serpent (list): le serpent à modifier
        num_joueur (int): le numéro du joueur à qui appartient le serpent
        operation (str): '/' pour diviser sinon cela multiplie
    """    
    if operation=="/":
        op=operator.floordiv
    else:
        op=operator.mul
    mat=arene["matrice"]

    for ind in range(len(serpent)-1,-1,-1):
        (lig,col)=serpent[ind]
        la_case=matrice.get_val(mat,lig,col)
        val=case.get_val_boite(la_case)
        val=op(val,2)
        if val==0:
            case.enlever_boite(la_case)
            serpent.pop()
        else:
            case.set_val_temps_restant_boite(la_case,val,TEMPS_FUSION)
    if len(serpent)==0:
        lig,col=choisir_case_vide(arene)
        init_joueur(arene,num_joueur,lig,col)


def enlever_queue(arene:dict,serpent:list, num_joueur:int):
    """enlève la boite de queue du serpent. si le serpent n'avait qu'une boite, le serpent
        est ré-initialisé et réapparait sur une case aléatoire de l'arène

    Args:
        arene (dict): l'arène considérée
        serpent (list): le serpent à modifier
        num_joueur (int): le numéro du joueur à qui appartient le serpent
    """    
    mat=arene["matrice"]
    (lig,col)=serpent[-1]
    la_case=matrice.get_val(mat,lig,col)
    case.enlever_boite(la_case)
    serpent.pop()
    if len(serpent)==0:
        lig,col=choisir_case_vide(arene)
        init_joueur(arene,num_joueur,lig,col)

def ajouter_boite_serpent(arene:dict,serpent:list,num_joueur:int,lig:int,col:int):
    """ ajoute une boite de la même valeur que la queue du serpent en lig,col

    Args:
        arene (dict): l'arène considérée
        serpent (list): le serpent à modifier
        lig (int): ligne où va se mettre la nouvelle tête
        col (int): colonne où va se mette la nouvelle tête
    """    
    mat=arene["matrice"]
    (lig_fin,col_fin)=serpent[-1]
    la_case=matrice.get_val(mat,lig_fin,col_fin)
    val=case.get_val_boite(la_case)
    serpent.insert(0,(lig,col))
    matrice.set_val(mat,lig,col,case.Case(False,val,num_joueur,TEMPS_FUSION))
    descendre_tete(arene,serpent)



def descendre_tete(arene:dict,serpent:list)->int:
    """descend la boite de tête du serpent afin que celui-ci reste trié

    Args:
        arene (dict): l'arène de jeu
        serpent (list): le serpent considéré

    Returns:
        int: l'indice de la place finale de la boite
    """
    mat=arene["matrice"]
    i=1
    fini=False
    lig_prec,col_prec=serpent[0]
    boite_prec=matrice.get_val(mat,lig_prec,col_prec)
    val_prec=case.get_val_boite(boite_prec)
    while i<len(serpent) and not fini:
        lig,col=serpent[i]
        boite=matrice.get_val(mat,lig,col)
        val=case.get_val_boite(boite)
        if val<=val_prec:
            fini=True
        else:
            matrice.set_val(mat,lig_prec,col_prec,boite)
            matrice.set_val(mat,lig,col,boite_prec)
            lig_prec,col_prec,val_prec=lig,col,val
            i+=1
    return i


def remonter_boite(arene:dict,serpent:list,i_debut:int)->int:
    """remonte la boite dans le serpent afin que celui-ci reste trié

    Args:
        arene (dict): l'arène de jeu
        serpent (list): le serpent considéré
        i_debut (int): la place actuelle de la boite

    Returns:
        int: l'indice de la place finale de la boite
    """
    mat=arene["matrice"]
    i=i_debut-1
    fini=False
    lig_prec,col_prec=serpent[i_debut]
    boite_prec=matrice.get_val(mat,lig_prec,col_prec)
    val_prec,temps_prec=case.get_val_temps(boite_prec)
    while i>=0 and not fini:
        lig,col=serpent[i]
        boite=matrice.get_val(mat,lig,col)
        val,temps=case.get_val_temps(boite)
        if val>val_prec :
            fini=True
        else:
            matrice.set_val(mat,lig_prec,col_prec,boite)
            matrice.set_val(mat,lig,col,boite_prec)
            lig_prec,col_prec=lig,col
            i-=1
    return i


def fusionner_boites(arene:dict,proprietaire:int)->int:
    """Cherche à fusionner les deux boites consécutives de même valeur d'un serpent les plus proches de la tête.

    Args:
        arene (dict): l'arène considérée
        proprietaire (int): le numéro du joueur du serpent à traiter

    Returns:
        int: valeur des boites fusionnées
    """
    mat=arene["matrice"]
    serp=serpent.get_liste_pos(arene["serpents"][proprietaire-1])
    val_prec,tr_prec=case.get_val_temps(matrice.get_val(mat,serp[0][0],serp[0][1]))
    val_tete=val_prec
    for i in range(1,len(serp)):
        val,tr=case.get_val_temps(matrice.get_val(mat,serp[i][0],serp[i][1]))
        if tr==0 and tr_prec==0 and val==val_prec:
            case.set_val_temps_restant_boite(matrice.get_val(mat,serp[i-1][0],serp[i-1][1]),2*val,TEMPS_FUSION)
            decaler_queue(arene,serp,i)
            remonter_boite(arene,serp,i-1)
            return val_tete+val*2
        val_prec=val
        tr_prec=tr
    return val_tete

def supprimer_queue(arene:dict,num_joueur:int, lig:int,col:int)->int:
    """supprime la queue du serpent d'un joueur

    Args:
        arene (dict): l'arène considérée
        num_joueur (int): le numéro du joueur à qui appartient le serpent
        lig (int): ligne de la première boite à supprimer
        col (int): colonne de la première boite à supprimer

    Returns:
        int: somme des valeurs des boites supprimées
    """    
    serp=serpent.get_liste_pos(arene["serpents"][num_joueur-1])
    i=0
    mat=arene["matrice"]

    while i<len(serp) and serp[i]!=(lig,col):
        i+=1
    somme=0
    while len(serp)>i:
        lig2,col2=serp.pop()
        somme+=case.get_val_boite(matrice.get_val(mat,lig2,col2))
        matrice.set_val(mat,lig2,col2,case.Case(False))
    if len(serp)==0:
        lig,col=choisir_case_vide(arene)
        init_joueur(arene,num_joueur,lig,col)
    return somme

def deplacer_serpent(arene:dict,num_joueur:int,lig_arr:int,col_arr:int,valeur:int, direction:str)->None:
    """Déplace le serpent du joueurs num_joueur et met à jour l'arène en conséquence

    Args:
        arene (dict): l'arène considérée
        num_joueur (int): le numéro du joueur dont on déplace le serpent
        lig_arr (int): ligne d'arrivée de la tête
        col_arr (int): ligne d'arrivée de la tête
        valeur (int): valeur de la boîte à ajouter au serpent (0 si rien à ajouter)
    """
    mat=arene["matrice"]
    serpent.set_derniere_direction(arene["serpents"][num_joueur-1],direction)
    serp:list=serpent.get_liste_pos(arene["serpents"][num_joueur-1])
    serp.insert(0,(lig_arr,col_arr))
    i=1
    lig_prec,col_prec=lig_arr,col_arr
    while i<len(serp):
        lig,col=serp[i]
        la_case=matrice.get_val(mat,lig,col)
        val=case.get_val_boite(la_case)
        if val<=valeur:
            matrice.set_val(mat,lig_prec,col_prec,case.Case(False,valeur,num_joueur,TEMPS_FUSION))
            return
        matrice.set_val(mat,lig_prec,col_prec,la_case)
        lig_prec,col_prec=lig,col
        i+=1
    if valeur>0:
        matrice.set_val(mat,lig_prec,col_prec,case.Case(False,valeur,num_joueur,TEMPS_FUSION))
    else:
        matrice.set_val(mat,lig_prec,col_prec,case.Case(False))
        serp.pop()

def directions_possibles(arene:dict,num_joueur:int)->str:
    res=''
    mat=arene["matrice"]
    nb_lig=matrice.get_nb_lignes(mat)
    nb_col=matrice.get_nb_colonnes(mat)
    lig_dep,col_dep=serpent.get_liste_pos(arene["serpents"][num_joueur-1])[0]
    for dir in 'NOSE':
        delta_lig,delta_col=DIRECTIONS[dir]
        lig_arr=lig_dep+delta_lig
        col_arr=col_dep+delta_col
        if lig_arr<0 or lig_arr>=nb_lig or col_arr<0 or col_arr>=nb_col:
            continue
        if case.est_mur(matrice.get_val(mat,lig_arr,col_arr)):
            continue
        if case.get_proprietaire(matrice.get_val(mat,lig_arr,col_arr))==num_joueur:
            continue
        res+=dir
    return res

def arrivee_dans_un_mur(arene:dict,joueur:dict,num_joueur:int,lig_arr:int,col_arr:int,direction:str)->str:
    serpent.ajouter_points(joueur,MALUS)
    if serpent.get_temps_mange_mur(joueur)>0:
        deplacer_serpent(arene,num_joueur,lig_arr,col_arr,0,direction)
        return "Le joueur "+str(num_joueur)+" a mangé un mur"
    mult_div_serpent(arene,serpent.get_liste_pos(joueur),num_joueur,"/")
    return "Le joueur "+str(num_joueur)+" s'est cogné dans un mur"

def arrivee_dans_une_boite_sup(arene:dict,joueur:dict,num_joueur:int,lig_arr:int,col_arr:int,case_arr:dict,direction:str)->str:
    serpent.ajouter_points(joueur,MALUS)
    if serpent.get_temps_surpuissance(joueur)<=0:
        mult_div_serpent(arene,serpent.get_liste_pos(joueur),num_joueur,"/")
        return "Le joueur "+str(num_joueur)+" s'est cogné dans une boite trop grosse pour lui"
    valeur,prop,tps=case.enlever_boite(case_arr)
    res="Le joueur "+str(num_joueur)+" a mangé une boite de "+str(valeur)+" grâce à sa surpuissance"
    if prop>0:
        if serpent.get_temps_protection(arene["serpents"][prop-1])>=0:
            mult_div_serpent(arene,serpent.get_liste_pos(joueur),num_joueur,"/")
            case.set_boite(case_arr,valeur,prop,tps)
            return "Le joueur "+str(num_joueur)+" a mordu un autre joueur qui bénéficie d'une protection"
        nb_points=supprimer_queue(arene,prop,lig_arr,col_arr)+valeur
        serpent.ajouter_points(arene["serpents"][prop-1],-nb_points)
        serpent.ajouter_points(joueur,nb_points)
        res="Le joueur "+str(num_joueur)+" a mordu un autre joueur grace à sa surpuissance ce qui lui a rapporté "+nb_points+" points"
    deplacer_serpent(arene,num_joueur,lig_arr,col_arr,valeur,direction)
    return res

def deplacer_joueur(arene:dict,num_joueur:int,direction:str)->str:
    """déplace le joueur dans la direction indiquée. Si le déplacement n'est
    pas possible le joueur reste sur place
    La fonction retourne un message indiquant ce qu'il s'est passé

    Args:
        arene (dict): l'arène considérée
        num_joueur (int): le joueur à déplacer
        direction (str): la diction du déplacement

    Returns:
        str: un message indiquant ce qu'il s'est passé
    """
    mat=arene["matrice"]
    
    joueur=arene["serpents"][num_joueur-1]
    lig_dep,col_dep=serpent.get_liste_pos(joueur)[0]
    if direction not in DIRECTIONS:
        mult_div_serpent(arene,serpent.get_liste_pos(joueur),num_joueur,"/")
        serpent.ajouter_points(joueur,MALUS)
        return "Le joueur "+str(num_joueur)+" a joué une direction incorrecte"
    
    nb_lig,nb_col=get_dim(arene)
    delta_lig,delta_col=DIRECTIONS[direction]
    lig_arr=lig_dep+delta_lig
    col_arr=col_dep+delta_col
    if lig_arr<0 or lig_arr>=nb_lig or col_arr<0 or col_arr>=nb_col:
        mult_div_serpent(arene,serpent.get_liste_pos(joueur),num_joueur,"/")
        serpent.ajouter_points(joueur,MALUS)
        return "Le joueur "+str(num_joueur)+" est sorti de l'arène"
    
    case_arr=matrice.get_val(mat,lig_arr,col_arr)
    case_dep=matrice.get_val(mat,lig_dep,col_dep)
    if case.est_mur(case_arr):
        return arrivee_dans_un_mur(arene,joueur,num_joueur,lig_arr,col_arr,direction)
        
    if case.contient_boite(case_arr) and case.get_val_boite(case_arr)>case.get_val_boite(case_dep):
        return arrivee_dans_une_boite_sup(arene,joueur,num_joueur,lig_arr,col_arr,case_arr,direction)
    
    # le joueur arrive sur une case a priori possible
    valeur,prop,tps=case.enlever_boite(case_arr)
    serpent.ajouter_points(joueur,valeur)    
    if prop>0:
        if serpent.get_temps_protection(arene["serpents"][prop-1])>0:
            # finalement le joueur visé est protégé => perte de points
            serpent.ajouter_points(joueur,-valeur) 
            mult_div_serpent(arene,serpent.get_liste_pos(joueur),num_joueur,"/")
            case.set_boite(case_arr,valeur,prop,tps)
            return "Le joueur "+str(num_joueur)+" a mordu le joueur "+str(prop)+ " qui bénéficie d'une protection "
        nb_points=supprimer_queue(arene,prop,lig_arr,col_arr)
        serpent.ajouter_points(arene["serpents"][prop-1],-nb_points-valeur)
        serpent.ajouter_points(joueur,nb_points)
        deplacer_serpent(arene,num_joueur,lig_arr,col_arr,valeur,direction)
        res="Le joueur "+str(num_joueur)+" a mordu le joueur "+str(prop)+ " echange de "+str(nb_points+valeur)+" points"
    elif valeur==PROTECTION:
        deplacer_serpent(arene,num_joueur,lig_arr,col_arr,0,direction)
        serpent.ajouter_temps_protection(joueur,TEMPS_BONUS)
        res="Le joueur "+str(num_joueur)+" a gagné le bonus de protection"
    elif valeur==MULTIPLIE:
        ligq,colq=serpent.get_queue(joueur)
        val_queue=2*case.get_val_boite(matrice.get_val(mat,ligq,colq))
        deplacer_serpent(arene,num_joueur,lig_arr,col_arr,val_queue,direction)
        enlever_queue(arene,serpent.get_liste_pos(joueur),num_joueur)
        res="Le joueur "+str(num_joueur)+" a gagné le bonus de multiplication qui multiplie sa queue par deux "+str(val_queue)
    elif valeur==AJOUTE:
        ligq,colq=serpent.get_queue(joueur)
        val_queue=case.get_val_boite(matrice.get_val(mat,ligq,colq))
        deplacer_serpent(arene,num_joueur,lig_arr,col_arr,val_queue,direction)
        res="Le joueur "+str(num_joueur)+" a gagné le bonus d'addition qui lui ajoute une boite de "+str(val_queue)
    elif valeur==SURPUISSANCE:
        deplacer_serpent(arene,num_joueur,lig_arr,col_arr,0,direction)
        serpent.ajouter_temps_surpuissance(joueur,TEMPS_BONUS)
        res="Le joueur "+str(num_joueur)+" a gagné le bonus de surpuissance"
    elif valeur==MANGE_MUR:
        deplacer_serpent(arene,num_joueur,lig_arr,col_arr,0,direction)
        serpent.ajouter_temps_mange_mur(joueur,TEMPS_BONUS)
        res="Le joueur "+str(num_joueur)+" a gagné le bonus qui permet de manger des murs"
    else:
        deplacer_serpent(arene,num_joueur,lig_arr,col_arr,valeur,direction)
        if valeur>0:
            res= "Le joueur "+str(num_joueur)+" a mangé une boite de valeur "+str(valeur)
        else:
            res= "Le joueur "+str(num_joueur)+" s'est déplacé sur une case vide"
    return res

def afficher_arene(arene:dict):
    """Affiche en mode texte une arène

    Args:
        arene (dict): l'arène à afficher
    """
    mat=arene["matrice"]
    ansiColor.clearscreen()
    for lig in range(matrice.get_nb_lignes(mat)):
        for col in range(matrice.get_nb_colonnes(mat)):
            la_case=matrice.get_val(mat,lig,col)
            if case.est_mur(la_case):
                print('X',sep='',end='')
            elif not case.contient_boite(la_case):
                print(' ',sep='',end='')
            else:
                valeur=case.get_val_boite(la_case)
                if valeur>10:
                    fond=ansiColor.CYAN
                    valeur=valeur%10
                elif valeur<0:
                    fond=ansiColor.VERT
                    valeur=-valeur
                else:
                    fond=ansiColor.GRIS
                ansiColor.pcouleur(valeur,case.get_proprietaire(la_case),fond,ansiColor.GRAS)
        print()
    for num_j in range(arene["nb_joueurs"]):
        ansiColor.pcouleur(serpent.to_str(arene["serpents"][num_j])+'\n',num_j+1)

def afficher_serpent(arene:dict,num_joueur:int):
    """affiche un serpent en mode texte

    Args:
        arene (dict): arène considérée
        num_joueur (int): numéro du joueur dont on veut affiche le serpent
    """    
    mat=arene["matrice"]
    for lin,col in serpent.get_liste_pos(arene["serpents"][num_joueur-1]):
        la_case=matrice.get_val(mat,lin,col)
        print("[",case.get_val_boite(la_case),",",case.get_temps_restant(la_case),"]",sep="",end="<-")

def fusionner_boites_ex(arene:dict):
    """permet de fusionner les boites des serpents présents sur l'arène et d'ajouter les points correspondants

    Args:
        arene (dict): l'arène considérée
    """    
    for j in range(1,arene["nb_joueurs"]+1):
        serpent.ajouter_points(arene["serpents"][j-1],fusionner_boites(arene,j))
        
def jouer_un_tour(arene):
    """effectue un tour de jeu où tous les joueurs jouent de manière aléatoire (pour tester)

    Args:
        arene (dict): l'arène considérée
    """    
    for j in range(1,arene["nb_joueurs"]+1):
            dir_pos=directions_possibles(arene,j)
            if dir_pos=='':
                dir=random.choice('NOSE')
            else:
                dir=random.choice(dir_pos)
            deplacer_joueur(arene,j,dir)
    for j in range(1,arene["nb_joueurs"]+1):
        serpent.ajouter_points(arene["serpents"][j-1],fusionner_boites(arene,j))
    mise_a_jour_temps(arene)
    ajouter_des_boites_ou_bonus(arene,1,2,4)
    ajouter_des_boites_ou_bonus(arene,-5,-1,2)

def arene_2_str(arene:dict,sep=";")->str:
    """Sérialise une arène sous la forme d'une chaine de caractères

    Args:
        arene (dict): l'arene considérée
        sep (str, optional): le caractère séparateur des informations de l'arène. Defaults to ";".

    Returns:
        str: l'arène sérialisée
    """    
    mat=arene["matrice"]
    res=str(matrice.get_nb_lignes(mat))+sep+str(matrice.get_nb_colonnes(mat))+'\n'
    for lig in range(matrice.get_nb_lignes(mat)):
        prec=''
        for col in range(matrice.get_nb_colonnes(mat)):
            la_case=matrice.get_val(mat,lig,col)
            if case.est_mur(la_case):
                res+=prec+'X'+sep+'0'+sep+'0'
            elif not case.contient_boite(la_case):
                res+=prec+' '+sep+'0'+sep+'0'
            else:
                valeur=case.get_val_boite(la_case)
                res+=prec+str(valeur)+sep+str(case.get_proprietaire(la_case))+sep+str(case.get_temps_restant(la_case))
            prec=sep
        res+='\n'
    for num_j in range(arene["nb_joueurs"]):
        res+=serpent.serpent_2_str(arene["serpents"][num_j],sep)
    return res

def arene_from_str(chaine:str,sep=';')->dict:
    """reforme une arène à partir d'une chaine de caractères

    Args:
        chaine (str): la chaine de caractères contenant les informations de l'arène
        sep (str, optional): le caractère séparateur des informations de l'arène. Defaults to ';'.

    Returns:
        dict: l'arène reconstituée
    """    
    contenu=chaine.split('\n')
    nb_lig,nb_col=contenu[0].split(sep)
    nb_lig=int(nb_lig)
    nb_col=int(nb_col)
    mat= matrice.Matrice(nb_lig,nb_col)
    for ind in range(1,nb_lig+1):
        ligne=contenu[ind].split(";")
        for col in range(nb_col):
            val=ligne[3*col]
            if val=='X':
                matrice.set_val(mat,ind-1,col,case.Case(True))
            elif val==' ':
                matrice.set_val(mat,ind-1,col,case.Case(False))
            else:
                val=int(val)
                prop=int(ligne[3*col+1])
                ts=int(ligne[3*col+2])
                matrice.set_val(mat,ind-1,col,case.Case(False,val,prop,ts))
    les_serpents=[]
    for ind in range(nb_lig+1,len(contenu)-1):
        if ind%2==0:
            serp=serpent.serpent_from_str("\n".join(contenu[ind:ind+2]),sep)
            les_serpents.append(serp)
    return {"matrice":mat,"nb_joueurs":len(les_serpents),"serpents":les_serpents}

def sauver_score(arene:dict,nom_fic:str):
    """sauvegarde le score des joueurs dans un fichier texte

    Args:
        arene (dict): l'arène considérée
        nom_fic (str): le nom du fichier où sauvegarder le score
    """    
    with open(nom_fic, "w") as fic:
        for serp in arene["serpents"]:
            fic.write(serpent.get_nom(serp).replace("~", ".").replace(";", ",") + ";" + \
                            str(serpent.get_points(serp)) + "\n")

def copy_arene(arene:dict)->dict:
    """recopie une arene. Attention à ce que la matrice et les listes
    soient bien des recopies.
    Compléxité : O(N)**n    

    Args:
        arene (dict): l'arene considérée

    Returns:
        dict: la copie de l'arène passée en paramètre
    """
    return copie_dico(arene)  

def get_serpent_complet(arene:dict, num_joueur:int) -> dict:
    """Obtenir le serpent complet d'un joueur.
    Complexité : O(N)
    
    Args:
        arene (dict): L'arène considérée
        num_joueur (int): Le numéro du joueur

    Returns:
        dict: Le serpent du joueur
    """

    for serpent_data in arene["serpents"]:
        if serpent.get_num_joueur(serpent_data) == num_joueur:
            return serpent_data
    return None

def get_case(arene:dict, ligne: int, colonne: int):
    return matrice.get_val(arene["matrice"],ligne,colonne)