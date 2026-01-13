
import os
import sys
import time
import matplotlib.pyplot as plt
import numpy as np

# Adjust path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from solvers.multi_objective.nsga2_solver import NSGA2Solver
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
    
    print(f"Time: {elapsed:.4f}s")
    
    # --- Detailed Results ---
    # NSGA2Solver stores final population in self.population
    # We need to extract the Non-Dominated Front from the final population
    
    final_pop = solver.population
    pop_data = []
    
    # Calculate objectives for all
    for chrom in final_pop:
        p, c, k = solver.calculate_objectives(chrom)
        pop_data.append({
            'profit': p,
            'carbon': c,
            'cut_idx': k,
            'stop_part': chrom[k-1] if k > 0 else "None",
            'perm': chrom
        })
        
    # Find Non-Dominated Set
    non_dominated = []
    for i in range(len(pop_data)):
        is_dominated = False
        p1 = pop_data[i]
        for j in range(len(pop_data)):
            if i == j: continue
            p2 = pop_data[j]
            # Dominated if p2 is better/equal in all AND strictly better in at least one
            # Objectives: Max Profit, Min Carbon
            # p2 better if p2.profit >= p1.profit AND p2.carbon <= p1.carbon
            if (p2['profit'] >= p1['profit'] and p2['carbon'] <= p1['carbon']) and \
               (p2['profit'] > p1['profit'] or p2['carbon'] < p1['carbon']):
                is_dominated = True
                break
        if not is_dominated:
            # Check duplicates based on objectives?
            # Or just append. We'll filter duplicates by profit/carbon below to avoid clutter
            non_dominated.append(p1)
            
    # Filter duplicates manually for display
    unique_solutions = {}
    for sol in non_dominated:
        key = (round(sol['profit'], 4), round(sol['carbon'], 4))
        if key not in unique_solutions:
            unique_solutions[key] = sol
            
    sorted_sols = sorted(unique_solutions.values(), key=lambda x: x['profit'])
    
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
