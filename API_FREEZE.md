# ADCC — API Freeze Document
# These contracts are FROZEN. Do NOT change field names, paths, or response shapes.
# Frontend depends on exact field names listed here.

---

## Base URL

```
http://localhost:8000/api
```

---

## Endpoints

---

### POST /api/disaster/create

Triggers a new disaster simulation. Starts the LangGraph agent pipeline.

**Request Body:**
```json
{
  "disaster_type": "flood",
  "region": "Assam",
  "zones_count": 50,
  "scenario": "operation_brahmaputra"
}
```

**Response 200:**
```json
{
  "disaster_id": "dis_001",
  "disaster_type": "flood",
  "region": "Assam",
  "triggered_at": "2025-01-01T10:00:00Z",
  "zones_initialized": 50,
  "agents_activated": ["coordinator", "route", "resource", "medical", "drone"],
  "status": "running"
}
```

---

### GET /api/disaster/{disaster_id}

Returns current disaster state.

**Response 200:**
```json
{
  "disaster_id": "dis_001",
  "disaster_type": "flood",
  "region": "Assam",
  "triggered_at": "2025-01-01T10:00:00Z",
  "status": "running"
}
```

---

### GET /api/zones

Returns all zones for current disaster.

**Response 200:**
```json
{
  "zones": [
    {
      "zone_id": "Z-001",
      "name": "Dibrugarh North",
      "lat": 27.47,
      "lon": 94.91,
      "severity": 9,
      "population": 4200,
      "status": "critical",
      "road_accessible": false,
      "assigned_agent": "drone"
    }
  ]
}
```

---

### GET /api/agents/decisions

Returns all agent decisions for current disaster.

**Response 200:**
```json
{
  "decisions": [
    {
      "agent": "coordinator",
      "action": "Prioritized Zone Z-001 as critical",
      "target_zone": "Z-001",
      "reasoning": "Zone Z-001 has severity 9, population 4200, road blocked. Dispatching Drone Agent.",
      "timestamp": "2025-01-01T10:01:00Z"
    }
  ]
}
```

---

### POST /api/route/optimize

Runs OR-Tools VRP to find optimal routes.

**Request Body:**
```json
{
  "disaster_id": "dis_001",
  "blocked_zone_ids": ["Z-001", "Z-007"]
}
```

**Response 200:**
```json
{
  "routes": [
    {
      "route_id": "R-001",
      "from_id": "WH-001",
      "to_id": "Z-002",
      "waypoints": [
        {"lat": 27.47, "lon": 94.91},
        {"lat": 27.50, "lon": 94.95}
      ],
      "distance_km": 12.4,
      "eta_minutes": 18,
      "blocked": false,
      "via_drone": false
    }
  ]
}
```

---

### POST /api/resource/allocate

Allocates resources to zones.

**Request Body:**
```json
{
  "disaster_id": "dis_001",
  "priority_zone_ids": ["Z-001", "Z-003", "Z-007"]
}
```

**Response 200:**
```json
{
  "allocations": [
    {
      "resource_id": "RES-001",
      "type": "medicine",
      "quantity": 500,
      "warehouse_id": "WH-001",
      "allocated_to": "Z-001"
    }
  ]
}
```

---

### GET /api/metrics/{disaster_id}

Returns computed impact metrics.

**Response 200:**
```json
{
  "disaster_id": "dis_001",
  "response_time_reduction": 42.0,
  "delivery_efficiency": 67.0,
  "supplies_delivered": 91.0,
  "lives_impacted": 3200
}
```

---

### GET /api/timeline/{disaster_id}

Returns all timeline events.

**Response 200:**
```json
{
  "events": [
    {
      "event_id": "EVT-001",
      "timestamp": "2025-01-01T10:01:00Z",
      "agent": "coordinator",
      "event_type": "priority_change",
      "description": "Zone Z-001 elevated to CRITICAL — population 4200 at risk",
      "zone_id": "Z-001"
    }
  ]
}
```

---

## Rules

1. **NEVER** rename `disaster_id` to `id`
2. **NEVER** rename `zone_id` to `id`
3. **NEVER** rename `reasoning` to `reason` or `explanation`
4. **NEVER** rename `allocated_to` to `assigned_to`
5. **NEVER** change HTTP methods (all GETs stay GET, all POSTs stay POST)
6. **NEVER** add authentication middleware without flagging it — frontend has no auth
7. All timestamps in **ISO 8601** format
8. All severity scores as **integers 1–10** (not floats, not strings)
