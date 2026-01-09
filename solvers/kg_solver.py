
import random
import numpy as np
from typing import List, Tuple, Dict, Optional
from .problem_data import StaplerData
from .multi_objective_utils import calculate_hypervolume_two, generate_hypervolume_samples

class KGSolver:
    """
    K&G (Kang & Genetic Algorithm) Solver for Disassembly Line Balancing.
    Ports logic from 'LBGA.m' (K&G GA) and 'ppx.m' (Precedence Preserving Crossover).
    
    Objectives:
    1. Maximize Profit (f1)
    2. Minimize Carbon Footprint (f2)
    """
    
    def __init__(self, population_size: int = 100, generations: int = 100, 
                 crossover_rate: float = 0.7, mutation_rate: float = 0.9):
        self.population_size = population_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        
        # Helper Data
        self.data = StaplerData
        self.num_jobs = self.data.NUM_PARTS
        
        # Precompute Precedence Matrix
        self.precedence_matrix = self._build_transitive_closure(
            self.data.CONSTRAINTS, self.num_jobs
        )
        
        # Utopia Points (Same as NPSO)
        self.utopia = [350.0, 0.001]     
        self.anti_utopia = [0.0, 100.0]
        self.num_samples = 1000
        self.hv_samples = generate_hypervolume_samples(
            self.num_samples, self.utopia, self.anti_utopia
        )
        
        # Population
        self.population: List[List[int]] = []
        
        self.history_hv = []
        
        # Global Best logic
        self.gbest_permutation = None
        self.gbest_score = (float('-inf'), float('inf'))
        self.gbest_cut_index = -1
        self.gbest_metric = float('inf')

    def _build_transitive_closure(self, constraints: List[Tuple[int, int]], num_nodes: int) -> np.ndarray:
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
        # PPX usually maintains precedence, but mutation might break it?
        # Standard repair reuse
        seq = chromosome[:]
        n = len(seq)
        for i in range(n):
            for j in range(i + 1, n):
                job_prior = seq[i]
                job_later = seq[j]
                if self.precedence_matrix[job_later - 1, job_prior - 1] == 1:
                    seq[i], seq[j] = seq[j], seq[i]
                    job_prior = seq[i]
        return seq

    def calculate_objectives(self, sequence: List[int]) -> Tuple[float, float, int]:
        # Reusing identical logic to ensure fair comparison
        # (Could extract to a Mixin, but duplication is safer for now)
        data = self.data
        
        # Strategy 1 Scan
        total_weight = sum(data.WEIGHTS)
        limit = total_weight * 0.7
        rang = len(sequence)
        current_w = 0
        for i, part in enumerate(sequence):
            current_w += data.WEIGHTS[part - 1]
            if current_w >= limit:
                rang = i + 1
                break
        
        best_res_1 = (float('-inf'), float('inf'), -1)
        best_f1 = float('-inf')
        start_cut = 2
        if rang < 2: rang = 2
        for k in range(start_cut, rang + 1):
             f1, f2 = self._calculate_metrics_at_cut(sequence, k)
             if f1 > best_f1:
                 best_f1 = f1
                 best_res_1 = (f1, f2, k)
                 
        # Strategy 2 Heuristic
        rt = []
        for part in sequence:
            if part in data.REUSE: val = 1
            elif part in data.RECYCLE: val = -0.5
            elif part in data.REMANUFACTURING: val = -0.3
            else: val = -2
            rt.append(val)
            
        best_ratio = float('-inf')
        best_cut = 1
        for i in range(2, len(sequence)):
            sum_a = sum(rt[:i])
            sum_b = sum(rt[i:])
            if abs(sum_b) < 1e-9: ratio = -9999
            else: ratio = sum_a / sum_b
            if ratio > best_ratio:
                best_ratio = ratio
                best_cut = i
        
        f1_h, f2_h = self._calculate_metrics_at_cut(sequence, best_cut)
        best_res_2 = (f1_h, f2_h, best_cut)
        
        d1 = np.sqrt((self.utopia[0]-best_res_1[0])**2 + (self.utopia[1]-best_res_1[1])**2)
        d2 = np.sqrt((self.utopia[0]-best_res_2[0])**2 + (self.utopia[1]-best_res_2[1])**2)
        
        if d1 <= d2: return best_res_1
        else: return best_res_2

    def _calculate_metrics_at_cut(self, sequence: List[int], cut_index: int) -> Tuple[float, float]:
        # Identical logic
        parts_disassembled = sequence[:cut_index]
        parts_remaining = sequence[cut_index:]
        data = self.data
        
        add_cost = 0.0
        for part in parts_disassembled:
            try:
                idx = data.DC_SEQUENCE.index(part)
                add_cost += data.DISASSEMBLY_COSTS[idx]
            except ValueError: pass
        reman_count = sum(1 for p in parts_disassembled if p in data.REMANUFACTURING)
        add_cost += (data.PROCESSING_COST_FACTOR * reman_count)
        for part in parts_remaining:
            add_cost += data.NEW_PART_COSTS[part - 1]
        weight_remaining = sum(data.WEIGHTS[p - 1] for p in parts_remaining)
        revenue = weight_remaining * data.RECYCLE_REVENUE_RATE
        
        weight_disassembled = sum(data.WEIGHTS[p - 1] for p in parts_disassembled)
        cf = weight_disassembled * data.CARBON_COEFF_DISASSEMBLY
        cp = 0.0
        cm = sum((data.WEIGHTS[p-1] * data.CARBON_COEFFS[p-1]) for p in parts_disassembled if p in data.REMANUFACTURING)
        cy = 0.0
        
        tool_sequence = [data.JOB_TOOL_MAPPING[p - 1] for p in parts_disassembled]
        tool_changes = 0
        if len(tool_sequence) > 1:
            for k in range(1, len(tool_sequence)):
                if tool_sequence[k] != tool_sequence[k-1]:
                    tool_changes += 1
        dc_val = 48 + tool_changes
        time_score = (dc_val * 0.049) + 5.0306
        sss = tool_changes * 0.1
        
        f1 = 350 - (add_cost + time_score) + revenue
        f2 = cf + cp + cm + cy + sss
        return f1, f2
        
    # --- K&G Specific Logic ---
    
    def _ppx_crossover(self, parent1: List[int], parent2: List[int]) -> List[int]:
        """
        Precedence Preserving Crossover (PPX).
        Logic from ppx.m:
        1. Generate binary mask (random vector of length n with 1s and 2s).
        2. Pick from P1 or P2 based on mask.
        3. Remove picked gene from BOTH parents (conceptually) to avoid duplicates.
        """
        n = self.num_jobs
        # Mask: 1 means pick from P1, 0 (or 2) means pick from P2
        # ppx.m: D=fix(rand(2,n)*2+1); (1 or 2). D(e,t).
        # It generates a random binary string of length N approx?
        # Let's generate a list of N choices.
        mask = [random.choice([1, 2]) for _ in range(n)]
        
        child = []
        # Working copies of parents to 'remove' items from
        p1_temp = parent1[:]
        p2_temp = parent2[:]
        
        for k in range(n):
            source = mask[k]
            if source == 1:
                # Pick next available from P1
                # Find first item in p1_temp that is not already in child?
                # Actually ppx.m does: "C=[C,b1(1)]; h=find(b2==b1(1)); b1(1)=[]; b2(h)=[];"
                # It literally removes the head of P1, and removes that same item from P2 wherever it is.
                # So p1_temp and p2_temp shrink.
                
                # Check if p1_temp is empty (shouldn't be if loop matches n)
                if not p1_temp: break # safety
                
                gene = p1_temp[0]
                child.append(gene)
                
                # Remove from P1
                p1_temp.pop(0)
                # Remove from P2
                if gene in p2_temp:
                    p2_temp.remove(gene)
                    
            else: # source == 2
                if not p2_temp: break
                
                gene = p2_temp[0]
                child.append(gene)
                
                p2_temp.pop(0)
                if gene in p1_temp:
                    p1_temp.remove(gene)
                    
        return child

    def evolve(self) -> Tuple[List[int], Tuple[float, float], int]:
        if not self.population:
            for _ in range(self.population_size):
                p = np.random.permutation(self.num_jobs) + 1
                p = self._repair_chromosome(list(p))
                self.population.append(list(p))
                
        new_pop = []
        indices = list(range(self.population_size))
        random.shuffle(indices)
        
        # Crossover
        for i in range(0, self.population_size, 2):
            if i+1 >= self.population_size:
                new_pop.append(self.population[indices[i]])
                break
            p1 = self.population[indices[i]]
            p2 = self.population[indices[i+1]]
            
            if random.random() < self.crossover_rate:
                c1 = self._ppx_crossover(p1, p2)
                c2 = self._ppx_crossover(p2, p1)
                new_pop.extend([c1, c2])
            else:
                new_pop.extend([p1, p2])
        
        # Mutation (Standard Swap)
        # K&G LBGA.m uses "LBb.m" (Mutation). LBb0? 
        # LBGA.m uses "LBb(n,a,b...)"
        # Assuming simple mutation (Swap) for K&G usually.
        # LBb0 was Greedy. LBb is likely simpler?
        # I'll implement random swap mutation.
        for i in range(len(new_pop)):
            if random.random() < self.mutation_rate:
                # Swap two random genes
                idx1, idx2 = random.sample(range(self.num_jobs), 2)
                new_pop[i][idx1], new_pop[i][idx2] = new_pop[i][idx2], new_pop[i][idx1]
                # Repair after swap to maintain precedence
                new_pop[i] = self._repair_chromosome(new_pop[i])
                
        self.population = new_pop
        
        # Evaluate
        best_gen_dist = float('inf')
        for chrom in self.population:
             profit, carbon, cut = self.calculate_objectives(chrom)
             dist = np.sqrt((self.utopia[0]-profit)**2 + (self.utopia[1]-carbon)**2)
             
             if dist < self.gbest_metric:
                 self.gbest_metric = dist
                 self.gbest_score = (profit, carbon)
                 self.gbest_permutation = chrom[:]
                 self.gbest_cut_index = cut
        
        hv = calculate_hypervolume_two(self.gbest_score, self.hv_samples)
        self.history_hv.append(hv)
        
        return self.gbest_permutation, self.gbest_score, self.gbest_cut_index
