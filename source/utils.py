def copie_dico(dico: dict) -> dict:
    """Faire la copie en profondeur d'un dictionnaire.
    Compléxité : O(N)**n avec n le nombre de profondeur du dictionnaire

    Args:
        dico (dict): Un dictionnaire

    Returns:
        dict: Un dictionnaire copié en profondeur
    """

    dict_copie = dict(dico)
    for (cle, valeur) in dict_copie.items():
        type_valeur = type(valeur)
        if type_valeur == dict:
            dict_copie[cle] = copie_dico(valeur)
        else:
            # On ne peut pas redéfinir None avec son type
            if valeur == None:
                dict_copie[cle] = None
            else:
                dict_copie[cle] = type_valeur(valeur)
    return dict_copie