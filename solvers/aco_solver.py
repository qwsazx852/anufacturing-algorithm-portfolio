import random
import numpy as np
from typing import List, Tuple, Set

class ACOSolver:
    """
    蟻群演算法 (ACO) 優化器 - 用於解決工作站最小化問題。
    特色：螞蟻在建構解的過程中，只會選擇符合優先順序限制 (Precedence Constraints) 的作業，
    保證產生的解皆為可行解，無需修復機制。
    """
    def __init__(self, num_jobs: int, num_ants: int, 
                 constraints: List[Tuple[int, int]], time_info: List[int], cycle_time: int,
                 alpha: float = 1.0, beta: float = 2.0, rho: float = 0.1, q: float = 1.0):
        """
        Args:
            num_jobs: 作業數量
            num_ants: 螞蟻數量 (通常設為與作業數相當或更多)
            constraints: 優先順序限制 (pre, suc) - 1-based
            time_info: 每個作業的時間 - 0-based index
            cycle_time: 週期時間 (GCT)
            alpha: 費洛蒙重要性 (Phromone Weight)
            beta: 啟發式資訊重要性 (Heuristic Weight)
            rho: 費洛蒙揮發率 (Evaporation Rate)
            q: 費洛蒙強度常數
        """
        self.num_jobs = num_jobs
        self.num_ants = num_ants
        self.time_info = time_info
        self.cycle_time = cycle_time
        
        # Hyperparameters
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q
        
        # 建立前置作業列表 (Predecessors List) - 用於快速檢查限制
        # predecessors[j] = {i, k, ...} 表示作業 j 需要先完成 i, k...
        # 轉成 0-based
        self.predecessors = [set() for _ in range(num_jobs)]
        for pre, suc in constraints:
            self.predecessors[suc - 1].add(pre - 1)
            
        # Pheromone Matrix (NxN)
        # tau[i][j] 表示從作業 i 接續做作業 j 的費洛蒙濃度
        # 初始值設為一個小常數
        self.pheromones = np.full((num_jobs, num_jobs), 1.0)
        
        # Global Best
        self.gbest_sequence = None
        self.gbest_fitness = float('inf')

    def calculate_stations(self, sequence: List[int]) -> int:
        """計算工作站數量 (Fitness Function)"""
        current_sum = 0
        stations = 1
        for job in sequence: # job is 0-based here
            job_time = self.time_info[job]
            current_sum += job_time
            if current_sum > self.cycle_time:
                current_sum = job_time 
                stations += 1
        return stations

    def _select_next_job(self, current_job: int, available_candidates: List[int]) -> int:
        """
        根據費洛蒙與啟發式資訊選擇下一個作業 (Roulette Wheel)。
        """
        if not available_candidates:
            return None
            
        probabilities = []
        denom = 0.0
        
        # Heuristic (eta): 這裡簡單用 1.0，也可以改成 (1 / time) 或其他貪婪規則
        # Advanced ACO often uses heuristic related to the problem greedy logic
        eta = 1.0 
        
        for job in available_candidates:
            # 如果是第一個作業 (current_job is None)，假設來自虛擬節點或平均分佈
            if current_job is None:
                tau = 1.0 # 初始均勻
            else:
                tau = self.pheromones[current_job][job]
                
            prob = (tau ** self.alpha) * (eta ** self.beta)
            probabilities.append(prob)
            denom += prob
            
        if denom == 0:
            # 避免除以零，平均分配
            return random.choice(available_candidates)
            
        probabilities = [p / denom for p in probabilities]
        
        # 輪盤選擇
        return np.random.choice(available_candidates, p=probabilities)

    def construct_solution(self) -> Tuple[List[int], int]:
        """
        單隻螞蟻建構解的過程。
        Returns: (sequence, fitness)
        """
        sequence = []
        completed = set()
        
        # 初始候選集 (沒有前置作業的工作)
        # 注意：每次選擇後，可能會有新的工作解鎖，所以要在迴圈內動態檢查
        # 優化：indegree 方式可能更快，但 N=18 用集合檢查這還可以
        
        for _ in range(self.num_jobs):
            # 1. Find valid candidates
            candidates = []
            for j in range(self.num_jobs):
                if j not in completed:
                    # 檢查 j 的所有前置作業是否都在 completed 中
                    if self.predecessors[j].issubset(completed):
                        candidates.append(j)
            
            # 2. Select next job
            last_job = sequence[-1] if sequence else None
            next_job = self._select_next_job(last_job, candidates)
            
            sequence.append(next_job)
            completed.add(next_job)
            
        fitness = self.calculate_stations(sequence)
        return sequence, fitness

    def evolve(self) -> Tuple[List[int], int]:
        """
        執行一代ACO迭代。
        1. 讓所有螞蟻建構解
        2. 更新全域最佳解
        3. 更新費洛蒙 (揮發 + 堆積)
        """
        # 1. Construct Solutions
        iteration_solutions = []
        
        iteration_best_seq = None
        iteration_best_fit = float('inf')
        
        for _ in range(self.num_ants):
            seq, fitness = self.construct_solution()
            iteration_solutions.append((seq, fitness))
            
            if fitness < iteration_best_fit:
                iteration_best_fit = fitness
                iteration_best_seq = seq
                
            if fitness < self.gbest_fitness:
                self.gbest_fitness = fitness
                self.gbest_sequence = seq[:]
        
        # 2. Update Pheromones
        # (1) Evaporation
        self.pheromones *= (1.0 - self.rho)
        
        # (2) Deposition
        # 這裡採用 Max-Min Ant System (MMAS) 概念，只讓表現好的螞蟻留下費洛蒙
        # 可以是 Iteration Best 或 Global Best
        # 這裡混合：加強 Global Best 路徑
        
        if self.gbest_sequence:
            reward = self.q / self.gbest_fitness
            for i in range(self.num_jobs - 1):
                u = self.gbest_sequence[i]
                v = self.gbest_sequence[i+1]
                self.pheromones[u][v] += reward
                
        # 轉成 1-based 回傳給使用者看
        gbest_1based = [x + 1 for x in self.gbest_sequence]
        return gbest_1based, self.gbest_fitness
