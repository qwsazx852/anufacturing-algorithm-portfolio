import numpy as np
import random
import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solvers import ga_utils

#參數設置(input)
n=8#零件數
p=100#族群數
PP=100#迭代數
crossover=0.8#交配率
mutation=0.1#突變率
order=[]
# order = np.array([
#   [3 ,2],
#   [3 ,1],
#   [4 ,5],
#   [4 ,8],
#   [5 ,7],
#   [5 ,6],
#   [6 ,9],
#   [7 ,9],
#   [8 ,6],
#   [10 ,12],
#   [11 ,12],
#   [13 ,12],
#   [14 ,1],
#   [14 ,4],
#   [15 ,12],
#   [16 ,15],
#   [17 ,15],
#   [18 ,10],
#   [18 ,11],
#   [18 ,13]
#   ])#優先順序限制ex：3在2之前
order = np.array([
  [1 ,2],
  [2 ,3],
  [2 ,4],
  [3 ,5],
  [3 ,6],
  [4 ,6],
  [5 ,7],
  [6 ,8]
  ])#優先順序限制ex：3在2之前
time_imformation=[11,17,9,5,8,12,10,3]
print(time_imformation)
GCT=20#週期時間（Cycle time)
  #................................................
  #初始族群產生
ip=np.zeros((p,n), dtype=int)

for _ in range (p):
  p1=random.sample(range(1,n+1),n)
  ip[_]=p1

Or = ga_utils.LBbn(order, n)

#初始族群
ip_anser=[]

RR=[]
for i in range(len(ip)):
    RR=ip[i,:]
    RR=ga_utils.LBrr1(Or,n,RR)
    ip[i]=RR
print(ip)
#適應值計算
#選擇
#交配機制

# 最佳解追蹤
global_best_stations = float('inf')
global_best_chromosome = None

for generation in range(PP):
    #交配機制
    for i in range (0,p,2):
        # print(i)
        parent1 = ip[i].tolist()
        parent2 = ip[i+1].tolist()
        offspring = ga_utils.ppx(n,crossover,parent1,parent2)
        ip[i] = offspring[0]
        ip[i+1] = offspring[1]

    #突變機制
    for i in range(p):
        ip[i] = ga_utils.mutation_swap(ip[i], n, mutation, Or)
        
    # print(f"Generation {generation+1} Population (sample):")
    # print(ip[:5])

    #適應值計算
    station_counts = []
    
    current_best_stations = float('inf')
    current_best_idx = -1

    for i in range(p):
        current_sum=0
        add=1
        for j in ip[i]:
            current_sum+=time_imformation[j-1]
            if current_sum>GCT:
              current_sum=time_imformation[j-1]
              add+=1
        station_counts.append(add)
        
        # 更新當代最佳
        if add < current_best_stations:
            current_best_stations = add
            current_best_idx = i
            
    # 更新全域最佳
    if current_best_stations < global_best_stations:
        global_best_stations = current_best_stations
        global_best_chromosome = ip[current_best_idx].copy()
        print(f"Generation {generation+1}: New Best Stations = {global_best_stations}")

    #適應值計算 (望小: 越小越好 -> 1/stations)
    fitness_values = [1.0 / count for count in station_counts]
    total_fitness = sum(fitness_values)
    probs = [f / total_fitness for f in fitness_values]

    #選擇 (輪盤法)
    indices = np.random.choice(range(p), size=p, p=probs)
    ip = ip[indices].copy() # 更新族群

print("-" * 30)
print(f"Optimization Completed over {PP} generations.")
print(f"Global Best Stations: {global_best_stations}")
print(f"Global Best Chromosome: \n{global_best_chromosome}")


    



#選擇
