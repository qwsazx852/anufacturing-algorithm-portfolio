import sys
import os
import numpy as np

# Add parent directory to sys.path to identify 'solvers' and 'app'
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from app.utils import data_adapter
from solvers.ga_solver import GeneticOptimizer
from solvers.pso_solver import PSOSolver
from solvers.aco_solver import ACOSolver
from solvers.sa_solver import SASolver
from solvers.npso_solver import NPSOSolver
from solvers.block_ga_solver import BlockGASolver
from solvers.kg_solver import KGSolver
from solvers.nsga2_solver import NSGA2Solver
from solvers.nsga2_legacy_solver import NSGA2LegacySolver
from solvers.pso_ppx_solver import PSOPPXSolver
import os
import time
import matplotlib.pyplot as plt

import argparse
from solvers.problem_data import get_problem_data

def run_comparison():
    parser = argparse.ArgumentParser(description='Compare Algorithms on different datasets.')
    parser.add_argument('--dataset', type=str, default='Stapler', 
                        help='Dataset name: Stapler (n=18), CeilingFan (n=20), Printer (n=100)')
    args = parser.parse_args()
    
    print(f"=== Algorithm Comparison on {args.dataset} Dataset ===")
    
    # 1. Load Config (for Algorithm Params only)
    config_path = os.path.join(parent_dir, 'data', 'config.xlsx')
    loader = data_adapter.ConfigLoader(config_path)
    config = loader.load_config()
    
    # Load Problem Data
    data_class = get_problem_data(args.dataset)
    print(f"Loaded Data: {data_class.__name__} (n={data_class.NUM_PARTS})")
    
    # Override Problem Params from Dataset
    num_jobs = data_class.NUM_PARTS
    constraints = data_class.CONSTRAINTS
    time_info = data_class.OPERATION_TIMES
    cycle_time = data_class.CYCLE_TIME
    
    # Algorithm Params
    pop_size = int(config.get('POPULATION_SIZE', 50))
    max_generations = int(config.get('MAX_GENERATIONS', 50))
    # Override for large datasets if needed?
    if num_jobs >= 50:
         pop_size = max(pop_size, 100)
         # max_generations = max(max_generations, 100) # Keep short for demo unless requested
    
    results = {} # Store (history, time, final_score)
    
    # ==========================================
    # 1. Genetic Algorithm (GA)
    # ==========================================
    print("\n[1/7] Running GA...")
    ga = GeneticOptimizer(num_jobs, pop_size, 0.8, 0.1, constraints, time_info, cycle_time)
    ga.initialize_population()
    
    start_time = time.time()
    ga_history = []
    current_best = float('inf')
    
    for _ in range(max_generations):
        _, score = ga.evolve()
        if score < current_best:
            current_best = score
        ga_history.append(current_best)
        
    results['GA'] = {
        'history': ga_history,
        'time': time.time() - start_time,
        'score': current_best
    }
    
    # ==========================================
    # 2. Particle Swarm Optimization (PSO)
    # ==========================================
    print("[2/7] Running PSO...")
    pso = PSOSolver(num_jobs, pop_size, constraints, time_info, cycle_time)
    
    start_time = time.time()
    pso_history = []
    
    for _ in range(max_generations):
        _, score = pso.evolve()
        # PSOSolver.evolve returns the best score of the swarm in that iteration
        # accessing pso.gbest_score gives global best
        pso_history.append(pso.gbest_score)
        
    results['PSO'] = {
        'history': pso_history,
        'time': time.time() - start_time,
        'score': pso.gbest_score
    }
    
    # ==========================================
    # 3. Ant Colony Optimization (ACO)
    # ==========================================
    print("[3/7] Running ACO...")
    # Matches main_aco.py settings
    num_ants = 50 
    aco = ACOSolver(num_jobs, num_ants, constraints, time_info, cycle_time)
    
    start_time = time.time()
    aco_history = []
    
    for _ in range(max_generations):
        _, _ = aco.evolve() # internal update
        aco_history.append(aco.gbest_fitness)
        
    results['ACO'] = {
        'history': aco_history,
        'time': time.time() - start_time,
        'score': aco.gbest_fitness
    }
    
    # ==========================================
    # 4. Simulated Annealing (SA)
    # ==========================================
    print("[4/7] Running SA...")
    sa = SASolver(num_jobs, constraints, time_info, cycle_time, 
                  initial_temp=1000.0, cooling_rate=0.99, stopping_temp=0.1)
    
    start_time = time.time()
    sa_history = []
    
    while sa.temp > sa.stopping_temp:
        sa.step()
        sa_history.append(sa.best_fitness)
        
    results['SA'] = {
        'history': sa_history,
        'time': time.time() - start_time,
        'score': sa.best_fitness
    }
    
    # ==========================================
    # 5. NPSO (Multi-Objective)
    # ==========================================
    # ==========================================
    # 5. NPSO (Multi-Objective)
    # ==========================================
    # ==========================================
    # 5. NPSO (Multi-Objective)
    # ==========================================
    print(f"[5/7] Running NPSO (Multi-Objective) on {args.dataset}...")
    npso = NPSOSolver(generations=max_generations, num_particles=pop_size, data_class=data_class)
    
    start_time = time.time()
    npso_history_hv = []
    
    for _ in range(max_generations):
        npso.evolve() 
        npso_history_hv.append(npso.history_hv[-1])
        
    results['NPSO'] = {
        'history': npso_history_hv,
        'time': time.time() - start_time,
        'score': npso.history_hv[-1], # Final HV
        'final_obj': npso.gbest_score, # (Profit, Carbon)
        'front': npso.get_pareto_front(),
        'type': 'Selective Disassembly (HV)'
    }

    # ==========================================
    # 6. Block-Based GA
    # ==========================================
    print(f"[6/8] Running Block-Based GA on {args.dataset}...")
    bga = BlockGASolver(generations=max_generations, population_size=pop_size, data_class=data_class)
    
    start_time = time.time()
    bga_history_hv = []
    
    for _ in range(max_generations):
        bga.evolve()
        bga_history_hv.append(bga.history_hv[-1])
        
    results['BlockGA'] = {
        'history': bga_history_hv,
        'time': time.time() - start_time,
        'score': bga.history_hv[-1],
        'final_obj': bga.gbest_score,
        'front': bga.get_pareto_front(),
        'type': 'Selective Disassembly (HV)'
    }

    # ==========================================
    # 7. K&G (PPX)
    # ==========================================
    print(f"[7/8] Running K&G (PPX) on {args.dataset}...")
    kg = KGSolver(generations=max_generations, population_size=pop_size, data_class=data_class)
    
    start_time = time.time()
    _, _, _ = kg.evolve()
    for _ in range(max_generations - 1):
        kg.evolve()
    kg_time = time.time() - start_time
    kg_history_hv = kg.history_hv

    # ==========================================
    # 8. NSGA-II (True MO)
    # ==========================================
    print(f"[8/8] Running NSGA-II (True MO) on {args.dataset}...")
    nsga2 = NSGA2Solver(generations=max_generations, population_size=pop_size, data_class=data_class)
    
    start_time = time.time()
    _, _, _ = nsga2.evolve()
    for _ in range(max_generations - 1):
        nsga2.evolve()
    nsga2_time = time.time() - start_time
    nsga2_history_hv = nsga2.history_hv

    # ==========================================
    # 9. NSGA-II (Legacy / User Version)
    # ==========================================
    print(f"[9/9] Running NSGA-II (Legacy) on {args.dataset}...")
    nsga2_legacy = NSGA2LegacySolver(generations=max_generations, population_size=pop_size, data_class=data_class)
    
    start_time = time.time()
    _, _, _ = nsga2_legacy.evolve()
    for _ in range(max_generations - 1):
        nsga2_legacy.evolve()
    nsga2_legacy_time = time.time() - start_time
    nsga2_legacy_history_hv = nsga2_legacy.history_hv

    # ==========================================
    # 10. PSO+PPX (Hybrid Neighborhood)
    # ==========================================
    print(f"[10/10] Running PSO+PPX (Hybrid) on {args.dataset}...")
    # Ns = 50% of generations or fixed 200? Matlab: Ns=200, gen=1000. Ratio 0.2.
    # Let's use 20% of max_generations
    ns_start = int(max_generations * 0.2)
    pso_ppx = PSOPPXSolver(generations=max_generations, population_size=pop_size, 
                           neighborhood_start_gen=ns_start, data_class=data_class)
    
    start_time = time.time()
    _, _, _ = pso_ppx.evolve()
    for _ in range(max_generations - 1):
        pso_ppx.evolve()
    pso_ppx_time = time.time() - start_time
    pso_ppx_history_hv = pso_ppx.history_hv
        
    results['K&G'] = {
        'history': kg_history_hv,
        'time': kg_time,
        'score': kg_history_hv[-1],
        'final_obj': kg.gbest_score,
        'front': kg.get_pareto_front(),
        'type': 'Selective Disassembly (HV)'
    }
    
    results['NSGA-II'] = {
        'history': nsga2_history_hv,
        'time': nsga2_time,
        'score': nsga2_history_hv[-1],
        'final_obj': nsga2.gbest_score,
        'front': nsga2.get_pareto_front(),
        'type': 'Selective Disassembly (HV)'
    }
    
    results['NSGA-II (Legacy)'] = {
        'history': nsga2_legacy_history_hv,
        'time': nsga2_legacy_time,
        'score': nsga2_legacy_history_hv[-1],
        'final_obj': nsga2_legacy.gbest_score,
        'front': nsga2_legacy.get_pareto_front(),
        'type': 'Selective Disassembly (HV)'
    }
    
    results['PSO+PPX'] = {
        'history': pso_ppx_history_hv,
        'time': pso_ppx_time,
        'score': pso_ppx_history_hv[-1],
        'final_obj': pso_ppx.gbest_score,
        'front': pso_ppx.get_pareto_front(),
        'type': 'Selective Disassembly (HV)'
    }
    
    # ==========================================
    # Prints & Plotting
    # ==========================================
    print("\n" + "="*80)
    print(f"{'Algorithm':<15} | {'Type':<28} | {'Score':<15} | {'Time (s)':<10}")
    print("-" * 80)
    
    # helper to format score
    def fmt_score(res):
        if res.get('type') == 'Selective Disassembly (HV)':
            return f"HV: {res['score']:.4f}"
        return f"{res['score']} stns"

    for name, data in results.items():
        type_str = data.get('type', 'Assembly (Stations)')
        print(f"{name:<15} | {type_str:<28} | {fmt_score(data):<15} | {data['time']:.4f}")
    print("="*80)
    
    base_dir = current_dir
    plot_comparison(results, base_dir)

