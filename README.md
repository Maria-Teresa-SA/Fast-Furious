# MetroNyam
El projecte MetroNyam consisteix en un bot de Telegram que té l'objectiu d'ajudar a la gent de Barcelona a decidir a quin restaurant volen anar a menjar d'entre tots els restaurants de la ciutat i els dona la ruta més ràpida per arribar-hi des de la seva ubicació, caminant i en metro. 

## Estructura
Per tal de crear el bot MetroNyam, s'han desenvolupat 4 mòduls:
- `restaurants.py` conté les funcions que permeten obtenir la llista de restaurants de Barcelona i cerca-los en funció de les preferències de l'usuari.
- `metro.py` és on es crea el graf de les diferents línies de metro, amb les estacions i els correponents accessos, i conté funcions per visualitzar-lo.
- `city.py` és on es crea el graf de la ciutat, que uneix un graf de carrers de Barcelona i el graf desenvolupat a metro.py. Aquest mòdul també conté funcions per visualitzar el graf i obtenir el camí més ràpid entre dues coordenades de barcelona.
- `bot.py` ajunta els tres mòduls anteriors i permet l'interacció amb l'usuari per poder-lo guiar des de la seva ubicació al restaurant desitjat.

### Mòdul restaurants.py 🍽️
En aquest primer mòdul es llegeix un fitxer csv (restaurants.csv) amb les dades sobre els restaurants de Barcelona i es genera una llista on es guarden les dades rellevants d'aquests (nom, adressa, localització i categoria). També s'implementa una funció que, donades unes demandes - queries - retorna els restaurants que millor s'adeqüen a aquestes. S'ha implementat una cercla múltiple i difusa que té certes prioritats en ment a l'hora de retornar els resultats per no donar prioritat a aquells restaurants que apareixen abans a la llista de restaurants.

### Mòdul metro.py 🚇
En aquest mòdul es crea el graf que conté les diferents línies i estacions de metro i els seus corresponents accessos. Aquesta informació s'ha descarregat dels següents fitxers de dades:
- https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/blob/main/estacions.csv (estacions de metro)
- https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/blob/main/accessos.csv (accessos de metro)

El graf de metro és un graf no dirigit de `networkx`. Es poden diferenciar dos tipus de nodes, les estacions i els accessos, i tres tipus d'arestes, els trams de metro, els transbordaments, i els accessos (uneixen un node de tipus accés amb un de tipus estació). EXPLICAR ELS DIFERENTS ATRIBUTS DE NODES I ARESTES

D'altra banda, aquest mòdul també permet visualitzar gràficament el graf de metro creat. Això es pot fer amb dues funcions diferents:
```python3
def show(g: MetroGraph) -> None: ...
def plot(g: MetroGraph, filename: str) -> None: ...
```
La primera __________________-

En canvi la segona funció guarda una imatge en el fitxer desitjat on es pot veure el graf de metro representat sobre un mapa de la ciutat de barcelona.

### Mòdul city.py
En aquest mòdul es crea el graf de la ciutat de Barcelona, resultat de la unió del graf de les línies de metro, construit a `metro.py`, i del graf de carrers de barcelona, obtingut amb el mòdul `osmnx `. Aquest graf és el que utiltzem per trobar el camí més ràpid entre dues coordenades. 

### Mòdul bot.py
El mòdul bot.py és el que s'encarrega de comunicar-se amb l'usuari, obtenir les demandes d'aquest i retornar la informació requerida. Per assolir-ho, s'implementen dos tipus de funcions: 
1. Funcions d'interacció amb l'usuari
2. Funcions no accessibles per l'usuari

Un petit resum d'aquestes primeres són: 
1. /start - inicia la conversa amb l'usuari
2. /help - ofereix ajuda a l'usuari i informació sobre les altres comandes
3. /author - mostra el nom de les autores del projecte
4. /find - cerca quins restaurants compleixen la cerca realitzada
5. /info - mostra la informació del restaurant especificat
6. /guide - guia a l'usuari al restaurant especificat

## Començant

### Executar el codi
Per tal d'utilitzar el bot creat, cal tenir descarregat Python a l'ordinador, i Telegram o bé a l'ordinador o bé al mòbil. A més, cal tenir descarregades les llibreries especificades al arxiu `requeriments.txt`.

A més cal tenir descarregades en l'ordinador les bases de dades ______________ (no se si aixo va dins de requiriments idk)

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
El projecte MetroNyam (versió Fast&Furious) ha estat creat per Laura Solà Garcia i Sílvia Fàbregas Salazar, estudiants de Ciència i Enginyeria de Dades a la UPC com a part de l'assignatura Algorísmia i Programació 2. L'especificació del treball es pot trobar a https://github.com/jordi-petit/ap2-metro-nyam-2022

## Llicència
Copyright © 2022 Laura Solà Garcia and Sílvia Fàbregas Salazar.

Aquest projecte està disponible sota els termes de la GNU General Public License (Llicència Pública General). Vegeu LICENSE.md per a més informació.
