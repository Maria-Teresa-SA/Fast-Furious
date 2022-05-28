# MetroNyam
El projecte MetroNyam consisteix en un bot de Telegram que té l'objectiu d'ajudar a la gent de barcelona a decidir a quin restaurant volen anar a menjar d'entre tots els restaurants de la ciutat i els dona la ruta més ràpida per arribar-hi des de la seva ubicació, caminant i en metro. 

## Estructura
Per tal de crear el bot MetroNyam, s'han desenvolupat 4 mòduls:
- `restaurants.py` conté les funcions que permeten obtenir la llista de restaurants de barcelona i cerca-los en funció de les preferències del usuari
- `metro.py` on es crea el graf de les diferents línies de metro, amb les estacions i els correponents accessos, i conté funcions per visualitzar-lo
- `city.py` on es crea el graf de la ciutat, que ajunta un graf de carrers i el graf desenvolupat a metro.py. Aquest mòdul també conté funcions per visualitzar el graf i obtenir el camí més ràpid entre dues coordenades de barcelona.
- `bot.py` el qual ajunta els tres mòduls anteriors i permet l'interacció amb l'usuari per poder-lo guiar des de la seva ubicació al restaurant desitjat

### Mòdul restaurants.py

### Mòdul metro.py

### Mòdul city.py

### Mòdul bot.py

## Començant

### Executar el codi
Per tal d'utilitzar el bot creat, cal tenir descarregat Python a l'ordinador, i Telegram o bé a l'ordinador o bé al mòbil. A més, cal tenir descarregades les llibreries especificades al arxiu `requeriments.txt`.

Per començar a utilitzar el bot cal escriure la següent línia de comandes a la terminal
``` 
pip3 install -r requirements.txt 
python3 bot.py 
```
Un cop fet això, ja es pot començar a utiltzar el bot

### Inicialitzar el bot



## Example de funcionament del bot

En les següents fotografies es pot veure un exemple de com funciona el bot si busques un restaurant ¿de sushi a sants?, en aquest cas ¿_______? i a algú des de la seva ubicació fins al restaurant

POSAR FOTOS !!!


## Autores
El projecte MetroNyam ha estat creat per Laura Solà Garcia i Sílvia Fàbregas Salazar, estudiants de Ciència i Enginyeria de Dades a la UPC com a part de l'assignatura Algorísmia i Programació 2. L'especificació del treball es pot trobar a https://github.com/jordi-petit/ap2-metro-nyam-2022

## Llicència
Copyright © 2022 Laura Solà Garcia and Sílvia Fàbreagas Salazar.

Aquest projecte està disponible sota els termes de la GNU General Public License (Llicència Pública General), versió 3. Vegeu LICENSE.md per a més informació.
