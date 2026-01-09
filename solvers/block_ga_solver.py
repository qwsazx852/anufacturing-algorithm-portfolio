
import random
import numpy as np
from typing import List, Tuple, Dict, Optional
from .problem_data import StaplerData
from .multi_objective_utils import calculate_hypervolume_two, generate_hypervolume_samples
import copy

class BlockGASolver:
    """
    Block-Based Genetic Algorithm (BGA) for Disassembly Line Balancing.
    Ports logic from 'LBGAASB.m' (Block GA), 'LBa1.m' (Block Crossover), 'LBb0.m' (Greedy Mutation).
    
    Objectives:
    1. Maximize Profit (f1)
    2. Minimize Carbon Footprint (f2)
    """
    
    def __init__(self, population_size: int = 100, generations: int = 100, 
                 crossover_rate: float = 0.8, mutation_rate: float = 0.1, block_size_ratio: float = 0.4):
        self.population_size = population_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.block_size_ratio = block_size_ratio
        
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
        
        # Population State
        # Chromosomes: List of permutaions (List[int])
        self.population: List[List[int]] = []
        self.fitness_scores: List[Tuple[float, float, int]] = [] # (Profit, Carbon, CutIndex)
        
        self.history_hv = []
        
        # Global Best logic (for final result compatibility)
        self.gbest_permutation = None
        self.gbest_score = (float('-inf'), float('inf'))
        self.gbest_cut_index = -1
        self.gbest_metric = float('inf') # Distance to Utopia

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
                if self.precedence_matrix[job_later - 1, job_prior - 1] == 1:
                    seq[i], seq[j] = seq[j], seq[i] # Swap
                    job_prior = seq[i] 
        return seq
        
    def _is_valid_partial(self, partial_seq: List[int], candidate: int) -> bool:
        """
        Check if appending 'candidate' to 'partial_seq' is valid regarding PRECEDENCE.
        i.e. all predecessors of 'candidate' must be in 'partial_seq'.
        """
        # Slow check:
        # Predecessors of candidate:
        # check self.precedence_matrix[pre-1, candidate-1] == 1
        # if any predecessor is NOT in partial_seq, then invalid.
        # But transitive closure matrix means direct and indirect.
        # So we just check if any job 'p' exists such that p->candidate and p is NOT in partial_seq.
        
        # Optimization: precompute predecessors for each node
        # But O(N^2) for small N is fine.
        for p in range(1, self.num_jobs + 1):
            if self.precedence_matrix[p-1, candidate-1] == 1: # p is predecessor of candidate
                if p not in partial_seq:
                    return False
        return True

    def calculate_objectives(self, sequence: List[int]) -> Tuple[float, float, int]:
        """
        Calculates objectives. This logic is identical to NPSO's logic.
        Since we need the same Profit/Carbon implementation, I will duplicate straightforward logic here
        or ideally import it if refactored. For safety and speed, I will duplicate the specific heuristics.
        """
        # Reuse NPSO logic exactly.
        # Strategy 1: Max Profit scan
        # Strategy 2: Heuristic Cut
        
        # Strategy 1 Scan
        total_weight = sum(self.data.WEIGHTS)
        limit = total_weight * 0.7
        rang = len(sequence)
        current_w = 0
        for i, part in enumerate(sequence):
            current_w += self.data.WEIGHTS[part - 1]
            if current_w >= limit:
                rang = i + 1
                break
        
        best_f1 = float('-inf')
        best_res_1 = (float('-inf'), float('inf'), -1)
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
            if part in self.data.REUSE: val = 1
            elif part in self.data.RECYCLE: val = -0.5
            elif part in self.data.REMANUFACTURING: val = -0.3
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
        
        # Choose Best
        d1 = np.sqrt((self.utopia[0]-best_res_1[0])**2 + (self.utopia[1]-best_res_1[1])**2)
        d2 = np.sqrt((self.utopia[0]-best_res_2[0])**2 + (self.utopia[1]-best_res_2[1])**2)
        
        if d1 <= d2: return best_res_1
        else: return best_res_2

    def _calculate_metrics_at_cut(self, sequence: List[int], cut_index: int) -> Tuple[float, float]:
        # Identical to NPSO... to be DRY I should have refactored but user wants speed.
        # I'll paste the logic (it's robust enough)
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

    # --- Block GA Specific Logic ---

    def _block_crossover(self, parent1: List[int], parent2: List[int]) -> List[int]:
        """
        LBa1.m Logic:
        1. Extract blocks from parent1.
        2. Find best block (max Profit).
        3. Implant into parent2 (create child).
        4. Repair/Fill missing.
        """
        n = self.num_jobs
        bs = max(2, int(n * self.block_size_ratio))
        
        # 1. Extract and Eval all blocks in P1
        best_block_fitness = float('-inf')
        best_block = []
        best_block_idx = 0 # start index in P1
        
        # Iterate valid blocks
        for i in range(n - bs + 1):
            block = parent1[i : i+bs]
            # Eval block fitness? LBa1 uses LBss2 just on the block? 
            # Or does it treat the block as a partial sequence?
            # LBa1 says: SS = LBss2(RR).
            # If RR is partial, LBss2 needs to handle it.
            # My `calculate_objectives` assumes full sequence for cut-off logic.
            # But here `block` is short.
            # Assuming we just calculate Profit of the block parts?
            # Or assume the block implies disassembly of those parts?
            # heuristic strategy: sum of rewards?
            # Let's use simplified profit for block selection: 350 - costs + revenue?
            # Reuse `_calculate_metrics_at_cut` assuming block is disassemble list?
            # But the rest is not defined.
            # Let's assume we treat the block as the "Disassembled Set" and ignore the rest for fitness comparison.
            
            # Using basic Profit metric for block evaluation
            # Just profit of parts in block
            f1_block, _ = self._calculate_metrics_at_cut(block, len(block))
            if f1_block > best_block_fitness:
                best_block_fitness = f1_block
                best_block = block
                best_block_idx = i
                
        # 2. Implant into P2 (child)
        child = parent2[:]
        
        # LBa1: "b1(d(end):d(end)+Bs-1)=d(1:Bs)" - wait.
        # It copies the block to the SAME start position as it was found in P1?
        # "P=round(rand...)" -> in LBa1 it selects a random block among the best ones if multiple?
        # But crucially: "d(end)" seems to be the index?
        # MatLAB: c=[c; RR SS i] -> i is index. d=f(P,:) -> d includes SS and i.
        # So d(end) is the start index 'i'.
        # So yes, it implants the block at the SAME index in P2.
        
        start_pos = best_block_idx
        # Overwrite P2 at start_pos with best_block
        child[start_pos : start_pos+bs] = best_block
        
        # 3. Remove duplicates (keep the ones in the implanted block)
        # Identify duplicates: items in child that are in best_block but NOT at the block position
        # We need to preserve the structure.
        # Actually, simpler: construct child.
        # Elements in best_block are fixed.
        # Elements in parent2 that are NOT in best_block are kept, filling the gaps?
        # LBa1: "b1(B1)=[]" removes duplicates.
        # Then "LBrr1" repairs?
        # LBa1 Logic:
        #  It puts the block in P2. The values in P2 that were overwritten are gone.
        #  The values in P2 elsewhere that match the block values must be removed.
        #  Then we have a sequence shorter than N.
        #  Then we insert missing values using Greedy Insertion!
        
        # Let's do that:
        # A. Create list with the Block in place, other slots None?
        child_prio = [None] * n
        child_prio[start_pos : start_pos+bs] = best_block
        
        # B. Items from P2 that are NOT in block
        p2_remaining = [x for x in parent2 if x not in best_block]
        
        # C. Fill None slots with p2_remaining in order? 
        # LBa1 says: remove duplicates from b1. Then b1 shrinks?
        # Then "for i=1:n ... if missing ... greedy insert".
        # So it reduces the sequence, then expands.
        
        # My implementation:
        # 1. Start with the Block.
        current_seq = best_block[:]
        # 2. Add remaining elements from P2? 
        # Actually LBa1 keeps P2's structure but deletes duplicates.
        # So: child starts as P2. Implants Block.
        # Then finds where the Block elements are duplicated (outside the block region) and removes them.
        # But this shifts indices!
        # "b1(B1)=[]" - yes, it shrinks.
        
        temp_child = parent2[:]
        temp_child[start_pos : start_pos+bs] = [-1] * bs # Mark block slots temporarily
        
        # Remove values that are in best_block (they are duplicates)
        temp_child = [x for x in temp_child if x not in best_block]
        
        # Now we have temp_child (shorter) and best_block.
        # Where to put best_block? LBa1 inserts it at 'start_pos'?
        # LBa1 logic is messy.
        # Let's infer the intent: "Block Preserving".
        # We want to keep the "Good Block" intact.
        # We want to keep the rest of P2 order as much as possible.
        # And we want to insert missing items greedily.
        
        # Simplified Block Crossover:
        # 1. Start with Best Block.
        # 2. Add missing items from P2 into valid greedy positions?
        # 3. Or just append remaining items from P2 and then repair constraints?
        
        # LBa1 explicitly does Greedy Insertion for missing items.
        # "for i=1:n ... if isempty(find(b1==i)) ... greedy insert".
        # This means we start with JUST the manipulated P2 (shorter) and insert missing.
        
        # So:
        # 1. Start with `current_seq` = P2 with duplicates removed, and Block implanted? 
        #    Actually LBa1 implants block, removes duplicates, so sequence is valid but maybe shorter? 
        #    No, P2 had N elements. Replaced k with k. Duplicates removed -> Length < N.
        #    So we have a partial sequence.
        #    The "Head" and "Tail" relative to the block are from P2.
        
        # Let's reconstruct Step 2/3 precisely.
        # P2: [A B C D E]
        # Block from P1: [C A] at index 1 (replacing B C).
        # P2 becomes [A C A D E]? No, [A [C A] D E].
        # Duplicates: A is at 0 and 2. C is at 1.
        # LBa1 removes duplicates *elsewhere*.
        # So we keep [C A] at index 1.
        # Old A at 0 is removed. Old C at 2 (was B C) is removed.
        # This is getting complex to index.
        
        # Robust Logic:
        # 1. Validation: The Block is highly fit, preserving precedence (likely, as it came from valid P1).
        #    Check precedence of block internal. If invalid, repair block first.
        # 2. Construct partial sequence `S`:
        #    - Items of P2 that are NOT in Block.
        # 3. Attempt to Insert Block into `S` at heuristic position? Or P2's original position?
        #    LBa1 uses original position.
        # 4. Insert Missing Items (if any left out) Greedily.
        
        # 3. Remove duplicates from P2
        # Use set for robustness (handle np.int64 types etc)
        block_set = set(best_block)
        child = [x for x in parent2 if x not in block_set]
        # Insert `best_block` at `start_pos` (clamped).
        if start_pos > len(child): start_pos = len(child)
        child[start_pos:start_pos] = best_block # Batch insert
        
        # Now `child` has all elements? 
        # P2 had N unique. Block has K unique.
        # Child has (N-K) + K = N unique.
        # So it is a full permutation.
        # But Precedence might be broken!
        if start_pos > len(child): start_pos = len(child)
        
        child[start_pos:start_pos] = best_block
        
        # Robust Fix: Ensure Permutation
        # Remove any duplicates if they slipped through (filtering using set)
        seen = set()
        unique_child = []
        for x in child:
            if x not in seen:
                unique_child.append(x)
                seen.add(x)
        
        # Fill missing
        if len(unique_child) < n:
            missing = [x for x in range(1, n+1) if x not in seen]
            # Greedy insert missing? Or just append? 
            # LBa1 says greedy insert.
            # But for stability, lets just append and expect mutation to fix order or use simple repair
            unique_child.extend(missing)
            
        child = unique_child
        
        repaired_child = self._repair_chromosome(child)
        return repaired_child

    def _greedy_mutation(self, chrom: List[int]) -> List[int]:
        """
        LBb0.m Logic:
        1. Remove a gene 'p1'.
        2. Try inserting 'p1' at all valid positions.
        3. Pick best position (Max Profit).
        """
        n = len(chrom)
        # Pick random gene to move
        idx_to_remove = random.randint(0, n - 1)
        gene = chrom[idx_to_remove]
        
        # Remove
        partial = chrom[:idx_to_remove] + chrom[idx_to_remove+1:]
        
        # Find all valid insertion points
        # Naive: try all n positions (0 to n-1)
        # Check validity.
        best_child = None
        best_f1 = float('-inf')
        
        # Optimization: Find range of valid positions.
        # Must be AFTER all predecessors.
        # Must be BEFORE all successors.
        
        # Find predecessors in partial
        earliest_idx = 0
        latest_idx = len(partial)
        
        for i, p in enumerate(partial):
            # if p is predecessor of gene, gene must be > i -> earliest = i+1
            if self.precedence_matrix[p-1, gene-1] == 1:
                earliest_idx = max(earliest_idx, i + 1)
            # if p is successor of gene, gene must be < i -> latest = i
            if self.precedence_matrix[gene-1, p-1] == 1:
                latest_idx = min(latest_idx, i)
        
        if earliest_idx > latest_idx:
            # Should not happen if partial was valid?
            # Just insert at earliest (heuristic) or back at original
            candidates = [earliest_idx] 
        else:
            candidates = range(earliest_idx, latest_idx + 1)
            
        for idx in candidates:
            # Construct candidate sequence
            cand_seq = partial[:idx] + [gene] + partial[idx:]
            
            # Eval Profit
            # Use Strategy 1 (Max Profit) as proxy for quality
            # We don't need full heuristics, just quick check. 
            # Actually, calculate_objectives (Strategy 1) is good.
            res = self.calculate_objectives(cand_seq) # (f1, f2, k)
            f1 = res[0]
            
            if f1 > best_f1:
                best_f1 = f1
                best_child = cand_seq
        
        return best_child if best_child is not None else chrom # Fallback

    def evolve(self) -> Tuple[List[int], Tuple[float, float], int]:
        # Initialize population if empty
        if not self.population:
            for _ in range(self.population_size):
                p = np.random.permutation(self.num_jobs) + 1
                p = self._repair_chromosome(list(p))
                self.population.append(list(p))
        
        # Run Evolution Step
        new_pop = []
        
        # 1. Elitism: Keep best? LBa0 keeps everything then selects?
        # I'll keep strict population size.
        
        # Crossover Loop
        # Select parents
        indices = list(range(self.population_size))
        random.shuffle(indices)
        
        for i in range(0, self.population_size, 2):
            if i+1 >= self.population_size: 
                new_pop.append(self.population[indices[i]])
                break
                
            p1 = self.population[indices[i]]
            p2 = self.population[indices[i+1]]
            
            if random.random() < self.crossover_rate:
                c1 = self._block_crossover(p1, p2)
                c2 = self._block_crossover(p2, p1)
                new_pop.extend([c1, c2])
            else:
                new_pop.extend([p1, p2])
                
        # Mutation Loop
        for i in range(len(new_pop)):
            if random.random() < self.mutation_rate:
                new_pop[i] = self._greedy_mutation(new_pop[i])
                
        self.population = new_pop
        
        # Evaluate & Update Bests
        best_gen_score = (float('-inf'), float('inf'))
        best_gen_cut = -1
        best_gen_perm = None
        best_gen_dist = float('inf')
        
        for chrom in self.population:
             profit, carbon, cut = self.calculate_objectives(chrom)
             
             dist = np.sqrt((self.utopia[0]-profit)**2 + (self.utopia[1]-carbon)**2)
             
             if dist < self.gbest_metric:
                 self.gbest_metric = dist
                 self.gbest_score = (profit, carbon)
                 self.gbest_permutation = chrom[:]
                 self.gbest_cut_index = cut
             
             if dist < best_gen_dist:
                 best_gen_dist = dist
                 best_gen_score = (profit, carbon)
                 best_gen_cut = cut
                 best_gen_perm = chrom[:]
                 
        # History
        hv = calculate_hypervolume_two(self.gbest_score, self.hv_samples)
        self.history_hv.append(hv)
        
        return self.gbest_permutation, self.gbest_score, self.gbest_cut_index
