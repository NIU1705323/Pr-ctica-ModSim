
MAX_ITER = 100 # maxim iteracions
N = 10 # tamany de la graella 10x10
DIM_ESPAI=2 # graella de 2 dimensions
TIPUS_DE_VEINS=2 # qui sap que passarà si l'augmentem
PROBABILITATS_VEINS=[0.25, 0.25] # al 50% restant no hi ha ningú
INDEXOS_VEINS = [ # veins del [0,0]
    [-1,-1], [-1,0], [-1,1],
    [0,-1],          [0,1],
    [1,-1],  [1,0],  [1,1]
]
PONDERACIONS = [1]*8 # tots els veïns tenen la mateixa importància