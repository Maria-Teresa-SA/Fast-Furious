import pandas as pd                             # llegir fitxers csv
from dataclasses import dataclass               # dataclasses
from typing_extensions import TypeAlias         # typing
from typing import Optional, TextIO, List       # typing
from collections import namedtuple              # generar tuples (Coord)
import networkx as nx                           # generar graf
import matplotlib.pyplot as plt                 # plotejar mapa
from staticmap import StaticMap, Line, CircleMarker                   # plotejar mapa

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
    Dict = {}  # type: Dict[str, List[int]]
    # el diccionari tindrà unes 150/160 entrades. Mida petita.
   
    # ESTACIONS
    stations = read_stations()

    s = stations[0]
    G.add_node(0, tipus = "station", name= s.name, x = s.coord.x, y = s.coord.y, color = s.color)
    Dict[stations[0].name] = [0]

    for id in range(1, len(stations)):
        s = stations[id]
        G.add_node(id, tipus = "station", name= s.name, x = s.coord.x, y = s.coord.y, color = s.color)
        
        
        if s.name in Dict:
            Dict[s.name].append(id)
        else:
            Dict[s.name] = [id]
        
        if s.line == stations[id-1].line:
          G.add_edge(id, id-1, tipus = "tram")


    # ACABAR DE MIRAR BÉ TEMA ACCESSOS: HI HA DIFERENTS  ACCESSOS PER LÍNIA??? LES LÍNIES QUE COMPARTEIXEN PARADA ESTAN CONNECTADES, AIXÍ QUE EN PRINCIPI NO HAURIA DE FER FALTA.
    # ES POT LLEGIR TOT ALESHORES DE FORMA LINIAL?? TÉ PINTA.
    # MIRAR COM VOLEM AFEGIR ELS NODES I LES ARESTES REALMENT AL GRAF. NO TOTES LES ARESTES PODEN PESAR EL MATEIX.

    # ACCESSOS:
    accesses = read_accesses()
    # nodes
    # print(Dict)
    for i in range(0, len(accesses)):
        id = i + len(stations)
        a = accesses[i]
        G.add_node(id, tipus = "access", name = (a.name_access, a.name_station), x = a.coord.x, y = a.coord.y, color = a.color)
        llista = Dict[a.name_station]
        for j in llista:
            G.add_edge(j, id, tipus = "access")

    return G


# NO HAURIA DE FER FALTA AQUESTA FUNCIÓ SI ELS NODES TENEN UN ATRIBUT QUE ES DIU COLOR
# def _assign_color(i) -> str:
#     """Assigna un color a cada línia de metro"""

#     # estaria bé fer-ho amb el nom de la línia i assignar-li el color real del metro de barcelona
#     if i < 30:
#         return 'red'
#     elif i < 48:
#         return 'cyan'
#     elif i < 74:
#         return 'green'
#     elif i < 96:
#         return 'black'
#     elif i < 123:
#         return 'purple'
#     elif i < 132:
#         return 'grey'
#     elif i < 147:
#         return 'orange'
#     elif i < 153:
#         return 'brown'
#     elif i < 164:
#         return 'yellow'
#     elif i < 169:
#         return 'black'
#     return 'pink'


# def get_colors(g: MetroGraph):
#     dict_colors = nx.get_node_attributes(g, 'color')
#     list_colors = []
#     for a in dict_colors:
#         list_colors.append(dict_colors[a])
#     return list_colors


def show(g: MetroGraph) -> None:
    """Mostra el graf amb nodes les estacions de metro i els accesos a aquestes de la ciutat i les seves arestes corresponents."""

    nx.draw(g, pos=nx.get_node_attributes(g, 'coord'), node_size=50, node_color=nx.get_node_attributes(g, 'color'))
    plt.show()


# desa el graf com a imatge amb el mapa de la ciutat com a fons en l'arxiu especificat a filename
# usar staticmaps
def plot(g: MetroGraph, filename: str) -> None:
    m = StaticMap(1200, 800, 10)
    for u in g.nodes:
        inf = g.nodes[u]["info"]
        coordinate_u = inf.coord
        color = inf.color
        marker = CircleMarker(coordinate_u, color, 10)
        m.add_marker(marker)
        for v in g.adj[u]:
            coordinate_v = g.nodes[v]['position']
            line = Line({coordinate_u, coordinate_v}, color, 5)
            m.add_line(line)

    image = m.render()
    image.save(filename)


plot(get_metro_graph(), "bon_dia.png")
