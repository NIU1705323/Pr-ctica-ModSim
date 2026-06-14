import numpy as np
import matplotlib.pyplot as plt
from config import *
from utils.utils import satisfet, segregacio_local
from utils.moviment_agent import moure_agent

def simular(tau: float, llavor: int) -> tuple:
    """
    Executa una simulació completa amb un llindar de tolerància tau.
    Retorna (segregacio_final, iteracions_convergencia).
    """
    rng = np.random.default_rng(llavor)

    # Tipus i probabilitats
    tipus_disponibles = list(range(TIPUS_DE_VEINS)) + [-1]
    probabilitats = PROBABILITATS_VEINS + [1 - sum(PROBABILITATS_VEINS)]

    # Graella inicial
    arr = rng.choice(tipus_disponibles, size=DIMENSIONS, p=probabilitats)

    # Simulació
    for iteracio in range(MAX_ITER):
        posicions = np.argwhere(arr != -1)
        rng.shuffle(posicions)

        canvis = 0
        for posicio in posicions:
            if satisfet(posicio, arr) < tau:
                if moure_agent(posicio, arr):
                    canvis += 1

        if canvis == 0:          # convergència
            break

    segregacio = segregacio_local(arr)
    return segregacio, iteracio if canvis == 0 else MAX_ITER

if __name__ == "__main__":
    TAUX = []
    segregacio_mitjana = []
    convergencia_mitjana = []
    N_SIMULACIONS = 1          # nombre d'execucions per cada TAU

    for TAU in np.arange(0.01, 1.0, 0.02):
        print(f"Simulant TAU = {TAU} ...")
        segs = []
        iters = []

        for s in range(N_SIMULACIONS):
            seg, it = simular(TAU, llavor=s*100 + int(TAU*10))
            segs.append(seg)
            iters.append(it)

        TAUX.append(TAU)
        segregacio_mitjana.append(np.mean(segs))
        convergencia_mitjana.append(np.mean(iters))

    # Gràfics
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(TAUX, segregacio_mitjana, 'o-')
    ax1.set_xlabel('TAU (llindar de tolerància)')
    ax1.set_ylabel('Segregació mitjana')
    ax1.set_title('Segregació vs TAU')
    ax1.grid(True)

    ax2.plot(TAUX, convergencia_mitjana, 's-')
    ax2.set_xlabel('TAU')
    ax2.set_ylabel('Iteracions fins a convergència')
    ax2.set_title('Convergència vs TAU')
    ax2.grid(True)

    plt.tight_layout()
    plt.show()