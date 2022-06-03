# MetroNyam 🍕🍔
El projecte MetroNyam consisteix en un bot de Telegram que té l'objectiu d'ajudar a la gent de Barcelona a decidir a quin restaurant volen anar a menjar d'entre tots els restaurants de la ciutat i els dona la ruta més ràpida per arribar-hi des de la seva ubicació, caminant i en metro. 

## Estructura
Per tal de crear el bot MetroNyam, s'han desenvolupat 4 mòduls:
- `restaurants.py` conté les funcions que permeten obtenir la llista de restaurants de Barcelona i cerca-los en funció de les preferències de l'usuari.
- `metro.py` és on es crea el graf de les diferents línies de metro, amb les estacions i els correponents accessos, i conté funcions per visualitzar-lo.
- `city.py` és on es crea el graf de la ciutat, que uneix un graf de carrers de Barcelona i el graf desenvolupat a metro.py. Aquest mòdul també conté funcions per visualitzar el graf i obtenir el camí més ràpid entre dues coordenades de barcelona.
- `bot.py` ajunta els tres mòduls anteriors i permet l'interacció amb l'usuari per poder-lo guiar des de la seva ubicació al restaurant desitjat.

### Mòdul restaurants.py 🍽️
En aquest primer mòdul es llegeix un fitxer csv (restaurants.csv) amb les dades sobre els restaurants de Barcelona i es genera una llista on es guarden les dades rellevants d'aquests (nom, adressa, localització i categoria). També s'implementa una funció que, donades unes demandes - queries - retorna els restaurants que millor s'adeqüen a aquestes. S'ha implementat una cercla múltiple i difusa que té certes prioritats en ment a l'hora de retornar els resultats per no donar prioritat a aquells restaurants que apareixen abans a la llista de restaurants. Les prioritats permeten un semi-filtratge de cerques  no vàlides que són acceptades per la fuzzysearch. Per exemple, si busquéssim restaurants al barri de Sants (query = "Sants"), a dalt de la llista apareixerien tots els restaurants de Sant-Gervasi i Sant Andreu. Amb la implementacio de les prioritats, la coicidència total amb la paraula Sants permetrà que aquests resultats apareguin abans.

### Mòdul metro.py 🚇
En aquest mòdul es crea el graf que conté les diferents línies i estacions de metro i els seus corresponents accessos. Aquesta informació s'ha descarregat dels següents fitxers de dades:
- https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/blob/main/estacions.csv (estacions de metro)
- https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/blob/main/accessos.csv (accessos de metro)

El graf de metro és un graf no dirigit de `networkx`. Es poden diferenciar dos tipus de nodes, les estacions i els accessos, i tres tipus d'arestes, els trams de metro, els transbordaments, i els accessos (uneixen un node de tipus accés amb un de tipus estació). 

D'altra banda, aquest mòdul també permet visualitzar gràficament el graf de metro creat de dues maneres: el pots veure com un graf dinàmic que s'obre en una finestra de la terminal, o alternativament guardar una imatge en el fitxer desitjat on es pot veure el graf de metro representat sobre un mapa de la ciutat de barcelona.


### Mòdul city.py 🏙
En aquest mòdul es crea el graf de la ciutat de Barcelona, resultat de la unió del graf de les línies de metro, construit a `metro.py`, i del graf de carrers de barcelona, obtingut amb el mòdul `osmnx `. 
Llavors, a partir del graf de la ciutat de Barcelona, hi ha implementada una funció que troba el camí més ràpid, caminant i en metro, entre dos punts de la ciutat. A més, també es pot obtenir l'expilcació de la ruta que cal seguir i el temps que es trigaria en fer-la.
Per últim, de la mateixa manera que el graf de metro, el graf de Barcelona també es pot visualitzar tant en forma de graf dinàmic, com en forma  d'imatge amb el mapa de Barcelona com a fons.

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

### Prerequisits
Per tal d'utilitzar el bot creat, cal tenir descarregat [Python](https://www.python.org/) a l'ordinador, i [Telegram](https://telegram.org/) o bé a l'ordinador o bé al mòbil. A més, cal tenir descarregades les llibreries especificades al arxiu `requeriments.txt`. Això es pot fer amb la següent línia de comandes:
```
python -m pip install -r requirements.txt
```

També cal tenir descarregats els fitxers de dades que utilitzen els diferents mòduls. Aquests són:
- https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/blob/main/estacions.csv
- https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/blob/main/accessos.csv
- https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/restaurants.csv
- https://github.com/amoudgl/short-jokes-dataset/blob/master/data/reddit-cleanjokes.csv



### Inicialitzar el bot
Per poder utilitzar el bot, primer necessites crear un Access token, un identificador que Telegram us dóna per identificar el bot. Per fer-ho cal obrir Telegram i visitar el [@BotFather](https://telegram.me/botfather). Executa la comanda `\newbot` i escriu el que et demani sobre el nom complet i nom d'usuari del bot (pots posar el que vulguis mentre acabi amb `bot`). Un cop fet, el [@BotFather](https://telegram.me/botfather) et donarà un access token, el qual has de guardar en un fitxer anomenat `token.txt`. Guarda l'arxiu en el directori principal del projecte. 

Ara el bot ja està creat, i per executar-lo escriu la següent comanda a la terminal
``` 
python3 bot.py 
```
Ara ja podràs parlar des de [Telegram](https://telegram.org/) amb el bot i que et guiï al restaurant que prefereixis!


## Example de funcionament del bot

En les següents fotografies es pot veure un exemple de com funciona el bot si busques un restaurant ¿de sushi a sants?, en aquest cas ¿_______? i a algú des de la seva ubicació fins al restaurant

POSAR FOTOS !!!


## Autores
El projecte MetroNyam (versió Fast&Furious) ha estat creat per Laura Solà Garcia i Sílvia Fàbregas Salazar, estudiants de Ciència i Enginyeria de Dades a la UPC com a part de l'assignatura Algorísmia i Programació 2. L'especificació del treball es pot trobar a https://github.com/jordi-petit/ap2-metro-nyam-2022

## Llicència
Copyright © 2022 Laura Solà Garcia and Sílvia Fàbregas Salazar.

Aquest projecte està disponible sota els termes de la GNU General Public License (Llicència Pública General). 
