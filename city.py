# Haurem de settejar els atributs de les edges


# El primer cop que es demani el graf de carrers l'obtindrem a través d'osmnx i l'enmagatzemarem en un fitxer. Si es demana un altre cop pel graf, l'obtindrem llegint el fitxer a on estan les seves dades. 
# funcions estan mig fetes ja


# FA FALTA IMPORTAR LLIBRERIES?

# import pandas  # llegir fitxers csv
# from dataclasses import dataclass  # dataclasses
# from typing_extensions import TypeAlias
# from typing import Optional, TextIO, List  # typing
# from collections import namedtuple  # generar tuples
# import networkx as nx  # generar graf
from metro import *
import osmnx as ox
import os
import pickle  # per guardar graf osmnx en un fitxer i no haver de crearlo cada cop

CityGraph: TypeAlias = nx.Graph

OsmnxGraph: TypeAlias = nx.MultiDiGraph

fn = "barcelona.grf"

# MÈTODE 1

def get_osmnx_graph() -> OsmnxGraph:
    return load_osmnx_graph(fn)
        
def save_osmnx_graph(g: OsmnxGraph, filename: str) -> None:
    """ens guarda el graf a un file"""
    # guarda el graf g al fitxer filename

     # wb es igual a write in binary format
    pickle_out = open(filname, 'wb')
    pickle.dump(g, pickle_out)
    pickle_out.close()


def load_osmnx_graph(filename: str) -> OsmnxGraph:

    if not os.path.exists(filename):
       # descargar graf dels carrers de barcelona
        bcn_graph = ox.graph_from_place('Barcelona', network_type='walk', simplify=True)
        save_osmnx_graph(bcn_graph, filename)
        return bcn_graph
    # rb es igual a read in binary format
    """ens retorna el graf guardat a filename"""
    pickle_in = open(filname, "rb")
    bcn_streets = pickle.load(pickle_in)
    return bcn_streets
    """ retorna el graf. si ja existia, el retorna, sinó, el loadeja i el retorna """
    

# MÈTODE 2

# def get_osmnx_graph() -> OsmnxGraph:
#     """Obté el graf dels carrers de Barcelona de la web mitjançant osmnx."""
#     return ox.graph_from_place('Barcelona', network_type='walk', simplify=True)
        
# def save_osmnx_graph(g: OsmnxGraph, filename: str) -> None:
#     """Ens guarda el graf de carrers al fitxer de nom filename per poder-hi accedir futurament sense carregar-lo constantment de la web."""

#     pickle_out = open(filname, 'wb')
#     pickle.dump(g, pickle_out)
#     pickle_out.close()


# def load_osmnx_graph(filename: str) -> OsmnxGraph:
#     """Retorna el graf de carrers. En cas que és el primer cop que intentem accedir a aquest graf, 
#       se'l descarrega de la web, sinó accedeix al fitxer de nom filename on està guardat."""

#     if not os.path.exists(filename):
#         bcn_streets = get_osmnx_graph()
#         save_osmnx_graph(bcn_graph, filename)
#         return bcn_streets
#     pickle_in = open(filname, "rb")
#     bcn_streets = pickle.load(pickle_in)
#     return bcn_streets
   

def build_city_graph(g1: OsmnxGraph, g2: MetroGraph) -> CityGraph: ...
# retorna un graf fusió de g1 i g2 de tipus CityGraph. Transferirem tots els nodes i arestes del graf g2 a g1 i després seleccionarem les que necessitem (i filtrant també la informació que requerim)
# del graf g1.
    city_graph = nx.Graph()                     # type = CityGraph
 # NO, fer servir mètode de la unió.
 
    # city_graph.add_nodes_from(g2)               # hi afegim els nodes del graf g2
    # city_graph.add_edges_from(g2.edges)         # hi afegim les arestes del graf g2
    # city_graph.add_nodes_from(g1)               # hi afegim els nodes del graf g1

    # afegir les arestes del graf g1:
    for u, nbrsdict in g.adjacency():
    # for each adjacent node v and its (u, v) edges' information ...
        for v, edgesdict in nbrsdict.items():
            # print('   ', v)
            # EDITAR LA INFORMACIÓ DE L'ARESTA, ESBORRAR LA BIDIRECCIONALITAT.
            # osmnx graphs are multigraphs, but we will just consider their first edge
            eattr = edgesdict[0]    # eattr contains the attributes of the first edge
            # we remove geometry information from eattr because we don't need it and take a lot of space
            if 'geometry' in eattr:
                del(eattr['geometry'])
            print('        ', eattr)

     
    

# #
# #
# #
# # def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path: ...
# #
# #
# # NodeID: TypeAlias = Union[int, str]
# # Path: TypeAlias = List[NodeID]
# #
# #
# # def show(g: CityGraph) -> None: ...
# # # mostra g de forma interactiva en una finestra
# #
# #
# # def plot(g: CityGraph, filename: str) -> None: ...
# # # desa g com una imatge amb el mapa de la cuitat de fons en l'arxiu filename


# def plot_path(g: CityGraph, p: Path, filename: str, ...) -> None: ...
# # mostra el camí p en l'arxiu filename


# def save_osmnx_graph(g: OsmnxGraph, filename: str) -> None: ... 
#     # guarda el graf g al fitxer filename


# def load_osmnx_graph(filename: str) -> OsmnxGraph: ... 

#     if os.path.exists(filename):
#         return blah blah

#     # retorna el graf guardat al fitxer filename


# # g2 és el graf calculat a get_metro_graph()
# # s'han de fusionar aquest i el graf que es loadeja UNIÓ nodes STREET/STATION/ACCESS. UNIÓ arestes CARRER/ACCÉS/ENLLAÇ/TRAM com poden ser unhashable types nodes?? preguntar
# # S'ha de connectar cada accés amb node més proper de tipus street. Arestes de tipus Street.
# def build_city_graph(g1: OsmnxGraph, g2: MetroGraph) -> CityGraph




