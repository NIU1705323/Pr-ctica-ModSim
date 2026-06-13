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
    
    
def wrap_posicio(posicio: np.ndarray, mapa: np.ndarray) -> np.ndarray:
    """Aplica wrap-around (condicions periòdiques) a les coordenades"""
    return np.array([posicio[i] % mapa.shape[i] for i in range(len(posicio))])
    
    
def veins_propers(posicio: np.ndarray, mapa: np.ndarray) -> np.ndarray:
    """Funció que retorna l'importància ponderada de cada color de veí"""
    
    resultat=[0]*TIPUS_DE_VEINS
    for i, pos in enumerate(INDEXOS_VEINS):
        vei = np.array(posicio) + np.array(pos)
        if TORUS: vei = wrap_posicio(vei, mapa)
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


def crear_dibuix(mapa: np.ndarray) -> dict:
    """Funció que crea el mapa del veinat per a poder veure-ho"""
    
    fig, ax = plt.subplots(figsize=(6,6))
    mapa_visual = np.tile(mapa, (REPETICIONS, REPETICIONS))
    im = ax.imshow(np.where(mapa_visual == -1, np.nan, mapa_visual), cmap=COLOR, vmin=-1, vmax=TIPUS_DE_VEINS)
    fig.colorbar(im)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    return {"fig": fig, "ax": ax, "im": im}


def dibuixar(dibuix: dict, iter:int, mapa: np.ndarray) -> None:
    """Funció que ens mostra el mapa del veinat en el seu estat actual (un plot)"""
    
    mapa_visual = np.tile(mapa, (REPETICIONS, REPETICIONS))
    dibuix["im"].set_data(np.where(mapa_visual == -1, np.nan, mapa_visual))
    dibuix["ax"].set_title(f"Iteració {iter}")
    dibuix["fig"].canvas.draw()
    plt.pause(TEMPS_ESPERA) # augmentar si va massa ràpid!!
    
    
def plot_segregacio(valors) -> None:
    """Funció que fa el plot dels valors obtinguts segons la mètrica de segregació"""
    
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(valors)), valors, marker='o', linestyle='-', markersize=4)
    plt.xlabel('Iteració')
    plt.ylabel('Segregació')
    plt.title('Evolució de la segregació al llarg del temps')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    
from collections import deque
def trobar_blocs(mapa, tipus):
    """
    Retorna llista de blocs (components connexos) d'un tipus.
    Connexió 4-neighbours (es pot ampliar a 8 si vols).
    """

    visitat = np.zeros_like(mapa, dtype=bool)
    blocs = []

    n, m = mapa.shape

    for i in range(n):
        for j in range(m):

            if visitat[i, j]:
                continue

            if mapa[i, j] != tipus:
                continue

            # BFS per component
            cua = deque([(i, j)])
            visitat[i, j] = True
            bloc = []

            while cua:
                x, y = cua.popleft()
                bloc.append((x, y))

                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nx, ny = x + dx, y + dy

                    if 0 <= nx < n and 0 <= ny < m:
                        if not visitat[nx, ny] and mapa[nx, ny] == tipus:
                            visitat[nx, ny] = True
                            cua.append((nx, ny))

            blocs.append(bloc)

    return blocs


def segregacio_local(mapa): # Densitat clusters
    """
    Mesura com de compactes són els grups.
    0 = dispers
    1 = un sol bloc compacte
    """

    tipus_unics = [t for t in np.unique(mapa) if t != -1]

    densitats = []

    for t in tipus_unics:
        blocs = trobar_blocs(mapa, t)

        if len(blocs) == 0:
            continue

        mides = np.array([len(b) for b in blocs])

        # bloc dominant vs dispersió
        max_bloc = np.max(mides)
        total = np.sum(mides)

        # proporció del bloc més gran
        densitat = max_bloc / total

        densitats.append(densitat)

    if len(densitats) == 0:
        return 0.0

    return float(np.mean(densitats))


def segregacio_local_1(mapa): # Entropia blocs
    """
    0 = un sol bloc per tipus (molt segregat)
    alta = molts blocs petits (dispers)
    """

    from math import log

    tipus_unics = [t for t in np.unique(mapa) if t != -1]

    entropies = []

    for t in tipus_unics:
        blocs = trobar_blocs(mapa, t)

        if len(blocs) <= 1:
            continue

        mides = np.array([len(b) for b in blocs])
        probs = mides / mides.sum()

        ent = -np.sum(probs * np.log(probs + 1e-12))
        entropies.append(ent)

    if len(entropies) == 0:
        return 0.0

    return float(np.mean(entropies))