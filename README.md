# Physion-Core
Physion V20 Web Simulation Engine — MVP for multiphysics battery simulation


## 📦 Project Architecture
- **API (api_main.py)** → Handles simulation requests and job management
- **Worker (worker.py)** → Executes simulations and stores results
- **Queue (Redis)** → Manages job scheduling
- **Database (SQLite)** → Stores job status and simulation results
- **Simulation Core (physion_core/)** → Implements physical models and multiphysics coupling
- **Frontend (frontend.py)** → Streamlit-based user interface
- **Admin Panel (admin_panel.py)** → Streamlit-based monitoring and management panel
- **Deployment (docker-compose.yml)** → Full deployment setup with Docker Compose


## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt


2. Start Redis

redis-server


3. Run the Worker

python worker.py


4. Run the API

uvicorn api_main:app --host 0.0.0.0 --port 8000


5. Launch the Frontend

streamlit run frontend.py


6. Launch the Admin Panel

streamlit run admin_panel.py


7. Deploy with Docker Compose

docker-compose up -d



⚙️ Features

• Multiphysics simulation: mass transport, charge transport, thermal effects, resistance, cycling
• Fully coupled physics models
• Modular architecture for extension
• Simple user interface for testing and visualization
• Admin panel for monitoring jobs and results



🛠 Roadmap

• ✅ MVP operational
• ⏳ Validation with experimental datasets
• ⏳ Benchmarking against PyBaMM/COMSOL
• ⏳ Advanced frontend (React/Next.js)
• ⏳ Deployment on VPS/Cloud



