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

### ⚡ Engineering Methodology: AI-Accelerated Development ("Vibe Coding")
To showcase these algorithms in a production-ready context, I leveraged **AI-Assisted Development** for the peripheral infrastructure:
- **FastAPI Backend**: Rapidly scaffolded a high-performance REST API to expose the solvers.
- **Frontend Visualization**: Used modern web tools to build a glassmorphism dashboard for real-time convergence monitoring.
*This approach demonstrates my ability to focus deep technical content while efficiently utilizing modern tools to deliver complete full-stack solutions.*

### 🔬 Provenance: Research to Production
I initially prototyped and validated these algorithms in **MATLAB** to establish mathematical correctness before porting them to a production-grade Python microservice.
- **Legacy Research Code**: Available in the [`matlab_legacy/`](matlab_legacy/) directory.
- **Scope**: Contains early experiments with BGA (Binary GA), NPSO, and different encoding schemes.

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

## �️ System Architecture
The system follows a clean separation of concerns:

```
├── 🧠 Core Solvers (My Key Focus)
│   ├── ga_solver.py      # Genetic Evolutionary Logic
│   ├── pso_solver.py     # Swarm Intelligence / SPV Logic
│   ├── aco_solver.py     # Pheromone Matrix Logic
│   └── sa_solver.py      # Probabilistic Search Logic
│
├── 🔌 Service Layer (AI-Scaffolded)
│   ├── fastapi_demo.py   # REST Endpoints
│   └── static/           # Visualization Dashboard
│
└── 📊 Data Layer
    └── Constraint Matrix & Job Times (Excel/Pandas)
```

## 🚀 Quick Start

1.  **Install & Run**:
    ```bash
    pip install -r requirements.txt
    python main_portfolio.py
    ```
2.  **Explore**:
    *   **Dashboard**: `http://localhost:8000/scheduler` (Run algorithms & visualize results)
    *   **API Docs**: `http://localhost:8000/docs`

---
*Created by [Jun] - 2025*
