import random
import numpy as np
from typing import List, Tuple, Optional

class PSOSolver:
    """
    粒子群演算法 (PSO) 優化器 - 用於解決工作站最小化問題。
    使用 SPV (Smallest Position Value) 規則將連續的粒子位置轉換為離散的作業排序。
    """
    def __init__(self, num_jobs: int, pop_size: int, 
                 constraints: List[Tuple[int, int]], time_info: List[int], cycle_time: int,
                 w: float = 0.7, c1: float = 2.0, c2: float = 2.0):
        """
        初始化 PSO 優化器。
        Args:
            num_jobs: 作業數量
            pop_size: 粒子數量 (Swarm Size)
            constraints: 優先順序限制 (pre, suc)
            time_info: 每個作業的時間
            cycle_time: 週期時間 (GCT)
            w: 慣性權重 (Inertia Weight)
            c1: 自我認知參數 (Cognitive Parameter)
            c2: 社會認知參數 (Social Parameter)
        """
        self.num_jobs = num_jobs
        self.pop_size = pop_size
        self.time_info = time_info
        self.cycle_time = cycle_time
        self.w = w
        self.c1 = c1
        self.c2 = c2
        
        # 建立 Precedence Matrix (copied from GeneticOptimizer)
        self.precedence_matrix = self._build_transitive_closure(constraints, num_jobs)
        
        # PSO State
        # Position X: [pop_size, num_jobs] (Continuous)
        # Velocity V: [pop_size, num_jobs] (Continuous)
        self.X = np.random.uniform(-10, 10, size=(pop_size, num_jobs))
        self.V = np.random.uniform(-1, 1, size=(pop_size, num_jobs))
        
        # Personal Best
        self.pbest_X = self.X.copy()
        self.pbest_scores = np.full(pop_size, float('inf')) # Minimize stations
        
        # Global Best
        self.gbest_X = None
        self.gbest_score = float('inf')
        self.gbest_permutation = None

    def _build_transitive_closure(self, constraints: List[Tuple[int, int]], num_nodes: int) -> np.ndarray:
        """建立可達性矩陣 (同 GA)"""
        matrix = np.zeros((num_nodes, num_nodes), dtype=int)
        for pre, suc in constraints:
            matrix[pre - 1, suc - 1] = 1
        for k in range(num_nodes):
            for i in range(num_nodes):
                for j in range(num_nodes):
                    if matrix[i, k] and matrix[k, j]:
                        matrix[i, j] = 1
        return matrix

    def _decode_position(self, x_vector: np.ndarray) -> List[int]:
        """
        SPV Rule: 將連續位置向量轉換為排列。
        數值越小，優先順序越高 (argsort)。
        Returns: 1-based permutation list.
        """
        # argsort 回傳的是 0-based index，我們需要 +1 變成作業編號
        permutation = list(np.argsort(x_vector) + 1)
        return permutation

    def _repair_chromosome(self, chromosome: List[int]) -> List[int]:
        """修復排列以滿足優先順序限制 (同 GA)"""
        n = len(chromosome)
        seq = chromosome[:] 
        for i in range(n):
            for j in range(i + 1, n):
                job_prior = seq[i]
                job_later = seq[j]
                if self.precedence_matrix[job_later - 1, job_prior - 1] == 1:
                    seq[i], seq[j] = seq[j], seq[i]
                    job_prior = seq[i] 
        return seq

    def calculate_stations(self, chromosome: List[int]) -> int:
        """計算工作站數量 (Fitness Function)"""
        current_sum = 0
        stations = 1
        for job in chromosome:
            job_time = self.time_info[job - 1]
            current_sum += job_time
            if current_sum > self.cycle_time:
                current_sum = job_time 
                stations += 1
        return stations

    def evolve(self) -> Tuple[List[int], int]:
        """
        執行一步 PSO 迭代。
        Returns: (global_best_permutation, global_best_score)
        """
        # 1. Update Fitness & Best
        for i in range(self.pop_size):
            # Decode Position -> Permutation
            perm = self._decode_position(self.X[i])
            
            # Repair (Optionally update X to match repaired perm? No, std SPV doesn't)
            # 但為了正確評估，我們必須評估修復後的解
            repaired_perm = self._repair_chromosome(perm)
            
            # Evaluate
            score = self.calculate_stations(repaired_perm)
            
            # Update Personal Best
            if score < self.pbest_scores[i]:
                self.pbest_scores[i] = score
                self.pbest_X[i] = self.X[i].copy()
                
            # Update Global Best
            if score < self.gbest_score:
                self.gbest_score = score
                self.gbest_X = self.X[i].copy()
                self.gbest_permutation = repaired_perm[:]
                
        # 2. Update Velocity and Position
        r1 = np.random.rand(self.pop_size, self.num_jobs)
        r2 = np.random.rand(self.pop_size, self.num_jobs)
        
        # V = w*V + c1*r1*(pbest - X) + c2*r2*(gbest - X)
        self.V = (self.w * self.V + 
                  self.c1 * r1 * (self.pbest_X - self.X) + 
                  self.c2 * r2 * (self.gbest_X - self.X))
        
        # X = X + V
        self.X = self.X + self.V
        
        return self.gbest_permutation, self.gbest_score
