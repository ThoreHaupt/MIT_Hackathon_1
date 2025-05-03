import planning
import osmnx as ox


if __name__ == "__main__":
    planner = planning.PathPlanning()
    print("planning path")
    path = planner.plan((8.421517, 49.016828), (13.400381, 52.518980))
    print(path)
