
import sys
import os
import time
import numpy as np
import matplotlib.pyplot as plt

# Add parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from solvers.multi_objective.pso_ppx_solver import PSOPPXSolver
from solvers.problem_data import StaplerData

def main():
    print("=== PSO+PPX (Hybrid) Solver Demo ===")
    
    # Parameters
    pop_size = 100
    generations = 100
    ns_start = 20 # Start PPX at generation 20
    
    # Initialize Solver
    solver = PSOPPXSolver(
        population_size=pop_size,
        generations=generations,
        neighborhood_start_gen=ns_start,
        data_class=StaplerData
    )
    
    print(f"Data: Stapler")
    print(f"Algorithm: PSO (Gen 0-{ns_start}) -> PSO+PPX Hybrid (Gen {ns_start}-{generations})")
    
    start_time = time.time()
    
    # Run
    # PSOPPXSolver inherits from NPSOSolver, evolve returns (cut, global_best, cut_idx)
    # But for MO this signature might be different?
    # Let's run evolve inside a loop to track progress
    
    hv_history = []
    
    # Initial evolve to setup
    solver.evolve()
    
    print(f"Progress: 0/{generations}", end='\r')
    for i in range(generations):
        _, gbest_score, _ = solver.evolve()
        hv_history.append(solver.history_hv[-1] if solver.history_hv else 0)
        
        if i % 10 == 0:
             print(f"Progress: {i}/{generations} | Current Best HV: {hv_history[-1]:.4f}", end='\r')
             
    elapsed = time.time() - start_time
    print(f"\nDone in {elapsed:.4f} seconds.")
    
    # Results
    print(f"Final HV: {hv_history[-1]:.4f}")
    
    # Retrieve Archive
    archive_perms = solver.archive_permutations
    archive_objs = solver.archive_objs
    
    print(f"Pareto Front Size: {len(archive_objs)}")
    print("-" * 80)
    print(f"{'Profit':<10} | {'Carbon':<10} | {'Cut Idx':<8} | {'Stop Part':<10} | {'Sequence (First 10)'}")
    print("-" * 80)
    
    front_data = []
    
    for i in range(len(archive_objs)):
        perm = archive_perms[i]
        profit, carbon = archive_objs[i]
        
        # Recalculate to get Cut Index
        _, _, cut_idx = solver.calculate_objectives(perm)
        
        # Identify Stop Part (Last disassembled part)
        # cut_idx is the number of parts disassembled (sequence[:cut_idx])
        # So the last disassembled part is sequence[cut_idx - 1]
        stop_part = perm[cut_idx - 1] if cut_idx > 0 else "None"
        
        front_data.append({
            'profit': profit,
            'carbon': carbon,
            'cut_idx': cut_idx,
            'stop_part': stop_part,
            'perm': perm
        })
        
    # Sort by Profit
    front_data.sort(key=lambda x: x['profit'])
    
    for item in front_data:
        seq_str = str(item['perm'][:10]) + "..."
        print(f"{item['profit']:<10.4f} | {item['carbon']:<10.4f} | {item['cut_idx']:<8} | {str(item['stop_part']):<10} | {seq_str}")
        
    front = [(d['profit'], d['carbon']) for d in front_data]
    
    # Sort front for plotting
    front.sort(key=lambda x: x[0])
    p = [x[0] for x in front]
    c = [x[1] for x in front]
    
    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Convergence
    ax1.plot(hv_history, label='Hypervolume')
    ax1.set_title('Convergence History')
    ax1.set_xlabel('Generation')
    ax1.set_ylabel('Hypervolume')
    ax1.grid(True)
    
    # Pareto Front
    ax2.scatter(p, c, c='red', marker='o', label='Pareto Front')
    ax2.plot(p, c, c='red', alpha=0.5, linestyle='--')
    ax2.scatter([350], [0.001], c='gold', marker='*', s=200, label='Utopia')
    
    ax2.set_title(f'Pareto Front (PSO+PPX) - HV: {hv_history[-1]:.4f}')
    ax2.set_xlabel('Profit (Max)')
    ax2.set_ylabel('Carbon (Min)')
    ax2.grid(True)
    ax2.legend()
    
    plt.tight_layout()
    output_path = os.path.join(current_dir, 'pso_ppx_result.png')
    plt.savefig(output_path)
    print(f"Plot saved to: {output_path}")
    plt.show()

if __name__ == "__main__":
    main()
