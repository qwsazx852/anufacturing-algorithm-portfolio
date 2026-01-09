import sys
import os

# Add parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from solvers.ga_solver import GeneticOptimizer
from app.utils.data_adapter import ConfigLoader
import numpy as np
import time
import matplotlib.pyplot as plt

# ==========================================
# Configuration Loading /讀取外部設定
# ==========================================
# Config is in ../data/config.xlsx
CONFIG_FILE = os.path.join(parent_dir, "data", "config.xlsx")

def load_settings():
    """
    嘗試從 Excel 讀取設定，如果檔案不存在則使用預設值 (Fall-back)。
    """
    if os.path.exists(CONFIG_FILE):
        print(f"發現設定檔 '{CONFIG_FILE}'，正在讀取...")
        loader = ConfigLoader(CONFIG_FILE)
        config = loader.load_config()
        return config
    else:
        print(f"警告：找不到 '{CONFIG_FILE}'，將使用程式內建預設值。")
        # 預設值 (Hardcoded fallback)
        return {
            "NUM_JOBS": 18,
            "POPULATION_SIZE": 100,
            "MAX_GENERATIONS": 100,
            "CROSSOVER_RATE": 0.8,
            "MUTATION_RATE": 0.1,
            "CONSTRAINTS": [
                (3, 2), (3, 1), (4, 5), (4, 8), (5, 7), (5, 6),
                (6, 9), (7, 9), (8, 6), (10, 12), (11, 12), (13, 12),
                (14, 1), (14, 4), (15, 12), (16, 15), (17, 15),
                (18, 10), (18, 11), (18, 13)
            ]
        }

def main():
    """
    主程式執行入口。
    """
    # 1. 載入設定 (Load Configuration)
    config = load_settings()
    
    # 從設定字典中提取參數
    NUM_JOBS = int(config["NUM_JOBS"])
    POPULATION_SIZE = int(config["POPULATION_SIZE"])
    MAX_GENERATIONS = int(config["MAX_GENERATIONS"])
    CROSSOVER_RATE = float(config["CROSSOVER_RATE"])
    MUTATION_RATE = float(config.get("MUTATION_RATE", 0.1)) # 若設定檔沒寫，預設 0.1
    CONSTRAINTS = config["CONSTRAINTS"]
    
    # 從設定檔讀取時間資訊與週期時間
    # 若 config 中沒有 TIME_INFO，則給空列表或預設值（這裡假設 data_adapter 會處理好）
    TIME_INFO = config.get("TIME_INFO", [])
    CYCLE_TIME = int(config.get("CYCLE_TIME", 20))
    print(f"開始遺傳演算法優化... 作業數: {NUM_JOBS}, 族群大小: {POPULATION_SIZE}")
    print(f"限制條件數量: {len(CONSTRAINTS)}")
    print(f"週期時間 (GCT): {CYCLE_TIME}")
    
    # 2. 實例化優化器 (Instantiate the Optimizer)
    optimizer = GeneticOptimizer(
        num_jobs=NUM_JOBS,
        pop_size=POPULATION_SIZE,
        crossover_rate=CROSSOVER_RATE,
        mutation_rate=MUTATION_RATE,
        constraints=CONSTRAINTS,
        time_info=TIME_INFO,
        cycle_time=CYCLE_TIME
    )
    
    # 3. 初始化族群 (Initialize Population)
    print("初始化並修復族群中...")
    optimizer.initialize_population()
    
    initial_pop = optimizer.get_population()
    print("\n初始族群範例 (前 5 個):")
    print(np.array(initial_pop[:5])) 
    
    # 4. 演化迴圈 (Evolution Loop)
    print(f"\n開始演化 {MAX_GENERATIONS} 代 ...")
    
    start_time = time.time() # Start timer
    
    global_best_stations = float('inf')
    global_best_chromosome = None
    
    history_best_stations = []
    
    for generation in range(MAX_GENERATIONS):
        best_chromosome, best_stations = optimizer.evolve()
        
        # 更新全域最佳解
        if best_stations < global_best_stations:
            global_best_stations = best_stations
            global_best_chromosome = best_chromosome
            print(f"Generation {generation+1}: New Best Stations = {global_best_stations}")
            
        history_best_stations.append(global_best_stations)
            
    end_time = time.time() # End timer
    execution_time = end_time - start_time
            
    # 5. 結果 (Results)
    print("-" * 30)
    print("優化完成 (Optimization Complete)。")
    print(f"Global Best Stations: {global_best_stations}")
    print(f"Global Best Chromosome: \n{np.array(global_best_chromosome)}")
    print(f"Execution Time: {execution_time:.4f} seconds")

    # 6. 繪製收斂圖 (Plotting)
    plot_convergence(history_best_stations, "Genetic Algorithm (GA)", "convergence_ga.png")

def plot_convergence(history, title, filename):
    """
    繪製收斂曲線並存檔。
    """
    # 設定中文字型 (macOS: PingFang / Windows: Microsoft JhengHei)
    import platform
    system_name = platform.system()
    if system_name == 'Darwin':  # macOS
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
    
    # Save to the same directory as the script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, filename)
    plt.savefig(file_path)
    print(f"收斂圖已儲存至: {file_path}")
    plt.close()

if __name__ == "__main__":
    main()
