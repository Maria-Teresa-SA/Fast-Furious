from metro import *
import osmnx as ox
import os
import pickle                       # per guardar graf osmnx en un fitxer i no haver de baixar-lo cada cop. Serveix també per obrir el fitxer amb el graf quan ja ha set descarregat.

CityGraph: TypeAlias = nx.Graph

OsmnxGraph: TypeAlias = nx.MultiDiGraph


def get_osmnx_graph() -> OsmnxGraph:
    """Obté el graf dels carrers de Barcelona de la web mitjançant osmnx."""
    return ox.graph_from_place('Barcelona', network_type='walk', simplify=True)
        
def save_osmnx_graph(g: OsmnxGraph, filename: str) -> None:
    """Ens guarda el graf de carrers al fitxer de nom filename per poder-hi accedir futurament sense carregar-lo constantment de la web."""

    pickle_out = open(filename, 'wb')
    pickle.dump(g, pickle_out)
    pickle_out.close()


def load_osmnx_graph(filename: str) -> OsmnxGraph:
    """Retorna el graf de carrers. En cas que és el primer cop que intentem accedir a aquest graf, 
      se'l descarrega de la web, sinó accedeix al fitxer de nom filename on està guardat."""

    if not os.path.exists(filename):
        bcn_streets = get_osmnx_graph()
        save_osmnx_graph(bcn_graph, filename)
        return bcn_streets
    pickle_in = open(filename, "rb")
    bcn_streets = pickle.load(pickle_in)
    return bcn_streets
   

def build_city_graph(g1: OsmnxGraph, g2: MetroGraph) -> CityGraph: 
    """Retorna un graf fusió del graf de Barcelona (carrers) i el graf de metros. Primer recorrem el primer 
    graf afegint al nostre graf de carrers tots els nodes, arestes i informació rellevant.
    Després fem la unió amb el graf g2 i en retornem el resultat"""
    
    city_graph = nx.Graph()                     # type = CityGraph

    # for each node and its neighbors' information
    for u, nbrsdict in g1.adjacency():
        
        city_graph.add_node(u, tipus = "street", position = Coord(g1.nodes[u]['x'], g1.nodes[u]['y']))  # Nota per L i S: x i y ja són floats així que no fa falta canviar el tipus   
        # for each adjacent node v and its (u, v) edges' information
        for v, edgesdict in nbrsdict.items():
                # osmnx graphs are multigraphs, but we will just consider their first edge
            eattr = edgesdict[0]    # eattr contains the attributes of the first edge
                # we remove geometry information from eattr because we don't need it and take a lot of space
            if 'geometry' in eattr:
                del(eattr['geometry'])
            # afegim una aresta entre u i v i hi associem tota la informació d'aquesta i el seu tipus.
            city_graph.add_edge(u, v, tipus = "enllaç", info = eattr)

    city_graph = nx.union(g2, city_graph)
    tipus = nx.get_node_attributes(g2, 'tipus') # diccionari amb els tipus
    list_x,list_y, list_a = [], [], []
    for i in g2.nodes:
        if tipus[i] == "access":
            coords = g2.nodes[i]["position"]
            list_x.append(coords.x)
            list_y.append(coords.y)
            list_a.append(i)
    
    nearest = ox.distance.nearest_nodes(g1, list_x, list_y)
    j = 0
    for i in list_a:
        coords = g2.nodes[i]["position"]
        city_graph.add_edge(i, nearest[j], tipus = "acces")
        j += 1
        
    return city_graph

H = build_city_graph(load_osmnx_graph("barcelona.grf"),  get_metro_graph())
print(H.nodes())     

    

NodeID: TypeAlias = int
Path: TypeAlias = List[NodeID]                   # tots els nodes tenen identificadors enters

def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path:
  """Retorna el camí més curt des de les coordenades de sortida fins les coordenades destí.
  Utilitza l'OsmnxGraph per trobar l'ID del node més proper a aquestes coordenades i empra el
  city graph per calcular el camí més curt que les connecta."""


# alguna cosa falla aquí ahhh
  nearest_src = ox.distance.nearest_nodes(ox_g, src.x, src.y)
  nearest_dst = ox.distance.nearest_nodes(ox_g, dst.x, dst.y)
  return nx.shortest_path(g, nearest_src, nearest_dst)


# #
# # def show(g: CityGraph) -> None: ...
# # # mostra g de forma interactiva en una finestra
# #
# #
# # def plot(g: CityGraph, filename: str) -> None: ...
# # # desa g com una imatge amb el mapa de la cuitat de fons en l'arxiu filename


# def plot_path(g: CityGraph, p: Path, filename: str, ...) -> None: ...
# # mostra el camí p en l'arxiu filename





