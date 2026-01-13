
import numpy as np
import random
from typing import List, Tuple

def calculate_hypervolume_two(F, samples: np.ndarray) -> float:
    """
    Approximates the hypervolume contribution of a point or a set of points F 
    against a set of random samples within the Utopia-AntiUtopia box.
    
    Ported from MATLAB's hypervolumetwo.m
    
    Args:
        F: A single point (Profit, Carbon) OR a List of points [(P, C), ...].
           - Objective 1: Profit (Maximize) -> The MATLAB code checks F(1) > sample(1)
           - Objective 2: Carbon (Minimize) -> The MATLAB code checks F(2) < sample(2)
        samples: A (N, 2) array of random samples in the objective space.
        
    Returns:
        The ratio of samples dominated by F (or by ANY point in F if F is a list).
    """
    if isinstance(F, list):
        # Union of dominated spaces
        if not F: return 0.0
        final_mask = np.zeros(len(samples), dtype=bool)
        for pt in F:
            # Check dominance for this point
            mask = (pt[0] > samples[:, 0]) & (pt[1] < samples[:, 1])
            final_mask |= mask # Union
        dominated_count = np.sum(final_mask)
        return float(dominated_count) / len(samples)

    else:
        # Single Point
        # Vectorized implementation
        # Check if F dominates samples:
        # Profit > Sample Profit AND Carbon < Sample Carbon
        dominated_mask = (F[0] > samples[:, 0]) & (F[1] < samples[:, 1])
        dominated_count = np.sum(dominated_mask)
        
        return float(dominated_count) / len(samples)

def generate_hypervolume_samples(n_samples: int, utopia: Tuple[float, float], anti_utopia: Tuple[float, float]) -> np.ndarray:
    """
    Generates random samples for Hypervolume approximation.
    
    Args:
        n_samples: Number of samples (e.g., 1000)
        utopia: Ideal point [Max Profit, Min Carbon] -> e.g., [350, 0.001]
        anti_utopia: Worst point [Min Profit, Max Carbon] -> e.g., [0, 100]
        
    Returns:
        (N, 2) array of samples
    """
    # MATLAB: samples = bsxfun(@plus, AU, bsxfun(@times, (U - AU), rand(N, dim)));
    
    u = np.array(utopia)
    au = np.array(anti_utopia)
    diff = u - au # vector from AU to U
    
    # Note: U-AU might have negative components if U(2) < AU(2).
    # Carbon: U=0.001, AU=100 -> Diff = -99.999.
    # Profit: U=350, AU=0 -> Diff = 350.
    # rand * diff + AU correctly interpolates.
    
    random_scaling = np.random.rand(n_samples, 2)
    samples = au + (diff * random_scaling)
    
    return samples

def is_dominated(p1: Tuple[float, float], p2: Tuple[float, float]) -> bool:
    """
    Checks if p1 dominates p2.
    Assuming:
    - Obj 1 (Profit): Maximize
    - Obj 2 (Carbon): Minimize
    
    p1 dominates p2 if:
    p1.profit >= p2.profit AND p1.carbon <= p2.carbon
    AND at least one inequality is strict.
    """
    # Profit: Higher is better
    better_profit = p1[0] >= p2[0]
    strict_profit = p1[0] > p2[0]
    
    # Carbon: Lower is better
    better_carbon = p1[1] <= p2[1]
    strict_carbon = p1[1] < p2[1]
    
    return (better_profit and better_carbon) and (strict_profit or strict_carbon)

def compute_pareto_front(population_scores: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """
    Filters a list of (Profit, Carbon) tuples to return the Non-Dominated Set (Pareto Front).
    """
    pareto_front = []
    for i, p in enumerate(population_scores):
        dominated = False
        for j, q in enumerate(population_scores):
            if i == j: continue
            if is_dominated(q, p):
                dominated = True
                break
        if not dominated:
            pareto_front.append(p)
            
    # Sort by Profit (Ascending) for cleaner plotting curves
    pareto_front.sort(key=lambda x: x[0])
    
    # Remove duplicates
    unique_front = []
    if pareto_front:
        unique_front.append(pareto_front[0])
        for pt in pareto_front[1:]:
            # If slightly different floating point, keep? 
            # Or strict equality check.
            if abs(pt[0] - unique_front[-1][0]) > 1e-6 or abs(pt[1] - unique_front[-1][1]) > 1e-6:
                unique_front.append(pt)
                
    return unique_front
