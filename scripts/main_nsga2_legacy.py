
import os
import sys
import time
import matplotlib.pyplot as plt
import numpy as np

# Adjust path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from solvers.multi_objective.nsga2_legacy_solver import NSGA2LegacySolver
from solvers.problem_data import get_problem_data, StaplerData

def main():
    print("=== NSGA-II (Legacy/MATLAB Version) Optimization ===")
    print("Features: Archive + Random Fill Strategy")
    
    # Setup
    solver = NSGA2LegacySolver(
        population_size=100,
        generations=100,
        crossover_rate=0.8,
        mutation_rate=0.2,
        data_class=StaplerData
    )
    
    print(f"Goal: Stapler (n={solver.num_jobs})")
    
    start_time = time.time()
    
    hv_history = []
    
    for i in range(solver.generations):
        solver.evolve()
        hv_history.append(solver.history_hv[-1] if solver.history_hv else 0)
        
        if (i + 1) % 10 == 0:
            pareto_front = solver.get_pareto_front()
            print(f"   Gen {i+1}: Front Size={len(pareto_front)}, Current HV={hv_history[-1]:.4f}")

    elapsed = time.time() - start_time
    print("-" * 30)
    print("Optimization Completed!")
    print(f"Time: {elapsed:.4f}s")
    
    print(f"Time: {elapsed:.4f}s")
    
    # --- Detailed Results Table ---
    # Legacy Solver usage: archive_pop and archive_front are aligned.
    final_perms = solver.archive_pop
    final_objs = solver.archive_front
    
    pop_data = []
    
    for i in range(len(final_perms)):
        perm = final_perms[i]
        p = final_objs[i][0]
        c = final_objs[i][1]
        
        # Calc Cut Idx
        _, _, k = solver.calculate_objectives(perm)
        
        pop_data.append({
            'profit': p,
            'carbon': c,
            'cut_idx': k,
            'stop_part': perm[k-1] if k > 0 else "None",
            'perm': perm
        })
        
    # Sort
    sorted_sols = sorted(pop_data, key=lambda x: x['profit'])
    
    print("-" * 80)
    print(f"{'Profit':<10} | {'Carbon':<10} | {'Cut Idx':<8} | {'Stop Part':<10} | {'Sequence (First 10)'}")
    print("-" * 80)
    
    profits = []
    carbons = []
    
    for item in sorted_sols:
        seq_str = str(item['perm'][:10]) + "..."
        print(f"{item['profit']:<10.4f} | {item['carbon']:<10.4f} | {item['cut_idx']:<8} | {str(item['stop_part']):<10} | {seq_str}")
        profits.append(item['profit'])
        carbons.append(item['carbon'])
        
    print(f"Non-dominated Solutions Found: {len(sorted_sols)}")
    
    # Plot Side-by-Side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Convergence
    ax1.plot(hv_history, label='Set-Based Hypervolume')
    ax1.set_title('Legacy NSGA-II Convergence')
    ax1.set_xlabel('Generation')
    ax1.set_ylabel('Hypervolume')
    ax1.grid(True)
    
    # Plot 2: Front
    ax2.scatter([350], [0.001], color='gold', marker='*', s=200, label='Utopia')
    ax2.scatter(profits, carbons, color='orange', label='Legacy Front')
    ax2.plot(profits, carbons, color='orange', alpha=0.5, linestyle='--')
    
    ax2.set_xlabel('Profit (Maximize)')
    ax2.set_ylabel('Carbon (Minimize)')
    ax2.set_title('Legacy NSGA-II Pareto Frontier')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    out_path = os.path.join(os.path.dirname(__file__), 'nsga2_legacy_result.png')
    plt.savefig(out_path)
    print(f"Plot saved to: {out_path}")
    plt.show()

if __name__ == "__main__":
    main()
