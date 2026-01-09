
import random
import numpy as np
from typing import List, Tuple, Dict, Optional
from .npso_solver import NPSOSolver
from .multi_objective_utils import calculate_hypervolume_two

class PSOPPXSolver(NPSOSolver):
    """
    Hybrid PSO + PPX + Neighborhood Search Solver (Legacy Version).
    Based on 'taxpsonoc.m'.
    
    Mechanism:
    1. Runs valid NPSO (Particle Swarm) logic primarily.
    2. After 'neighborhood_start_gen' (Ns), it activates PPX Crossover.
    3. The PPX crossover acts as a "Neighborhood Search" on the swarm.
    4. Maintains a Pareto Archive (a1) to preserve best solutions.
    """

    def __init__(self, population_size: int = 100, generations: int = 100, 
                 crossover_rate: float = 0.8, mutation_rate: float = 0.2, 
                 neighborhood_start_gen: int = 50, data_class=None):
        # NPSOSolver uses 'num_particles' instead of 'population_size'
        super().__init__(num_particles=population_size, generations=generations, data_class=data_class)
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.neighborhood_start_gen = neighborhood_start_gen
        
        # Archive (stores Permutations, not X)
        self.archive_permutations: List[List[int]] = []
        self.archive_objs: List[Tuple[float, float]] = []
        
        self.current_gen = 0

    def _ppx_crossover(self, parent1: List[int], parent2: List[int]) -> List[int]:
        n = self.num_jobs
        mask = [random.choice([1, 2]) for _ in range(n)]
        child = []
        p1_temp = parent1[:]
        p2_temp = parent2[:]
        
        for k in range(n):
            source = mask[k]
            if source == 1:
                if not p1_temp: break
                gene = p1_temp[0]
                child.append(gene)
                p1_temp.pop(0)
                if gene in p2_temp: p2_temp.remove(gene)
            else:
                if not p2_temp: break
                gene = p2_temp[0]
                child.append(gene)
                p2_temp.pop(0)
                if gene in p1_temp: p1_temp.remove(gene)
        return child

    def _encode_permutation_to_continuous(self, permutation: List[int]) -> np.ndarray:
        """
        Encodes a permutation (job sequence) back to continuous X values suitable for PSO.
        Strategy: X[job_id - 1] = position_index
        This ensures argsort(X) returns the original permutation.
        """
        x_vec = np.zeros(self.num_jobs)
        for idx, job_id in enumerate(permutation):
            x_vec[job_id - 1] = float(idx)
        return x_vec

    def evolve(self):
        # 1. Standard NPSO Step (Velocity Update + Move)
        # This updates self.X, self.V, pbest, gbest
        super().evolve() # NPSO has 'evolve' method? Wait ensure checking npso_solver logic
        # NPSO Logic:
        # It calls _calculate_objectives_all -> updates pbest -> updates gbest
        # Then updates V, X.
        
        self.current_gen += 1
        
        # 2. Update Archive (Pareto Front of Current Pop)
        # Decode current X to Perms
        current_perms = []
        current_pop_objs = []
        
        # NPSOSolver doesn't store computed objectives for current gen X generally exposed?
        # It updates pbest. Let's re-calculate to be safe or inspect NPSO internals.
        # NPSO evolve implementation usually calcs them.
        
        for i in range(self.num_particles):
            perm = self._decode_position(self.X[i])
            current_perms.append(perm)
            f1, f2, _ = self.calculate_objectives(perm)
            current_pop_objs.append((f1, f2))
             
        # Combine with existing Archive
        all_perms = current_perms + self.archive_permutations
        all_objs = current_pop_objs + self.archive_objs
        
        # Non-Dominated Sort (Simple Filter)
        combined_data = list(zip(all_perms, all_objs))
        non_dominated = []
        
        for i in range(len(combined_data)):
            is_dominated = False
            p1_obj = combined_data[i][1]
            for j in range(len(combined_data)):
                if i == j: continue
                p2_obj = combined_data[j][1]
                # Dominated if p2 better/equal in all
                if (p2_obj[0] >= p1_obj[0] and p2_obj[1] <= p1_obj[1]) and \
                   (p2_obj[0] > p1_obj[0] or p2_obj[1] < p1_obj[1]):
                    is_dominated = True
                    break
            if not is_dominated:
                non_dominated.append(combined_data[i])
        
        # Update Archive
        self.archive_permutations = [x[0] for x in non_dominated]
        self.archive_objs = [x[1] for x in non_dominated]
        
        # 3. Neighborhood Search (PPX) Logic
        # Active only after Ns
        if self.current_gen > self.neighborhood_start_gen:
            new_perms = []
            
            # Shuffle indices for mating
            indices = list(range(self.num_particles))
            random.shuffle(indices)
            
            for i in range(0, self.num_particles, 2):
                if i+1 >= self.num_particles:
                    new_perms.append(current_perms[indices[i]])
                    break
                p1 = current_perms[indices[i]]
                p2 = current_perms[indices[i+1]]
                
                if random.random() < self.crossover_rate:
                    c1 = self._ppx_crossover(p1, p2)
                    c2 = self._ppx_crossover(p2, p1)
                    new_perms.extend([c1, c2])
                else:
                    new_perms.extend([p1, p2])
            
            # Inject Archive (Elitism) replacing tail - MATLAB Logic
            # Matlab: fxm_ans{pp+i} = a1(i,:)
            # Replaces the last N slots with Archive
            num_archive = len(self.archive_permutations)
            if num_archive > 0:
                count_to_inject = min(num_archive, self.num_particles)
                for k in range(count_to_inject):
                    # Replace
                    new_perms[-(k+1)] = self.archive_permutations[k][:]
            
            # Encode back to X (Continuous)
            # This effectively "Teleports" particles, disrupting velocity
            for i in range(self.num_particles):
                self.X[i] = self._encode_permutation_to_continuous(new_perms[i])
                # Note: Velocity V is kept as is (Momentum preserved in direction, but position jumped)
                
        # 4. History HV Update (Use Archive best balance like NPSO compatibility)
        # Ideally calculate HV of the whole archive
        if self.archive_objs:
             best_dist = float('inf')
             best_point = (0,0)
             for p, c in self.archive_objs:
                 dist = np.sqrt((self.utopia[0]-p)**2 + (self.utopia[1]-c)**2)
                 if dist < best_dist:
                     best_dist = dist
                     best_point = (p, c)
             
             self.gbest_score = best_point 
             
             hv = calculate_hypervolume_two(self.archive_objs, self.hv_samples)
             # Update historical record
             if len(self.history_hv) >= self.current_gen:
                 self.history_hv[-1] = hv
             else:
                 self.history_hv.append(hv)

        return [], self.gbest_score, -1
        
    def get_pareto_front(self) -> List[Tuple[float, float]]:
        """Return the current Pareto Archive."""
        return self.archive_objs
