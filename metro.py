import pandas as pd                                                   # llegir fitxers csv
from dataclasses import dataclass                                     # dataclasses
from typing_extensions import TypeAlias                               # typing
from typing import Optional, TextIO, List                             # typing
from collections import namedtuple                                    # generar tuples (Coord)
import networkx as nx                                                 # generar graf
import matplotlib.pyplot as plt                                       # plotejar mapa
from staticmap import StaticMap, Line, CircleMarker                   # plotejar mapa
from haversine import haversine, Unit                                 # calcular distàncies entre coordenades


######################
#   Tipus de dades   #
######################

Coord: TypeAlias = namedtuple('Coord', ['long', 'lat']) # (longitude, latitude)

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
    coord: TypeAlias = Coord            # coordenades de l'accés
    color: TypeAlias = str              # color del node


Stations: TypeAlias = List[Station]

Accesses: TypeAlias = List[Access]

MetroGraph: TypeAlias = nx.Graph


#############################
#  Funcions implementades   #
#############################


#####################
#  Lectura de dades #
#####################

# Pre: tenir el fitxer csv estacions_linia.csv
def read_stations() -> Stations:
    """Llegeix un fitxer csv amb la informació requerida de les estacions de metro de Barcelona i en retorna una llista d'aquestes."""

    cols = ["NOM_ESTACIO", "NOM_LINIA", "GEOMETRY", "COLOR_LINIA"] # columnes que guardem
    data_table_stations = pd.read_csv("estacions_linia.csv", usecols = cols, keep_default_na=False, dtype={cols[0]: str, cols[1]: str, cols[2]: str, cols[3]: str})
    
    stations = []
    for i, row in data_table_stations.iterrows():
        p = row["GEOMETRY"].strip('POINT( )').split()
        s = Station(row["NOM_ESTACIO"], row["NOM_LINIA"], Coord(float(p[0]), float(p[1])), '#' + row["COLOR_LINIA"])
        stations.append(s)

    return stations


# Pre: tenir el fitxer csv accessos_estacio_linia.csv
def read_accesses() -> Accesses:
    """Llegeix un fitxer csv amb la informació requerida dels accessos de metro de Barcelona i en retorna una llista d'aquests."""

    cols = ['NOM_ACCES', 'NOM_ESTACIO', 'NOM_LINIA', 'GEOMETRY'] #columnes que guardem
    data_table_accesses = pd.read_csv("accessos_estacio_linia.csv", usecols=cols, keep_default_na=False, dtype={cols[0]: str, cols[1]: str, cols[2]: str, cols[3]: str})
    
    accesses = []
    for i, row in data_table_accesses.iterrows():
        p = row['GEOMETRY'].strip('POINT ( )').split()  # type: List[str]
        a = Access(row['NOM_ACCES'], row['NOM_ESTACIO'], Coord(float(p[0]), float(p[1])), 'black')
        accesses.append(a)

    return accesses


##################
#   Graf metro   #
##################

# Pre: el tipus és "Street", "Tran", "Access" o "Transfer" i la distància està en metres
def set_time(dtype: str, dist: float) -> float:
    """Funció que retorna el temps que es triga en recórrer una distància (d'un graf) depenent del tipus d'aresta (Street, Tram, Enllaç, Accés).
    
    Velocitat mitja caminant -> 5km/h = 83 m/min
    Velocitat mitja en metro -> 26 km/h = 433.3 m/min
    Accessos -> 2.5 min d'espera més 3km/h velocitat d'escales = 2.5 + 50m/min
    Enllaços -> 2.5 minuts d'espera més 4km/h = 2.5 + 66.7 m/min
    """

    if dtype == "Street": return dist/83
    elif dtype == "Tram": return dist/433.3
    elif dtype == "Access": return dist/50
    elif dtype == "Transfer": return 2.5 + dist/66.7


