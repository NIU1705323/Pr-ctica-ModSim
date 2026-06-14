import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor, as_completed
from config import *
from utils.utils import satisfet, segregacio_local
from utils.moviment_agent import moure_agent

def simular(tau: float, llavor: int) -> tuple:
    """
    Executa una simulació completa amb un llindar de tolerància tau.
    Retorna (segregacio_final, iteracions_convergencia).
    """
    # Fixem la llavor global per a totes les operacions aleatòries d'aquest procés
    np.random.seed(llavor)

    # Tipus i probabilitats
    tipus_disponibles = list(range(TIPUS_DE_VEINS)) + [-1]
    probabilitats = PROBABILITATS_VEINS + [1 - sum(PROBABILITATS_VEINS)]

    # Graella inicial (com al main1 optimitzat)
    arr = np.random.choice(tipus_disponibles, size=DIMENSIONS, p=probabilitats)

    # Llista de caselles buides (es manté actualitzada durant la simulació)
    buides = np.argwhere(arr == -1)

    # Simulació
    for iteracio in range(MAX_ITER):
        posicions = np.argwhere(arr != -1)
        np.random.shuffle(posicions)

        canvis = 0
        for posicio in posicions:
            satisfaccio = satisfet(posicio, arr)
            if satisfaccio < tau:
                if moure_agent(posicio, arr, buides, satisfaccio):
                    canvis += 1

        if canvis == 0:          # convergència
            break

    segregacio = segregacio_local(arr)
    return segregacio, iteracio if canvis == 0 else MAX_ITER


if __name__ == "__main__":
    N_SIMULACIONS = 10          # nombre d'execucions per cada TAU

    TAUX = []
    segregacio_mitjana = []
    convergencia_mitjana = []

    # Creem totes les tasques (TAU, llavor)
    tasques = []
    for TAU in np.arange(0.01, 1.0, 0.02):
        for s in range(N_SIMULACIONS):
            llavor = s * 100 + int(TAU * 10)
            tasques.append((TAU, llavor))

    total_tasques = len(tasques)
    print(f"Iniciant {total_tasques} simulacions en paral·lel...")

    # Execució paral·lela amb registre de progrés
    resultats_per_tau = {}
    completed = 0
    with ProcessPoolExecutor() as executor:
        futurs = {executor.submit(simular, tau, llavor): (tau, llavor)
                  for tau, llavor in tasques}

        for futur in as_completed(futurs):
            tau, llavor = futurs[futur]
            try:
                seg, it = futur.result()
                if tau not in resultats_per_tau:
                    resultats_per_tau[tau] = {"segs": [], "iters": []}
                resultats_per_tau[tau]["segs"].append(seg)
                resultats_per_tau[tau]["iters"].append(it)
            except Exception as e:
                print(f"Error amb TAU={tau}, llavor={llavor}: {e}")
            finally:
                completed += 1
                if completed % max(1, total_tasques // 10) == 0 or completed == total_tasques:
                    print(f"  Progrés: {completed}/{total_tasques} simulacions finalitzades", flush=True)

    # Calculem mitjanes i generem les llistes ordenades per TAU
    print("\nResultats finals per TAU:")
    for tau in sorted(resultats_per_tau.keys()):
        dades = resultats_per_tau[tau]
        seg_avg = np.mean(dades["segs"])
        it_avg = np.mean(dades["iters"])
        TAUX.append(tau)
        segregacio_mitjana.append(seg_avg)
        convergencia_mitjana.append(it_avg)
        print(f"  TAU = {tau:.2f} -> segregació mitjana: {seg_avg:.4f}, iteracions: {it_avg:.1f}")

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