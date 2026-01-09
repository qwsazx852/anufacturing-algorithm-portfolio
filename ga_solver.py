import random
import numpy as np
from collections import deque
from typing import List, Tuple, Optional

class GeneticOptimizer:
    """
    專業級遺傳演算法優化器（Genetic Algorithm Optimizer）。
    適用於 Job Shop Scheduling 或其他具有優先順序限制（Precedence Constraints）的序列排序問題。
    
    Attributes:
        num_jobs (int): 總作業數（節點數）。
        pop_size (int): 族群大小（Population Size）。
        crossover_rate (float): 執行交配的機率。
        precedence_matrix (np.ndarray): 布林矩陣，若 matrix[i, j] 為 True，表示作業 i 必須在作業 j 之前（包含直接或間接依賴）。
        population (List[List[int]]): 目前的族群染色體（作業序列）。
    """

    def __init__(self, num_jobs: int, pop_size: int, crossover_rate: float, mutation_rate: float,
                 constraints: List[Tuple[int, int]], time_info: List[int], cycle_time: int):
        """
        初始化遺傳優化器。

        Args:
            num_jobs (int): 總作業數。
            pop_size (int): 族群大小（必須為偶數）。
            crossover_rate (float): 交配率（0.0 - 1.0）。
            mutation_rate (float): 突變率（0.0 - 1.0）。
            constraints (List[Tuple[int, int]]): (前置作業, 後續作業) 的配對列表，使用 1-based 編號。
            time_info (List[int]): 每個作業的時間列表（0-based index）。
            cycle_time (int): 週期時間 (GCT)。
        """
        self.num_jobs = num_jobs
        self.pop_size = pop_size 
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.time_info = time_info
        self.cycle_time = cycle_time
        
        # 建立傳遞閉包矩陣 (Transitive Closure Matrix / Reachability Matrix)
        # 這允許我們用 O(1) 的時間檢查「A 是否需要在 B 之前？」
        self.precedence_matrix = self._build_transitive_closure(constraints, num_jobs)
        
        self.population = []

    def _build_transitive_closure(self, constraints: List[Tuple[int, int]], num_nodes: int) -> np.ndarray:
        """
        使用 Floyd-Warshall 演算法概念建立可達性矩陣（傳遞閉包）。
        這能捕捉直接與間接的相依關係（例如 1->2, 2->3，則隱含 1->3）。
        
        複雜度: O(N^3) - 對於 N=18 來說非常快。
        """
        # 矩陣初始化: matrix[i][j] = 1 表示存在 i -> j 的路徑
        # 內部使用 0-based 索引
        matrix = np.zeros((num_nodes, num_nodes), dtype=int)
        
        # 1. Fill direct constraints
        for pre, suc in constraints:
            # Convert 1-based input to 0-based index
            matrix[pre - 1, suc - 1] = 1
            
        # 2. 計算傳遞閉包 (Compute Transitive Closure)
        # 如果 i -> k 且 k -> j，則 i -> j
        for k in range(num_nodes):
            for i in range(num_nodes):
                for j in range(num_nodes):
                    if matrix[i, k] and matrix[k, j]:
                        matrix[i, j] = 1
                        
        return matrix

    def initialize_population(self):
        """產生初始隨機族群，並進行修復以滿足優先順序限制。"""
        self.population = []
        for _ in range(self.pop_size):
            # Generate random permutation
            chromosome = list(np.random.permutation(self.num_jobs) + 1) # 1-based
            
            # Repair to satisfy precedence
            repaired = self._repair_chromosome(chromosome)
            self.population.append(repaired)
            
    def _repair_chromosome(self, chromosome: List[int]) -> List[int]:
        """
        修復染色體序列以遵守優先順序限制。
        使用類似氣泡排序的交換法。
        
        Args:
            chromosome: 1-based 的作業序列。
        """
        n = len(chromosome)
        # 我們會原地修改列表或複製。這裡進行多次掃描以確保一致性。
        # 因為這是拓樸調整，如果限制是無環的，簡單的檢查與交換是可行的。
        
        # 優化：對於小型列表，純 Python 列表操作通常比轉換為 numpy 陣列更快。
        seq = chromosome[:] 
        
        # Bubble-like fix: if we find (Job B ... Job A) but A must precede B, we swap them.
        for i in range(n):
            for j in range(i + 1, n):
                job_prior = seq[i]
                job_later = seq[j]
                
                # Check if 'job_later' must actually precede 'job_prior'
                # Matrix is 0-indexed
                if self.precedence_matrix[job_later - 1, job_prior - 1] == 1:
                    # Constraint violated: job_later must come before job_prior
                    # Swap them
                    seq[i], seq[j] = seq[j], seq[i]
                    # Update local vars after swap for next comparison
                    job_prior = seq[i] 
                    
        return seq

    def _crossover_ppx(self, parent1: List[int], parent2: List[int]) -> List[List[int]]:
        """
        優先順序保留交配法 (PPX)。
        使用 collections.deque 進行 O(1) 的移除操作，比列表的 O(N) pop(0) 效率高很多。
        """
        if random.random() >= self.crossover_rate:
            return [parent1[:], parent2[:]]

        # 使用 deque 進行 O(1) pop 操作
        p1_queue = deque(parent1)
        p2_queue = deque(parent2)
        
        # 我們需要兩個子代
        # 標準 PPX 通常一次產生一個子代。
        # 這裡保留原始代碼邏輯：產生 2 個子代，每個都從全新的父母複製開始。
        
        offspring = []
        
        for _ in range(2):
            # 為每個子代產生新的父母副本
            current_p1 = deque(parent1)
            current_p2 = deque(parent2)
            child = []
            
            # 用於決定從哪個父母取基因的二元遮罩向量
            # 1 -> 取自 P1, 2 -> 取自 P2
            mask = np.random.randint(1, 3, size=self.num_jobs)
            
            for t in range(self.num_jobs):
                if mask[t] == 1:
                    # 取 P1 的第一個元素
                    gene = current_p1.popleft() # O(1)
                    child.append(gene)
                    # 從 P2 中移除該基因 (O(N)，在 list/deque 搜尋中無法避免，除非有額外映射)
                    current_p2.remove(gene)
                else:
                    # 取 P2 的第一個元素
                    gene = current_p2.popleft() # O(1)
                    child.append(gene)
                    current_p1.remove(gene)
            
            offspring.append(child)
            
        return offspring

    def _mutate_swap(self, chromosome: List[int]) -> List[int]:
        """
        兩點交換變異 (Two-Point Swap Mutation)。
        隨機交換兩個基因，並進行修復。
        """
        if random.random() >= self.mutation_rate:
            return chromosome
            
        n = self.num_jobs
        mutated = list(chromosome)
        
        # 1. Randomly pick two indices
        idx1, idx2 = random.sample(range(n), 2)
        
        # 2. Swap
        mutated[idx1], mutated[idx2] = mutated[idx2], mutated[idx1]
        
        # 3. Repair precedence constraints
        return self._repair_chromosome(mutated)

    def calculate_stations(self, chromosome: List[int]) -> int:
        """
        計算單個染色體所需的工作站數量。
        """
        current_sum = 0
        stations = 1
        
        for job in chromosome:
            # 作業編號從 1 開始，列表索引從 0 開始
            job_time = self.time_info[job - 1]
            
            current_sum += job_time
            if current_sum > self.cycle_time:
                # 超過週期時間，新開一個工作站，當前作業放入新工作站
                current_sum = job_time 
                stations += 1
                
        return stations
    
    def _roulette_selection(self, population: List[List[int]], station_counts: List[int]) -> List[List[int]]:
        """
        輪盤選擇法 (Roulette Wheel Selection) - 望小。
        Fitness = 1 / stations
        """
        # 計算適應度 (越小越好 -> 倒數)
        fitness_values = [1.0 / count for count in station_counts]
        total_fitness = sum(fitness_values)
        
        # 計算被選中的機率
        probs = [f / total_fitness for f in fitness_values]
        
        # 隨機選擇索引
        indices = np.random.choice(range(len(population)), size=len(population), p=probs)
        
        # 根據索引建立新族群
        new_population = [population[i] for i in indices]
        
        return new_population

    def evolve(self) -> Tuple[List[int], int]:
        """
        執行一代的演化（Evolution）。
        1. 交配
        2. 突變
        3. 計算適應度
        4. 選擇
        
        Returns:
            Tuple[List[int], int]: (本代最佳染色體, 本代最少工作站數量)
        """
        # 1. 交配 (Crossover)
        next_gen_pop = []
        for i in range(0, self.pop_size, 2):
            parent1 = self.population[i]
            # 確保有成對的父母，如果是奇數個體最後一個這輪可能會落單或需要特殊處理
            # 這裡假設 pop_size 為偶數
            parent2 = self.population[i+1] if i+1 < self.pop_size else self.population[0]
            
            children = self._crossover_ppx(parent1, parent2)
            next_gen_pop.extend(children)
            
        # 2. 突變 (Mutation)
        mutated_pop = []
        for ind in next_gen_pop:
            mutated_pop.append(self._mutate_swap(ind))
            
        # 3. 計算適應度與尋找最佳解 (Evaluate)
        station_counts = []
        current_best_stations = float('inf')
        current_best_chromosome = None
        
        for chromosome in mutated_pop:
            stations = self.calculate_stations(chromosome)
            station_counts.append(stations)
            
            if stations < current_best_stations:
                current_best_stations = stations
                current_best_chromosome = chromosome[:]
        
        # 4. 選擇 (Selection)
        final_pop = self._roulette_selection(mutated_pop, station_counts)
            
        self.population = final_pop
        
        return current_best_chromosome, current_best_stations

    def get_population(self):
        return self.population
