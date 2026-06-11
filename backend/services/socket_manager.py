import socketio

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

async def emit_agent_update(agent: str, action: str, reasoning: str):
    await sio.emit("agent_update", {
        "agent": agent,
        "action": action,
        "reasoning": reasoning
    })

async def emit_timeline_event(event: dict):
    await sio.emit("timeline_event", event)

async def emit_state_update(state: dict):
    await sio.emit("state_update", state)

async def emit_metrics_update(metrics: dict):
    await sio.emit("metrics_update", metrics)

async def emit_citizen_report(report: dict):
    await sio.emit("citizen_report", report)
