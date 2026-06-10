from backend.agents.state import ADCCState
from backend.agents.severity_node import severity_node
from backend.agents.route_agent import route_node
from backend.agents.resource_agent import resource_node
from backend.agents.medical_agent import medical_node
from backend.agents.drone_agent import drone_node
from backend.agents.coordinator_agent import coordinator_node

class CustomGraph:
    async def astream(self, state: ADCCState):
        # 1. Severity Node
        out_sev = severity_node(state)
        self._merge_state(state, out_sev)
        yield {"severity_node": out_sev}
        
        # 2. Parallel Nodes (Route, Resource, Medical)
        out_route = route_node(state)
        self._merge_state(state, out_route)
        
        out_res = resource_node(state)
        self._merge_state(state, out_res)
        
        out_med = medical_node(state)
        self._merge_state(state, out_med)
        
        yield {
            "route_node": out_route,
            "resource_node": out_res,
            "medical_node": out_med
        }
        
        # 3. Drone Node
        out_drone = drone_node(state)
        self._merge_state(state, out_drone)
        yield {"drone_node": out_drone}
        
        # 4. Coordinator Node
        out_coord = coordinator_node(state)
        self._merge_state(state, out_coord)
        yield {"coordinator_node": out_coord}
        
    def _merge_state(self, state: dict, update: dict):
        for k, v in update.items():
            if k in ["agent_decisions", "timeline_events", "drone_assignments", "medical_actions"]:
                state.setdefault(k, []).extend(v)
            else:
                state[k] = v

app = CustomGraph()
