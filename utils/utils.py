############################## ÚTILS ##############################
##                                                               ##
##                  Document amb funcions vàries                 ##
##                                                               ##
##  Les funcions tenen com a arguments els seguents paràmetres:  ##
##   mapa: mapa del veinat, l'espai on conviuen els veins        ##
##   posicio: el/s index del veí sobre el que actua la funció    ##
##                                                               ##
###################################################################

import numpy as np
import matplotlib.pyplot as plt
from config import *
from utils.metriques import *

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
    if tipus == -1: return SATISFET

    # Si no té veins, també ho està
    veins = veins_propers(posicio, mapa)
    total = sum(veins)
    if total == 0: return SATISFET

    # En cas contrari, depén del llindar
    proporcio = float(veins[tipus] / total)
    return proporcio


def crear_dibuix(mapa: np.ndarray):
    """Funció que crea el mapa del veinat per a poder veure-ho"""
    
    fig, ax = plt.subplots(figsize=(6,6))
    im = ax.imshow(np.where(mapa == -1, np.nan, mapa), cmap=COLOR, vmin=-1, vmax=TIPUS_DE_VEINS)
    fig.colorbar(im)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    return {"fig": fig, "ax": ax, "im": im}


def dibuixar(dibuix: dict, iter:int, mapa: np.ndarray) -> None:
    """Funció que ens mostra el mapa del veinat en el seu estat actual (un plot)"""
    
    dibuix["im"].set_data(np.where(mapa == -1, np.nan, mapa))
    dibuix["ax"].set_title(f"Iteració {iter}")
    dibuix["fig"].canvas.draw()
    plt.pause(TEMPS_ESPERA) # augmentar si va massa ràpid!!