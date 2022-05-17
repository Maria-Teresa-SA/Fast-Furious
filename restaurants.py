import pandas 
from dataclasses import dataclass
from typing import Optional, TextIO, List
from collections import namedtuple              # generar tuples (Coord)

# import fuzzysearch import find_near_matches

# falta typealias
Coord = namedtuple('Coord', ['x', 'y']) # (longitude, latitude)


# IDEA 1: tenir una llista dels elements per poder comparar
districts = ['Sants-Montjuïc',
 'Eixample',
 'Sant Andreu',
 'Sarrià-Sant Gervasi',
 'Sant Martí',
 'Ciutat Vella',
 'Gràcia',
 'Les Corts',
 'Nou Barris',
 'Horta-Guinardó']

hoods = ['Sants',
 "la Dreta de l'Eixample",
 "l'Antiga Esquerra de l'Eixample",
 'Sant Andreu',
 'el Putxet i el Farró',
 'Provençals del Poblenou',
 'el Barri Gòtic',
 'Sant Gervasi - Galvany',
 'la Vila de Gràcia',
 'Hostafrancs',
 'el Bon Pastor',
 'Sant Antoni',
 'el Fort Pienc',
 'Sant Pere, Santa Caterina i la Ribera',
 'el Poblenou',
 'Sant Martí de Provençals',
 'el Poble-sec',
 'el Raval',
 'la Vila Olímpica del Poblenou',
 'les Corts',
 'el Congrés i els Indians',
 "el Camp de l'Arpa del Clot",
 "la Nova Esquerra de l'Eixample",
 'la Marina de Port',
 'la Sagrada Família',
 "el Camp d'en Grassot i Gràcia Nova",
 'la Barceloneta',
 'Sarrià',
 'Diagonal Mar i el Front Marítim del Poblenou',
 'Navas',
 'el Parc i la Llacuna del Poblenou',
 'Porta',
 'la Maternitat i Sant Ramon',
 'Sant Gervasi - la Bonanova',
 'la Font de la Guatlla',
 'Vallvidrera, el Tibidabo i les Planes',
 'Vilapicina i la Torre Llobeta',
 'la Marina del Prat Vermell',
 'Vallcarca i els Penitents',
 'Horta',
 'el Guinardó',
 'la Verneda i la Pau',
 'la Bordeta',
 'Pedralbes',
 'Torre Baró',
 'la Teixonera',
 'les Tres Torres',
 'Can Baró',
 'Sants - Badal',
 'la Sagrera',
 'la Salut',
 'el Carmel',
 'el Clot',
 'el Coll',
 'la Guineueta',
 "la Font d'en Fargues",
 'el Baix Guinardó',
 'el Besòs i el Maresme',
 'Verdun',
 "la Vall d'Hebron",
 'el Turó de la Peira',
 'la Trinitat Vella',
 'la Prosperitat',
 'Canyelles',
 'Montbau']

categories = ['Restaurants',
 'Tablaos flamencs',
 'Cocteleries',
 'Xampanyeries',
 'Bars i pubs musicals',
 'Discoteques',
 'Karaokes',
 'Teatres']

@dataclass
class Address:
  address_name: str # nom del carrer
  address_num: Optional[int] # número del carrer, falta tractar amb els valors Nan
  neighbourhood: str # barri
  district: str # districte
  zip_code: int #codi postal

@dataclass
class Restaurant: 
  name: str # nom del restaurant
  address: Address # adressa del restaurant
  category : str # tipus de restaurant
  position: Coord

Restaurants = [Restaurant]
 
# descarregar i llegir el fitxers de restaurants i retornar-ne la seva llista
def read() -> Restaurants:

    columnes_guardem = ['name', 'addresses_road_name', 'addresses_start_street_number', 'addresses_neighborhood_name',
                        'addresses_district_name', 'addresses_zip_code', 'secondary_filters_name', 'geo_epgs_4326_x','geo_epgs_4326_y']
    taula_dades = pandas.read_csv("restaurants.csv", usecols=columnes_guardem, keep_default_na=False, dtype={'name': str,
                                                                                                   'addresses_road_name': str,
                                                                                                   'addresses_start_street_number': str,
                                                                                                   'addresses_neighborhood_name': str,
                                                                                                   'addresses_district_name': str,
                                                                                                   'addresses_zip_code': str,
                                                                                                   'secondary_filters_name': str,
                                                                                                   'geo_epgs_4326_x': float,
                                                                                                   'geo_epgs_4326_y': float
                                                                                                   })
    ls = []  # type: Restaurants
    for i, row in taula_dades.iterrows():
        restaurant = Restaurant(row['name'], Address(row['addresses_road_name'], row['addresses_start_street_number'],
                                row['addresses_neighborhood_name'], row['addresses_district_name'], row['addresses_zip_code']),  row['secondary_filters_name'], Coord(row['geo_epgs_4326_y'], row['geo_epgs_4326_x']))
        ls.append(restaurant)
    # POSSIBLE ALTERNATIVA
    #ls = taula_dades.tolist()
    # problema: no guarda adreces com a struct

    return ls


# https://pypi.org/project/fuzzysearch/ Per implementar la cerca difusa

#busca els restaurants que satisfan la cerca
def find(query: str, restaurants: Restaurants) -> Restaurants:

  queries = query.split(" ") # multiple queries
  possibilities = [] # type: Restaurants
  for restaurant in restaurants:
    for query in queries:
      add = False
      for el in [restaurant.category, restaurant.address.district, restaurant.address.neighbourhood, restaurant.address.address_name, restaurant.name]:
        if query in el:
          add = True
          break
      if not add: break  
    if add: possibilities.append(restaurant)

  return possibilities
