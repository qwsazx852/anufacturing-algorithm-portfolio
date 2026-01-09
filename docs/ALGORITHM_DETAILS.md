# Smart Manufacturing Schedule Optimizer
> **Automated Job Shop Scheduling System using Meta-Heuristic Algorithms (GA, PSO, ACO, SA)**

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Service-green?style=flat&logo=fastapi)
![Algorithm](https://img.shields.io/badge/Algorithm-Meta--Heuristics-orange?style=flat)

## 📖 Project Overview
This project addresses a classic **NP-Hard** optimization problem in manufacturing: **Workstation Minimization** (Assembly Line Balancing). 

Given a set of manufacturing jobs with specific `process_times` and strictly defined `precedence_constraints` (e.g., Job A must be done before Job B), the goal is to assign these jobs to the **minimum number of workstations** possible while respecting the `Cycle Time` (maximum time allowed per station).

This solution implements and compares four state-of-the-art meta-heuristic algorithms from scratch:
1.  **Genetic Algorithm (GA)**: Evolutionary search with custom crossover/repair logic.
2.  **Particle Swarm Optimization (PSO)**: Swarm intelligence using SPV (Smallest Position Value) rule.
3.  **Ant Colony Optimization (ACO)**: Pheromone-based construction of job sequences.
4.  **Simulated Annealing (SA)**: Physics-inspired probabilistic search.

The core engine is wrapped in a **FastAPI Microservice**, allowing precise real-time scheduling via a RESTful API.

---

## 🏗️ System Architecture

### 1. The Core Solvers (Python)
-   **Modular Design**: Each algorithm inherits from a common interface or follows a strictly consistent pattern.
-   **Robust Constraints**: Features a custom `Transitive Closure` matrix builder to ensure all generated schedules (chromosomes/particles) are valid repairable topological sorts.
-   **High Performance**: Vectorized operations using `NumPy` where applicable (e.g., PSO velocity updates).

### 2. The Microservice (FastAPI)
-   Exposes endpoints (`/optimize/ga`, `/optimize/pso`, etc.) for remote execution.
-   Returns JSON-formatted schedules including `min_stations` and the optimal `sequence`.
-   Includes Swagger UI for interactive testing.

---

## 🚀 How to Run

### Prerequisites
```bash
pip install numpy pandas matplotlib fastapi uvicorn openpyxl
```

### 1. Run the API Service
```bash
# Navigate to the project directory
cd GA

# Start the server (Dev mode)
uvicorn fastapi_demo:app --reload
```
Access the Interactive API Docs at: **http://127.0.0.1:8000/docs**

### 2. Run Comparative Analysis
To see which algorithm performs best on your dataset:
```bash
python compare_algorithms.py
```
This will generate:
-   `convergence_comparison.png`: A graph showing how quickly each algorithm finds the optimal solution.
-   Console output table with execution times and best scores.

---

## 📊 Performance Benchmark

| Algorithm | Mean Execution Time | Features | Ideal Use Case |
| :--- | :--- | :--- | :--- |
| **Simulated Annealing (SA)** | ~0.05s | Fast, one-solution logic | Real-time simple re-scheduling |
| **Genetic Algorithm (GA)** | ~0.30s | Robust population search | Complex constraints, large scale |
| **PSO** | ~1.00s | Continuous space search | If SPV encoding suits the problem |
| **ACO** | ~3.00s | Constructive heuristics | Very strictly constrained graphs |

---

## 🛠️ Technology Stack
-   **Language**: Python 3.x
-   **Core Libs**: NumPy (Math), Matplotlib (Viz), Pandas (Data)
-   **Web Framework**: FastAPI, Pydantic (Validation)
-   **Algorithms**: Custom Implementation (No "black box" optimization libraries used)

---

## 📬 Contact
**Algorithm Engineer**: Jun
**Focus**: AI for Manufacturing, Operations Research, Intelligent Systems.
