########################## CONFIGURACIÓ ##########################
##                                                              ##
## Document amb els paràmetres de la simulació                  ##
##                                                              ##
## Es poden ajustar tal i com sigui convenient                  ##
##                                                              ##
##################################################################

# Variables de l'entorn de la simulació
MAX_ITER = 100 # maxim iteracions
DIMENSIONS = [20, 30] # Forma del mapa (de moment matriu)
TAU = 0.7 # no posar proper a 1 q no acaba mai (no estan satisfets)
SEED = None # paràmetre per a repetir inicialitzacions


# Variables dels veins
TIPUS_DE_VEINS=2 # Nombre de colors diferents excloent Null
PROBABILITATS_VEINS=[0.2, 0.4] # Vector de proporcions dels veins


# Taules d'adjacencia amb les seves ponderacions
INDEXOS_VEINS = [ # veins del [0,0]
    [-1,-1], [-1,0], [-1,1],
    [0,-1],          [0,1],
    [1,-1],  [1,0],  [1,1]
]
PONDERACIONS = [1]*8 # tots els veïns tenen la mateixa importància