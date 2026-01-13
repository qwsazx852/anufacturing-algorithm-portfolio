import random
import numpy as np
import math
from typing import List, Tuple, Optional

class SASolver:
    """
    模擬退火 (Simulated Annealing) 優化器 - 用於解決工作站最小化問題。
    特色：透過接受「變差」的解來跳出局部最佳解 (Local Optima)。
    """
    def __init__(self, num_jobs: int, 
                 constraints: List[Tuple[int, int]], time_info: List[int], cycle_time: int,
                 initial_temp: float = 1000.0, cooling_rate: float = 0.995, stopping_temp: float = 0.01):
        """
        Args:
            num_jobs: 作業數量
            constraints: 優先順序限制 (pre, suc)
            time_info: 每個作業的時間
            cycle_time: 週期時間 (GCT)
            initial_temp: 初始溫度
            cooling_rate: 冷卻率 (alpha)
            stopping_temp: 停止溫度
        """
        self.num_jobs = num_jobs
        self.time_info = time_info
        self.cycle_time = cycle_time
        
        # SA parameters
        self.temp = initial_temp
        self.cooling_rate = cooling_rate
        self.stopping_temp = stopping_temp
        
        # 建立 Precedence Matrix (copied from GA/PSO)
        self.precedence_matrix = self._build_transitive_closure(constraints, num_jobs)
        
        # Current State
        self.current_solution = self._initial_solution() # 1-based
        self.current_fitness = self.calculate_stations(self.current_solution)
        
        # Best State
        self.best_solution = self.current_solution[:]
        self.best_fitness = self.current_fitness
        
    def _build_transitive_closure(self, constraints: List[Tuple[int, int]], num_nodes: int) -> np.ndarray:
        """建立可達性矩陣"""
        matrix = np.zeros((num_nodes, num_nodes), dtype=int)
        for pre, suc in constraints:
            matrix[pre - 1, suc - 1] = 1
        for k in range(num_nodes):
            for i in range(num_nodes):
                for j in range(num_nodes):
                    if matrix[i, k] and matrix[k, j]:
                        matrix[i, j] = 1
        return matrix

    def _repair_chromosome(self, chromosome: List[int]) -> List[int]:
        """修復排列以滿足優先順序限制"""
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

    def _initial_solution(self) -> List[int]:
        """產生隨機並修復過的初始解"""
        perm = list(np.random.permutation(self.num_jobs) + 1)
        return self._repair_chromosome(perm)

    def calculate_stations(self, chromosome: List[int]) -> int:
        """計算工作站數量 (Objective Function)"""
        current_sum = 0
        stations = 1
        for job in chromosome:
            job_time = self.time_info[job - 1]
            current_sum += job_time
            if current_sum > self.cycle_time:
                current_sum = job_time 
                stations += 1
        return stations

    def get_neighbor(self, current: List[int]) -> List[int]:
        """
        產生鄰居解 (Neighbor)：隨機交換兩個工作並修復。
        """
        neighbor = current[:]
        n = self.num_jobs
        
        # Random Swap
        idx1, idx2 = random.sample(range(n), 2)
        neighbor[idx1], neighbor[idx2] = neighbor[idx2], neighbor[idx1]
        
        # Repair
        return self._repair_chromosome(neighbor)

    def step(self):
        """
        執行一步 SA 迭代 (產生鄰居 -> 評估 -> 接受/拒絕 -> 降溫)。
        """
        # 1. Generate Neighbor
        neighbor_solution = self.get_neighbor(self.current_solution)
        neighbor_fitness = self.calculate_stations(neighbor_solution)
        
        # 2. Acceptance Probability (Metropolis Criterion)
        # 目標是最小化 fitness
        delta_E = neighbor_fitness - self.current_fitness
        
        accept = False
        if delta_E < 0:
            # New solution is better: Always accept
            accept = True
        else:
            # New solution is worse: Accept with probability exp(-delta / T)
            # 避免 overflow
            if self.temp > 0:
                prob = math.exp(-delta_E / self.temp)
                if random.random() < prob:
                    accept = True
        
        if accept:
            self.current_solution = neighbor_solution
            self.current_fitness = neighbor_fitness
            
            # Update Global Best
            if self.current_fitness < self.best_fitness:
                self.best_fitness = self.current_fitness
                self.best_solution = self.current_solution[:]
                
        # 3. Cooling
        self.temp *= self.cooling_rate
        
        return self.best_fitness, self.temp
