import math

import osmnx as ox
import pickle

from planning.customPathPlanner import CustomPathPlanner
from scraping import scraper_api
from scipy.spatial import cKDTree



class PathPlanning:
    def __init__(self):
        self.graph = None
        self.planner = None

        self.loadRoadGraph("/media/louis/T7/road_graph_autobahn_cleared.pkl")
        self.idxs = [n for n in self.graph]
        self.roadTree = cKDTree([(self.graph.nodes[n]["x"],self.graph.nodes[n]["y"]) for n in self.graph])

        self.appendAirRoutes()

        self.planner = CustomPathPlanner(self.graph)

    def loadRoadGraph(self, path):
        with open(path, "rb") as f:
            G = pickle.load(f)
        G.graph["crs"] = "EPSG:4326"
        self.graph = G

    def appendAirRoutes(self):
        airports = scraper_api.get_airports()

        flights = scraper_api.get_flights()
        matchedAirports = []
        matchedNodes = []

        for key in airports:
            coordinates = airports[key]
            dist, idx = self.roadTree.query([coordinates[1], coordinates[0]])
            if dist > 0.01:
                continue
            matchedAirports.append(key)
            matchedNodes.append(self.idxs[idx])

        for i, airport in enumerate(matchedAirports):
            for j, airport2 in enumerate(matchedAirports):
                outgoingFlights = flights[(flights['Dept Station'] == airport) & (flights['Arr Station'] == airport2)]
                for row in outgoingFlights.itertuples():
                    attrs = {
                        "type": "air",
                        "startTime": row["ETD (Zulu)"],
                        "endTime": row["ETA (Zulu)"],
                        "length": math.dist((self.graph.nodes[matchedNodes[i]]["x"],self.graph.nodes[matchedNodes[i]]["y"],
                                            (self.graph.nodes[matchedNodes[j]]["x"],self.graph.nodes[matchedNodes[j]]["y"])))
                    }
                    self.graph.add_edge(matchedNodes[i], matchedNodes[j], **attrs)

    def plan(self, origin, destination):

        start = ox.nearest_nodes(self.graph, origin[1], origin[0])
        end  = ox.nearest_nodes(self.graph, destination[1], destination[0])

        path = self.planner.calculate_path(start, end)



        return path

