
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Tuple
import time
import numpy as np

# Import Solvers
from solvers.nsga2_solver import NSGA2Solver
from solvers.nsga2_legacy_solver import NSGA2LegacySolver
from solvers.pso_ppx_solver import PSOPPXSolver
from solvers.npso_solver import NPSOSolver
from solvers.kg_solver import KGSolver
from solvers.block_ga_solver import BlockGASolver
from solvers.problem_data import StaplerData, PrinterData

router = APIRouter()

class DisassemblyParams(BaseModel):
    pop_size: int = 100
    generations: int = 50
    crossover_rate: float = 0.8
    mutation_rate: float = 0.2
    
    # PSO+PPX specific
    neighborhood_start_gen: int = 20

@router.post("/optimize/nsga2")
def run_nsga2(params: DisassemblyParams):
    start_time = time.time()
    
    solver = NSGA2Solver(
        population_size=params.pop_size,
        generations=params.generations,
        crossover_rate=params.crossover_rate,
        mutation_rate=params.mutation_rate,
        data_class=StaplerData
    )
    
    hv_history = []
    for _ in range(params.generations):
        solver.evolve()
        hv_history.append(solver.history_hv[-1] if solver.history_hv else 0)
        
    # Apply monotonic check for pretty plotting similar to compare_algorithms.py
    hv_history = np.maximum.accumulate(hv_history).tolist()
    
    front = solver.get_pareto_front()
    # Sort front by Profit
    front.sort(key=lambda x: x[0])
    
    return {
        "algorithm": "NSGA-II (True)",
        "result": {
            "hypervolume": hv_history[-1],
            "history": hv_history,
            "pareto_front": front  # List of [Profit, Carbon]
        },
        "time": round(time.time() - start_time, 4)
    }

@router.post("/optimize/nsga2_legacy")
def run_nsga2_legacy(params: DisassemblyParams):
    start_time = time.time()
    
    solver = NSGA2LegacySolver(
        population_size=params.pop_size,
        generations=params.generations,
        crossover_rate=params.crossover_rate,
        mutation_rate=params.mutation_rate,
        data_class=StaplerData
    )
    
    hv_history = []
    for _ in range(params.generations):
        solver.evolve()
        hv_history.append(solver.history_hv[-1] if solver.history_hv else 0)
        
    hv_history = np.maximum.accumulate(hv_history).tolist()
    
    front = solver.get_pareto_front()
    front.sort(key=lambda x: x[0])
    
    return {
        "algorithm": "NSGA-II (Legacy)",
        "result": {
            "hypervolume": hv_history[-1],
            "history": hv_history,
            "pareto_front": front
        },
        "time": round(time.time() - start_time, 4)
    }

@router.post("/optimize/pso_ppx")
def run_pso_ppx(params: DisassemblyParams):
    start_time = time.time()
    
    solver = PSOPPXSolver(
        population_size=params.pop_size,
        generations=params.generations,
        crossover_rate=params.crossover_rate,
        mutation_rate=params.mutation_rate,
        neighborhood_start_gen=params.neighborhood_start_gen,
        data_class=StaplerData
    )
    
    hv_history = []
    for _ in range(params.generations):
        solver.evolve()
        hv_history.append(solver.history_hv[-1] if solver.history_hv else 0)
    
    hv_history = np.maximum.accumulate(hv_history).tolist()
    
    # Get Front
    # PSOPPXSolver maintains archive
    front = solver.get_pareto_front()
    # Ensure it's list of tuples/lists
    front.sort(key=lambda x: x[0])
    
    return {
        "algorithm": "PSO+PPX",
        "result": {
            "hypervolume": hv_history[-1],
            "history": hv_history,
            "pareto_front": front
        },
        "time": round(time.time() - start_time, 4)
    }

@router.post("/optimize/npso")
def run_npso(params: DisassemblyParams):
    start_time = time.time()
    # NPSO uses different params (w, c1, c2) vs GA (crossover, mutation)
    # We map pop_size -> num_particles
    solver = NPSOSolver(
        num_particles=params.pop_size,
        generations=params.generations,
        w=0.8, # Default or could add to params
        c1=0.5,
        c2=0.5,
        data_class=StaplerData
    )
    hv_history = []
    for _ in range(params.generations):
        solver.evolve()
        hv_history.append(solver.history_hv[-1] if solver.history_hv else 0)
    hv_history = np.maximum.accumulate(hv_history).tolist()
    
    front = solver.get_pareto_front()
    front.sort(key=lambda x: x[0])
    return {
        "algorithm": "NPSO",
        "result": { "hypervolume": hv_history[-1], "history": hv_history, "pareto_front": front },
        "time": round(time.time() - start_time, 4)
    }

@router.post("/optimize/kg")
def run_kg(params: DisassemblyParams):
    start_time = time.time()
    # K&G might need slightly different params or use defaults
    solver = KGSolver(
        population_size=params.pop_size,
        generations=params.generations,
        # K&G uses higher mutation usually, but we use param
        crossover_rate=params.crossover_rate,
        mutation_rate=params.mutation_rate,
        data_class=StaplerData
    )
    hv_history = []
    for _ in range(params.generations):
        solver.evolve()
        # KGSolver has history_hv from our previous view_file
        hv_history.append(solver.history_hv[-1] if solver.history_hv else 0)
    hv_history = np.maximum.accumulate(hv_history).tolist()
    
    front = solver.get_pareto_front()
    front.sort(key=lambda x: x[0])
    return {
        "algorithm": "K&G",
        "result": { "hypervolume": hv_history[-1], "history": hv_history, "pareto_front": front },
        "time": round(time.time() - start_time, 4)
    }

@router.post("/optimize/block_ga")
def run_block_ga(params: DisassemblyParams):
    start_time = time.time()
    solver = BlockGASolver(
        population_size=params.pop_size,
        generations=params.generations,
        crossover_rate=params.crossover_rate,
        mutation_rate=params.mutation_rate,
        data_class=StaplerData
    )
    hv_history = []
    for _ in range(params.generations):
        solver.evolve()
        hv_history.append(solver.history_hv[-1] if solver.history_hv else 0)
    hv_history = np.maximum.accumulate(hv_history).tolist()
    
    front = solver.get_pareto_front()
    front.sort(key=lambda x: x[0])
    return {
        "algorithm": "Block-based GA",
        "result": { "hypervolume": hv_history[-1], "history": hv_history, "pareto_front": front },
        "time": round(time.time() - start_time, 4)
    }

@router.post("/optimize/compare")
def run_compare(params: DisassemblyParams):
    # Run all 6 algorithms
    
    # MOEAs
    res_pso = run_pso_ppx(params)
    res_nsga2 = run_nsga2(params)
    res_legacy = run_nsga2_legacy(params)
    
    # Scalarized / Other
    res_kg = run_kg(params)
    res_npso = run_npso(params)
    res_block = run_block_ga(params)
    
    return {
        "algorithm": "ALL",
        "results": [res_pso, res_nsga2, res_legacy, res_kg, res_npso, res_block]
    }
