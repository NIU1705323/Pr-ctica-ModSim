# run_experiments.py
import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor, as_completed
import config
from utils.utils import satisfet, segregacio_local
from utils.moviment_agent import moure_agent
import os
from datetime import datetime

# ------------------------------------------------------------
# Funció de simulació (la mateixa que a main2, però aquí importa config)
# ------------------------------------------------------------
def simular(tau: float, llavor: int) -> tuple:
    """
    Executa una simulació completa amb un llindar de tolerància tau.
    Retorna (segregacio_final, iteracions_convergencia).
    """
    # Fixar la llavor global per a totes les operacions aleatòries d'aquest procés
    np.random.seed(llavor)

    # Tipus i probabilitats (ara venen de config)
    tipus_disponibles = list(range(config.TIPUS_DE_VEINS)) + [-1]
    probabilitats = config.PROBABILITATS_VEINS + [1 - sum(config.PROBABILITATS_VEINS)]

    # Graella inicial
    arr = np.random.choice(tipus_disponibles, size=config.DIMENSIONS, p=probabilitats)

    # Llista de caselles buides
    buides = np.argwhere(arr == -1)

    # Simulació
    for iteracio in range(config.MAX_ITER):
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
    return segregacio, iteracio if canvis == 0 else config.MAX_ITER


# ------------------------------------------------------------
# Funció que executa l'escombrat de TAU amb la configuració actual
# ------------------------------------------------------------
def run_tau_sweep(n_simulacions=10, output_dir="results"):
    """
    Executa l'escombrat de TAU amb la configuració actual de 'config'.
    Desa els resultats en un fitxer .npz i les gràfiques en .png.
    """
    # Crear carpeta de resultats amb data/hora per no sobreescriure
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(output_dir, timestamp)
    os.makedirs(run_dir, exist_ok=True)

    # Guardar la configuració utilitzada en un fitxer de text
    with open(os.path.join(run_dir, "config.txt"), "w") as f:
        for attr in dir(config):
            if not attr.startswith("__") and not callable(getattr(config, attr)):
                f.write(f"{attr} = {getattr(config, attr)}\n")

    TAUX = []
    segregacio_mitjana = []
    convergencia_mitjana = []

    # Crear totes les tasques (TAU, llavor)
    tasques = []
    for TAU in np.arange(0.01, 1.0, 0.02):
        for s in range(n_simulacions):
            llavor = s * 100 + int(TAU * 10)
            tasques.append((TAU, llavor))

    total_tasques = len(tasques)
    print(f"\n--- Iniciant {total_tasques} simulacions amb la configuració actual ---")

    # Execució paral·lela
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

    # Calcular mitjanes
    for tau in sorted(resultats_per_tau.keys()):
        dades = resultats_per_tau[tau]
        TAUX.append(tau)
        segregacio_mitjana.append(np.mean(dades["segs"]))
        convergencia_mitjana.append(np.mean(dades["iters"]))

    # Desar resultats numèrics
    np.savez(os.path.join(run_dir, "resultats.npz"),
             TAUX=TAUX,
             segregacio_mitjana=segregacio_mitjana,
             convergencia_mitjana=convergencia_mitjana)

    # Generar i desar gràfiques
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
    plt.savefig(os.path.join(run_dir, "grafica.png"))
    plt.close(fig)

    print(f"Resultats desats a: {run_dir}")
    return run_dir


# ------------------------------------------------------------
# Definició de les configuracions a provar
# ------------------------------------------------------------
if __name__ == "__main__":
    # Pots definir una llista de diccionaris amb els paràmetres a modificar.
    # Només cal incloure els valors que vols canviar respecte del config original.
    experiments = [
        {"MOVIMENT": 0, "DIMENSIONS": [20, 20]},               # Moviment adjacent
        {"MOVIMENT": 1, "DIMENSIONS": [20, 20]},               # Aleatori
        {"MOVIMENT": 2, "DIMENSIONS": [20, 20]},               # Global
        {"MOVIMENT": 3, "DIMENSIONS": [20, 20]},               # Primera millor (actual)
        {"MOVIMENT": 3, "DIMENSIONS": [30, 30], "MAX_ITER": 30}, # Mapa més gran
        {"TIPUS_DE_VEINS": 3, "PROBABILITATS_VEINS": [0.3, 0.3, 0.3]}, # 3 tipus
        {"TORUS": True, "MOVIMENT": 3},                        # Amb torus
    ]

    # Per a cada experiment, modifiquem config i executem l'escombrat
    for i, exp in enumerate(experiments, 1):
        print(f"\n{'='*60}")
        print(f"Experiment {i}/{len(experiments)}: {exp}")
        # Aplicar els canvis a config
        for key, value in exp.items():
            setattr(config, key, value)
        # Executar
        run_tau_sweep(n_simulacions=5, output_dir="experiments_results")  # ajusta n_simulacions

    print("\nTotes les configuracions completades.")