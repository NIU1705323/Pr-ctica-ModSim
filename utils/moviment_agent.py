import numpy as np
from config import *
from utils.utils import *

def moure_agent(posicio: np.ndarray, mapa: np.ndarray) -> bool:
    """Funció que desplaça a l'individu de la posició argument a una millor"""
    match MOVIMENT:
        case 0: return moure_agent_adjacent(posicio, mapa)
        case 1: return moure_agent_random(posicio, mapa)
        case 2: return moure_agent_global(posicio, mapa)
        case 3: return moure_agent_primera_millor(posicio, mapa)
    return False # Per evitar errors


def moure_agent_adjacent(posicio: np.ndarray, mapa: np.ndarray) -> bool:
    """Funció que desplaça a l'individu a una posició 'adjacent' millor"""
    
    # Definim les variables que necessitem
    tipus = mapa[tuple(posicio)]
    if tipus == -1: return False # Per a evitar errors
    nova_pos = None
    bst_prop = satisfet(posicio, mapa, clase=tipus)
    if bst_prop >= SATISFET: return False # Per a evitar errors
    indexos_veins = INDEXOS_VEINS.copy()
    np.random.shuffle(indexos_veins) # les revisem en ordre aleatori
    
    # Busquem caselles buides adjacents
    for pos in indexos_veins:
        vei = np.array(posicio) + np.array(pos)
        if index_valid(vei, mapa) and mapa[tuple(vei)] == -1:
            mapa_temp = mapa.copy()
            mapa_temp[tuple(vei)] = tipus
            mapa_temp[tuple(posicio)] = -1
            prop = satisfet(vei, mapa_temp, clase=tipus) # Revisem si estaria satisfet
            if prop >= SATISFET: # En cas afirmatiu, ens movem a aquella posició
                nova_pos = vei
                break
            if prop > bst_prop: # En cas negatiu, guardem la millor
                bst_prop = prop
                nova_pos = vei

    # Si no trobem cap casella on estaria satisfet, anem a una qualsevol
    if nova_pos is None: return False
    mapa[tuple(nova_pos)] = tipus
    mapa[tuple(posicio)] = -1
    return True


def moure_agent_random(posicio: np.ndarray, mapa: np.ndarray) -> bool:
    """Funció que desplaça a l'individu a una posició alèatoria"""
    
    buides = np.argwhere(mapa == -1) # busquem caselles buides O(n^^4) :(

    if len(buides) == 0: return False

    nova_pos = buides[np.random.randint(len(buides))] # nova posició aleatoria (el agent utilitza la porta mágica)
    mapa[tuple(nova_pos)] = mapa[tuple(posicio)]
    mapa[tuple(posicio)] = -1
    return True


def moure_agent_global(posicio: np.ndarray, mapa: np.ndarray) -> bool:
    """Funció que desplaça a l'individu a la millor posició del mapa"""
    
    # Definim les variables que necessitem
    buides = np.argwhere(mapa == -1) # busquem caselles buides
    if len(buides) == 0: return False
    np.random.shuffle(buides) # les revisem en ordre aleatori
    
    tipus = mapa[tuple(posicio)]
    if tipus == -1: return False # Per a evitar errors
    nova_pos = None
    bst_prop = satisfet(posicio, mapa, clase=tipus)
    if bst_prop >= SATISFET: return False # Per a evitar errors
    
    # Busquem caselles buides adjacents
    for vei in buides:
        mapa_temp = mapa.copy()
        mapa_temp[tuple(vei)] = tipus
        mapa_temp[tuple(posicio)] = -1
        prop = satisfet(vei, mapa_temp, clase=tipus) # Revisem si estaria satisfet
        if prop >= SATISFET: # En cas afirmatiu, ens movem a aquella posició
            nova_pos = vei
            break
        if prop > bst_prop: # En cas negatiu, guardem la millor
            bst_prop = prop
            nova_pos = vei

    # Si no trobem cap casella on estaria satisfet, anem a una qualsevol
    if nova_pos is None: return False
    mapa[tuple(nova_pos)] = tipus
    mapa[tuple(posicio)] = -1
    return True


def moure_agent_primera_millor(posicio: np.ndarray, mapa: np.ndarray) -> bool:
    """Funció que desplaça a l'individu a qualsevol millor posició del mapa"""
    
    # Definim les variables que necessitem
    buides = np.argwhere(mapa == -1) # busquem caselles buides
    if len(buides) == 0: return False
    np.random.shuffle(buides) # les revisem en ordre aleatori
    
    tipus = mapa[tuple(posicio)]
    if tipus == -1: return False # Per a evitar errors
    nova_pos = None
    bst_prop = satisfet(posicio, mapa, clase=tipus)
    if bst_prop >= SATISFET: return False # Per a evitar errors
    
    # Busquem caselles buides adjacents
    for vei in buides:
        mapa_temp = mapa.copy()
        mapa_temp[tuple(vei)] = tipus
        mapa_temp[tuple(posicio)] = -1
        prop = satisfet(vei, mapa_temp, clase=tipus) # Revisem si estaria satisfet
        if prop >= bst_prop: # En cas afirmatiu, ens movem a aquella posició
            nova_pos = vei
            break

    # Si no trobem cap casella on estaria satisfet, anem a una qualsevol
    if nova_pos is None: return False
    mapa[tuple(nova_pos)] = tipus
    mapa[tuple(posicio)] = -1
    return True