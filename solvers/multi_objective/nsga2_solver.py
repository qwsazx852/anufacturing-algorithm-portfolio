
import random
import numpy as np
from typing import List, Tuple, Dict, Optional
from .kg_solver import KGSolver
from .multi_objective_utils import calculate_hypervolume_two

class NSGA2Solver(KGSolver):
    """
    NSGA-II (Non-dominated Sorting Genetic Algorithm II) Solver.
    Inherits problem representation and PPX crossover from KGSolver,
    but replaces the selection logic with True Multi-Objective reasoning:
    1. Fast Non-Dominated Sorting (Pareto Ranking)
    2. Crowding Distance (Diversity Preservation)
    """

    def __init__(self, population_size: int = 100, generations: int = 100, 
                 crossover_rate: float = 0.8, mutation_rate: float = 0.2, data_class=None):
        super().__init__(population_size, generations, crossover_rate, mutation_rate, data_class)
        # Store population as objects or dicts to keep track of rank/crowding?
        # For simplicity, we'll compute rank/crowding ephemeral in each generation.

    def _fast_non_dominated_sort(self, population_objs: List[Tuple[float, float]]) -> List[List[int]]:
        """
        Returns list of fronts, where each front is a list of indices.
        Front 0 is the best (non-dominated).
        Objectives: Maximize Profit (0), Minimize Carbon (1).
        To standardize, we can negate Carbon so we Maximize both, or handle mixed logic.
        Standard NSGA2 usually assumes Minimization for all.
        Let's convert to Minimization for sorting:
        - Obj 1 (Profit): Multiply by -1 (to minimize)
        - Obj 2 (Carbon): Keep positive (to minimize)
        """
        S = [[] for _ in range(len(population_objs))]
        n = [0] * len(population_objs)
        rank = [0] * len(population_objs)
        fronts = [[]]

        # Standardize to Minimization
        # P = Profit (Max), C = Carbon (Min)
        # Target: Min(-P), Min(C)
        converted_objs = [(-p, c) for p, c in population_objs]

        for p in range(len(population_objs)):
            S[p] = []
            n[p] = 0
            for q in range(len(population_objs)):
                if p == q: continue
                
                # Check Dominance: p dominates q?
                # A dominates B if A <= B for all and A < B for at least one
                p_values = converted_objs[p]
                q_values = converted_objs[q]
                
                less_equal = (p_values[0] <= q_values[0]) and (p_values[1] <= q_values[1])
                less = (p_values[0] < q_values[0]) or (p_values[1] < q_values[1])
                
                if less_equal and less:
                    S[p].append(q)
                elif (q_values[0] <= p_values[0] and q_values[1] <= p_values[1]) and \
                     (q_values[0] < p_values[0] or q_values[1] < p_values[1]):
                    n[p] += 1
            
            if n[p] == 0:
                rank[p] = 0
                fronts[0].append(p)
        
        i = 0
        while i < len(fronts) and fronts[i]:
            Q = []
            for p in fronts[i]:
                for q in S[p]:
                    n[q] -= 1
                    if n[q] == 0:
                        rank[q] = i + 1
                        Q.append(q)
            if Q:
                fronts.append(Q)
            i += 1
            
        return fronts

    def _calculate_crowding_distance(self, front_indices: List[int], population_objs: List[Tuple[float, float]]) -> Dict[int, float]:
        distance = {i: 0.0 for i in front_indices}
        m = 2 # number of objectives
        
        l = len(front_indices)
        if l == 0: return distance
        
        # For each objective
        for i in range(m):
            # Sort by objective i
            # If i=0 (Profit), we want to sort ascending or descending? 
            # Doesn't matter as long as bounds are correct.
            # Let's sort Ranking values (converted). 
            # Or just raw values.
            
            sorted_indices = sorted(front_indices, key=lambda idx: population_objs[idx][i])
            
            # Boundary points get infinity
            distance[sorted_indices[0]] = float('inf')
            distance[sorted_indices[-1]] = float('inf')
            
            obj_range = population_objs[sorted_indices[-1]][i] - population_objs[sorted_indices[0]][i]
            if obj_range == 0: obj_range = 1e-9
            
            for k in range(1, l - 1):
                idx = sorted_indices[k]
                prev_idx = sorted_indices[k-1]
                next_idx = sorted_indices[k+1]
                
                # dist += (next - prev) / range
                distance[idx] += abs(population_objs[next_idx][i] - population_objs[prev_idx][i]) / obj_range
                
        return distance

    def evolve(self) -> Tuple[List[int], Tuple[float, float], int]:
        # 0. Initialize if needed
        if not self.population:
            for _ in range(self.population_size):
                p = np.random.permutation(self.num_jobs) + 1
                p = self._repair_chromosome(list(p))
                self.population.append(list(p))
        
        # 1. Create Offspring (P + Q)
        # Using Tournament Selection -> Crossover -> Mutation
        offspring_pop = []
        
        # Generate N offspring
        # Standard NSGA2: Binary Tournament based on Rank/Crowding from P
        
        # Calculate Rank/Crowding for P first to use in selection
        pop_objs = []
        for chrom in self.population:
            f1, f2, _ = self.calculate_objectives(chrom)
            pop_objs.append((f1, f2))
            
        fronts = self._fast_non_dominated_sort(pop_objs)
        ranks = {}
        for r, front in enumerate(fronts):
            distances = self._calculate_crowding_distance(front, pop_objs)
            for idx in front:
                ranks[idx] = (r, distances[idx]) # (Rank, Dist)
                
        # Generate Selection Pool
        indices = list(range(self.population_size))
        mating_pool = []
        for _ in range(self.population_size):
            p1_idx = random.choice(indices)
            p2_idx = random.choice(indices)
            
            # Crowded Comparison Operator
            # A < B if (rankA < rankB) or (rankA == rankB and distA > distB)
            r1, d1 = ranks[p1_idx]
            r2, d2 = ranks[p2_idx]
            
            if r1 < r2:
                winner = p1_idx
            elif r2 < r1:
                winner = p2_idx
            else:
                if d1 > d2:
                    winner = p1_idx
                else:
                    winner = p2_idx
            mating_pool.append(self.population[winner])
            
        # Crossover & Mutation on Mating Pool
        for i in range(0, self.population_size, 2):
            if i+1 >= len(mating_pool): break
            p1 = mating_pool[i]
            p2 = mating_pool[i+1]
            
            if random.random() < self.crossover_rate:
                c1 = self._ppx_crossover(p1, p2)
                c2 = self._ppx_crossover(p2, p1)
            else:
                c1, c2 = p1[:], p2[:]
                
            offspring_pop.extend([c1, c2])
            
        # Mutation
        for i in range(len(offspring_pop)):
            if random.random() < self.mutation_rate:
                idx1, idx2 = random.sample(range(self.num_jobs), 2)
                offspring_pop[i][idx1], offspring_pop[i][idx2] = offspring_pop[i][idx2], offspring_pop[i][idx1]
                offspring_pop[i] = self._repair_chromosome(offspring_pop[i])
                
        # 2. Combine R = P + Q
        combined_pop = self.population + offspring_pop
        
        # Combine Objectives
        combined_objs = []
        # Re-calc for P (cached?) No, re-calc is safer/easier
        # Calc for Q
        for chrom in combined_pop:
            f1, f2, _ = self.calculate_objectives(chrom)
            combined_objs.append((f1, f2))
            
        # 3. Non-Dominated Sort R
        fronts = self._fast_non_dominated_sort(combined_objs)
        
        # 4. Fill new P
        new_pop = []
        new_pop_indices = []
        
        i = 0
        while len(new_pop) + len(fronts[i]) <= self.population_size:
            # Include all of front i
            for idx in fronts[i]:
                new_pop.append(combined_pop[idx])
                new_pop_indices.append(idx)
            i += 1
            if i >= len(fronts): break
            
        # If not full, fill from the next front sorted by crowding distance
        if len(new_pop) < self.population_size and i < len(fronts):
            remaining = self.population_size - len(new_pop)
            last_front = fronts[i]
            
            crowding_dists = self._calculate_crowding_distance(last_front, combined_objs)
            # Sort descending by distance
            sorted_last_front = sorted(last_front, key=lambda idx: crowding_dists[idx], reverse=True)
            
            for k in range(remaining):
                idx = sorted_last_front[k]
                new_pop.append(combined_pop[idx])
                new_pop_indices.append(idx)
                
        self.population = new_pop
        
        # Update metrics just for tracking (HV of current Top rank?)
        # Let's track HV of the entire population? Or Best?
        # Standard: Update history with HV of the Non-Dominated Front of P
        
        # Get Pareto Front of current P for HV calc
        current_objs = []
        for chrom in self.population:
             f1, f2, _ = self.calculate_objectives(chrom)
             current_objs.append((f1, f2))
        
        from .multi_objective_utils import compute_pareto_front
        front_points = compute_pareto_front(current_objs)
        
        # Calculate HV with Utopia/AntiUtopia
        # Assuming front_points is list of (p, c)
        # Use simple method: pick the "Best Balance" for gbest_score for compatibility
        # Pick point closest to Utopia as "gbest_score" for display purposes
        best_dist = float('inf')
        for p, c in front_points:
            dist = np.sqrt((self.utopia[0]-p)**2 + (self.utopia[1]-c)**2)
            if dist < best_dist:
                best_dist = dist
                self.gbest_score = (p, c)
                # Ideally find the chromosome too but strictly needed? 
                # Just keeping compatibility
        
        # For HV, we usually need a reference point (Anti-Utopia)
        # Using best point in front as proxy for HV of the set? No, HV is set metric.
        # Let's assume we pass the BEST point or average? 
        # The existing history code expects a float.
        # Use HV of the WHOLE FRONT (Set-based metric).
        # This prevents oscillation caused by tracking a single point.
        hv = calculate_hypervolume_two(front_points, self.hv_samples) 
        self.history_hv.append(hv)
        
        return [], self.gbest_score, -1 # Return dummy perm/cut
