from metro import *
import osmnx as ox
import os
import pickle                       # per guardar graf osmnx en un fitxer i no haver de baixar-lo cada cop. Serveix també per obrir el fitxer amb el graf quan ja ha set descarregat.

CityGraph: TypeAlias = nx.Graph

OsmnxGraph: TypeAlias = nx.MultiDiGraph

NodeID: TypeAlias = int

Path: TypeAlias = List[NodeID]                   # tots els nodes tenen identificadors enters


def get_osmnx_graph() -> OsmnxGraph:
    """Obté el graf dels carrers de Barcelona de la web mitjançant osmnx."""

    graph = ox.graph_from_place('Barcelona', network_type = 'walk', simplify=True)
    
    # we remove geometry information from eattr because we don't need it and take a lot of space
    for u, v, key, geom in graph.edges(data = "geometry", keys = True):
        if geom is not None:
            del(graph[u][v][key]["geometry"])
    
    return graph
        
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
        save_osmnx_graph(bcn_streets, filename)
        return bcn_streets
    
    pickle_in = open(filename, "rb")
    bcn_streets = pickle.load(pickle_in)
    
    return bcn_streets
   

def build_city_graph(g1: OsmnxGraph, g2: MetroGraph) -> CityGraph: 
    """Retorna un graf fusió del graf de Barcelona (carrers) i el graf de metros. Primer recorrem el primer 
    graf afegint al nostre graf de carrers tots els nodes, arestes i informació rellevant.
    Després fem la unió amb el graf g2 i en retornem el resultat"""
    
    city_graph = nx.Graph()                     # type = CityGraph

    # PASSAR INFORMACIÓ DE GRAPH DE CARRERS A GRAPH DE LA CIUTAT

    # for each node and its neighbors' information
    for node, nbrs_dict in g1.adjacency(): 
        city_graph.add_node(node, tipus = "Street", position = Coord(g1.nodes[node]['x'], g1.nodes[node]['y']), color = "black" )  # Nota per L i S: x i y ja són floats així que no fa falta canviar el tipus   
        # for each adjacent node v and its (u, v) edges' information
        for nbr, edgesdict in nbrs_dict.items():
            # osmnx graphs are multigraphs, but we will just consider their first edge
            e_attrib = edgesdict[0]    # eattr contains the attributes of the first edge
            # afegim una aresta entre u i v i hi associem tota la informació d'aquesta i el seu tipus.
            city_graph.add_edge(node, nbr, tipus = "Street", color = "black", time = set_time("Street", e_attrib["length"]))
            # city_graph.add_edge(node, nbr, tipus = "street", color = "black", dist = e_attrib["length"])

    # UNIÓ AMB GRAPH DE METROS
    city_graph = nx.union(g2, city_graph)

    # AFEGIR ARESTES DE STREET - ACCÉS METRO - millorar
    tipus = nx.get_node_attributes(g2, 'tipus') # diccionari amb els tipus
    list_x,list_y, list_a = [], [], []
    for i in g2.nodes:
        if tipus[i] == "Access":
            coords = g2.nodes[i]["position"]
            list_x.append(coords.x)
            list_y.append(coords.y)
            list_a.append(i)
    
    nearest = ox.distance.nearest_nodes(g1, list_x, list_y)
    j = 0
    for i in list_a:
        coords = g2.nodes[i]["position"]
        city_graph.add_edge(i, nearest[j], tipus = "Street", color = "black", time=set_time("Street", haversine(city_graph.nodes[i]["position"], city_graph.nodes[nearest[j]]["position"])))
        j += 1
        
    city_graph.remove_edges_from(nx.selfloop_edges(city_graph))

    return city_graph


# RECORDEM QUE L'ESTRUCTURA DE COORD ÉS (longitud, latitud)
def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path:
  """Retorna el camí més curt des de les coordenades de sortida fins les coordenades destí.
  Utilitza l'OsmnxGraph per trobar l'ID del node més proper a aquestes coordenades i empra el
  city graph per calcular el camí més curt que les connecta."""

  nearest_src = ox.distance.nearest_nodes(ox_g, src.x, src.y)
  nearest_dst = ox.distance.nearest_nodes(ox_g, dst.x, dst.y)
  return nx.shortest_path(g, nearest_src, nearest_dst, weight="time")


def get_time_path(g: CityGraph, p: Path):
    time = 0
    for i in range(len(p)-1):
        time += g[p[i]][p[i+1]]["time"]
    return time

# SHOW TOT EL GRAPH
def show(g: CityGraph) -> None:
    nx.draw(g, pos=nx.get_node_attributes(g, 'position'), node_size=5, width=1,
            node_color=get_node_colors(g), edge_color=get_edge_colors(g))
    plt.show()


# PLOT DE TOT EL GRAPH
def plot(g: CityGraph, filename: str) -> None:
    m = StaticMap(1200, 800, 0)
    for u in g.nodes:
        coordinate_u = g.nodes[u]['position']
        color = g.nodes[u]['color']
        marker = CircleMarker(coordinate_u, color, 2)
        m.add_marker(marker)
    for v in g.edges:
        coordinate_u = g.nodes[v[0]]['position']
        coordinate_v = g.nodes[v[1]]['position']
        color = g.edges[v]['color']
        line = Line({coordinate_u, coordinate_v}, color, 1)
        m.add_line(line)

    image = m.render()
    image.save(filename)


# p path és una llista de nodes que tenen
def plot_path(g: CityGraph, p: Path, filename: str) -> None:
    m = StaticMap(1200, 800, 0)
    marker = CircleMarker(g.nodes[p[0]]["position"], g.nodes[p[0]]["color"], 10)
    m.add_marker(marker)
    marker = CircleMarker(g.nodes[p[-1]]["position"], g.nodes[p[-1]]["color"], 10)
    m.add_marker(marker)

    for i in range(len(p)-1):
        coord1 = g.nodes[p[i]]["position"]
        coord2 = g.nodes[p[i + 1]]["position"]
        if (g.nodes[p[i]]["tipus"] == "street"):
            color = "black"
        else:
            color = g[p[i]][p[i+1]]["color"]
        line = Line({coord1, coord2}, color, 5)
        m.add_line(line)

    image = m.render()
    image.save(filename)

