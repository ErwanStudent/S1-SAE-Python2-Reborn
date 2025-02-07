import serpent
import arene

Serpent1 = serpent.Serpent("Toto", 1)
Serpent2 = serpent.Serpent("Pierre", 2, 5, [(0, 5)], 2, 0, 9, "S")
Serpent3 = serpent.Serpent("Jean", 3, 2, None, 10, 0, 0, "O")

def tests_Serpent():
    assert serpent.Serpent("Toto", 1) == {'nom_joueur': 'Toto', 'num_joueur': 1, 'points': 0, 'positions': None, 'tps_s': 0, 'tps_p': 0, 'tps_m': 0, 'direction': 'N'}
    assert serpent.Serpent("Pierre", 2, 5, None, 2, 0, 9, "S") == {'nom_joueur': 'Pierre', 'num_joueur': 2, 'points': 5, 'positions': None, 'tps_s': 2, 'tps_p': 0, 'tps_m': 9, 'direction': 'S'}
    assert serpent.Serpent("Jean", 3, 2, None, 10, 0, 0, "N") == {'nom_joueur': 'Jean', 'num_joueur': 3, 'points': 2, 'positions': None, 'tps_s': 10, 'tps_p': 0, 'tps_m': 0, 'direction': 'N'}

def tests_get_nom():
    assert serpent.get_nom(Serpent1) == "Toto"
    assert serpent.get_nom(Serpent2) == "Pierre"
    assert serpent.get_nom(Serpent3) == "Jean"

def tests_get_num_joueur():
    assert serpent.get_num_joueur(Serpent1) == 1
    assert serpent.get_num_joueur(Serpent2) == 2
    assert serpent.get_num_joueur(Serpent3) == 3

def tests_get_points():
    assert serpent.get_points(Serpent1) == 0
    assert serpent.get_points(Serpent2) == 5
    assert serpent.get_points(Serpent3) == 2

def tests_get_liste_pos():
    assert serpent.get_liste_pos(Serpent1) == [] 
    assert serpent.get_liste_pos(Serpent2) == [(0, 5)]
    assert serpent.get_liste_pos(Serpent3) == []
    
def tests_get_queue():
    assert serpent.get_queue(Serpent1) == None
    assert serpent.get_queue(Serpent2) == (0, 5)
    assert serpent.get_queue(Serpent3) == None

def tests_get_derniere_direction():
    assert serpent.get_derniere_direction(Serpent1) == "N"
    assert serpent.get_derniere_direction(Serpent2) == "S"
    assert serpent.get_derniere_direction(Serpent3) == "O"

def tests_get_bonus():
    assert serpent.get_bonus(Serpent1) == []
    assert serpent.get_bonus(Serpent2) == [arene.SURPUISSANCE, arene.MANGE_MUR]
    assert serpent.get_bonus(Serpent3) == [arene.SURPUISSANCE]
    
def tests_ajouter_points():
    serpent.ajouter_points(Serpent1, 1)
    assert serpent.get_points(Serpent1) == 1

    serpent.ajouter_points(Serpent2, -2) 
    assert serpent.get_points(Serpent2) == 3

    serpent.ajouter_points(Serpent3, 5)
    assert serpent.get_points(Serpent3) == 7

def tests_set_liste_pos():
    serpent.set_liste_pos(Serpent1, [(3, 2)]) == [(3, 2)]
    assert serpent.get_liste_pos(Serpent1) == [(3, 2)]

    serpent.set_liste_pos(Serpent2, [])
    assert serpent.get_liste_pos(Serpent2) == [] 
    
    serpent.set_liste_pos(Serpent3, [(3, 2), (4, 2)])
    assert serpent.get_liste_pos(Serpent3) == [(3, 2), (4, 2)]

def tests_set_derniere_direction():
    serpent.set_derniere_direction(Serpent1, "N")
    assert serpent.get_derniere_direction(Serpent1) == "N"
    
    serpent.set_derniere_direction(Serpent2, "S")
    assert serpent.get_derniere_direction(Serpent2) == "S"

    serpent.set_derniere_direction(Serpent3, "O")
    assert serpent.get_derniere_direction(Serpent3) == "O"

def tests_to_str():
    Serpent1 = serpent.Serpent("Toto", 1)
    Serpent2 = serpent.Serpent("Pierre", 2, 5, [(0, 5)], 2, 0, 9, "S")
    Serpent3 = serpent.Serpent("Jean", 3, 2, None, 10, 0, 0, "O")

    assert serpent.to_str(Serpent1) == "Toto -> 0 s:0 m:0 p:0"
    assert serpent.to_str(Serpent2) == "Pierre -> 5 s:2 m:9 p:0"
    assert serpent.to_str(Serpent3) == "Jean -> 2 s:10 m:0 p:0"

def tests_get_temps_protection():
    Serpent1 = serpent.Serpent("Toto", 1)
    Serpent2 = serpent.Serpent("Pierre", 2, 5, [(0, 5)], 2, 0, 9, "S")
    Serpent3 = serpent.Serpent("Jean", 3, 2, None, 10, 2, 0, "O")

    assert serpent.get_temps_protection(Serpent1) == 0
    assert serpent.get_temps_protection(Serpent2) == 0
    assert serpent.get_temps_protection(Serpent3) == 2
    
