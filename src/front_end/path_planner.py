
import planning

planner = planning.PathPlanning()
def plan_route(start, destination, settings):
    print("planning path")
    path = planner.plan(start["coords"], destination["coords"], settings)

    return {"route_segments":path}
