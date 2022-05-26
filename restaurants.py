# llibreries importades

import pandas                                   # llegir fitxer csv
from dataclasses import dataclass               # classes
from typing import Optional, TextIO, List       # typing
from collections import namedtuple              # generar tuples (Coord)
from fuzzysearch import find_near_matches       # fer cerca difusa


######################
#                    #
#   Tipus de dades   #
#                    #
######################

categories = ['Restaurants', 'Tablaos flamencs', 'Cocteleries','Xampanyeries','Bars i pubs musicals' , 'Discoteques', 'Karaokes', 'Teatres']

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
#                           #
#  Funcions implementades   #
#                           #
#############################

# pre: tenir el fitxer restaurants.csv
def read() -> Restaurants:

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
  return e[1]

def find(queries: List[str], restaurants: Restaurants) -> Restaurants:

  """Retorna els restaurants que satisfan les condicions de la cerca realitzada. S'ha implementat una cerca
  múltiple i difusa (amb màxima distància d'un caràcter)."""

  pesos = []

  buscar_a_categories = False
  for query in queries:
    for category in categories:
      if query.title() in category:
        buscar_a_categories = True

  for restaurant in restaurants:
    add = True
    pes = 0
    for query in queries:
      found = False
      query = query.title() 

      for el in [restaurant.address.district, restaurant.address.neighbourhood, restaurant.address.address_name, restaurant.name]:
        fuzzy = find_near_matches(query, el, max_l_dist = 1)
        if len(fuzzy):
          found = True
          pes = pes + 2 - fuzzy[0].dist
          break
      # en cas que hem definit que volem buscar dins les categories
      if not found and buscar_a_categories:
        if query in restaurant.category:
          found = True
          pes += 2
          break

      # si una query no encaixa amb cap element del restaurant
      if not found:
        add = False
        break

    if add: 
      pesos.append([restaurant, pes])

  pesos.sort(reverse=True, key=myFunc)

  possibilitats = []

  for el in pesos:
    possibilitats.append(el[0])
  return possibilitats