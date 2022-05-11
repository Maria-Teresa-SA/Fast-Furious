import pandas as pd                             # llegir fitxers csv
from dataclasses import dataclass               # dataclasses
from typing_extensions import TypeAlias         # typing
from typing import Optional, TextIO, List       # typing
from collections import namedtuple              # generar tuples (Coord)
import networkx as nx                           # generar graf
import matplotlib.pyplot as plt                 # plotejar mapa
import staticmaps                               # plotejar mapa

# falta typealias
Coord = namedtuple('Coord', ['x', 'y'])


@dataclass
class Station:
    """Infpormació associada a un node del graf de tipus Estacions de metro."""
    name: TypeAlias = str               # nom de l'estació
    line: TypeAlias = str               # línia de mtero
    coord: TypeAlias = Coord            # coordenades de l'estació
    color: TypeAlias = str              # color del node


@dataclass
class Access:
    """Informació associada a un node del graf de tipus Accessos a les estacions de metro."""
    name_access: TypeAlias = str        # nom de l'accés
    name_station: TypeAlias = str       # nom de l'estació associada a l'accés
    line: TypeAlias = str               # nom de la línia
    accessibility: TypeAlias = str      # accessibilitat, segurament informació inútil
    coord: TypeAlias = Coord            # coordenades de l'accés
    color: TypeAlias = str              # color del node


@dataclass
class Edge:
    tipus: str                          # pot ser de tipus tram // enllaç // accés 
    color: str                          # 
# falta acabar de definir-ne els atributs


Stations: TypeAlias = List[Station]

Accesses: TypeAlias = List[Access]

MetroGraph: TypeAlias = nx.Graph


# Pre: tenir el fitxer csv estacions_linia.csv
def read_stations() -> Stations:
    """Llegeix un fitxer csv amb la informació requerida de les estacions de metro de Barcelona i en retorna una llista d'aquestes."""

    taula_dades = pd.read_csv("estacions_linia.csv", usecols=["NOM_ESTACIO", "NOM_LINIA", "GEOMETRY"], keep_default_na=False, dtype={
                                  "NOM_ESTACIO": str, "NOM_LINIA": str, "GEOMETRY": str})
    
    stations = []
    for i, row in taula_dades.iterrows():
        p = row["GEOMETRY"].strip('POINT( )').split()  # type: List[int]
        s = Station(row["NOM_ESTACIO"], row["NOM_LINIA"], Coord(float(p[0]), float(p[1])), _assign_color(i))
        stations.append(s)

    return stations


# Pre: tenir el fitxer csv accessos_estacio_linia.csv
def read_accesses() -> Accesses:
    """Llegeix un fitxer csv amb la informació requerida dels accessos de metro de Barcelona i en retorna una llista d'aquests."""

    taula_accessos = pd.read_csv("accessos_estacio_linia.csv", usecols=['NOM_ACCES', 'NOM_ESTACIO', 'NOM_LINIA', 'NOM_TIPUS_ACCESSIBILITAT', 'GEOMETRY'], keep_default_na=False, dtype={
                                     "NOM_ACCES": str, "NOM_ESTACIO": str, "NOM_LINIA": str, "NOM_TIPUS_ACCESSIBILITAT": str, "GEOMETRY": str})
    
    accesses = []
    for i, row in taula_accessos.iterrows():
        p = row['GEOMETRY'].strip('POINT ( )').split()  # type: List[str]
        a = Access(row['NOM_ACCES'], row['NOM_ESTACIO'], row['NOM_LINIA'], row['NOM_TIPUS_ACCESSIBILITAT'], Coord(float(p[0]), float(p[1])), 'black')
        accesses.append(a)

    return accesses


