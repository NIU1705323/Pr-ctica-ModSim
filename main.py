import numpy as np
import matplotlib.pyplot as plt
from utils import *
from config import *
from random import seed

if __name__ == "__main__":
    
    seed(SEED) # Assignem una inicialització concreta si està definida
    t=list(range(TIPUS_DE_VEINS))+[-1] # Valors de les diferents caselles

    p=PROBABILITATS_VEINS+[1-sum(PROBABILITATS_VEINS)] # Probabilitats de cada tipus

    # Generació aleatòria de la graella
    arr = np.reshape(np.random.choice(t, np.prod(DIMENSIONS), p=p), DIMENSIONS)

    # ESTAT INICIAL
    print("ESTAT INICIAL:\n")
    print(arr)

    fig, ax = plt.subplots(figsize=(6,6))
    im = ax.imshow(np.where(arr == -1, np.nan, arr), cmap="hsv", vmin=-1, vmax=TIPUS_DE_VEINS)
    fig.colorbar(im)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    plt.show(block=False)
    
    # SIMULACIÓ
    canvis = -1 # Aquest valor està per a evitar errors
    for iteracio in range(MAX_ITER):
        canvis = 0
        posicions = np.argwhere(arr != -1) # Totes les posicions ocupades
        np.random.shuffle(posicions) # Ordre aleatori

        # Movem els veins que es volen moure
        for posicio in posicions:
            if satisfet(posicio, arr) < TAU:
                if moure_agent(posicio, arr) == True: canvis += 1

        # Mostrar evolució
        im.set_data(np.where(arr == -1, np.nan, arr))
        ax.set_title(f"Iteració {iteracio + 1}")
        plt.pause(0.01) # augmentar si va massa ràpid!!

        # Mostrem dades com poden ser el numero de moviments
        print(f"Iteració {iteracio + 1}: {canvis} moviments")

        # Equilibri
        if canvis == 0:
            print("\nEquilibri assolit")
            ax.set_title(f"Equilibri assolit en l'iteració {iteracio + 1}")
            break

    
    # ESTAT FINAL
    print("\nESTAT FINAL:\n")
    print(arr)

    if canvis != 0: ax.set_title(f"Equilibri NO assolit en l'iteració {MAX_ITER}")
    plt.show()