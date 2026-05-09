########################## CONFIGURACIÓ ##########################
##                                                              ##
## Document amb els paràmetres de la simulació                  ##
##                                                              ##
## Es poden ajustar tal i com sigui convenient                  ##
##                                                              ##
##################################################################

MAX_ITER = 100 # maxim iteracions
N = 10 # tamany de la graella 10x10
DIM_ESPAI=2 # graella de 2 dimensions
TIPUS_DE_VEINS=3 # Nombre de colors diferents excloent Null
PROBABILITATS_VEINS=[0.12, 0.12, 0.12] # Vector de proporcions dels veins
INDEXOS_VEINS = [ # veins del [0,0]
    [-1,-1], [-1,0], [-1,1],
    [0,-1],          [0,1],
    [1,-1],  [1,0],  [1,1]
]
PONDERACIONS = [1]*8 # tots els veïns tenen la mateixa importància
TAU = 0.7 # no posar proper a 1 q no acaba mai (no estan satisfets)
SEED = None # paràmetre per a repetir inicialitzacions