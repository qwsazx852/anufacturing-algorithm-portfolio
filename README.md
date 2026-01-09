# 🚀 AI Smart Portfolio Hub

A centralized hub showcasing advanced AI optimization algorithms applied to manufacturing scheduling problems. Built with **FastAPI** for the backend and a modern **Glassmorphism UI** for the frontend.



## 🌟 Featured Projects

### 1. Smart Manufacturing Scheduler (`/scheduler`)
An intelligent assembly line optimization system that solves the "Assembly Line Balancing Problem" (ALBP) using four different meta-heuristic algorithms.
> **[📖 Read Detailed Algorithm Documentation](ALGORITHM_DETAILS.md)**

- **🧬 Genetic Algorithm (GA)**
- **🐦 Particle Swarm Optimization (PSO)**
- **🐜 Ant Colony Optimization (ACO)**
- **🔥 Simulated Annealing (SA)**

**Key Features:**
- **Dynamic Visualization**: Real-time convergence charts using Chart.js.
- **Comparison Mode**: Run all algorithms sequentially to compare performance.
- **Custom Data Injection**: Upload your own Excel (`.xlsx`) configuration to solve different scheduling problems.

## 🛠️ Tech Stack
- **Backend**: Python 3.12, FastAPI, Uvicorn
- **Frontend**: HTML5, TailwindCSS, Chart.js, Vanilla JS
- **Data**: Pandas, Excel (OpenPyXL)

## 📦 Installation & Usage

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ai-portfolio-hub.git
   cd ai-portfolio-hub
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python main_portfolio.py
   ```

4. **Access the Dashboard**
   Open your browser and navigate to:
   - **Portfolio Hub**: [http://localhost:8000](http://localhost:8000)
   - **Scheduler App**: [http://localhost:8000/scheduler](http://localhost:8000/scheduler)

## 📂 Project Structure
```
.
├── main_portfolio.py       # Entry point (Portfolio Hub)
├── project_scheduler.py    # Scheduler Module (FastAPI Router)
├── data_adapter.py         # Excel Data Handler
├── config.xlsx             # Default Dataset
├── requirements.txt        # Python Dependencies
├── static/                 # Frontend Assets
│   ├── index.html          # Scheduler UI
│   ├── portfolio.html      # Portfolio Landing Page
│   └── ...
└── *_solver.py             # Algorithm Implementations (GA, PSO, ACO, SA)
```

## 📝 Custom Data Format
To use your own data, upload an Excel file with the following sheets:
- `Parameters`: Global settings (NUM_JOBS, etc.)
- `Constraints`: Precedence relations (Predecessor, Successor)
- `JobTimes`: Processing time for each job (JobId, Time)

---
*Created by Jun - 2025*
