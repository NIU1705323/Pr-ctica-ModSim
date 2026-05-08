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
        ponderació_caselles_veines : ponderació d'importància segons la distància
        
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
                   ponderació_caselles_veines : list[int]) -> np.ndarray:
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
    for pos in indexos_caselles_veines:
        vei=posicio+pos
        if index_valid(array, vei):
            if array[vei] != -1:
                resultat[array[vei]]+=ponderació_caselles_veines[vei]

    return resultat