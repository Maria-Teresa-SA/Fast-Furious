import pandas # llegir fitxers csv
from dataclasses import dataclass # dataclasses
from typing_extensions import TypeAlias 
from typing import Optional, TextIO, List # typing
from collections import namedtuple # generar tuples 
import networkx as nx # generar graf

import matplotlib.pyplot as plt # plotejar mapa

#import staticmaps

# falta typealias
Position = namedtuple('Position', ['x', 'y'])



@dataclass
class Station:  
    """Representa un node del graf. Estacions de metro."""
    name: TypeAlias = str
    line: TypeAlias = str
    order: TypeAlias = int
    position: TypeAlias = Position


@dataclass
class Access:
    """Representa un node del graf. Accessos a les estacions de metro."""
    name_access: TypeAlias = str
    name_station: TypeAlias = str
    line: TypeAlias = str
    accessibility: TypeAlias = str
    position: TypeAlias = Position


# encara NO definit
@dataclass
class Tram:  # aresta del graf
    line: TypeAlias = str
    distance: TypeAlias = float
    color: TypeAlias = str


# encara NO definit
@dataclass
class Enllac:  # aresta del graf
    distance: TypeAlias = float
    color: TypeAlias = str


# @dataclass
# class Access:  # aresta del graf


Stations: TypeAlias = List[Station]

Accesses: TypeAlias = List[Access]

MetroGraph: TypeAlias = nx.Graph


def read_stations() -> Stations:
    """Llegeix un fitxer csv amb la informació requerida de les estacions de metro de Barcelona i en retorna una llista."""

    taula_dades = pandas.read_csv("estacions_linia.csv", usecols = ["NOM_ESTACIO", "NOM_LINIA", "ORDRE_ESTACIO", "GEOMETRY"], keep_default_na = False, dtype={"NOM_ESTACIO": str, "NOM_LINIA": str, "ORDRE_ESTACIO": int, "GEOMETRY": str})
    stations = []

    for i, row in taula_dades.iterrows():
        p = row["GEOMETRY"].strip('POINT( )').split() # type: List[int]
        station = Station(row["NOM_ESTACIO"], row["NOM_LINIA"], row["ORDRE_ESTACIO"], Position(p[0], p[1]))
        stations.append(station)
        
    return stations


def read_accesses() -> Accesses:
    """Llegeix un fitxer csv amb la informació requerida dels accessos de metro de Barcelona i en retorna una llista."""

    taula_accessos = pandas.read_csv("accessos_estacio_linia.csv", usecols = ['NOM_ACCES', 'NOM_ESTACIO', 'NOM_LINIA', 'NOM_TIPUS_ACCESSIBILITAT', 'GEOMETRY'], keep_default_na=False, dtype = {"NOM_ACCES": str, "NOM_ESTACIO": str, "NOM_LINIA": str, "NOM_TIPUS_ACCESSIBILITAT": str, "GEOMETRY": str})
    accesses = []

    for i, row in taula_accessos.iterrows():
        p = row['GEOMETRY'].strip('POINT ( )').split()  # type List[str]
        access = Access(row['NOM_ACCES'], row['NOM_ESTACIO'], row['NOM_LINIA'], row['NOM_TIPUS_ACCESSIBILITAT'], Position(p[0], p[1]))
        accesses.append(access)

    return accesses


def get_metro_graph() -> MetroGraph:
    """Genera el graf amb nodes estacions i accessos als metros i amb les arestes requerides."""
    
    G = nx.Graph() 

    # versió 1: fem servir un diccionari 
    Dict = {} # type: Dict[str, List[int]]
    # ESTACIONS:
    stations = read_stations()
    # nodes
    for i in range(len(stations)):
        s = stations[i] # els assignem un identificador i, ja que vàries estacions tenen el mateix nom tot i ser de línies diferents
        G.add_node(i, name = s.name, line = s.line, order = s.order, position = s.position)
        
        if s.name in Dict.keys():
            Dict[s.name].append(i)
        else:
            Dict[s.name] = [i]

    # arestes
    llista = [(i-1, i) for i in range(1, len(stations)) if stations[i-1].line == stations[i].line]
    G.add_edges_from(llista)
    
    # ACCESSOS:
    accesses = read_accesses()
    # nodes
    for a in accesses:
        G.add_node(a.name_access, station_name = a.name_station, line = a.line, accessibility = a.accessibility, position = a.position)            
        # arestes
        for i in Dict[a.name_station]:
            G.add_edge(i, a.name_access)

    return G


def show(g: MetroGraph) -> None:
    """Mostra el graf amb els nodes de metros i accesos de la ciutat i les seves arestes."""
    nx.draw(g, pos = nx.get_node_attributes(g, 'position'))
    plt.show()



# desa el graf com a imatge amb el mapa de la ciutat com a fons en l'arxiu especificat a filename
# usar staticmaps
def plot(g: MetroGraph, filename: str) -> None:
    m = StaticMap(width = 100000, height= 75000, url_template = filename)



g = get_metro_graph()
# print(nx.number_of_nodes(g))
show(g)