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


def satisfet(posicio: np.ndarray, mapa: np.ndarray) -> bool: # Com esta el Roger quan fa EDP's
    """Funció que ens diu si un inividu està còmode en la seva posició actual"""

    # Si és una casella buida, està satisfeta
    tipus = mapa[tuple(posicio)]
    if tipus == -1: return True 

    # Si no té veins, també ho està
    veins = veins_propers(posicio, mapa)
    total = sum(veins)
    if total == 0: return True

    # En cas contrari, depén del llindar
    proporcio = veins[tipus] / total
    return bool(proporcio >= TAU)


def moure_agent(posicio: np.ndarray, mapa: np.ndarray) -> None:
    """Funció que desplaça a l'individu de la posició argument a una millor"""
    # Busquem caselles buides adjacents
    buides = []
    for pos in INDEXOS_VEINS:
        vei = np.array(posicio) + np.array(pos)
        if index_valid(vei, mapa) and mapa[tuple(vei)] == -1:
            buides.append(vei)

    # Si no es pot moure, no cal fer canvis al mapa
    if len(buides) == 0: return

    # En cas contrari, intercanviem la seva posició a una casella buida
    nova_pos = buides[np.random.randint(len(buides))] # nova posició aleatoria (el agent utilitza la porta mágica)
    mapa[tuple(nova_pos)] = mapa[tuple(posicio)]
    mapa[tuple(posicio)] = -1