def get_metro_graph() -> MetroGraph:
    """Genera el graf amb nodes Estacions i Accessos als metros i les arestes requerides entre aquests.
    A cada node li és assignat un identificador i uns atributs que n'especifiquen el tipus i tota la informació necessària (ex. posició).
    Les arestes també tenen un atribut amb la informació del seu tipus, el temps que es triga en ser recorregudes i el seu color.
    """

    G = nx.Graph()
    
    stations, accesses = read_stations(), read_accesses()
    n, m = len(stations), len(accesses)    
    repeated_stations = {} # type = Dict[str, List[int]]
    # diccionari que ens connectarà amb un Enllaç els nodes estació que comparteixen parada però no línia.
    j = 0

    for id in range(n):
        s = stations[id]

        # afegir estacions de metro (NODES)
        G.add_node(id, dtype = "Station", name = s.name, position = s.coord, color = s.color, line=s.line)
        
        # afegir enllaços de metro (ARESTES)
        if s.name in repeated_stations.keys():
            for s2 in repeated_stations[s.name]:
                G.add_edge(id, s2, dtype = "Transfer", time = set_time("Transfer", haversine(s.coord, G.nodes[s2]["position"], unit=Unit.METERS)), color = "black")
            repeated_stations[s.name].append(id)
        else: repeated_stations[s.name] = [id]

        # afegir accessos a l'estació (NODES I ARESTES)
        while j < m:
            a = accesses[j]
            if a.name_station == s.name:
                G.add_node(j + n, dtype = "Access", name = (a.name_access, a.name_station), position = a.coord, color = a.color)
                G.add_edge(j + n, id, dtype = "Access", time = set_time("Access", haversine(s.coord, a.coord, unit=Unit.METERS)), color = "black")
                j += 1
            else: break    
        
        # afegir trams de metro
        if id < n and s.line == stations[id-1].line:
            G.add_edge(id, id-1, dtype = "Tram", time = set_time("Tram", haversine(s.coord, stations[id-1].coord, unit=Unit.METERS)), color = s.color)

    return G


#################
#   Imatges     #
#################

# pre: nodes de g tenen atribut color
def get_node_colors(g: MetroGraph):
    """Traspassa la informació guardada en un diccionari de colors a una llista de colors per pintar els nodes al mapa.
    Aquest diccionari s'obté de l'atribut color guardat al graf g."""

    dict_colors = nx.get_node_attributes(g, 'color')
    return [dict_colors[x] for x in dict_colors]


# pre: arestes de g tenen atribut color
def get_edge_colors(g: MetroGraph):
    """Traspassa la informació guardada en un diccionari de colors a una llista de colors per pintar les arestes al mapa.
    Aquest diccionari s'obté de l'atribut color guardat al graf g."""
    
    dict_colors = nx.get_edge_attributes(g, 'color')
    return [dict_colors[x] for x in dict_colors]


def show(g: MetroGraph) -> None:
    """Mostra el graf amb les estacions de metro i els accesos a aquestes com a nodes i les seves arestes corresponents."""

    nx.draw(g, pos=nx.get_node_attributes(g, 'position'), node_size=10, node_color=get_node_colors(g), width = 2, edge_color = get_edge_colors(g))
    plt.show()


# desa el graf com a imatge amb el mapa de la ciutat com a fons en l'arxiu especificat a filename
# usar staticmap
def plot(g: MetroGraph, filename: str) -> None:
    """Guarda al fitxer "filename" un plot del graf de metros amb la ciutat de Barcelona de fons. S'usa staticmap."""

    m = StaticMap(1200, 800, 10)
    for u in g.nodes:
        coordinate_u = g.nodes[u]['position']
        color = g.nodes[u]['color']
        marker = CircleMarker(coordinate_u, color, 10)
        m.add_marker(marker)
    for v in g.edges:
        coordinate_v, coordinate_u = g.nodes[v[0]]['position'], g.nodes[v[1]]["position"]
        line = Line({coordinate_u, coordinate_v}, color, 5)
        m.add_line(line)

    image = m.render()
    image.save(filename)

