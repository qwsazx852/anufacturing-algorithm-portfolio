
from typing import List, Dict, Tuple

class StaplerData:
    """
    Data for the Stapler Disassembly Case Study (n=18).
    Source: MATLAB fitness1.m / fitness2.m
    """
    
    # 1. Basic Problem Size
    NUM_PARTS = 18
    
    # 2. Liaison Relationships (Component IDs in disassembly logic) -> "Dc"
    # Note: These values seem to be the Component IDs themselves or a mapping.
    # In fitness1.m: Dc = [18,10,16,17,3,14,2,9,5,6,7,15,11,12,13,1,8,4]
    DC_SEQUENCE = [18, 10, 16, 17, 3, 14, 2, 9, 5, 6, 7, 15, 11, 12, 13, 1, 8, 4]
    
    # 3. Disassembly Costs (Per Component?) -> "DC2"
    # Corresponds to DC_SEQUENCE
    DISASSEMBLY_COSTS = [
        0.9297, 0.911, 0.797, 0.797, 0.797, 0.797, 0.482, 0.294, 0.266, 0.266, 
        0.224, 0.1727, 0.1727, 0.1727, 0.1354, 0.0234, 0.0234, 0.0234
    ]
    
    # 4. Component Weights (kg) -> "gw"
    # Indexes presumably 1-based in MATLAB, so index 0 is Part 1.
    WEIGHTS = [
        0.015, 0.005, 0.003, 0.008, 0.0025, 0.003, 0.0013, 0.006, 0.002, 
        0.003, 0.002, 0.009, 0.0021, 0.0012, 0.0025, 0.003, 0.003, 0.004
    ]
    
    # 5. Component Costs (New Part Cost) -> "mc"
    NEW_PART_COSTS = [
        25, 5, 2, 25, 10, 8, 7, 10, 8, 2, 5, 20, 5, 5, 7, 2, 2, 2
    ]
    
    # 6. Carbon Coefficients -> "cc" 
    # (Used for remanufacturing carbon calc)
    CARBON_COEFFS = [
        0.31, 0.31, 0.43, 0.43, 0.12, 0.43, 0.12, 0.31, 0.43, 
        0.43, 0.31, 0.31, 0.12, 0.31, 0.31, 0.31, 0.31, 0.43
    ]
    
    # 7. Operation Sets (1-based IDs from MATLAB)
    # We will convert to 0-based in logic or keep 1-based and handle carefully.
    REUSE = [2, 5, 7, 9, 13]
    RECYCLE = [1, 3, 10, 14, 15, 16, 17, 18]
    REMANUFACTURING = [4, 6, 8, 11]
    TRASH = [12] # inferred from 't' variable in fitness1.m
    
    # 8. Constants
    TOTAL_DISASSEMBLY_COST_REF = 7.2844 # 'c'
    CARBON_COEFF_DISASSEMBLY = 0.509 # 'Cs'
    RECYCLE_REVENUE_RATE = 0.005 # 5 NTD/kg ? (Code says 0.005)
    PROCESSING_COST_FACTOR = 1.5
    
    # 9. Tooling Data (Approximate based on T1, T2 in PSO_line_balance.m)
    # T1 seems to be Tool Type ID for each job position in a sequence? 
    # Actually T1 length is 18. It maps Job ID to Tool ID?
    # T1=[3 1 2 3 4 3 3 3 3 3 1 1 1 2 4 2 2 3]
    JOB_TOOL_MAPPING = [3, 1, 2, 3, 4, 3, 3, 3, 3, 3, 1, 1, 1, 2, 4, 2, 2, 3] # Job 1->Tool 3, Job 2->Tool 1...
    
    # T2=[2 -2 -2 2 -2 -1 1 2 1 -2 2 -2 -2 -2 -2 -2 -2 -3]
    # Direction mappings? Job 1 -> Dir 2...
    JOB_DIRECTION_MAPPING = [2, -2, -2, 2, -2, -1, 1, 2, 1, -2, 2, -2, -2, -2, -2, -2, -2, -3]

    # Precedence Constraints (from PSO_line_balance.m)
    # 1-based pairs (Pre, Suc)
    # Disassembly Precedence
    CONSTRAINTS = [
        (3, 2), (3, 1), (4, 5), (4, 8), (5, 7), (5, 6), (6, 9), (7, 9), 
        (8, 6), (10, 12), (11, 12), (13, 12), (14, 1), (14, 4), (15, 12), 
        (16, 15), (17, 15), (18, 10), (18, 11), (18, 13)
    ]
