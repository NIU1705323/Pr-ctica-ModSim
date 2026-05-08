########## ÚTILS ##########
#
# Document amb les funcions programades
#

import numpy as np
from config import *

def index_valid(arr: np.ndarray, idx: int):
    """
    Funció que retorna les posicións vàlides 
    
    **Paràmetres**: 
        posició : llista amb la posició de l'element en la matriu
        array : mapa del veïnat
        indexos_Caselles_Veines : posicions adjacents a considerar
        ponderacio_caselles_veines : ponderació d'importància segons la distància
        
    **Retorna**:
        array : vector d
    """
    idx = np.asarray(idx)

    return (
        idx.ndim == 1 and
        len(idx) == arr.ndim and
        np.all(idx >= 0) and
        np.all(idx < arr.shape)
    )
    
def veins_propers(posicio: list[int], 
                   array: np.ndarray, 
                   indexos_caselles_veines : list[list[int]], 
                   ponderacio_caselles_veines : list[int]) -> np.ndarray:
    """
    Funció que retorna l'importància ponderada de cada color de veí
    
    **Paràmetres**: 
        posició : llista amb la posició de l'element en la matriu
        array : mapa del veïnat
        indexos_Caselles_Veines : posicions adjacents a considerar
        ponderació_caselles_veines : ponderació d'importància segons la distància
        
    **Retorna**:
        array : vector de mida TIPUS_DE_VEINS amb nombre de cada veí ponderat a distància
    """
    resultat=[0]*TIPUS_DE_VEINS
    for i, pos in enumerate(indexos_caselles_veines):
        vei = np.array(posicio) + np.array(pos)
        if index_valid(array, vei):
            valor = array[tuple(vei)]
            if valor != -1:
                resultat[valor] += ponderacio_caselles_veines[i]

    return resultat


def satisfet(posicio, arr, tau): # Com esta el Roger quan fa EDP's
    tipus = arr[tuple(posicio)] # tipus d'agent

    if tipus == -1:
        return True

    veins = veins_propers(posicio, arr, INDEXOS_VEINS, PONDERACIONS)
    total = sum(veins)
    if total == 0:
        return True

    proporcio = veins[tipus] / total
    return proporcio >= tau


def moure_agent(posicio, arr):
    buides = np.argwhere(arr == -1) # busquem caselles buides

    if len(buides) == 0:
        return

    nova_pos = buides[np.random.randint(len(buides))] # nova posició aleatoria (el agent utilitza la porta mágica)
    arr[tuple(nova_pos)] = arr[tuple(posicio)]
    arr[tuple(posicio)] = -1