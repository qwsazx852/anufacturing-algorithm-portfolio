import sys
import os

# Add parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from app.utils import data_adapter
from solvers.aco_solver import ACOSolver
import numpy as np
import time
import matplotlib.pyplot as plt

def run_aco():
    print("=== 蟻群演算法 (ACO) Workstation Minimization ===")
    
    # 1. 讀取設定檔
    # Config is in ../data/config.xlsx
    config_path = os.path.join(parent_dir, 'data', 'config.xlsx')
    
    print(f"1. Loading parameters from {config_path}...")
    loader = data_adapter.ConfigLoader(config_path)
    config = loader.load_config()
    
    num_jobs = int(config['NUM_JOBS'])
    # ACO 通常需要較多螞蟻才能有好的探索效果
    num_ants = 50 # 或 int(config['POPULATION_SIZE'])
    constraints = config['CONSTRAINTS']
    time_info = config['TIME_INFO']
    cycle_time = config['CYCLE_TIME']
    
    print(f"   - Jobs: {num_jobs}")
    print(f"   - Cycle Time: {cycle_time}")
    print(f"   - Ants: {num_ants}")
    
    # 2. 初始化 ACO Solver
    print("2. Initializing ACO Solver...")
    aco = ACOSolver(
        num_jobs=num_jobs, 
        num_ants=num_ants,
        constraints=constraints, 
        time_info=time_info, 
        cycle_time=cycle_time,
        alpha=1.0, beta=2.0, rho=0.1, q=10.0
    )
    
    # 3. 執行優化 loop
    generations = int(config['MAX_GENERATIONS'])
    print(f"3. Running Optimization for {generations} iterations...")
    
    start_time = time.time() # Start timer
    best_stations_history = []
    
    for gen in range(generations):
        best_perm, best_score = aco.evolve()
        best_stations_history.append(best_score)
        
        # 每 10 代印出一次進度
        if (gen + 1) % 10 == 0:
            print(f"   Iter {gen+1}: Best Stations = {best_score}")

    end_time = time.time() # End timer
    execution_time = end_time - start_time
            
    # 4. 輸出最終結果
    # 注意: best_perm 已經是 1-based
    final_solution, final_stations = aco.gbest_sequence, aco.gbest_fitness
    # 這裡 gbest_sequence 內部是 0-based，但 evolve 回傳的是 1-based
    # 我們直接拿 evolve 最後一次回傳的雖然是指 "本代最佳"，但 ACOSolver 物件內有存 gbest
    
    # 重新獲取 global best (1-based)
    final_solution_1based = [x + 1 for x in aco.gbest_sequence]
    
    print("-" * 30)
    print("Optimization Completed!")
    print(f"Global Best Stations: {final_stations}")
    print(f"Best Ant Path (Job Sequence): {final_solution_1based}")
    print(f"Execution Time: {execution_time:.4f} seconds")
    
    # 簡單驗證
    # calculate_stations 需要 0-based input
    recalc = aco.calculate_stations(aco.gbest_sequence)
    print(f"Verify calculation: {recalc}")

    # 5. 繪製收斂圖
    plot_convergence(best_stations_history, "Ant Colony Optimization (ACO)", "convergence_aco.png")

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
    plt.xlabel('Iteration')
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
    run_aco()
