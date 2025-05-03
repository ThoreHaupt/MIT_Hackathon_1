import math
from datetime import datetime

import osmnx as ox
import pickle

from planning.customPathPlanner import CustomPathPlanner
from scraping import scraper_api
from scipy.spatial import cKDTree

from scraping.ship_data import scrape_ship_traffic
from scraping import see_rout_v2


class PathPlanning:
    def __init__(self):
        self.graph = None
        self.planner = None
        self.customID = 1e9

        self.loadRoadGraph("/media/nils/Nils_Data/MIT-Hackathon/road_graph_autobahn_cleared.pkl")
        self.idxs = [n for n in self.graph]
        self.roadTree = cKDTree([(self.graph.nodes[n]["x"],self.graph.nodes[n]["y"]) for n in self.graph])

        self.appendAirRoutes()
        self.appendSeaRoutes()

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
            outgoingFlights = flights[flights['Dept Station'] == airport]
            for index, row in outgoingFlights.iterrows():
                if row['Arr Station'] not in matchedNodes:
                    coordinates = airports[row['Arr Station']]
                    self.graph.add_node(self.customID, x=coordinates[1], y=coordinates[0])
                    otherNode = self.graph.nodes[self.customID]
                    self.customID += 1

                attrs = {
                    "type": "Plane",
                    "startTime": row["ETD (Zulu)"],
                    "endTime": row["ETA (Zulu)"],
                    "length": math.dist((self.graph.nodes[matchedNodes[i]]["x"],self.graph.nodes[matchedNodes[i]]["y"]),
                                        (otherNode["x"],otherNode["y"]))
                }

                self.graph.add_edge(matchedNodes[i], self.customID-1, **attrs)

    def appendSeaRoutes(self):
        ports = scrape_ship_traffic.get_mock_data()

        flights = scraper_api.get_flights()
        matchedPorts = []
        matchedNodes = []

        for port in ports:
            coordinates = (port.latitude, port.longitude)
            dist, idx = self.roadTree.query([coordinates[1], coordinates[0]])
            if dist > 0.01:
                continue
            matchedPorts.append(port.name)
            matchedNodes.append(self.idxs[idx])

        for startPoint in [x for x in ports if x.name == "Hamburg"]:
            p = [x for x in ports if x != startPoint][0]
            endpoint = (p.latitude, p.longitude)
            prev = (startPoint.latitude, startPoint.longitude)
            if startPoint.name not in matchedPorts:
                self.graph.add_node(self.customID, x=prev[1], y=prev[0])
                othernode = self.customID
                self.customID += 1
            else:
                othernode= matchedNodes[matchedPorts.index(startPoint.name)]

            for routePoint in see_rout_v2.getRouteHamburgBoston():
                attrs = {
                    "type": "Ship",
                    "length": math.dist((prev[0], prev[1]), (routePoint[0], routePoint[1])),
                    "maxspeed": 40
                }
                self.graph.add_node(self.customID, x=routePoint[1], y=routePoint[0])
                otherNode2 = self.customID
                self.customID += 1

                self.graph.add_edge(othernode, otherNode2, **attrs)
                prev = routePoint
                othernode = otherNode2
            attrs = {
                "type": "Ship",
                "length": math.dist((prev[0], prev[1]), (endpoint[0], endpoint[1])),
                "maxspeed": 40
            }
            self.graph.add_node(self.customID, x=endpoint[1], y=endpoint[0])
            otherNode = self.customID
            self.customID += 1

            self.graph.add_edge(otherNode2, otherNode, **attrs)



    def plan(self, origin, destination):

        start = ox.nearest_nodes(self.graph, origin[1], origin[0])
        end  = ox.nearest_nodes(self.graph, destination[1], destination[0])

        path = self.planner.calculate_path(start, end)



        return path

