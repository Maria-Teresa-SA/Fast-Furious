
from typing import List
from collections import namedtuple
import pandas 
from dataclasses import dataclass

Position = namedtuple('Position', ['x', 'y'])

@dataclass
class Station:
    nom: str
    linia: str
    ubi: Position
    
Stations = List[Station]

def read_stations() -> Stations:
    taula_dades = pandas.read_csv("estacions.csv", usecols = ["NOM_ESTACIO", "PICTO", "GEOMETRY"], keep_default_na = False, dtype={})
    stations = []
    for i, row in taula_dades.iterrows():
        
        # first approach
        a = row["PICTO"][1:] # type: str
        lines = []
        nova_estacio = row["PICTO"][0]
        for char in a:
            if char == 'L':
                lines.append(nova_estacio)
                nova_estacio = 'L'
            elif char == 'F':
                lines.append(nova_estacio)
                nova_estacio = 'F'
            else:
                nova_estacio += char 
        lines.append(nova_estacio)


        for line in lines:
            p = row["GEOMETRY"].strip('POINT( )').split() # type: List[int]
            ubi = Position(p[0], p[1])
            station = Station(row["NOM_ESTACIO"], line, ubi)
            stations.append(station)
        
    return stations

stations = read_stations()
for station in stations:
    if station.nom == 'La Sagrera':
        print(station)

