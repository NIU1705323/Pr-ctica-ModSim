########################## CONFIGURACIÓ ##########################
##                                                              ##
## Document amb els paràmetres de la simulació                  ##
##                                                              ##
## Es poden ajustar tal i com sigui convenient                  ##
##                                                              ##
##################################################################

# Variables de l'entorn de la simulació
MAX_ITER = 67 # maxim iteracions
DIMENSIONS = [20, 20] # Forma del mapa (de moment matriu)
SEED = 1234 # paràmetre per a repetir inicialitzacions
COLOR = "hsv" # color dels plots, per exemple hsv, twilight, terrain
VISUALITZACIONS = 1 # cada quantes iteracions mostrar el plot
TEMPS_ESPERA = 0.01 # minim tems en que es mostra el plot (recomanat 0.01)
REPETICIONS = 1 # plots adjacents identics, útil pel torus (default 1)


# Variables de conformitat:
TAU = 0.75 # no posar proper a 1 q no acaba mai (no estan satisfets)
SATISFET = 1.0 # valor al qual ja es considera satisfet (default 1.0)


# Variables dels veins
TIPUS_DE_VEINS=3 # nombre de colors diferents excloent Null
PROBABILITATS_VEINS=[0.4, 0.3, 0.25] # vector de proporcions dels veins
MOVIMENT = 3 # 0: Adjacent, 1: Aleatori, 2: Global, 3: Primera Millor
TIPUS_PONDERACIONS = 0 #0: Tots 1, 1: Inversament proporcional a la distancia
DISTANCIA_MAXIMA_VEINS = 3 # distancia en la que els veins s'afecten
METRICA = 2 # 0: l_inf, qualsevol altre N: l_N 
TORUS = False # True: els bordes donen la volta, False: limitat per matriu