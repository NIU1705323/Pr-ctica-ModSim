import numpy as np


def generar_veins_l_inf(n_dim: int, distancia: float) -> np.ndarray:
    R = int(distancia)
    valorsPossibles = np.arange(-R, R + 1)
    producte_cartesia = np.meshgrid(*([valorsPossibles] * n_dim), indexing='ij')
    res=np.stack(producte_cartesia, axis=-1).reshape(-1, n_dim)
    return res[np.any(res != 0, axis=1)]


def generar_veins_l1(n_dim: int, distancia: float) -> np.ndarray:
    punts = generar_veins_l_inf(n_dim, distancia)
    return punts[np.sum(np.abs(punts), axis=1) <= distancia]


def generar_veins_l2(n_dim: int, distancia: float) -> np.ndarray:
    punts = generar_veins_l_inf(n_dim, distancia)
    return punts[np.sum(punts**2, axis=1) <= distancia**2]

def generar_ponderació_inversa(punts : np.ndarray, funció) -> np.ndarray:
    return np.array([1/funció(i) for i in punts])

def f_l1(punt : np.ndarray) -> float:
    return np.sum(punt)

def f_l2(punt : np.ndarray) -> float:
    return np.sqrt(np.sum(punt**2))

def f_l_inf(punt : np.ndarray) -> float:
    return np.max(np.abs(punt))

def generar_ponderació_identitat(punts : np.ndarray) -> np.ndarray:
    return np.array([1]*punts.shape()[0])

print(generar_veins_l1(2, 2))