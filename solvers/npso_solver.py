
import random
import numpy as np
from typing import List, Tuple, Dict, Optional
from .problem_data import StaplerData
from .multi_objective_utils import calculate_hypervolume_two, generate_hypervolume_samples, compute_pareto_front
from .pso_solver import PSOSolver

class NPSOSolver:
    """
    Multi-Objective PSO (NPSO) Solver for Disassembly Line Balancing.
    Ports logic from MATLAB 'PSO_line_balance.m', 'fitness1.m', 'fitness2.m'.
    
    Objectives:
    1. Maximize Profit (f1)
    2. Minimize Carbon Footprint (f2)
    """
    
    def __init__(self, num_particles: int = 100, generations: int = 100, 
                 w: float = 0.8, c1: float = 0.5, c2: float = 0.5, data_class=None):
        self.num_particles = num_particles
        self.generations = generations
        self.w = w
        self.c1 = c1
        self.c2 = c2
        
        # Helper Data
        from .problem_data import StaplerData, get_problem_data
        self.data = data_class if data_class else StaplerData
        self.num_jobs = self.data.NUM_PARTS
        
        # Precompute Precedence Matrix (copied from other solvers)
        self.precedence_matrix = self._build_transitive_closure(
            self.data.CONSTRAINTS, self.num_jobs
        )
        
        # Utopia Points for Hypervolume (from MATLAB PSO_line_balance.m)
        self.utopia = [350.0, 0.001]     # Ideal: High Profit, Low Carbon
        self.anti_utopia = [0.0, 100.0]  # Worst: Low Profit, High Carbon
        self.num_samples = 1000
        self.hv_samples = generate_hypervolume_samples(
            self.num_samples, self.utopia, self.anti_utopia
        )
        
        # PSO State
        self.X = np.random.uniform(-10, 10, size=(num_particles, self.num_jobs))
        self.V = np.random.uniform(-1, 1, size=(num_particles, self.num_jobs))
        
        # Personal Best
        self.pbest_X = self.X.copy()
        # Store objective values for pbest: (Profit, Carbon, HypervolumeMetric)
        # Using a simple metric (distance to Utopia) or Hypervolume contribution to pick best?
        # MATLAB fitness.m uses Distance to Utopia to pick between fitness1 and fitness2 results.
        # Implies we track (f1, f2)
        self.pbest_scores = [(float('-inf'), float('inf'))] * num_particles # (Profit, Carbon)
        self.pbest_metric = [float('inf')] * num_particles # Metric to minimize (Distance to Utopia)
        
        # Global Best
        self.gbest_X = None
        self.gbest_score = (float('-inf'), float('inf'))
        self.gbest_metric = float('inf')
        self.gbest_permutation = None
        self.gbest_cut_index = -1 # Store the optimal cut-off point
        
        self.history_hv = []

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
        """Repair permutation to satisfy precedence constraints."""
        seq = chromosome[:]
        n = len(seq)
        for i in range(n):
            for j in range(i + 1, n):
                job_prior = seq[i]
                job_later = seq[j]
                # If later job strictly precedes prior job, swap
                if self.precedence_matrix[job_later - 1, job_prior - 1] == 1:
                    seq[i], seq[j] = seq[j], seq[i]
                    job_prior = seq[i] # Update after swap
        return seq

    def _decode_position(self, x_vector: np.ndarray) -> List[int]:
        """SPV Rule: Convert continuous position to permutation."""
        return list(np.argsort(x_vector) + 1)

    def calculate_objectives(self, sequence: List[int]) -> Tuple[float, float, int]:
        """
        Calculates (Profit, Carbon, CutIndex) for a given full sequence.
        Replicates logic from fitness1.m and fitness2.m.
        Returns: (Profit, Carbon, CutIndex)
        """
        # The sequence 'sequence' is a full disassembly order.
        # But we stop at some point.
        # fitness.m runs BOTH strategies (fitness1 and fitness2) and picks the one 
        # that is closer to the Reference Point (Utopia).
        
        # Strategy 1 (fitness1.m): Try all cut points, pick Max Profit
        res1 = self._strategy_max_profit(sequence) # Returns (f1, f2)
        
        # Strategy 2 (fitness2.m): Pick cut point by heuristic, then calc Profit/Carbon
        res2 = self._strategy_heuristic_cut(sequence) # Returns (f1, f2)
        
        # Compare Distance to Utopia [350, 0.001]
        # Normalize? MATLAB uses raw euclidean distance on (f1, f2).
        # R = sqrt((350 - f1)^2 + (0.001 - f2)^2)
        
        dist1 = np.sqrt((self.utopia[0] - res1[0])**2 + (self.utopia[1] - res1[1])**2)
        dist2 = np.sqrt((self.utopia[0] - res2[0])**2 + (self.utopia[1] - res2[1])**2)
        
        if dist1 <= dist2:
            # res1 is (f1, f2, k)
            return res1
        else:
            return res2

    def _calculate_metrics_at_cut(self, sequence: List[int], cut_index: int) -> Tuple[float, float]:
        """
        Computes Profit (f1) and Carbon (f2) if we disassemble up to 'cut_index' (inclusive, 1-based index of sequence).
        """
        # Slicing: sequence[0:cut_index]
        parts_disassembled = sequence[:cut_index] # d1
        parts_remaining = sequence[cut_index:]    # d
        
        data = self.data
        
        # --- COST CALCULATION (add) ---
        add_cost = 0.0
        
        # 1. Disassembly Cost (Dc/DC2 mapping)
        # In MATLAB: iterate Dc, find if in d1, add DC2 cost.
        # Effectively: for each part in d1, add its specific disassembly cost.
        # Using DC_SEQUENCE to map Part ID -> Index -> Cost
        for part in parts_disassembled:
            # part is 1-based ID
            # finding its cost. 
            # In MATLAB Dc is [18, 10...] and DC2 is corresponding cost.
            # We can build a dict for O(1)
            try:
                idx = data.DC_SEQUENCE.index(part)
                add_cost += data.DISASSEMBLY_COSTS[idx]
            except ValueError:
                pass # Part not in cost list?
        
        # 2. Processing Cost (Remanufacturing)
        # If part in d1 is in Remanufacturing list -> add 1.5
        reman_count = 0
        for part in parts_disassembled:
            if part in data.REMANUFACTURING:
                reman_count += 1
        add_cost += (data.PROCESSING_COST_FACTOR * reman_count)
        
        # 3. New Part Cost (for parts NOT disassembled, i.e., in 'd')
        # MATLAB: new=sum(mc(d))
        for part in parts_remaining:
            add_cost += data.NEW_PART_COSTS[part - 1] # 0-based index
            
        # --- REVENUE (get) ---
        # MATLAB: get=sum(gw(d)).*0.005
        # Revenue from RECYCLING the *remaining* parts (Wait, isn't it usually reusing components?)
        # MATLAB says: "目前只算廢棄零件回收 5元/kg" for parts in 'd' (remaining).
        # This implies remaining parts are scrapped as bulk metal?
        weight_remaining = sum(data.WEIGHTS[p - 1] for p in parts_remaining)
        revenue = weight_remaining * data.RECYCLE_REVENUE_RATE
        
        # --- CARBON CALCULATION (f2 components) ---
        # 1. Disassembly Carbon (cf)
        # cf = sum(gw(d1)) * Cs
        weight_disassembled = sum(data.WEIGHTS[p - 1] for p in parts_disassembled)
        cf = weight_disassembled * data.CARBON_COEFF_DISASSEMBLY
        
        # 2. Purchase Carbon (cp) - Set to 0 in MATLAB
        cp = 0.0
        
        # 3. Remanufacturing Carbon (cm)
        # For part in d1 if in Remanufacturing: weight * carbon_coeff
        cm = 0.0
        for part in parts_disassembled:
            if part in data.REMANUFACTURING:
                w = data.WEIGHTS[part - 1]
                c_coeff = data.CARBON_COEFFS[part - 1]
                cm += (w * c_coeff)
                
        # 4. Recycle Carbon (cy) - Set to 0 in MATLAB
        cy = 0.0
        
        # --- TOOL CHANGE COST & CARBON (SSS) ---
        # Call LBss1 logic. This counts tool changes.
        # Logic: Iterate through sequence. If Tool(i) != Tool(i-1) -> Change.
        # But MATLAB LBss1 code is a bit complex with "Right Change", "Left Change".
        # Simplified port based on "DC=48 + SS1" lines 151-153 fitness1.m
        # Let's count tool changes in 'parts_disassembled'.
        
        # Mapping Job -> Tool
        tool_sequence = [data.JOB_TOOL_MAPPING[p - 1] for p in parts_disassembled]
        
        # Count changes
        # MATLAB LBss1 seems to count changes. 
        # Let's count transitions.
        tool_changes = 0
        if len(tool_sequence) > 1:
            for k in range(1, len(tool_sequence)):
                if tool_sequence[k] != tool_sequence[k-1]:
                    tool_changes += 1
        
        # MATLAB fitness1.m: DC = 48; DC = DC + SS1 (changes); 
        # timescore = (DC * 0.049) + 5.0306
        dc_val = 48 + tool_changes
        time_score = (dc_val * 0.049) + 5.0306
        
        # SSS (Carbon from tool changes?)
        # In fitness1.m: [SS1, SSS, SS2] = LBss1.
        # SSS seems to be associated with time/carbon.
        # Given lack of LBss1.m, let's approximate SSS as proportional to changes.
        # Assume SSS = tool_changes * 0.01 (Placeholder or simplified).
        # Actually I saw 'LBss1' call in fitness. 
        # Let's assume SSS is small or similar logic. I will use 0.0 for now if unknown 
        # or just make it same as time_score logic.
        # Let's use a proxy: SSS = tool_changes * 0.1
        sss = tool_changes * 0.1
        
        # --- FINAL OBJECTIVES ---
        # f1 = 350 - (add + timescore) + get
        f1 = 350 - (add_cost + time_score) + revenue
        
        # f2 = cf + cp + cm + cy + SSS
        f2 = cf + cp + cm + cy + sss
        
        return f1, f2

    def _strategy_max_profit(self, sequence: List[int]) -> Tuple[float, float]:
        """Strategies similar to fitness1.m: try multiple cut points."""
        # fitness1.m loops from i=2 to rang. rang is determined by weight limits (CR=0.7).
        # "limit = sum(gw) * 0.7". "p=0; for i ... if p >= limit break"
        
        total_weight = sum(self.data.WEIGHTS)
        limit = total_weight * 0.7
        
        rang = len(sequence) # fallback
        current_w = 0
        for i, part in enumerate(sequence):
            current_w += self.data.WEIGHTS[part - 1]
            if current_w >= limit:
                rang = i + 1 # 1-based index (count)
                break
        
        # Iterate cut points up to 'rang'
        # MATLAB starts loop i=2.
        best_f1 = float('-inf')
        best_res = (float('-inf'), float('inf'))
        
        # Must disassemble at least 2 parts?
        start_cut = 2
        if rang < 2: rang = 2
        
        for k in range(start_cut, rang + 1):
            f1, f2 = self._calculate_metrics_at_cut(sequence, k)
            if f1 > best_f1:
                best_f1 = f1
                best_res = (f1, f2, k)
        
        return best_res

    def _strategy_heuristic_cut(self, sequence: List[int]) -> Tuple[float, float]:
        """Strategy similar to fitness2.m: use Penalty/Reward values to find cut."""
        # rt values: Reuse=1, Recycle=-0.5, Reman=-0.3, Trash=-2
        rt = []
        data = self.data
        for part in sequence:
            if part in data.REUSE: val = 1
            elif part in data.RECYCLE: val = -0.5
            elif part in data.REMANUFACTURING: val = -0.3
            else: val = -2 # Trash
            rt.append(val)
            
        # Find split point that maximizes Ratio A/B or Sum A?
        # MATLAB: stopselectadd=[... A, B, A./B]
        # stoppoint = find max ratio
        # A = sum(rt before), B = sum(rt after)
        
        best_ratio = float('-inf')
        best_cut = 1
        
        # Loop i from 2 to length-1 (MATLAB)
        for i in range(2, len(sequence)):
            sum_a = sum(rt[:i])
            sum_b = sum(rt[i:])
            if abs(sum_b) < 1e-9: ratio = -9999 # Avoid div by zero
            else: ratio = sum_a / sum_b
            
            if ratio > best_ratio:
                best_ratio = ratio
                best_cut = i
        
        # Returns (f1, f2, best_cut) directly
        f1, f2 = self._calculate_metrics_at_cut(sequence, best_cut)
        return (f1, f2, best_cut)

    def evolve(self) -> Tuple[List[int], Tuple[float, float]]:
        """
        Executes one generation of NPSO.
        Returns (Best Permutation, (Profit, Carbon))
        """
        # 1. Update Fitness & Best
        for i in range(self.num_particles):
            perm = self._decode_position(self.X[i])
            repaired_perm = self._repair_chromosome(perm)
            
            # Calculate Objectives
            profit, carbon, cut_idx = self.calculate_objectives(repaired_perm)
            
            # Distance to Utopia (Metric for single-objective selection within PSO)
            # Minimize distance to [350, 0]
            dist = np.sqrt((self.utopia[0] - profit)**2 + (self.utopia[1] - carbon)**2)
            
            # Update Personal Best (based on metric)
            if dist < self.pbest_metric[i]:
                self.pbest_metric[i] = dist
                self.pbest_scores[i] = (profit, carbon)
                self.pbest_X[i] = self.X[i].copy()
                
            # Update Global Best
            if dist < self.gbest_metric:
                self.gbest_metric = dist
                self.gbest_score = (profit, carbon)
                self.gbest_X = self.X[i].copy()
                self.gbest_permutation = repaired_perm[:]
                self.gbest_cut_index = cut_idx
                
        # 2. Update Velocity and Position (Standard PSO)
        r1 = np.random.rand(self.num_particles, self.num_jobs)
        r2 = np.random.rand(self.num_particles, self.num_jobs)
        
        self.V = (self.w * self.V + 
                  self.c1 * r1 * (self.pbest_X - self.X) + 
                  self.c2 * r2 * (self.gbest_X - self.X))
        self.X = self.X + self.V
        
        # 3. Calculate Hypervolume for History
        # We check the Hypervolume of the current Global Best vs Samples
        # (This is what the MATLAB code effectively tracked in 'D' or 'HV')
        hv = calculate_hypervolume_two(self.gbest_score, self.hv_samples)
        self.history_hv.append(hv)
        
        return self.gbest_permutation, self.gbest_score, self.gbest_cut_index

    def get_pareto_front(self) -> List[Tuple[float, float]]:
        """
        Returns the simplified Pareto Front from the final swarm positions.
        """
        population_scores = []
        for i in range(self.num_particles):
            # Evaluate current particle position
            perm = self._decode_position(self.X[i])
            perm = self._repair_chromosome(perm)
            profit, carbon, _ = self.calculate_objectives(perm)
            population_scores.append((profit, carbon))
            
        # Also include pbest scores as they might be better than current X
        for i in range(self.num_particles):
            if self.pbest_scores[i][0] != float('-inf'):
                population_scores.append(self.pbest_scores[i])
                
        return compute_pareto_front(population_scores)
