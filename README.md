# Autonomous Disaster Coordination Center (ADCC)

ADCC is an advanced, AI-driven disaster management orchestration platform designed to simulate and coordinate disaster response operations across various natural calamities. It leverages an agentic graph system to intelligently process incoming disaster data, analyze severity, plan routes, allocate resources, dispatch medical assistance, and deploy drones for surveillance and supply delivery.

## Key Features

- **Multi-Scenario Simulation**: Supports various disaster scenarios across different regions of India:
  - 🌊 Operation Brahmaputra (Flood in Assam)
  - 🌍 Operation Himalayan Quake (Earthquake in Uttarakhand)
  - ⛰️ Operation Sikkim Slide (Landslide in Sikkim)
  - 🌀 Operation Cyclone Amphan (Cyclone in Odisha)
  - ❄️ Operation White Death (Avalanche in Himachal Pradesh)
- **Agentic Workflow**: Utilizes a custom state machine graph with specialized agents:
  - `Severity Agent`: Evaluates impact and prioritizes zones.
  - `Route Agent`: Determines accessible routes and bypasses blockages.
  - `Resource Agent`: Allocates supplies from available warehouses.
  - `Medical Agent`: Dispatches medical teams from nearby hospitals.
  - `Drone Agent`: Deploys drones for rapid surveillance and critical deliveries.
  - `Coordinator Agent`: Oversees the entire operation and generates final response metrics.
- **Real-Time Dashboard**: A Next.js frontend featuring a live map, KPI tracking, agent activity logs, and an operational timeline.
- **WebSockets Integration**: Socket.IO streams agent decisions and state changes to the UI in real-time, providing an interactive simulation experience.
- **Dynamic Scenario Switching**: A seamless trigger mechanism to cycle through different disaster scenarios, complete with automatic data cleanup and state resets.

## Architecture

- **Backend**: FastAPI (Python), SQLAlchemy (PostgreSQL), Custom Graph State Machine, Socket.IO.
- **Frontend**: Next.js (React), React-Leaflet (Maps), Socket.IO-Client.
- **Database**: PostgreSQL (Seed data loaded via JSON schemas).

## Project Structure

- `/backend`: Contains the FastAPI server, agent logic, database models, and simulation engine.
- `/frontend`: Next.js application containing the interactive dashboard, map, and real-time visualization components.
- `/seed_data`: JSON files containing realistic geographical and demographic data for various disaster scenarios.

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js & npm
- PostgreSQL

### Setup Backend
1. Navigate to the project root.
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your PostgreSQL database and update connection strings in `backend/db/database.py` if necessary.
4. Run the FastAPI server:
   ```bash
   uvicorn backend.main:app --reload
   ```

### Setup Frontend
1. Navigate to the `frontend` directory.
2. Install Node dependencies:
   ```bash
   npm install
   ```
3. Run the Next.js development server:
   ```bash
   npm run dev
   ```

### Usage
- Open `http://localhost:3000/dashboard` in your browser.
- Click the **TRIGGER DISASTER** button to initiate a random disaster simulation.
- Watch the map update, KPIs compute, and agent logs stream in real-time.

## License

This project is licensed under the MIT License.
