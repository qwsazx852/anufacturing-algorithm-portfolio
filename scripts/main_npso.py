
import sys
import os

# Add parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from solvers.npso_solver import NPSOSolver
import time
import matplotlib.pyplot as plt

def run_npso():
    print("=== NPSO (多目標) 拆解線平衡優化演算法 ===")
    print("目標產品: 釘書機 (n=18)")
    print("優化目標: 1. 極大化利潤 (Profit)  2. 極小化碳足跡 (Carbon)")
    
    # 1. Initialize Saver
    # Default settings from MATLAB: Pop=100, Gen=100 (or 1000)
    generations = 100 
    npso = NPSOSolver(
        num_particles=100,
        generations=generations,
        w=0.8, c1=0.5, c2=0.5
    )
    
    print(f"2. 開始執行優化 (共 {generations} 代)...")
    
    start_time = time.time()
    
    history_metrics = [] # Profit, Carbon, HV
    
    for gen in range(generations):
        best_perm, (best_profit, best_carbon), cut_idx = npso.evolve() # Unpack 3 values
        current_hv = npso.history_hv[-1]
        
        history_metrics.append((best_profit, best_carbon, current_hv))
        
        if (gen + 1) % 10 == 0:
            print(f"   第 {gen+1} 代: 利潤={best_profit:.2f}, 碳足跡={best_carbon:.4f}, HV={current_hv:.4f}")
            
    end_time = time.time()
    
    # 3. Final Results
    final_perm, (f1, f2), best_cut = npso.gbest_permutation, npso.gbest_score, npso.gbest_cut_index
    
    disassembled = final_perm[:best_cut]
    remaining = final_perm[best_cut:]
    
    print("-" * 30)
    print("優化完成 (Optimization Completed)!")
    print(f"最佳利潤 (Best Profit): {f1:.2f}")
    print(f"最佳碳足跡 (Best Carbon): {f2:.4f}")
    print(f"Hypervolume (近似值): {npso.history_hv[-1]:.4f}")
    
    print("\n[最佳選擇性拆裝規劃 (Optimal Selective Disassembly Plan)]")
    print(f"建議中止點: 拆解第 {best_cut} 個零件後停止")
    print(f"執行拆解 ({len(disassembled)}): {disassembled}")
    print(f"保留/丟棄 ({len(remaining)}):       {remaining}")
    
    print(f"\n執行時間: {end_time - start_time:.4f} 秒")
    
    # 4. Plotting
    plot_npso_results(history_metrics, "NPSO 拆解線平衡優化")

def plot_npso_results(history, title):
    import platform
    system_name = platform.system()
    if system_name == 'Darwin':
        plt.rcParams['font.sans-serif'] = ['PingFang HK', 'PingFang SC', 'Arial Unicode MS']
    elif system_name == 'Windows':
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei']
    plt.rcParams['axes.unicode_minus'] = False # Fix minus sign

    profit = [h[0] for h in history]
    carbon = [h[1] for h in history]
    hv = [h[2] for h in history]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    
    # Plot 1: Objectives Convergence
    ax1.plot(profit, label='利潤 (Profit - Maximize)', color='blue')
    ax1.set_ylabel('利潤 (Profit)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    
    ax1_twin = ax1.twinx()
    ax1_twin.plot(carbon, label='碳足跡 (Carbon - Minimize)', color='red', linestyle='--')
    ax1_twin.set_ylabel('碳足跡 (Carbon Footprint)', color='red')
    ax1_twin.tick_params(axis='y', labelcolor='red')
    
    ax1.set_title(f'{title} - 目標函數收斂圖')
    ax1.set_xlabel('代數 (Generation)')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Hypervolume
    ax2.plot(hv, label='Hypervolume (Quality)', color='green')
    ax2.set_title(f'{title} - Hypervolume 指標')
    ax2.set_xlabel('代數 (Generation)')
    ax2.set_ylabel('Hypervolume (Dominated Ratio)')
    ax2.grid(True)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(base_dir, 'convergence_npso.png')
    plt.savefig(output_path)
    print(f"Convergence plot saved to: {output_path}")
    plt.close()

if __name__ == "__main__":
    run_npso()
