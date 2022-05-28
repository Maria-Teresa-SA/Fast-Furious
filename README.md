# MetroNyam
El projecte MetroNyam consisteix en un bot de Telegram que té l'objectiu d'ajudar a la gent de barcelona a decidir a quin restaurant volen anar a menjar d'entre tots els restaurants de la ciutat i els dona la ruta més ràpida per arribar-hi des de la seva ubicació, caminant i en metro. 

## Estructura
Per tal de crear el bot MetroNyam, s'han desenvolupat 4 mòduls:
- `restaurants.py` conté les funcions que permeten obtenir la llista de restaurants de barcelona i cerca-los en funció de les preferències del usuari
- `metro.py` on es crea el graf de les diferents línies de metro, amb les estacions i els correponents accessos, i conté funcions per visualitzar-lo
- `city.py` on es crea el graf de la ciutat, que ajunta un graf de carrers i el graf desenvolupat a metro.py. Aquest mòdul també conté funcions per visualitzar el graf i obtenir el camí més ràpid entre dues coordenades de barcelona.
- `bot.py` el qual ajunta els tres mòduls anteriors i permet l'interacció amb l'usuari per poder-lo guiar des de la seva ubicació al restaurant desitjat

## Mòdul restaurants.py

## Mòdul metro.py

## Mòdul city.py

## Mòdul bot.py

##Començant


Per Laura Solà i Sílvia Fàbregas