def get_metro_graph() -> MetroGraph:
    """Genera el graf amb nodes Estacions i Accessos als metros i amb les arestes requerides entre aquests.
    A cada node li és assignat un identificador i uns atributs que n'especifiquen el tipus i tota la informació requerida.
    Les arestes també tenen un atribut amb la informació del seu tipus."""

    # G = nx.Graph()
    # Dict = {}  # type: Dict[str, List[int]]
    # # versió 1: fem servir un diccionari

    # # ESTACIONS:
    # stations = read_stations()
    # # nodes
    # for i in range(len(stations)):
    #     # els assignem un identificador i, ja que vàries estacions tenen el mateix nom tot i ser de línies diferents
    #     s = stations[i]
    #     G.add_node(i, station_name=s.name, line=s.line, coord=s.coord, color=s.color)

    #     if s.name in Dict.keys():
    #         Dict[s.name].append(i)
    #     else:
    #         Dict[s.name] = [i]

    # # arestes # FALTARÀ DEFINIR QUIN TIPUS D'EGE ÉS I BLAH BLAH
    # llista = [(i-1, i) for i in range(1, len(stations)) if stations[i-1].line == stations[i].line]
    # G.add_edges_from(llista)

    # # ACCESSOS:
    # accesses = read_accesses()
    # # nodes
    # for i in range(len(accesses)):
    #     a = accesses[i]
    #     G.add_node((a.name_access, i), station_name=a.name_station,
    #                line=a.line, coord=a.coord, color=a.color)
    #     # arestes
    #     llista = Dict[a.name_station]
    #     # print("1", a.name_access, "2", a.name_station,"3", llista)
    #     for j in llista:
    #         # FALTARÀ DEFINIR QUIN TIPUS D'EDGE ÉS
    #         G.add_edge(j, (a.name_access, i))


###################################################################################################################################################

    G = nx.Graph()
    Dict = {}  # type: Dict[str, List[int]]
   
    # ESTACIONS:
    stations = read_stations()
    n = len(stations)
    s = stations[0]
    G.add_node(0, tipus = "station", info = s, position = s.coord)
    Dict[stations[0].name] = [0]

    for i in range(1, n):
        s = stations[i]
        G.add_node(i, tipus = "station", info = s, position = s.coord)
        if s.name in Dict.keys():
            Dict[s.name].append(i)
        else:
            Dict[s.name] = [i]
        if s.line == stations[i-1].line:
          G.add_edge(i, i-1, tipus = "tram")

    # ACCESSOS:
    accesses = read_accesses()
    m = len(accesses)
    # nodes
    # print(Dict)
    for i in range(n, n + m):
        a = accesses[i - n]
        G.add_node(i, tipus = "access", info = a, position = a.coord)
        # arestes
        # print(a.name_access, a.name_station)
        llista = Dict[a.name_station]
        for j in llista:
            G.add_edge(j, i, tipus = "acces")

    return G


def _assign_color(i) -> str:
    """Assigna un color a cada línia de metro"""

    # estaria bé fer-ho amb el nom de la línia i assignar-li el color real del metro de barcelona
    if i < 30:
        return 'red'
    elif i < 48:
        return 'cyan'
    elif i < 74:
        return 'green'
    elif i < 96:
        return 'black'
    elif i < 123:
        return 'purple'
    elif i < 132:
        return 'grey'
    elif i < 147:
        return 'orange'
    elif i < 153:
        return 'brown'
    elif i < 164:
        return 'yellow'
    elif i < 169:
        return 'black'
    return 'pink'


def get_colors(g: MetroGraph):
    dict_colors = nx.get_node_attributes(g, 'color')
    list_colors = []
    for a in dict_colors:
        list_colors.append(dict_colors[a])
    return list_colors


def show(g: MetroGraph) -> None:
    """Mostra el graf amb nodes les estacions de metro i els accesos a aquestes de la ciutat i les seves arestes corresponents."""

    nx.draw(g, pos=nx.get_node_attributes(g, 'coord'), node_size=50, node_color=get_colors(g))
    plt.show()


# desa el graf com a imatge amb el mapa de la ciutat com a fons en l'arxiu especificat a filename
# usar staticmaps
def plot(g: MetroGraph, filename: str) -> None:
    m = StaticMap(width=100000, height=75000, url_template=filename)
