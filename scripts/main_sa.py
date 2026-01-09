import sys
import os

# Add parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from app.utils import data_adapter
from solvers.sa_solver import SASolver
import numpy as np
import time
import matplotlib.pyplot as plt

def run_sa():
    print("=== 模擬退火 (Simulated Annealing) Workstation Minimization ===")
    
    # 1. 讀取設定檔
    # Config is in ../data/config.xlsx
    config_path = os.path.join(parent_dir, 'data', 'config.xlsx')
    
    print(f"1. Loading parameters from {config_path}...")
    loader = data_adapter.ConfigLoader(config_path)
    config = loader.load_config()
    
    num_jobs = int(config['NUM_JOBS'])
    constraints = config['CONSTRAINTS']
    time_info = config['TIME_INFO']
    cycle_time = config['CYCLE_TIME']
    
    # SA Parameters
    # 這些通常需要調整，我們設定一組經驗值
    initial_temp = 1000.0
    cooling_rate = 0.99
    stopping_temp = 0.1
    # 估計迭代次數用於印出
    # iterations = log(stopping / initial) / log(cooling)
    estimated_iter = int(np.log(stopping_temp / initial_temp) / np.log(cooling_rate))
    
    print(f"   - Jobs: {num_jobs}")
    print(f"   - Cycle Time: {cycle_time}")
    print(f"   - Initial Temp: {initial_temp}")
    print(f"   - Cooling Rate: {cooling_rate}")
    
    # 2. 初始化 SA Solver
    print("2. Initializing SA Solver...")
    sa = SASolver(
        num_jobs=num_jobs, 
        constraints=constraints, 
        time_info=time_info, 
        cycle_time=cycle_time,
        initial_temp=initial_temp,
        cooling_rate=cooling_rate,
        stopping_temp=stopping_temp
    )
    
    # 3. 執行優化 loop
    print(f"3. Running Optimization (~{estimated_iter} iterations)...")
    
    start_time = time.time() # Start timer
    best_stations_history = []
    
    iter_count = 0
    while sa.temp > sa.stopping_temp:
        iter_count += 1
        current_best_score, current_temp = sa.step()
        best_stations_history.append(current_best_score)
        
        # 每 100 代印出一次進度
        if iter_count % 100 == 0:
            print(f"   Iter {iter_count}: Temp = {current_temp:.2f}, Best Stations = {current_best_score}")
            
    end_time = time.time() # End timer
    execution_time = end_time - start_time
            
    # 4. 輸出最終結果
    final_solution = sa.best_solution
    final_stations = sa.best_fitness
    
    print("-" * 30)
    print("Optimization Completed!")
    print(f"Total Iterations: {iter_count}")
    print(f"Global Best Stations: {final_stations}")
    print(f"Best Solution (Job Sequence): {final_solution}")
    print(f"Execution Time: {execution_time:.4f} seconds")
    
    # 驗證
    recalc = sa.calculate_stations(final_solution)
    print(f"Verify calculation: {recalc}")

    # 5. 繪製收斂圖
    plot_convergence(best_stations_history, "Simulated Annealing (SA)", "convergence_sa.png")

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
    run_sa()
