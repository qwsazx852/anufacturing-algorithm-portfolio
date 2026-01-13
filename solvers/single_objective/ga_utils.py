import random
import numpy as np
def LBbn(order, n):
    # 初始化 CA 和 bn
    CA = [None] * n
    bn = np.zeros(n)

    for i in range(1, n + 1):
        if np.sum(order[:, 0] == i) != 0:
            ww = np.concatenate([order[order[:, 0] == i, 1], [10000]])
            xx = np.concatenate([order[order[:, 0] == i, 1], order[order[:, 0] == ww[0], 1]])
            
            while np.sum(ww) != 10000:
                ww = np.concatenate([ww[1:], order[order[:, 0] == ww[0], 1], [ww[-1]]])
                ww = np.unique(ww)
                xx = np.concatenate([xx, order[order[:, 0] == ww[0], 1]])
                xx = np.unique(xx)

            bn[i - 1] = np.count_nonzero(xx)
            CA[i - 1] = xx
        else:
            bn[i - 1] = 0

    # 创建输出矩阵 Or
    Or = np.zeros((n, n))

    for i in range(n):
        if CA[i] is not None:
            for j in range(len(CA[i])):
                Or[i, int(CA[i][j] - 1)] = 1  # 减去1以适应0索引

    return Or

def LBrr1(Or, n, RR):
    """生成可行解"""
    non_zero_indices = np.nonzero(RR)[0]

    for i in range(len(non_zero_indices)):
        for j in range(i+1, len(non_zero_indices)):
           
            if Or[RR[j]-1, RR[i]-1] == 1:
                # 交换元素
                b = RR[j]
                RR[j] = RR[i]
                RR[i] = b
                
    return RR

def ppx(n,crossover,parent1,parent2):
    offspring = []
    fitness = []
    #交配機制
    # D = np.random.randint(1, 3, size=(2, n))
    if random.random() < crossover:
        D = np.random.randint(1, 3, size=(2, n))
        for e in range(2):
            b1 = parent1[:]
            # print(b1)
            b2 = parent2[:]
            # print(b2)
            child = []

            for t in range(n):
                if D[e, t] == 1:
                    gene = b1.pop(0)  # pop取第一個直回傳並移除
                    child.append(gene)
                    b2.remove(gene)
                    
                else:
                    gene = b2.pop(0)
                    child.append(gene)
                    b1.remove(gene)
                    
                
            offspring.append(child)
            # print(offspring)
    else:
        offspring.append(parent1)
        offspring.append(parent2)
        # print(offspring)
    #突變機制
    print(offspring)
    return offspring

def mutation_swap(chromosome, n, mutation_rate, Or):
    """
    兩點交換變異 (Two-point Swap Mutation)
    隨機交換兩個基因位置，並進行修復以滿足優先順序限制。
    """
    # 確保 chromosome 是 numpy array，因為 LBrr1 需要
    if not isinstance(chromosome, np.ndarray):
        chromosome = np.array(chromosome)
        
    if random.random() <= mutation_rate:
        # 隨機選取兩個不同的索引
        idx1, idx2 = random.sample(range(n), 2)
        
        # 交換
        chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]
        
        # 修復 (Repair) 以滿足限制
        # LBrr1 會原地修改並回傳
        chromosome = LBrr1(Or, n, chromosome)
        
    return chromosome
