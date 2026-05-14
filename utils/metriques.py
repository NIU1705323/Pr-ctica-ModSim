############################ MÈTRIQUES ############################
##                                                               ##
##          Document amb funcions per generar caselles           ##
##                                                               ##
###################################################################

import numpy as np
from config import *

######## generació de veins ########

def generar_veins() -> np.ndarray:
    """Funció que genera les posicions on els veins influeixen segons la mètrica"""
    
    match METRICA: 
        case 0: return generar_veins_l_inf()
        case _: return generar_veins_ln()
    return np.array([]) # Per evitar errors


def generar_veins_l_inf() -> np.ndarray:
    """Funció que genera el plà de mida 2R * 2R dels veins"""
    
    R = int(DISTANCIA_MAXIMA_VEINS)
    valorsPossibles = np.arange(-R, R + 1)
    producte_cartesia = np.meshgrid(*([valorsPossibles] * len(DIMENSIONS)), indexing='ij')
    res=np.stack(producte_cartesia, axis=-1).reshape(-1, len(DIMENSIONS))
    return res[np.any(res != 0, axis=1)]


def generar_veins_ln() -> np.ndarray:
    """Funció que filtra les posicions on els veins influeixen segons la mètrica"""
    
    punts = generar_veins_l_inf() 
    return punts[np.sum(np.abs(punts)**METRICA, axis=1)**(1/METRICA) <= DISTANCIA_MAXIMA_VEINS]


INDEXOS_VEINS=generar_veins()


######## funcions de distància ########

def f_l(punt : np.ndarray) -> float:
    """Funció que retorna la norma segons la mètrica"""
    match METRICA: 
        case 0: return f_l_inf(punt)
        case _: return f_ln(punt)
    return -1.0 # Per evitar errors


def f_ln(punt : np.ndarray) -> float:
    """La norma d'ordre METRICA"""
    return np.power(np.sum(np.abs(punt)**METRICA), 1/METRICA)


def f_l_inf(punt : np.ndarray) -> float:
    """La norma d'ordre infinit"""
    return np.max(np.abs(punt))


######## generació de ponderacions ########

def generar_ponderació() -> np.ndarray:
    """Funció que genera els pesos dels veins segons la configuració"""
    
    match TIPUS_PONDERACIONS:
        case 0: return generar_ponderació_identitat()
        case _: return generar_ponderació_inversa()
    return np.array([]) # Per evitar errors


def generar_ponderació_inversa() -> np.ndarray:
    """Funció que genera els pesos dels veins inversament a la distància"""
    return np.array([1/f_l(i) for i in INDEXOS_VEINS])


def generar_ponderació_identitat() -> np.ndarray:
    """Funció que genera els pesos dels veins on tots pesen igual"""
    return np.array([1]*INDEXOS_VEINS.shape[0])


PONDERACIONS = generar_ponderació()