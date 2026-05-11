########################## CONFIGURACIÓ ##########################
##                                                              ##
## Document amb els paràmetres de la simulació                  ##
##                                                              ##
## Es poden ajustar tal i com sigui convenient                  ##
##                                                              ##
##################################################################

# Variables de l'entorn de la simulació
MAX_ITER = 100 # maxim iteracions
DIMENSIONS = [50, 50] # Forma del mapa (de moment matriu)
SEED = 1234 # paràmetre per a repetir inicialitzacions
COLOR = "hsv" # color dels plots, per exemple hsv, twilight, terrain
VISUALITZACIONS = 1 # cada quantes iteracions mostrar el plot
TEMPS_ESPERA = 0.01 # minim tems en que es mostra el plot (recomanat 0.01)


# Variables de conformitat:
TAU = 0.7 # no posar proper a 1 q no acaba mai (no estan satisfets)
SATISFET = 1.0 # valor al qual ja es considera satisfet


# Variables dels veins
TIPUS_DE_VEINS=2 # Nombre de colors diferents excloent Null
PROBABILITATS_VEINS=[0.3, 0.3] # Vector de proporcions dels veins


# Taules d'adjacencia amb les seves ponderacions
INDEXOS_VEINS = [ # veins del [0,0]
    [-1,-1], [-1,0], [-1,1],
    [0,-1],          [0,1],
    [1,-1],  [1,0],  [1,1]
]
PONDERACIONS = [1]*8 # tots els veïns tenen la mateixa importància
MOVIMENT = 0 # 0: Adjacent, 1: Aleatori, 2: Global, 3: Primera Millor