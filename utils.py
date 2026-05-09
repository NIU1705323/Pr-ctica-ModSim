############################## ÚTILS ##############################
##                                                               ##
## Document amb les funcions programades                         ##
##                                                               ##
## Les funcions tenen com a arguments els seguents paràmetres:   ##
##   mapa: mapa del veinat, l'espai on conviuen els veins        ##
##   posicio: el/s index del veí sobre el que actua la funció    ##
##                                                               ##
###################################################################

import numpy as np
from config import *

def index_valid(posicio: np.ndarray, mapa: np.ndarray):
    """Funció que retorna les posicións vàlides"""
    
    return (
        posicio.ndim == 1 and
        len(posicio) == mapa.ndim and
        np.all(posicio >= 0) and
        np.all(posicio < mapa.shape)
    )
    
    
def veins_propers(posicio: np.ndarray, mapa: np.ndarray) -> np.ndarray:
    """Funció que retorna l'importància ponderada de cada color de veí"""
    
    resultat=[0]*TIPUS_DE_VEINS
    for i, pos in enumerate(INDEXOS_VEINS):
        vei = np.array(posicio) + np.array(pos)
        if index_valid(vei, mapa):
            valor = mapa[tuple(vei)]
            if valor != -1:
                resultat[valor] += PONDERACIONS[i]
    
    return np.asarray(resultat)


def satisfet(posicio: np.ndarray, mapa: np.ndarray, clase: np.ndarray = np.array(None)) -> float: # Com esta el Roger quan fa EDP's
    """Funció que ens diu si un inividu està còmode en la seva posició actual"""

    # Si és una casella buida, està satisfeta
    if clase == None: tipus = mapa[tuple(posicio)] 
    else: tipus = clase
    if tipus == -1: return 1.0 

    # Si no té veins, també ho està
    veins = veins_propers(posicio, mapa)
    total = sum(veins)
    if total == 0: return 1.0

    # En cas contrari, depén del llindar
    proporcio = float(veins[tipus] / total)
    return proporcio


def moure_agent(posicio: np.ndarray, mapa: np.ndarray) -> bool:
    """Funció que desplaça a l'individu de la posició argument a una millor"""
    
    # Definim les variables que necessitem
    tipus = mapa[tuple(posicio)]
    if tipus == -1: return False # Per a evitar errors
    nova_pos = None
    bst_prop = satisfet(posicio, mapa, clase=tipus)
    if bst_prop == 1.0: return False # Per a evitar errors
    
    # Busquem caselles buides adjacents
    for pos in INDEXOS_VEINS:
        vei = np.array(posicio) + np.array(pos)
        if index_valid(vei, mapa) and mapa[tuple(vei)] == -1:
            prop = satisfet(vei, mapa, clase=tipus) # Revisem si estaria satisfet
            if prop == 1.0: # En cas afirmatiu, ens movem a aquella posició
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