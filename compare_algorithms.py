import data_adapter
from ga_solver import GeneticOptimizer
from pso_solver import PSOSolver
from aco_solver import ACOSolver
from sa_solver import SASolver
import numpy as np
import os
import time
import matplotlib.pyplot as plt

def run_comparison():
    print("=== Algorithm Comparison: GA vs PSO vs ACO vs SA ===")
    
    # 1. Load Config
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, 'config.xlsx')
    
    loader = data_adapter.ConfigLoader(config_path)
    config = loader.load_config()
    
    # Common Parameters
    num_jobs = int(config['NUM_JOBS'])
    constraints = config['CONSTRAINTS']
    time_info = config['TIME_INFO']
    cycle_time = config['CYCLE_TIME']
    pop_size = int(config['POPULATION_SIZE'])
    max_generations = int(config['MAX_GENERATIONS'])
    
    results = {} # Store (history, time, final_score)
    
    # ==========================================
    # 1. Genetic Algorithm (GA)
    # ==========================================
    print("\n[1/4] Running GA...")
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
    print("[2/4] Running PSO...")
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
    print("[3/4] Running ACO...")
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
    print("[4/4] Running SA...")
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
    # Prints & Plotting
    # ==========================================
    print("\n" + "="*40)
    print(f"{'Algorithm':<10} | {'Score':<5} | {'Time (s)':<10} | {'Iterations':<5}")
    print("-" * 40)
    for name, data in results.items():
        print(f"{name:<10} | {data['score']:<5} | {data['time']:.4f}     | {len(data['history']):<5}")
    print("="*40)
    
    plot_comparison(results, base_dir)

def plot_comparison(results, output_dir):
    # Set Font
    import platform
    system_name = platform.system()
    if system_name == 'Darwin':
        plt.rcParams['font.sans-serif'] = ['PingFang HK', 'PingFang SC', 'Arial Unicode MS']
    elif system_name == 'Windows':
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    plt.figure(figsize=(12, 8))
    
    # Define styles for distinction
    styles = {
        'GA': {'color': 'blue', 'linestyle': '-', 'linewidth': 2},
        'PSO': {'color': 'red', 'linestyle': '--', 'linewidth': 2},
        'ACO': {'color': 'green', 'linestyle': '-.', 'linewidth': 2},
        'SA': {'color': 'purple', 'linestyle': ':', 'linewidth': 2}
    }
    
    for name, data in results.items():
        history = data['history']
        plt.plot(history, label=f"{name} (Best: {data['score']})", **styles.get(name, {}))
        
    plt.xlabel('Iteration / Generation')
    plt.ylabel('Best Station Count')
    plt.title('Algorithm Convergence Comparison')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Determine safe y-limits (zoomed in to interest area)
    all_scores = [x for res in results.values() for x in res['history']]
    if all_scores:
        plt.ylim(min(all_scores) - 0.5, min(all_scores) + 5)
    
    output_path = os.path.join(output_dir, 'convergence_comparison.png')
    plt.savefig(output_path, dpi=300)
    print(f"\nCombined plot saved to: {output_path}")
    plt.close()

if __name__ == "__main__":
    run_comparison()