def tests_get_temps_mange_mur():
    Serpent1 = serpent.Serpent("Toto", 1)
    Serpent2 = serpent.Serpent("Pierre", 2, 5, [(0, 5)], 2, 0, 9, "S")
    Serpent3 = serpent.Serpent("Jean", 3, 2, None, 10, 2, 0, "O")

    assert serpent.get_temps_mange_mur(Serpent1) == 0
    assert serpent.get_temps_mange_mur(Serpent2) == 9
    assert serpent.get_temps_mange_mur(Serpent3) == 0

def tests_get_temps_surpuissance():
    Serpent1 = serpent.Serpent("Toto", 1)
    Serpent2 = serpent.Serpent("Pierre", 2, 5, [(0, 5)], 2, 0, 9, "S")
    Serpent3 = serpent.Serpent("Jean", 3, 2, None, 10, 2, 0, "O")

    assert serpent.get_temps_surpuissance(Serpent1) == 0
    assert serpent.get_temps_surpuissance(Serpent2) == 2
    assert serpent.get_temps_surpuissance(Serpent3) == 10

def tests_ajouter_temps_protection():
    serpent.ajouter_temps_protection(Serpent1, 5)
    assert serpent.get_temps_protection(Serpent1) == 5 
    
    serpent.ajouter_temps_protection(Serpent2, 1)
    assert serpent.get_temps_protection(Serpent2) == 1

    serpent.ajouter_temps_protection(Serpent3, 8)
    assert serpent.get_temps_protection(Serpent3) == 8

def tests_ajouter_temps_mange_mur():
    Serpent1 = serpent.Serpent("Toto", 1)
    Serpent2 = serpent.Serpent("Pierre", 2, 5, [(0, 5)], 2, 0, 9, "S")
    Serpent3 = serpent.Serpent("Jean", 3, 2, None, 10, 2, 0, "O")

    serpent.ajouter_temps_mange_mur(Serpent1, 0)
    assert serpent.get_temps_mange_mur(Serpent1) == 0

    serpent.ajouter_temps_mange_mur(Serpent2, 9)
    assert serpent.get_temps_mange_mur(Serpent2) == 18

    serpent.ajouter_temps_mange_mur(Serpent3, 0)
    assert serpent.get_temps_mange_mur(Serpent3) == 0

def tests_ajouter_temps_surpuissance():
    serpent.ajouter_temps_surpuissance(Serpent1, 5)
    assert serpent.get_temps_surpuissance(Serpent1) == 5
    
    serpent.ajouter_temps_surpuissance(Serpent2, 2)
    assert serpent.get_temps_surpuissance(Serpent2) == 4

    serpent.ajouter_temps_surpuissance(Serpent3, -10)
    assert serpent.get_temps_surpuissance(Serpent3) == 0

def tests_maj_temps():
    Serpent1 = serpent.Serpent("Toto", 1)
    Serpent2 = serpent.Serpent("Pierre", 2, 5, [(0, 5)], 2, 0, 9, "S")
    Serpent3 = serpent.Serpent("Jean", 3, 2, None, 10, 2, 0, "O")

    serpent.maj_temps(Serpent1)
    assert serpent.get_temps_surpuissance(Serpent1) == 0
    assert serpent.get_temps_protection(Serpent1) == 0
    assert serpent.get_temps_mange_mur(Serpent1) == 0

    serpent.maj_temps(Serpent2)
    assert serpent.get_temps_surpuissance(Serpent2) == 1
    assert serpent.get_temps_protection(Serpent2) == 0
    assert serpent.get_temps_mange_mur(Serpent2) == 8 

    serpent.maj_temps(Serpent3)
    assert serpent.get_temps_surpuissance(Serpent3) == 9
    assert serpent.get_temps_protection(Serpent3) == 1
    assert serpent.get_temps_mange_mur(Serpent3) == 0

def tests_serpent_2_str():
    Serpent1 = serpent.Serpent("Toto", 1)
    Serpent2 = serpent.Serpent("Pierre", 2, 5, [(0, 5)], 2, 0, 9, "S")
    Serpent3 = serpent.Serpent("Jean", 3, 2, [(1, 2), (2, 3)], 10, 2, 0, "O")

    assert serpent.serpent_2_str(Serpent1) == "Toto;1;0;0;0;0;N\n\n"
    assert serpent.serpent_2_str(Serpent2) == "Pierre;2;5;2;9;0;S\n0;5\n"
    assert serpent.serpent_2_str(Serpent3) == "Jean;3;2;10;0;2;O\n1;2;2;3\n"

def tests_serpent_from_str():
    Serpent1 = serpent.Serpent("Toto", 1)
    Serpent2 = serpent.Serpent("Pierre", 2, 5, [(0, 5)], 2, 0, 9, "S")
    Serpent3 = serpent.Serpent("Jean", 3, 2, [(1, 2), (2, 3)], 10, 2, 0, "O")

    assert serpent.serpent_from_str("Toto;1;0;0;0;0;N\n") == Serpent1
    assert serpent.serpent_from_str("Pierre;2;5;2;9;0;S\n0;5") == Serpent2
    assert serpent.serpent_from_str("Jean;3;2;10;0;2;O\n1;2;2;3") == Serpent3

def tests_copy_serpent():
    copie1 = serpent.copy_serpent(Serpent1)
    serpent.ajouter_points(Serpent1, 1)
    assert copie1 != Serpent1

    copie2 = serpent.copy_serpent(Serpent2)
    serpent.ajouter_temps_mange_mur(Serpent2, 5)
    assert copie2 != Serpent2

    copie3 = serpent.copy_serpent(Serpent3)
    serpent.set_liste_pos(Serpent3, [(1, 4)])
    assert copie3 != Serpent3