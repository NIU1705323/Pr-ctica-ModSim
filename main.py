import numpy as np
import matplotlib.pyplot as plt
from utils import *
from config import *
from random import seed

if __name__ == "__main__":
    
    seed(SEED) # Assignem una inicialització concreta si està definida
    
    # Tipus possibles:
    # 0 -> agent blau
    # 1 -> agent vermell
    # -1 -> casella buida
    t=list(range(TIPUS_DE_VEINS))+[-1]

    p=PROBABILITATS_VEINS+[1-sum(PROBABILITATS_VEINS)] # Probabilitats de cada tipus

    # Generació aleatòria de la graella
    arr = np.reshape(
        np.random.choice(t, N**DIM_ESPAI, p=p),
        [N] * DIM_ESPAI
    )

    # ESTAT INICIAL
    print("ESTAT INICIAL:\n")
    print(arr)

    plt.figure(figsize=(6,6))
    plt.imshow(arr, cmap="hsv", vmin=-1, vmax=TIPUS_DE_VEINS)
    plt.title("Estat inicial")
    plt.colorbar()
    plt.show(block=False)

    
    # SIMULACIÓ
    for iteracio in range(MAX_ITER):
        canvis = 0
        posicions = np.argwhere(arr != -1) # Totes les posicions ocupades
        np.random.shuffle(posicions) # Ordre aleatori

        for posicio in posicions:
            if not satisfet(posicio, arr):
                moure_agent(posicio, arr)
                canvis += 1

        # Mostrar evolució
        plt.clf()
        plt.imshow(np.where(arr == -1, np.nan, arr), cmap="hsv", vmin=-1, vmax=TIPUS_DE_VEINS)
        plt.title(f"Iteració {iteracio + 1}")
        plt.colorbar()
        plt.pause(0.3) # augmentar si va massa ràpid!!

        # Mostrem dades com poden ser el numero de moviments
        print(f"Iteració {iteracio + 1}: {canvis} moviments")

        # Equilibri
        if canvis == 0:
            print("\nEquilibri assolit")
            break

    
    # ESTAT FINAL
    print("\nESTAT FINAL:\n")
    print(arr)

    plt.figure(figsize=(6,6))
    plt.imshow(np.where(arr == -1, np.nan, arr), cmap="hsv", vmin=-1, vmax=TIPUS_DE_VEINS)
    plt.title("Estat final")
    plt.colorbar()
    plt.show()