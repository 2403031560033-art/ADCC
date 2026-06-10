from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import disaster, zones, agents, routes, resources, metrics, timeline

app = FastAPI(title="ADCC API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(disaster.router)
app.include_router(zones.router)
app.include_router(agents.router)
app.include_router(routes.router)
app.include_router(resources.router)
app.include_router(metrics.router)
app.include_router(timeline.router)

@app.get("/")
async def root():
    return {"message": "ADCC API Running"}

# Mount Socket.IO
import socketio
from backend.services.socket_manager import sio
app = socketio.ASGIApp(sio, other_asgi_app=app)

