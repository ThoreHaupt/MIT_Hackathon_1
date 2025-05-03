import math

import osmnx as ox
import networkx as nx
import pickle
from pyrosm import OSM
#import pathPlanner
#import customPathPlanner
from scraping import scraper_api

class PathPlanning:
    def __init__(self):
        self.graph = None
        self.planner = None

        self.loadRoadGraph("/media/nils/Nils_Data/MIT-Hackathon/road_graph_cleared.pkl")
        self.appendAirRoutes()

    def loadRoadGraph(self, path):
        with open(path, "rb") as f:
            G = pickle.load(f)
        G.graph["crs"] = "EPSG:4326"
        self.graph = G

    def appendAirRoutes(self):
        airports = scraper_api.get_airports()
        for key in airports:
            coordinates = airports[key]
            node = ox.nearest_nodes(self.graph, coordinates[0], coordinates[1])
            dist = math.dist(coordinates, (node["x"], node["y"]))
            print(dist)
            if dist > 100:
                continue