def plot_comparison(results, output_dir):
    # Set Font
    import platform
    if platform.system() == 'Darwin':
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    else:
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # Split results
    assembly_algs = {k:v for k,v in results.items() if v.get('type', 'Assembly (Stations)') == 'Assembly (Stations)'}
    disassembly_algs = {k:v for k,v in results.items() if v.get('type') == 'Selective Disassembly (HV)'}
    
    # Plot 1: Assembly (Minimization)
    plt.figure(figsize=(10, 6))
    for name, data in assembly_algs.items():
        plt.plot(data['history'], label=f"{name} (Best: {data['score']})", linewidth=2)
    plt.xlabel('代數 (Generation)')
    plt.ylabel('工作站數量 (Minimization)')
    plt.title('裝配線平衡比較 (Assembly Line Balancing)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    out1 = os.path.join(output_dir, 'comparison_assembly.png')
    plt.savefig(out1, dpi=300)
    print(f"\n[1/3] 裝配線比較圖已儲存: {out1}")
    plt.close()

    # Plot 2: Disassembly (HV Maximization)
    plt.figure(figsize=(10, 6))
    for name, data in disassembly_algs.items():
        # Use Monotonic 'Best So Far' for convergence plot
        # This matches user expectation: "Didn't you draw it continuing from current best?"
        history = list(data['history'])
        if history:
            monotonic_history = np.maximum.accumulate(history)
            plt.plot(monotonic_history, label=f"{name} (Best HV: {data['score']:.4f})", linewidth=2)
        else:
             plt.plot([], label=f"{name} (No Data)")
    plt.xlabel('代數 (Generation)')
    plt.ylabel('Hypervolume (Maximization)')
    plt.title('選擇性拆解規劃 - Hypervolume 收斂比較')
    plt.legend()
    plt.grid(True, alpha=0.3)
    out2 = os.path.join(output_dir, 'comparison_hypervolume.png')
    plt.savefig(out2, dpi=300)
    print(f"[2/3] Hypervolume 比較圖已儲存: {out2}")
    plt.close()
    
    # Plot 3: Pareto Objective Space (Profit vs Carbon)
    plt.figure(figsize=(10, 6))
    
    # Draw Reference Points (Original: X=Profit, Y=Carbon)
    plt.scatter([350], [0.001], color='gold', marker='*', s=200, label='Utopia (Ideal)')
    plt.scatter([0], [100], color='gray', marker='x', s=100, label='Anti-Utopia')
    
    markers = {'NPSO': 'o', 'BlockGA': 's', 'K&G': '^', 'NSGA-II': 'D', 'NSGA-II (Legacy)': 'x', 'PSO+PPX': '*'}
    colors = {'NPSO': 'red', 'BlockGA': 'blue', 'K&G': 'green', 'NSGA-II': 'purple', 'NSGA-II (Legacy)': 'orange', 'PSO+PPX': 'brown'}
    
    for name, data in disassembly_algs.items():
        # Plot Pareto Front (Points)
        if 'front' in data and data['front'] and len(data['front']) > 0:
            # Sort by Profit (x-axis) to prevent zigzag lines
            sorted_front = sorted(data['front'], key=lambda p: p[0])
            profits = [p[0] for p in sorted_front]
            carbons = [p[1] for p in sorted_front]
            # X=Profit, Y=Carbon
            plt.scatter(profits, carbons, s=50, 
                       label=f"{name} Front",
                       marker=markers.get(name, 'o'),
                       color=colors.get(name, 'black'), alpha=0.6)
            
            # Connect them if sorted (which they are) - Original: Plot(profits, carbons)
            plt.plot(profits, carbons, color=colors.get(name, 'black'), alpha=0.3, linestyle='--')
                       
        # Highlight Best Balanced Solution
        profit, carbon = data['final_obj']
        # X=Profit, Y=Carbon
        plt.scatter(profit, carbon, s=150, 
                   # label=f"{name} Best", # Avoid cluttering legend
                   marker=markers.get(name, 'o'),
                   color=colors.get(name, 'black'), edgecolors='black', linewidth=2)
        
        # Annotate Best
        plt.annotate(f"{name}", (profit, carbon), xytext=(5, 5), textcoords='offset points', fontsize=9)

    plt.xlabel('利潤 (Profit) - Maximize')
    plt.ylabel('碳足跡 (Carbon) - Minimize')
    plt.title('選擇性拆解規劃 - 最終帕累托前沿 (Pareto Frontier)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    out3 = os.path.join(output_dir, 'comparison_pareto.png')
    plt.savefig(out3, dpi=300)
    print(f"[3/3] 帕累托解分佈圖已儲存: {out3}")
    plt.close()

    # Plot 4: Separated Pareto Plots (Subplots)
    # 6 Subplots for 6 algorithms
    fig, axes = plt.subplots(1, 6, figsize=(36, 6), sharex=False, sharey=False) 
    
    # Collect all data points to decide reasonable shared limits (zoomed in)
    all_profits = []
    all_carbons = []
    for data in disassembly_algs.values():
        if 'front' in data and data['front']:
            all_profits.extend([p[0] for p in data['front']])
            all_carbons.extend([p[1] for p in data['front']])
        elif 'final_obj' in data:
             all_profits.append(data['final_obj'][0])
             all_carbons.append(data['final_obj'][1])
             
    if not all_profits:
        all_profits = [0, 350]
        all_carbons = [0, 100]

    # Add 5% padding around the DATA
    p_min, p_max = min(all_profits), max(all_profits)
    c_min, c_max = min(all_carbons), max(all_carbons)
    
    p_range = p_max - p_min if p_max != p_min else 10
    c_range = c_max - c_min if c_max != c_min else 1
    
    # Set limits based on DATA - ORIGINAL MAPPING
    # X Limits -> Profit Range
    xlims = (p_min - p_range * 0.1, p_max + p_range * 0.1)
    # Y Limits -> Carbon Range
    ylims = (c_min - c_range * 0.1, c_max + c_range * 0.1)

    # Order: NPSO, BlockGA, K&G, NSGA-II, NSGA-II (Legacy), PSO+PPX
    alg_order = ['NPSO', 'BlockGA', 'K&G', 'NSGA-II', 'NSGA-II (Legacy)', 'PSO+PPX']
    
    for i, name in enumerate(alg_order):
        ax = axes[i]
        data = disassembly_algs.get(name)
        
        # Set limits explicitely to ignore the remote Scatter markers
        ax.set_xlim(xlims)
        ax.set_ylim(ylims)
        
        # Draw Reference Points (Original)
        ax.scatter([350], [0.001], color='gold', marker='*', s=200, label='Utopia')
        
        if data:
            if 'front' in data and data['front'] and len(data['front']) > 0:
                # Sort for clean line connection
                sorted_front = sorted(data['front'], key=lambda p: p[0])
                front_p = [p[0] for p in sorted_front]
                front_c = [p[1] for p in sorted_front]
                # X=Profit, Y=Carbon
                ax.scatter(front_p, front_c, color=colors.get(name, 'black'), s=50, label='Front')
                ax.plot(front_p, front_c, color=colors.get(name, 'black'), alpha=0.5, linestyle='--')
            
            # Best
            final_p, final_c = data['final_obj']
            # X=Profit, Y=Carbon
            ax.scatter(final_p, final_c, color=colors.get(name, 'black'), s=150, edgecolors='black', linewidth=2, label='Best')
            ax.set_title(f"{name} (HV: {data['score']:.4f})", fontsize=14, fontweight='bold', color=colors.get(name, 'black'))
        else:
            ax.set_title(f"{name} (Not Run)", fontsize=14)

        ax.grid(True, alpha=0.3)
        ax.set_xlabel('Profit ($) - Maximize') # Original Label
        if i == 0:
            ax.set_ylabel('Carbon (kg) - Minimize') # Original Label
            ax.legend(loc='best')
            
    plt.suptitle('選擇性拆解規劃 - 分離視圖 (Separated Pareto Views)', fontsize=16)
    plt.tight_layout()
    
    out4 = os.path.join(output_dir, 'comparison_pareto_separated.png')
    plt.savefig(out4, dpi=300)
    print(f"[Bonus] 分離視圖已儲存: {out4}")
    plt.close()

if __name__ == "__main__":
    run_comparison()
