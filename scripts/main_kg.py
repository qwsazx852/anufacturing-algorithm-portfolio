
import sys
import os
import time
import matplotlib.pyplot as plt

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solvers.kg_solver import KGSolver

def run_kg():
    print("=== K&G (Kang & GA) 選擇性拆解規劃優化 (Selective Disassembly Planning) ===")
    print("目標: Stapler (n=18)")
    print("特色: PPX (Precedence Preserving Crossover) 保持優先權關係")
    
    generations = 20
    solver = KGSolver(
        population_size=100,
        generations=generations,
        crossover_rate=0.7,
        mutation_rate=0.9
    )
    
    print(f"2. 開始執行優化 (共 {generations} 代)...")
    
    start_time = time.time()
    history_metrics = [] # Profit, Carbon, HV
    
    for gen in range(generations):
        best_perm, (best_profit, best_carbon), cut_idx = solver.evolve()
        current_hv = solver.history_hv[-1]
        
        history_metrics.append((best_profit, best_carbon, current_hv))
        
        if (gen + 1) % 10 == 0:
            print(f"   第 {gen+1} 代: 利潤={best_profit:.2f}, 碳足跡={best_carbon:.4f}, HV={current_hv:.4f}")
            
    end_time = time.time()
    
    final_perm, (f1, f2), best_cut = solver.gbest_permutation, solver.gbest_score, solver.gbest_cut_index
    
    disassembled = final_perm[:best_cut]
    remaining = final_perm[best_cut:]
    
    print("-" * 30)
    print("優化完成 (Optimization Completed)!")
    print(f"最佳利潤: {f1:.2f}")
    print(f"最佳碳足跡: {f2:.4f}")
    print(f"Hypervolume: {solver.history_hv[-1]:.4f}")
    
    print("\n[最佳選擇性拆裝規劃]")
    print(f"建議中止點: 拆解第 {best_cut} 個零件後停止")
    print(f"執行拆解 ({len(disassembled)}): {disassembled}")
    print(f"保留/丟棄 ({len(remaining)}):       {remaining}")
    
    print(f"\n執行時間: {end_time - start_time:.4f} 秒")
    
    plot_results(history_metrics, "K&G (PPX) 拆解優化")

def plot_results(history, title):
    import platform
    if platform.system() == 'Darwin':
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    else:
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    profit = [x[0] for x in history]
    carbon = [x[1] for x in history]
    hv = [x[2] for x in history]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    
    ax1.plot(profit, label='利潤 (Profit)', color='blue')
    ax1.set_ylabel('利潤', color='blue')
    ax1_twin = ax1.twinx()
    ax1_twin.plot(carbon, label='碳足跡 (Carbon)', color='red', linestyle='--')
    ax1_twin.set_ylabel('碳足跡', color='red')
    ax1.set_title(f'{title} - 收斂圖')
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(hv, label='Hypervolume', color='green')
    ax2.set_title('Hypervolume 指標')
    ax2.set_xlabel('代數')
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('scripts/convergence_kg.png')
    print("圖表已儲存至 scripts/convergence_kg.png")

if __name__ == "__main__":
    run_kg()
