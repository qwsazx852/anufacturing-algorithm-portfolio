
import os
import sys
import time
import matplotlib.pyplot as plt
import numpy as np

# Adjust path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from solvers.nsga2_solver import NSGA2Solver
from solvers.problem_data import get_problem_data, StaplerData, CeilingFanData, PrinterData

def main():
    print("=== NSGA-II (True Multi-Objective) Optimization ===")
    
    # Setup
    solver = NSGA2Solver(
        population_size=100,
        generations=50,
        crossover_rate=0.8,
        mutation_rate=0.2,
        data_class=StaplerData
    )
    
    print(f"Goal: Stapler (n={solver.num_jobs})")
    print("Optimization targets: Profit (Max), Carbon (Min)")
    print("Selection: Dominance Rank + Crowding Distance")
    
    start_time = time.time()
    
    for i in range(solver.generations):
        solver.evolve()
        
        if (i + 1) % 10 == 0:
            # Get current front size
            unique_objs = set(solver.gbest_score) # Just a placeholder
            # Actually let's count unique non-dominated
            pareto_front = solver.get_pareto_front()
            print(f"   Gen {i+1}: Front Size={len(pareto_front)}, Best Balance={solver.gbest_score}")

    elapsed = time.time() - start_time
    print("-" * 30)
    print("Optimization Completed!")
    print(f"Time: {elapsed:.4f}s")
    
    # Final Front
    front = solver.get_pareto_front()
    profits = [p[0] for p in front]
    carbons = [p[1] for p in front]
    
    # Sort for plotting
    sorted_indices = np.argsort(profits)
    profits = [profits[i] for i in sorted_indices]
    carbons = [carbons[i] for i in sorted_indices]
    
    print(f"Non-dominated Solutions Found: {len(front)}")
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.scatter([350], [0.001], color='gold', marker='*', s=200, label='Utopia')
    plt.scatter(profits, carbons, color='purple', label='NSGA-II Front')
    plt.plot(profits, carbons, color='purple', alpha=0.5, linestyle='--')
    
    plt.xlabel('Profit (Maximize)')
    plt.ylabel('Carbon (Minimize)')
    plt.title('NSGA-II Pareto Frontier')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    out_path = os.path.join(os.path.dirname(__file__), 'nsga2_result.png')
    plt.savefig(out_path)
    print(f"Plot saved to: {out_path}")

if __name__ == "__main__":
    main()
