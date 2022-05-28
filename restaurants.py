# llibreries importades

import pandas                                          # llegir fitxer csv
from dataclasses import dataclass                      # classes
from typing_extensions import TypeAlias                # typealiases
from typing import Optional, TextIO, List, Tuple       # typing
from collections import namedtuple                     # generar tuples (Coord)
from fuzzysearch import find_near_matches              # fer cerca difusa

categories = ['Restaurants', 'Tablaos flamencs', 'Cocteleries','Xampanyeries', 'Bars i pubs musicals' , 'Discoteques', 'Karaokes', 'Teatres']

######################
#   Tipus de dades   #
######################

# (longitud, latitud)
Coord = namedtuple('Coord', ['x', 'y']) # type = Tuple[float, float]

@dataclass
class Address:
  address_name: TypeAlias = str # nom del carrer
  address_num: TypeAlias = Optional[int] # número del carrer, falta tractar amb els valors Nan
  neighbourhood: TypeAlias = str # barri
  district: TypeAlias = str # districte
  zip_code: TypeAlias = int # codi postal

@dataclass
class Restaurant: 
  name: TypeAlias = str # nom del restaurant
  address: TypeAlias = Address # adressa del restaurant
  category : TypeAlias = str # tipus de restaurant
  position: TypeAlias = Coord # coordenades del restaurant

Restaurants = List[Restaurant]


#############################
#  Funcions implementades   #
#############################

#####################
#  Lectura de dades #
#####################

# pre: tenir el fitxer restaurants.csv
def read_restaurants() -> Restaurants:

    """Llegeix el fitxer restaurants.csv i retorna una llista amb tots els restaurants de la ciutat de Barcelona amb les dades pertinents."""

    # columnes que guardem
    cols = ['name', 'addresses_road_name', 'addresses_start_street_number', 'addresses_neighborhood_name',
                        'addresses_district_name', 'addresses_zip_code', 'secondary_filters_name', 'geo_epgs_4326_x','geo_epgs_4326_y']
    # lectura de dades
    data_table = pandas.read_csv("restaurants.csv", usecols=cols, keep_default_na=False, dtype={cols[0]: str, cols[1]: str, cols[2]: str, cols[3]: str, cols[4]: str, cols[5]: str, cols[6]: str, cols[7]: float, cols[8]: float})
                                                                                                   
    ls = []  # type: Restaurants
    for i, row in data_table.iterrows():
        restaurant = Restaurant(row['name'], Address(row['addresses_road_name'], row['addresses_start_street_number'],
                                row['addresses_neighborhood_name'], row['addresses_district_name'], row['addresses_zip_code']),  row['secondary_filters_name'], Coord(row['geo_epgs_4326_y'], row['geo_epgs_4326_x']))
        ls.append(restaurant)

    return ls


#################
#     Cerca     #
#################

def myFunc(rest: Tuple[Restaurant, int]):

  """Criteri d'ordenació dels restaurants quan es realitza una búsqueda - De major a menor pes."""

  return rest[1]

def find_restaurants(queries: List[str], restaurants: Restaurants) -> Restaurants:

  """Retorna els restaurants que satisfan les condicions de la cerca realitzada. S'ha implementat una cerca
  múltiple i difusa (amb màxima distància d'un caràcter). A més a més, a cada restaurant que encaixa amb la cerca
  se li assigna un pes que depèn essencialment de si al comparar una query amb un element del restaurant hi ha hagut
  encert total o encert amb distància 1 (un caràcter de diferència). Si no es realitzés aquesta priorització, al realitzar
  la búsqueda "sushi Sants", els resultats capçalera serien tots de Sarrià-Sant Gervasi i Sant Antoni, ja que són les entrades
  que apareixen abans a la llista de restaurants.
  """

  for i in range(len(queries)):
    queries[i] = queries[i].title()   # millorar coincidències. Majoria de paraules es troben en aquest format al fitxer de restaurants.
    
  weigths = [] # weigths és una llista de parelles de [Restaurant, pes_associat]

  # només busquem dins les categories si hi ha un encert total (no fuzzysearch) per evitar problemes amb la fuzzysearch
  # i parelles de paraules com Sants i Restaurants.
  search_categories = False
  for query in queries:
    for category in categories:
      search_categories = query in category
      if search_categories: break
    if search_categories: break
      

  for restaurant in restaurants:
    w = 0 # pes inicial        
    for query in queries:
      match = False      # si coincidència és True : restaurant coincideix amb la cerca. Pes és la seva prioritat.        
      for el in [restaurant.address.district, restaurant.address.neighbourhood, restaurant.address.address_name, restaurant.name]:
        fuzzy = find_near_matches(query, el, max_l_dist = 1)
        if len(fuzzy):
          match = True
          w += 2 - fuzzy[0].dist
          break

      # en cas que hem definit que volem buscar dins les categories, si encara no ha coincidit
      if not match and search_categories and query in restaurant.category:
        match = True
        w += 2

      # si una query no encaixa amb cap element del restaurant, no l'afegirem
      if not match: break

    if match: 
      weigths.append([restaurant, w])

  weigths.sort(reverse=True, key=myFunc)

  return [el[0] for el in weigths] 



