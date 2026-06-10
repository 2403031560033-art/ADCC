import math
import uuid
from typing import List, Dict

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def create_data_model(warehouses, vehicles, priority_zones):
    data = {}
    
    locations = []
    # Index 0 to N-1: Warehouses
    for w in warehouses:
        locations.append({'id': w['warehouse_id'], 'lat': w['lat'], 'lon': w['lon'], 'type': 'warehouse'})
        
    # Index N to N+M-1: Zones
    for z in priority_zones:
        locations.append({'id': z['zone_id'], 'lat': z['lat'], 'lon': z['lon'], 'type': 'zone'})
        
    data['locations'] = locations
    
    # Compute distance matrix (in integers, scaled by 10)
    distance_matrix = []
    for from_node in locations:
        row = []
        for to_node in locations:
            dist = haversine(from_node['lat'], from_node['lon'], to_node['lat'], to_node['lon'])
            row.append(int(dist * 10))
        distance_matrix.append(row)
        
    data['distance_matrix'] = distance_matrix
    data['num_vehicles'] = len(vehicles)
    
    # Each vehicle starts and ends at its assigned warehouse
    starts = []
    ends = []
    for v in vehicles:
        base_id = v['base']
        w_idx = 0
        for i, w in enumerate(warehouses):
            if w['warehouse_id'] == base_id:
                w_idx = i
                break
        starts.append(w_idx)
        ends.append(w_idx)
        
    data['starts'] = starts
    data['ends'] = ends
    
    return data

def optimize_routes(warehouses: list, vehicles: list, priority_zones: list, blocked_zone_ids: list) -> List[Dict]:
    routes_output = []
    
    # Separate blocked zones for drones
    accessible_zones = [z for z in priority_zones if z['zone_id'] not in blocked_zone_ids]
    blocked_zones = [z for z in priority_zones if z['zone_id'] in blocked_zone_ids]
    
    for z in blocked_zones:
        # Find nearest warehouse
        best_w = None
        min_dist = 999999
        for w in warehouses:
            d = haversine(w['lat'], w['lon'], z['lat'], z['lon'])
            if d < min_dist:
                min_dist = d
                best_w = w
                
        if best_w:
            routes_output.append({
                "route_id": f"R-drone-{z['zone_id']}",
                "from_id": best_w['warehouse_id'],
                "to_id": z['zone_id'],
                "waypoints": [{"lat": best_w['lat'], "lon": best_w['lon']}, {"lat": z['lat'], "lon": z['lon']}],
                "distance_km": round(min_dist, 1),
                "eta_minutes": int((min_dist / 60.0) * 60), # 60 km/h drone speed
                "blocked": True,
                "via_drone": True
            })
            
    if not accessible_zones or not vehicles:
        return routes_output
        
    try:
        from ortools.constraint_solver import routing_enums_pb2
        from ortools.constraint_solver import pywrapcp
        data = create_data_model(warehouses, vehicles, accessible_zones)
        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['starts'], data['ends'])
        routing = pywrapcp.RoutingModel(manager)
        
        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]
            
        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        
        assignment = routing.SolveWithParameters(search_parameters)
        
        print('Solver status:', assignment)
        
        if assignment:
            for vehicle_id in range(data['num_vehicles']):
                index = routing.Start(vehicle_id)
                depot_node_idx = manager.IndexToNode(index)
                depot_location = data['locations'][depot_node_idx]
                
                while not routing.IsEnd(index):
                    index = assignment.Value(routing.NextVar(index))
                    if routing.IsEnd(index):
                        break
                    node_idx = manager.IndexToNode(index)
                    loc = data['locations'][node_idx]
                    
                    if loc['type'] == 'zone':
                        dist = haversine(depot_location['lat'], depot_location['lon'], loc['lat'], loc['lon'])
                        routes_output.append({
                            "route_id": f"R-veh-{vehicle_id}-{loc['id']}",
                            "from_id": depot_location['id'],
                            "to_id": loc['id'],
                            "waypoints": [
                                {"lat": depot_location['lat'], "lon": depot_location['lon']},
                                {"lat": loc['lat'], "lon": loc['lon']}
                            ],
                            "distance_km": round(dist, 1),
                            "eta_minutes": int((dist / 40.0) * 60), # 40 km/h truck speed
                            "blocked": False,
                            "via_drone": False
                        })
    except Exception as e:
        print("VRP failed or ortools not installed:", e)
        
    return routes_output
