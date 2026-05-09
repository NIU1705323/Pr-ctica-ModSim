# Treball 6. El model de Schelling: segregació urbana espontània 


**Motivació i context** 

Thomas Schelling, premi Nobel d'Economia el 2005, va proposar el 1971 un model sorprenent: agents amb una tolerància moderada cap a veïns d'un altre grup produeixen, per la seva interacció local, una segregació espacial molt superior a la que la tolerància individual semblaria justificar. 

El model és un cas paradigmàtic de comportament emergent: el resultat col·lectiu és qualitativament diferent de les intencions individuals, i il·lustra per què la intuïció falla en sistemes complexos. 


**Descripció del problema** 

Distribuïu aleatòriament tres tipus de cel·les en una graella N×N: agents vermells, agents blaus i cel·les buides. Un agent es considera satisfet si la proporció de veïns del seu tipus entre els seus veïns ocupats és ≥τ (llindar de tolerància). En cas contrari, l'agent està insatisfet i vol moure's. 


**Simulació** 

Estableix el protocol de la dinàmica de moviment i repetiu-lo fins que tots els agents estiguin satisfets (equilibri) o fins a un cert màxim d'iteracions. Mesureu la segregació: la proporció mitjana de veïns del mateix tipus per sobre del 50% esperat (si fos aleatòri). Feu un estudi de com afecta el llindar de tolerància. Interpreteu els resultats: fins a quin punt el model captura fenòmens reals de segregació urbana? Quines simplificacions fa? Com es podria ampliar per incorporar preus del sòl, xarxes socials o discriminació activa? Estudieu què passa quan el llindar de tolerància depen del tipus d'agent (vermell o blau) i l'efecte d'introduir un tercer agent diferent als dos anteriors. 



# Métode d'execució


**Fitxer de configuració**

Dins d'aquest fitxer s'inclouen els paràmetres de la simulació amb una breu descripció de cadascun d'ells. Es poden canviar per a obtenir noves simulacions amb diferents comportaments, dimensions, o fins i tot repetir experiments.

**Començar a simular**

Per a veure el comportament de la població, només cal executar el fitxer _main.py_.