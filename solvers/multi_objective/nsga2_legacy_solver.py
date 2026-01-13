
import random
import numpy as np
from typing import List, Tuple, Dict, Optional
from .nsga2_solver import NSGA2Solver
from .multi_objective_utils import compute_pareto_front, calculate_hypervolume_two

class NSGA2LegacySolver(NSGA2Solver):
    """
    Legacy NSGA-II Solver based on user's MATLAB implementation (NSGAII.m).
    
    Key Characteristics (Different from Standard NSGA-II):
    1. 'Elitist Random Search' behavior:
       - In each generation, the population is formed by:
         [Current Pareto Front (Archive)] + [New Random Individuals]
       - This differs from standard NSGA-II which creates offspring from parents.
    2. Maintains the 'Archive' (A) explicitly.
    """

    def __init__(self, population_size: int = 100, generations: int = 100, 
                 crossover_rate: float = 0.8, mutation_rate: float = 0.2, data_class=None):
        super().__init__(population_size, generations, crossover_rate, mutation_rate, data_class)
        self.archive_front = [] # Stores (profit, carbon) of best front
        self.archive_pop = []   # Stores chromosomes of best front

    def evolve(self) -> Tuple[List[int], Tuple[float, float], int]:
        # 1. Initialize logic
        if not self.population:
            for _ in range(self.population_size):
                p = np.random.permutation(self.num_jobs) + 1
                p = self._repair_chromosome(list(p))
                self.population.append(list(p))
        else:
            # === User's MATLAB Logic (Lines 69-83) ===
            # If we have an Archive (A), use it.
            # Pop = Archive + Randoms to fill Remaining
            
            new_pop = []
            
            # 1. Keep Archive (Elitism)
            if self.archive_pop:
                # If Archive is larger than Population, we must select the best (Crowding Distance)
                # otherwise we blindly cut potentially good solutions, causing HV fluctuation.
                if len(self.archive_pop) > self.population_size:
                    # Calculate Crowding for Archive
                    # self.archive_front contains the objectives for self.archive_pop
                    
                    # We need indices [0...N-1]
                    indices = list(range(len(self.archive_pop)))
                    # Calculate Distances using base class method
                    dists = self._calculate_crowding_distance(indices, self.archive_front)
                    
                    # Sort indices by distance descending (keep most isolated)
                    sorted_indices = sorted(indices, key=lambda i: dists[i], reverse=True)
                    
                    # Keep top N
                    keep_indices = sorted_indices[:self.population_size]
                    
                    # Rebuild archive
                    self.archive_pop = [self.archive_pop[i] for i in keep_indices]
                    self.archive_front = [self.archive_front[i] for i in keep_indices]
                    
                new_pop.extend(self.archive_pop)
                
            # 2. Fill the rest with Randoms
            slots_remaining = self.population_size - len(new_pop)
            
            # Since we ensured len(new_pop) <= pop_size above, slots_remaining >= 0
            
            for _ in range(slots_remaining):
                p = np.random.permutation(self.num_jobs) + 1
                p = self._repair_chromosome(list(p))
                new_pop.append(list(p))
            
            self.population = new_pop

        # === Crossover & Mutation (Lines 97-99) ===
        # User's code applies PPX and Mutation AFTER filling the population
        # This acts as a "Shake" on the archive + randoms
        
        # Crossover
        offspring_pop = []
        indices = list(range(len(self.population)))
        random.shuffle(indices)
        
        for i in range(0, len(self.population), 2):
            if i+1 >= len(self.population):
                offspring_pop.append(self.population[indices[i]])
                break
            
            p1 = self.population[indices[i]]
            p2 = self.population[indices[i+1]]
            
            if random.random() < self.crossover_rate:
                c1 = self._ppx_crossover(p1, p2)
                c2 = self._ppx_crossover(p2, p1)
                offspring_pop.extend([c1, c2])
            else:
                offspring_pop.extend([p1, p2])
        
        self.population = offspring_pop
        
        # Mutation
        for i in range(len(self.population)):
            if random.random() < self.mutation_rate:
                idx1, idx2 = random.sample(range(self.num_jobs), 2)
                self.population[i][idx1], self.population[i][idx2] = self.population[i][idx2], self.population[i][idx1]
                self.population[i] = self._repair_chromosome(self.population[i])
        
        # === Evaluation & Archive Update ===
        # Calculate Objectives
        current_objs = []
        for chrom in self.population:
            f1, f2, _ = self.calculate_objectives(chrom)
            current_objs.append((f1, f2))
            
        # Extract Pareto Front (The "p" function in MATLAB)
        # This will separate Non-Dominated from Dominated
        fronts = self._fast_non_dominated_sort(current_objs)
        best_front_indices = fronts[0]
        
        # Update Archive 'A'
        self.archive_pop = [self.population[i] for i in best_front_indices]
        self.archive_front = [current_objs[i] for i in best_front_indices]
        
        # Update metrics (GBest Balance)
        best_dist = float('inf')
        for idx in best_front_indices:
            p, c = current_objs[idx]
            dist = np.sqrt((self.utopia[0]-p)**2 + (self.utopia[1]-c)**2)
            if dist < best_dist:
                best_dist = dist
                self.gbest_score = (p, c)
                
        # HV
        if self.archive_front:
             # Use Set-based HV for stable convergence
             hv = calculate_hypervolume_two(self.archive_front, self.hv_samples)
             self.history_hv.append(hv)
        else:
             self.history_hv.append(0)

        return [], self.gbest_score, -1
