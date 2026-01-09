import sys
import os

# Add parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from app.utils import data_adapter
from solvers.pso_solver import PSOSolver
import numpy as np
import time
import matplotlib.pyplot as plt

def run_pso():
    print("=== 粒子群演算法 (PSO) Workstation Minimization ===")
    
    # 1. 讀取設定檔
    # Config is in ../data/config.xlsx
    config_path = os.path.join(parent_dir, 'data', 'config.xlsx')
    
    print(f"1. Loading parameters from {config_path}...")
    loader = data_adapter.ConfigLoader(config_path)
    config = loader.load_config()
    
    num_jobs = int(config['NUM_JOBS'])
    pop_size = int(config['POPULATION_SIZE']) # Correct key
    constraints = config['CONSTRAINTS']
    time_info = config['TIME_INFO']
    cycle_time = config['CYCLE_TIME']
    
    print(f"   - Jobs: {num_jobs}")
    print(f"   - Cycle Time: {cycle_time}")
    print(f"   - Population (Swarm Size): {pop_size}")
    
    # 2. 初始化 PSO
    print("2. Initializing PSO Solver...")
    pso = PSOSolver(
        num_jobs=num_jobs, 
        pop_size=pop_size,
        constraints=constraints, 
        time_info=time_info, 
        cycle_time=cycle_time,
        w=0.7, c1=2.0, c2=2.0
    )
    
    # 3. 執行優化 loop
    generations = int(config['MAX_GENERATIONS']) # Correct key & cast to int
    print(f"3. Running Optimization for {generations} generations...")
    
    start_time = time.time() # Start timer
    best_stations_history = []
    
    for gen in range(generations):
        best_perm, best_score = pso.evolve()
        best_stations_history.append(best_score)
        
        # 每 10 代印出一次進度
        if (gen + 1) % 10 == 0:
            print(f"   Gen {gen+1}: Best Stations = {best_score}")
            
    end_time = time.time() # End timer
    execution_time = end_time - start_time
            
    # 4. 輸出最終結果
    final_solution, final_stations = pso.gbest_permutation, pso.gbest_score
    print("-" * 30)
    print("Optimization Completed!")
    print(f"Global Best Stations: {final_stations}")
    print(f"Best Chromosome (Job Sequence): {final_solution}")
    print(f"Execution Time: {execution_time:.4f} seconds")
    
    # 簡單驗證
    recalc = pso.calculate_stations(final_solution)
    print(f"Verify calculation: {recalc}")

    # 5. 繪製收斂圖
    plot_convergence(best_stations_history, "Particle Swarm Optimization (PSO)", "convergence_pso.png")

def plot_convergence(history, title, filename):
    """
    繪製收斂曲線並存檔。
    """
    import platform
    system_name = platform.system()
    if system_name == 'Darwin':
        plt.rcParams['font.sans-serif'] = ['PingFang HK', 'PingFang SC', 'Arial Unicode MS']
    elif system_name == 'Windows':
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.figure(figsize=(10, 6))
    plt.plot(history, label='Best Stations')
    plt.xlabel('Generation')
    plt.ylabel('Station Count')
    plt.title(f'Convergence - {title}')
    plt.legend()
    plt.grid(True)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, filename)
    plt.savefig(file_path)
    print(f"收斂圖已儲存至: {file_path}")
    plt.close()

if __name__ == "__main__":
    run_pso()
