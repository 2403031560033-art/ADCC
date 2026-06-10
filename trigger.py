import requests
requests.post("http://localhost:8000/api/disaster/create", json={"disaster_type": "flood", "region": "Assam", "zones_count": 10, "scenario": "operation_brahmaputra"})
