import numpy as np
import matplotlib.pyplot as plt
from utils import *
from config import *

if __name__ == "main":
    t=list(range(TIPUS_DE_VEINS))+[-1]
    p=PROBABILITATS_VEINS+[1-sum(PROBABILITATS_VEINS)]

    arr=np.reshape(np.random.choice(t, N**DIM_ESPAI, p=p), [N]*DIM_ESPAI)
    print(arr)
    
    
    pass