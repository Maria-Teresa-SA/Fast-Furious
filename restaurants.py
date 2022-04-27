import pandas 
from dataclasses import dataclass
from typing import Optional, List

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
  register_id: int # ID del restaurant (potser inútil)
  address: Address # adressa del restaurant
  category : str # tipus de restaurant

Restaurants = [Restaurant]

#descarregar i llegir el fitxers de restaurants i retornar-ne la seva llista
def read() -> Restaurants: 
  
  csv_url = "https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/restaurants.csv"
  taula_dades = pandas.read_csv(csv_url)
  ls = [] # type: Restaurants
  for i, row in taula_dades.iterrows():
    restaurant = Restaurant(row['name'], int(row['register_id'].strip('\ufeff')), Address(row['addresses_road_name'], row['addresses_start_street_number'], row['addresses_neighborhood_name'], row['addresses_district_name'], row['addresses_zip_code']),  row['secondary_filters_name'])
    ls.append(restaurant)
 
  return ls



#busca els restaurants que satisfan la cerca
def find(query: str, restaurants: Restaurants) -> Restaurants: ...