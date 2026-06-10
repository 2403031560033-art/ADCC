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

def allocate_resources(priority_queue: List[str], zones: List[Dict], warehouses: List[Dict]) -> List[Dict]:
    allocations = []
    
    # Create a mutable copy of warehouse inventory
    wh_inventory = {}
    for w in warehouses:
        wh_inventory[w['warehouse_id']] = {
            'lat': w['lat'],
            'lon': w['lon'],
            'food': w['food_units'],
            'medicine': w['medicine_units'],
            'rescue_equipment': w['rescue_kits']
        }
        
    zone_map = {z['zone_id']: z for z in zones}
    
    for zone_id in priority_queue:
        zone = zone_map.get(zone_id)
        if not zone:
            continue
            
        sev = zone['severity']
        if sev >= 8:
            needs = {'food': 1000, 'medicine': 500, 'rescue_equipment': 50}
        elif sev >= 5:
            needs = {'food': 500, 'medicine': 200, 'rescue_equipment': 20}
        else:
            needs = {'food': 200, 'medicine': 100, 'rescue_equipment': 5}
            
        # Sort warehouses by distance to this zone
        sorted_wh = sorted(
            wh_inventory.keys(),
            key=lambda wid: haversine(wh_inventory[wid]['lat'], wh_inventory[wid]['lon'], zone['lat'], zone['lon'])
        )
        
        for resource_type, required_qty in needs.items():
            remaining_need = required_qty
            for wid in sorted_wh:
                if remaining_need <= 0:
                    break
                    
                available = wh_inventory[wid][resource_type]
                if available > 0:
                    allocated = min(remaining_need, available)
                    wh_inventory[wid][resource_type] -= allocated
                    remaining_need -= allocated
                    
                    allocations.append({
                        "resource_id": f"RES-{uuid.uuid4().hex[:8]}",
                        "type": resource_type,
                        "quantity": allocated,
                        "warehouse_id": wid,
                        "allocated_to": zone_id
                    })
                    
    return allocations
