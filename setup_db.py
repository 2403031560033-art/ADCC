from backend.db.database import engine, Base
# Import all models to register them
from backend.db.models import Disaster, Zone, Hospital, Warehouse, Resource, Route, AgentDecision, TimelineEvent

try:
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
except Exception as e:
    print("Error creating tables:", e)
