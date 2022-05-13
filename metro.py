import pandas as pd                             # llegir fitxers csv
from dataclasses import dataclass               # dataclasses
from typing_extensions import TypeAlias         # typing
from typing import Optional, TextIO, List       # typing
from collections import namedtuple              # generar tuples (Coord)
import networkx as nx                           # generar graf
import matplotlib.pyplot as plt                 # plotejar mapa
from staticmap import StaticMap, Line, CircleMarker                   # plotejar mapa
from haversine import haversine

# falta typealias
Coord = namedtuple('Coord', ['x', 'y']) # (longitude, latitude)


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

    taula_dades = pd.read_csv("estacions_linia.csv", usecols=["NOM_ESTACIO", "NOM_LINIA", "GEOMETRY", "COLOR_LINIA"], keep_default_na=False, dtype={
                                  "NOM_ESTACIO": str, "NOM_LINIA": str, "GEOMETRY": str, "COLOR_LINIA": str})
    
    stations = []
    for i, row in taula_dades.iterrows():
        p = row["GEOMETRY"].strip('POINT( )').split()  # type: List[int]
        s = Station(row["NOM_ESTACIO"], row["NOM_LINIA"], Coord(float(p[0]), float(p[1])), '#' + row["COLOR_LINIA"])
        stations.append(s)

    return stations


# Pre: tenir el fitxer csv accessos_estacio_linia.csv
def read_accesses() -> Accesses:
    """Llegeix un fitxer csv amb la informació requerida dels accessos de metro de Barcelona i en retorna una llista d'aquests."""

    taula_accessos = pd.read_csv("accessos_estacio_linia.csv", usecols=['NOM_ACCES', 'NOM_ESTACIO', 'NOM_LINIA', 'GEOMETRY'], keep_default_na=False, dtype={
                                     "NOM_ACCES": str, "NOM_ESTACIO": str, "NOM_LINIA": str, "GEOMETRY": str})
    
    accesses = []
    for i, row in taula_accessos.iterrows():
        p = row['GEOMETRY'].strip('POINT ( )').split()  # type: List[str]
        a = Access(row['NOM_ACCES'], row['NOM_ESTACIO'], row['NOM_LINIA'], Coord(float(p[0]), float(p[1])), 'black')
        accesses.append(a)

    return accesses


def get_metro_graph() -> MetroGraph:
    """Genera el graf amb nodes Estacions i Accessos als metros i amb les arestes requerides entre aquests.
    A cada node li és assignat un identificador i uns atributs que n'especifiquen el tipus i tota la informació requerida.
    Les arestes també tenen un atribut amb la informació del seu tipus."""

    G = nx.Graph()
    
    stations, accesses = read_stations(), read_accesses()
    s, a = stations[0], accesses[0]

    n, m = len(stations), len(accesses)
    G.add_node(0, tipus = "station", name = s.name, position = s.coord, color = s.color)
    G.add_node(n, tipus = "access", name = (a.name_access, a.name_station), position = a.coord, color = a.color)
    G.add_edge(0, n, tipus = "access", time = set_time(haversine(s.coord, a.coord)), color = "black")
    
    j = 1
    for id in range(1, n):
        s, a = stations[id], accesses[j]
        G.add_node(id, tipus = "station", name = s.name, position = s.coord, color = s.color)
        while a.name_station == s.name:
            G.add_node(j + n, tipus = "access", name = (a.name_access, a.name_station), position = a.coord, color = a.color)
            G.add_edge(j + n, id, tipus = "access", time = set_time(haversine(s.coord, a.coord)), color = "black")
            j += 1
            if j < m:
              a = accesses[j]
            else:
              break
        
        if s.line == stations[id-1].line:

            G.add_edge(id, id-1, tipus = "tram", time = set_time(haversine(s.coord, stations[id-1].coord)), color = s.color)

    return G


def get_node_colors(g: MetroGraph):
    dict_colors = nx.get_node_attributes(g, 'color')
    list_colors = []
    for a in dict_colors:
        list_colors.append(dict_colors[a])
    return list_colors

def get_edge_colors(g: MetroGraph):
    dict_colors = nx.get_edge_attributes(g, 'color')
    list_colors = []
    for a in dict_colors:
        list_colors.append(dict_colors[a])
    return list_colors


def show(g: MetroGraph) -> None:
    """Mostra el graf amb nodes les estacions de metro i els accesos a aquestes de la ciutat i les seves arestes corresponents."""

    nx.draw(g, pos=nx.get_node_attributes(g, 'position'), node_size=10, node_color=get_node_colors(g), width = 2, edge_color = get_edge_colors(g))
    plt.show()


# desa el graf com a imatge amb el mapa de la ciutat com a fons en l'arxiu especificat a filename
# usar staticmaps
def plot(g: MetroGraph, filename: str) -> None:
    m = StaticMap(1200, 800, 10)
    for u in g.nodes:
        coordinate_u = g.nodes[u]['position']
        color = g.nodes[u]['color']
        marker = CircleMarker(coordinate_u, color, 10)
        m.add_marker(marker)
    for v in g.edges:
        coordinate_v = g.nodes[v[0]]['position']
        coordinate_u = g.nodes[v[1]]["position"]

        line = Line({coordinate_u, coordinate_v}, color, 5)
        m.add_line(line)

    image = m.render()
    image.save(filename)

