
import numpy as np
import random
from typing import List, Tuple

def calculate_hypervolume_two(F: Tuple[float, float], samples: np.ndarray) -> float:
    """
    Approximates the hypervolume contribution of a single point F 
    against a set of random samples within the Utopia-AntiUtopia box.
    
    Ported from MATLAB's hypervolumetwo.m
    
    Args:
        F: A single point (Profit, Carbon)
           - Objective 1: Profit (Maximize) -> The MATLAB code checks F(1) > sample(1)
           - Objective 2: Carbon (Minimize) -> The MATLAB code checks F(2) < sample(2)
        samples: A (N, 2) array of random samples in the objective space.
        
    Returns:
        The ratio of samples dominated by F.
        Effectively approximates the area of the rectangle defined by F 
        that falls within the "better" region relative to the samples.
    """
    # MATLAB Logic:
    # dominated = 0;
    # for i = 1 : N
    #     if F(1) > samples(i,1) & F(2) < samples(i,2)
    #         dominated = dominated + 1;
    #     end
    # end
    # hv = dominated / N;
    
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
