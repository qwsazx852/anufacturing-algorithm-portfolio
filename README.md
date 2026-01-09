# 🧠 Meta-Heuristic Scheduling Optimization Engine
> **A Comparative Research Platform for Solving NP-Hard Manufacturing Problems**

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat&logo=python)
![Algorithm](https://img.shields.io/badge/Focus-Algorithm%20Design-orange?style=flat&logo=scipy)
![Architecture](https://img.shields.io/badge/Architecture-AI--Assisted%20Microservice-green?style=flat)

## � Project Focus & Role
**Positioning**: Algorithm Engineer / Optimization Researcher

This project was developed to demonstrate **advanced algorithmic problem solving** applied to real-world manufacturing constraints (Assembly Line Balancing Problem type-1). 

### 👨‍💻 My Contribution: Core Algorithmic Logic
My primary focus and manual implementation efforts were dedicated to the **mathematical modeling and optimization engine** located in the `*_solver.py` modules. Key technical challenges I solved include:

1.  **Constraint Handling**: Designed a robust `Transitive Closure` matrix ensuring all generated schedules respect strict precedence constraints (Job A → Job B).
2.  **Encoding Strategies**:
    *   **GA**: Implemented custom 2-point crossover and "Repair" gene operators to maintain valid topological sorts.
    *   **PSO**: Adapted continuous particle velocity vectors to discrete job sequences using the **SPV (Smallest Position Value)** rule.
3.  **Convergence Tuning**: Fine-tuned hyperparameters (cooling rate, pheromone evaporation, inertia weights) to balance *Exploration* vs *Exploitation*.

### ⚡ Engineering Methodology: Production-Grade Development
To showcase these algorithms in a real-world context, I implemented a comprehensive full-stack architecture:
- **FastAPI Backend**: High-performance REST API exposing the optimization solvers.
- **Frontend Visualization**: Modern, responsive dashboard for real-time convergence monitoring and interactive experimentation.

*This approach demonstrates my ability to bridge the gap between theoretical algorithm design and practical software engineering.*

### 🔬 Provenance: Research to Production
I initially prototyped and validated these algorithms in **MATLAB** to establish mathematical correctness before porting them to a production-grade Python microservice. This ensures the implementations are mathematically rigorous and optimized for performance.
- **Legacy Research Code**: Available in the [`matlab_legacy/`](matlab_legacy/) directory for reference and validation.

---

## 🔍 The Algorithms

I implemented and compared four distinct meta-heuristics from scratch (no "black-box" optimization libraries):

| Algorithm | Key Implementation Detail | Why I Chose It |
| :--- | :--- | :--- |
| **Genetic Algorithm (GA)** | Custom `Rank Selection` & `Order Crossover (OX)` | Best general performance for combinatorial problems. |
| **Particle Swarm (PSO)** | **SPV Rule** implementation | To test continuous-to-discrete mapping efficiency. |
| **Ant Colony (ACO)** | Probabilistic **Roulette Wheel** construction | Strong performance in graph-path based problems. |
| **Simulated Annealing (SA)** | Boltzmann distribution acceptance probability | Baseline for single-solution trajectory search. |

> **[📖 View Detailed Algorithmic Documentation & Benchmarks](ALGORITHM_DETAILS.md)**

---

## ️ System Architecture
The system follows a clean separation of concerns:

```
## 📂 Project Structure
.
├── main.py                 # Entry point (FastAPI App)
├── app/
│   ├── routers/            # API Endpoints (scheduler.py)
│   └── utils/              # Helper functions
├── solvers/                # Core Algorithm Logic (GA, PSO, ACO, SA)
├── scripts/                # Utility scripts & comparisons
├── data/                   # Configuration & Dataset (Excel)
├── docs/                   # Documentation & Resume Guide
├── matlab_legacy/          # Original Research Code (MATLAB)
└── static/                 # Frontend Assets
```

## 🚀 Quick Start

1.  **Install & Run**:
    ```bash
    pip install -r requirements.txt
    ```bash
   python main.py
   ```
2.  **Explore**:
    *   **Dashboard**: `http://localhost:8000/scheduler` (Run algorithms & visualize results)
    *   **API Docs**: `http://localhost:8000/docs`

---
*Created by [Jun] - 2025*
