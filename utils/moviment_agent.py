############################## ÚTILS ##############################
##                                                               ##
##             Document amb funcions per moure veins             ##
##                                                               ##
##  Les funcions tenen com a arguments els seguents paràmetres:  ##
##   mapa: mapa del veinat, l'espai on conviuen els veins        ##
##   posicio: el/s index del veí sobre el que actua la funció    ##
##                                                               ##
###################################################################

import numpy as np
from config import *
from utils.utils import *

def moure_agent(posicio: np.ndarray, mapa: np.ndarray, 
                buides: np.ndarray, satisfaccio: float) -> bool:
    """Funció que desplaça a l'individu de la posició argument a una millor"""
    match MOVIMENT:
        case 0: return moure_agent_adjacent(posicio, mapa, buides, satisfaccio)
        case 1: return moure_agent_random(posicio, mapa, buides, satisfaccio)
        case 2: return moure_agent_global(posicio, mapa, buides, satisfaccio)
        case 3: return moure_agent_primera_millor(posicio, mapa, buides, satisfaccio)
    return False # Per evitar errors


def moure_agent_adjacent(posicio: np.ndarray, mapa: np.ndarray, 
                         buides: np.ndarray, satisfaccio: float) -> bool:
    """Funció que desplaça a l'individu a una posició 'adjacent' millor"""
    
    # Definim les variables que necessitem
    tipus = mapa[tuple(posicio)]
    if tipus == -1: return False # Per a evitar errors
    nova_pos = None
    bst_prop = satisfaccio
    if bst_prop >= SATISFET: return False # Per a evitar errors
    indexos_veins = INDEXOS_VEINS.copy()
    np.random.shuffle(indexos_veins) # les revisem en ordre aleatori
    
    # Busquem caselles buides adjacents
    for pos in indexos_veins:
        vei = np.array(posicio) + np.array(pos)
        if index_valid(vei, mapa) and mapa[tuple(vei)] == -1:
            mapa[tuple(vei)] = tipus
            mapa[tuple(posicio)] = -1
            prop = satisfet(vei, mapa, clase=tipus) # Revisem si estaria satisfet
            mapa[tuple(posicio)] = tipus
            mapa[tuple(vei)] = -1
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


def moure_agent_random(posicio: np.ndarray, mapa: np.ndarray, 
                       buides: np.ndarray, satisfaccio: float) -> bool:
    """Funció que desplaça a l'individu a una posició alèatoria"""

    if len(buides) == 0: return False
    idx_nova_pos = np.random.randint(len(buides))
    nova_pos = buides[idx_nova_pos] # nova posició aleatoria (el agent utilitza la porta mágica)
    mapa[tuple(nova_pos)] = mapa[tuple(posicio)]
    mapa[tuple(posicio)] = -1
    buides[idx_nova_pos] = posicio.copy()
    return True

def moure_agent_global(posicio: np.ndarray, mapa: np.ndarray, 
                       buides: np.ndarray, satisfaccio: float) -> bool:
    """Funció que desplaça a l'individu a la millor posició del mapa"""
    
    # Definim les variables que necessitem
    if len(buides) == 0: return False
    
    # Crear índexs per a poder rastrejar les posicions i fer shuffle
    indexs = np.arange(len(buides))
    np.random.shuffle(indexs) # les revisem en ordre aleatori
    
    tipus = mapa[tuple(posicio)]
    if tipus == -1: return False # Per a evitar errors
    nova_pos = None
    idx_nova_pos = None
    bst_prop = satisfaccio
    if bst_prop >= SATISFET: return False # Per a evitar errors
    
    # Busquem caselles buides
    for idx in indexs:
        vei = buides[idx]
        mapa[tuple(vei)] = tipus
        mapa[tuple(posicio)] = -1
        prop = satisfet(vei, mapa, clase=tipus) # Revisem si estaria satisfet
        mapa[tuple(posicio)] = tipus
        mapa[tuple(vei)] = -1
        if prop >= SATISFET: # En cas afirmatiu, ens movem a aquella posició
            nova_pos = vei
            idx_nova_pos = idx
            break
        if prop > bst_prop: # En cas negatiu, guardem la millor
            bst_prop = prop
            nova_pos = vei
            idx_nova_pos = idx

    # Si no trobem cap casella on estaria satisfet, anem a una qualsevol
    if nova_pos is None: return False
    mapa[tuple(nova_pos)] = tipus
    mapa[tuple(posicio)] = -1
    buides[idx_nova_pos] = posicio.copy()
    return True


def moure_agent_primera_millor(posicio: np.ndarray, mapa: np.ndarray, 
                               buides: np.ndarray, satisfaccio: float) -> bool:
    """Funció que desplaça a l'individu a qualsevol millor posició del mapa"""
    
    # Definim les variables que necessitem
    if len(buides) == 0: return False
    
    # Crear índexs per a poder rastrejar les posicions i fer shuffle
    indexs = np.arange(len(buides))
    np.random.shuffle(indexs) # les revisem en ordre aleatori
    
    tipus = mapa[tuple(posicio)]
    if tipus == -1: return False # Per a evitar errors
    nova_pos = None
    idx_nova_pos = None
    bst_prop = satisfaccio
    if bst_prop >= SATISFET: return False # Per a evitar errors
    
    # Busquem caselles buides
    for idx in indexs:
        vei = buides[idx]
        mapa[tuple(vei)] = tipus
        mapa[tuple(posicio)] = -1
        prop = satisfet(vei, mapa, clase=tipus) # Revisem si estaria satisfet
        mapa[tuple(posicio)] = tipus
        mapa[tuple(vei)] = -1
        if prop >= bst_prop: # En cas afirmatiu, ens movem a aquella posició
            nova_pos = vei
            idx_nova_pos = idx
            break

    # Si no trobem cap casella on estaria satisfet, anem a una qualsevol
    if nova_pos is None: return False
    mapa[tuple(nova_pos)] = tipus
    mapa[tuple(posicio)] = -1
    buides[idx_nova_pos] = posicio.copy()
    return True