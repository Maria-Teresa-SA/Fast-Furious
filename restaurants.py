# llibreries importades

import pandas                                   # llegir fitxer csv
from dataclasses import dataclass               # classes
from typing import Optional, TextIO, List       # typing
from collections import namedtuple              # generar tuples (Coord)
from fuzzysearch import find_near_matches       # fer cerca difusa

categories = ['Restaurants', 'Tablaos flamencs', 'Cocteleries','Xampanyeries', 'Bars i pubs musicals' , 'Discoteques', 'Karaokes', 'Teatres']

######################
#   Tipus de dades   #
######################

Coord = namedtuple('Coord', ['x', 'y']) # type = tuple(longitude, latitude)

@dataclass
class Address:
  address_name: str # nom del carrer
  address_num: Optional[int] # número del carrer, falta tractar amb els valors Nan
  neighbourhood: str # barri
  district: str # districte
  zip_code: int # codi postal

@dataclass
class Restaurant: 
  name: str # nom del restaurant
  address: Address # adressa del restaurant
  category : str # tipus de restaurant
  position: Coord # coordenades del restaurant

Restaurants = List[Restaurant]


#############################
#  Funcions implementades   #
#############################

# pre: tenir el fitxer restaurants.csv
def read_restaurants() -> Restaurants:

    """Llegeix el fitxer restaurants.csv i retorna una llista amb tots els restaurants de la ciutat de Barcelona amb les dades pertinents."""

    # columnes que guardem
    c_g = ['name', 'addresses_road_name', 'addresses_start_street_number', 'addresses_neighborhood_name',
                        'addresses_district_name', 'addresses_zip_code', 'secondary_filters_name', 'geo_epgs_4326_x','geo_epgs_4326_y']
    # lectura de dades
    taula_dades = pandas.read_csv("restaurants.csv", usecols=c_g, keep_default_na=False, dtype={c_g[0]: str, c_g[1]: str, c_g[2]: str, c_g[3]: str, c_g[4]: str, c_g[5]: str, c_g[6]: str, c_g[7]: float, c_g[8]: float})
                                                                                                   
    ls = []  # type: Restaurants
    for i, row in taula_dades.iterrows():
        restaurant = Restaurant(row['name'], Address(row['addresses_road_name'], row['addresses_start_street_number'],
                                row['addresses_neighborhood_name'], row['addresses_district_name'], row['addresses_zip_code']),  row['secondary_filters_name'], Coord(row['geo_epgs_4326_y'], row['geo_epgs_4326_x']))
        ls.append(restaurant)

    return ls


def myFunc(e):

  """Criteri d'ordenació dels restaurants quan es realitza una búsqueda - De major a menor pes."""

  return e[1]

def find_restaurants(queries: List[str], restaurants: Restaurants) -> Restaurants:

  """Retorna els restaurants que satisfan les condicions de la cerca realitzada. S'ha implementat una cerca
  múltiple i difusa (amb màxima distància d'un caràcter). A més a més, a cada restaurant que encaixa amb la cerca
  se li assigna un pes que depèn essencialment de si al comparar una query amb un element del restaurant hi ha hagut
  encert total o encert amb distància 1 (un caràcter de diferència). Si no es realitzés aquesta priorització, al realitzar
  la búsqueda "sushi Sants", els resultats capçalera serien tots de Sarrià-Sant Gervasi i Sant Antoni, ja que són les entrades
  que apareixen abans a la llista de restaurants.
  """

  for i in range(len(queries)):
    queries[i] = queries[i].title()   # millorar coincidències
    
  pesos = []

  # només busquem dins les categories si hi ha un encert total (no fuzzysearch) per evitar problemes amb la fuzzysearch
  #  i parelles de paraules com Sants i Restaurants.
  buscar_categories = False
  for query in queries:
    for category in categories:
      buscar_categories = query in category
      if buscar_categories: break
    if buscar_categories: break
      

  for restaurant in restaurants:
    pes = 0        
    coincidencia = False        # si coincidència és True : restaurant coincideix amb la cerca. Pes és la seva prioritat.

    for query in queries:
      coincidencia = False            
      for el in [restaurant.address.district, restaurant.address.neighbourhood, restaurant.address.address_name, restaurant.name]:
        fuzzy = find_near_matches(query, el, max_l_dist = 1)
        if len(fuzzy):
          coincidencia = True
          pes += 2 - fuzzy[0].dist
          break

      # en cas que hem definit que volem buscar dins les categories, si encara no ha coincidit
      if not coincidencia and buscar_categories:
        if query in restaurant.category:
          coincidencia = True
          pes += 2

      # si una query no encaixa amb cap element del restaurant, no l'afegirem
      if not coincidencia: break

    if coincidencia: 
      pesos.append([restaurant, pes])

  pesos.sort(reverse=True, key=myFunc)

  return [el[0] for el in pesos]