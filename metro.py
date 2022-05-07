import pandas
from typing_extensions import TypeAlias
from dataclasses import dataclass
from typing import Optional, TextIO, List
from collections import namedtuple
import networkx as nx

# import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

#import staticmaps


# falta typealias
Position = namedtuple('Position', ['x', 'y'])


@dataclass
class Station:  # node del graf
    name: TypeAlias = str
    line: TypeAlias = str
    order: TypeAlias = int
    position: TypeAlias = Position


@dataclass
class Access:  # node del graf
    name_access: TypeAlias = str
    name_station: TypeAlias = str
    line: TypeAlias = str
    accessibility: TypeAlias = str
    position: TypeAlias = Position


@dataclass
class Tram:  # aresta del graf
    line: TypeAlias = str
    distance: TypeAlias = float
    color: TypeAlias = str


@dataclass
class Enllac:  # aresta del graf
    distance: TypeAlias = float
    color: TypeAlias = str


# @dataclass
# class Access:  # aresta del graf


Stations: TypeAlias = List[Station]

Accesses: TypeAlias = List[Access]


MetroGraph: TypeAlias = nx.Graph

# FALTA CANVIAR-HO --> NOU MAIL SILVIA


def read_stations() -> Stations:
    taula_dades = pandas.read_csv("estacions_linia.csv", usecols = ["NOM_ESTACIO", "NOM_LINIA", "ORDRE_ESTACIO", "GEOMETRY"], keep_default_na = False, dtype={"NOM_ESTACIO": str, "NOM_LINIA": str, "ORDRE_ESTACIO": int, "GEOMETRY": str})
    stations = []
    for i, row in taula_dades.iterrows():
        p = row["GEOMETRY"].strip('POINT( )').split() # type: List[int]
        ubi = Position(p[0], p[1])
        station = Station(row["NOM_ESTACIO"], row["NOM_LINIA"], row["ORDRE_ESTACIO"], ubi)
        stations.append(station)
        
    return stations


def read_accesses() -> Accesses:
    columnes_guardem = ['NOM_ACCES', 'NOM_ESTACIO',
                        'NOM_LINIA', 'NOM_TIPUS_ACCESSIBILITAT', 'GEOMETRY']
    taula_accessos = pandas.read_csv(
        "accessos_estacio_linia.csv", usecols=columnes_guardem, keep_default_na=False)
    ls = []
    for i, row in taula_accessos.iterrows():

        ubi = row['GEOMETRY'].strip('POINT ( )').split()  # type List[str]

        access = Access(row['NOM_ACCES'], row['NOM_ESTACIO'], row['NOM_LINIA'],
                        row['NOM_TIPUS_ACCESSIBILITAT'], Position(ubi[0], ubi[1]))
        ls.append(access)

    return ls


def get_metro_graph() -> MetroGraph:
    G = nx.Graph() 
    stations, accesos = read_stations(), read_accesses()
    dictionary = {}
    G.add_nodes_from([x for x in range(len(stations))])
    for i in range(len(stations)):
        dictionary[i] = stations[i]

    # G.add_nodes_from(accesos)
    llista = [(i-1, i) for i in range(1, len(stations)) if stations[i-1].line == stations[i].line]
    G.add_edges_from(llista)
    return G



def show(g: MetroGraph) -> None:
    nx.draw(g)
    plt.show()

    # desa el graf com a imatge amb el mapa de la ciutat com a fons en l'arxiu especificat a filename
    # usar staticmaps


def plot(g: MetroGraph, filename: str) -> None: ...


g = get_metro_graph()
# print(nx.number_of_nodes(g))
show(g)