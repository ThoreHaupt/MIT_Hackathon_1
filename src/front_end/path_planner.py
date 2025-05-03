
import planning


def plan_route(start, destination, settings):
    planner = planning.PathPlanning()
    print("planning path")
    path = planner.plan(start["coords"], destination["coords"])

    return {"route_segments":path}
