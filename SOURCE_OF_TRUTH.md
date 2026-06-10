# ADCC — Source of Truth Architecture
# Version: v1.0 | Project: Autonomous Disaster Command Center
# DO NOT DEVIATE FROM THIS FILE

---

## Project Identity

**Name:** Autonomous Disaster Command Center (ADCC)
**Scenario:** Operation Brahmaputra (Flood, Assam region, 50 villages)
**Pitch:** "An Autonomous Disaster Command Center where multiple AI agents continuously coordinate logistics, routes, medical priorities, and relief operations in real time during disasters."
**NOT:** "A disaster management dashboard"

---

## Tech Stack (LOCKED — do not replace any item)

### Frontend
- Framework: Next.js 15
- Styling: Tailwind CSS
- Map: Leaflet (react-leaflet)
- Real-time: Socket.IO Client
- Language: JavaScript (NOT TypeScript)

### Backend
- Framework: FastAPI
- ORM: SQLAlchemy
- Database: PostgreSQL
- Real-time: Socket.IO (python-socketio)
- Language: Python 3.11+

### AI / Agents
- Orchestration: LangGraph ONLY
- ~~CrewAI~~ → REMOVED. Do not use CrewAI anywhere.

### Optimization
- Library: Google OR-Tools (ortools)
- Use case: Vehicle Routing Problem (VRP) for route optimization, resource allocation

---

## Agent Roster (5 agents — no more, no less)

| Agent | Role | Color |
|---|---|---|
| Coordinator Agent | Prioritizes zones by severity, dispatches other agents | #534AB7 |
| Route Agent | Finds alternative paths when roads blocked | #378ADD |
| Resource Agent | Allocates food/medicine/rescue equipment | #BA7517 |
| Medical Agent | Assigns medical teams and supplies to hospitals | #1D9E75 |
| Drone Agent | Deploys drones to inaccessible villages | #D85A30 |

---

## Build Order Rule (CRITICAL)

```
Database models
    ↓
API stubs (return 200)
    ↓
Seed data (operation_brahmaputra.json)
    ↓
Leaflet map
    ↓
Severity engine
    ↓
OR-Tools optimization
    ↓
LangGraph agents
    ↓
Socket.IO real-time
    ↓
Polish
```

**Rule: Optimization First. LLM Second.**
Do NOT start with LangGraph. Build severity engine + OR-Tools first.

---

## Demo Metrics (use these exact numbers)

- Response time reduced: **42%**
- Delivery efficiency: **67%**
- Critical supplies delivered: **91%**
- Lives impacted: **3,200**

---

## Scenario Seed (Operation Brahmaputra)

```json
{
  "disaster": "Flood",
  "region": "Assam",
  "zones": 50,
  "hospitals": 10,
  "warehouses": 5,
  "drones": 10,
  "vehicles": 15,
  "requests": 100
}
```

---

## Folder Structure (canonical)

```
ADCC/
├── frontend/
│   ├── app/
│   │   ├── dashboard/
│   │   ├── disaster-map/
│   │   └── agents/
│   └── components/
│       ├── Map.jsx
│       ├── AgentPanel.jsx
│       ├── KPICards.jsx
│       └── Timeline.jsx
├── backend/
│   ├── db/
│   │   └── models/          ← start here (Day 1)
│   ├── agents/              ← LangGraph nodes
│   ├── services/
│   │   ├── severity_engine.py
│   │   ├── routing_service.py
│   │   └── resource_service.py
│   ├── api/
│   │   └── routes/
│   └── main.py
└── seed_data/
    └── operation_brahmaputra.json
```
