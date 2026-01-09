from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.utils import data_adapter
from solvers.ga_solver import GeneticOptimizer
from solvers.pso_solver import PSOSolver
from solvers.aco_solver import ACOSolver
from solvers.sa_solver import SASolver
import os
import shutil
import time

# Create Router
router = APIRouter()

# 定義請求的資料模型
class OptimizationParams(BaseModel):
    # Common
    pop_size: int = 100
    generations: int = 50
    cycle_time: int = 20
    
    # GA Specific
    crossover_rate: float = 0.8
    mutation_rate: float = 0.1
    
    # PSO Specific
    w: float = 0.7
    c1: float = 2.0
    c2: float = 2.0
    
    # ACO Specific
    alpha: float = 1.0
    beta: float = 2.0
    rho: float = 0.1
    
    # SA Specific
    initial_temp: float = 1000.0
    cooling_rate: float = 0.99

# Helper to load config
def get_config_path():
    # current file is in app/routers/
    # config is in data/ (up 2 levels)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_dir = os.path.join(base_dir, 'data')
    
    custom_path = os.path.join(data_dir, 'custom_config.xlsx')
    default_path = os.path.join(data_dir, 'config.xlsx')
    
    if os.path.exists(custom_path):
        return custom_path, "custom"
    return default_path, "default"

def get_config():
    path, _ = get_config_path()
    if not os.path.exists(path):
        return None
    loader = data_adapter.ConfigLoader(path)
    return loader.load_config()

# ==========================================
# Config Management Endpoints
# ==========================================
@router.get("/config/status")
def get_config_status():
    _, source = get_config_path()
    return {"source": source}

@router.get("/config/download")
def download_config():
    path, _ = get_config_path()
    filename = "config_template.xlsx" if "config.xlsx" in path else "current_config.xlsx"
    return FileResponse(path, filename=filename)

@router.post("/config/upload")
async def upload_config(file: UploadFile = File(...)):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    custom_path = os.path.join(base_dir, 'custom_config.xlsx')
    
    with open(custom_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"status": "success", "message": "Custom config uploaded"}

@router.post("/config/reset")
def reset_config():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    custom_path = os.path.join(base_dir, 'custom_config.xlsx')
    
    if os.path.exists(custom_path):
        os.remove(custom_path)
        return {"status": "success", "message": "Reset to default config"}
    return {"status": "ignored", "message": "Already using default"}

@router.get("/")
def read_root():
    """
    回傳 HTML Dashboard 介面
    """
    # 當被掛載到 /scheduler 時，此路徑為 /scheduler/
    # 我們回傳 static/index.html
    # 注意：static folder 必須在 main app 掛載
    return FileResponse('static/index.html')

# ==========================================
# 1. Genetic Algorithm (GA)
# ==========================================
@router.post("/optimize/ga")
def run_ga(params: OptimizationParams):
    config = get_config()
    if not config: return {"error": "Missing config.xlsx"}
    
    start_time = time.time()
    optimizer = GeneticOptimizer(
        num_jobs=int(config['NUM_JOBS']),
        pop_size=params.pop_size,
        crossover_rate=params.crossover_rate,
        mutation_rate=params.mutation_rate,
        constraints=config['CONSTRAINTS'],
        time_info=config['TIME_INFO'],
        cycle_time=params.cycle_time
    )
    optimizer.initialize_population()
    
    best_stations = float('inf')
    best_chrom = []
    history = []
    
    for _ in range(params.generations):
        chrom, stations = optimizer.evolve()
        if stations < best_stations:
            best_stations = stations
            best_chrom = chrom[:]
        history.append(int(best_stations)) # Log history
            
    return {
        "algorithm": "GA",
        # Convert list of numpy.int64 to list of python int 
        "result": {
            "stations": int(best_stations), 
            "sequence": [int(x) for x in best_chrom],
            "history": history
        },
        "time": round(time.time() - start_time, 4)
    }

# ==========================================
# 2. Particle Swarm Optimization (PSO)
# ==========================================
@router.post("/optimize/pso")
def run_pso(params: OptimizationParams):
    config = get_config()
    if not config: return {"error": "Missing config.xlsx"}
    
    start_time = time.time()
    pso = PSOSolver(
        num_jobs=int(config['NUM_JOBS']),
        pop_size=params.pop_size,
        constraints=config['CONSTRAINTS'],
        time_info=config['TIME_INFO'],
        cycle_time=params.cycle_time,
        w=params.w,
        c1=params.c1,
        c2=params.c2
    )
    
    history = []
    for _ in range(params.generations):
        pso.evolve()
        history.append(int(pso.gbest_score))
        
    return {
        "algorithm": "PSO",
        # Explicit conversion to native python int/list
        # PSOSolver uses 'gbest_score' and 'gbest_permutation'
        "result": {
            "stations": int(pso.gbest_score), 
            "sequence": [int(x) for x in pso.gbest_permutation],
            "history": history
        }, 
        "time": round(time.time() - start_time, 4)
    }

# ==========================================
# 3. Ant Colony Optimization (ACO)
# ==========================================
@router.post("/optimize/aco")
def run_aco(params: OptimizationParams):
    config = get_config()
    if not config: return {"error": "Missing config.xlsx"}
    
    start_time = time.time()
    aco = ACOSolver(
        num_jobs=int(config['NUM_JOBS']),
        num_ants=params.pop_size, 
        constraints=config['CONSTRAINTS'],
        time_info=config['TIME_INFO'],
        cycle_time=params.cycle_time,
        alpha=params.alpha,
        beta=params.beta,
        rho=params.rho
    )
    
    history = []
    for _ in range(params.generations):
        aco.evolve()
        history.append(int(aco.gbest_fitness))
        
    # Cast numpy.int64 to native python int during comprehension
    best_seq_1based = [int(x) + 1 for x in aco.gbest_sequence]
    
    return {
        "algorithm": "ACO",
        # Explicit convert fitness to int
        "result": {
            "stations": int(aco.gbest_fitness), 
            "sequence": best_seq_1based,
            "history": history
        },
        "time": round(time.time() - start_time, 4)
    }

# ==========================================
# 4. Simulated Annealing (SA)
# ==========================================
@router.post("/optimize/sa")
def run_sa(params: OptimizationParams):
    config = get_config()
    if not config: return {"error": "Missing config.xlsx"}
    
    start_time = time.time()
    sa = SASolver(
        num_jobs=int(config['NUM_JOBS']),
        constraints=config['CONSTRAINTS'],
        time_info=config['TIME_INFO'],
        cycle_time=params.cycle_time,
        initial_temp=params.initial_temp,
        cooling_rate=params.cooling_rate
    )
    
    iter_count = 0
    history = []
    # SA history might be long, let's downsample if needed or just return all?
    # For now, return all (SA is fast), but chart might get crowded.
    # Actually SA runs until stopping temp.
    while sa.temp > sa.stopping_temp:
        sa.step()
        iter_count += 1
        history.append(int(sa.best_fitness))
        
    return {
        "algorithm": "SA",
        "iterations": iter_count,
        # Ensure native types
        "result": {
            "stations": int(sa.best_fitness), 
            "sequence": [int(x) for x in sa.best_solution],
            "history": history
        },
        "time": round(time.time() - start_time, 4)
    }

# ==========================================
# 5. Compare All Algorithms
# ==========================================
@router.post("/optimize/compare")
def run_compare(params: OptimizationParams):
    config = get_config()
    if not config: return {"error": "Missing config.xlsx"}
    
    results = []
    
    # 1. Run GA
    ga_start = time.time()
    ga = GeneticOptimizer(
        num_jobs=int(config['NUM_JOBS']),
        pop_size=params.pop_size,
        crossover_rate=params.crossover_rate,
        mutation_rate=params.mutation_rate,
        constraints=config['CONSTRAINTS'],
        time_info=config['TIME_INFO'],
        cycle_time=params.cycle_time
    )
    ga.initialize_population()
    best_stations_ga = float('inf')
    history_ga = []
    for _ in range(params.generations):
        _, stations = ga.evolve()
        if stations < best_stations_ga: best_stations_ga = stations
        history_ga.append(int(best_stations_ga))
    results.append({
        "algorithm": "GA",
        "stations": int(best_stations_ga),
        "history": history_ga,
        "time": round(time.time() - ga_start, 4)
    })

    # 2. Run PSO
    pso_start = time.time()
    pso = PSOSolver(
        num_jobs=int(config['NUM_JOBS']),
        pop_size=params.pop_size,
        constraints=config['CONSTRAINTS'],
        time_info=config['TIME_INFO'],
        cycle_time=params.cycle_time,
        w=params.w,
        c1=params.c1,
        c2=params.c2
    )
    history_pso = []
    for _ in range(params.generations):
        pso.evolve()
        history_pso.append(int(pso.gbest_score))
    results.append({
        "algorithm": "PSO",
        "stations": int(pso.gbest_score),
        "history": history_pso,
        "time": round(time.time() - pso_start, 4)
    })

    # 3. Run ACO
    aco_start = time.time()
    aco = ACOSolver(
        num_jobs=int(config['NUM_JOBS']),
        num_ants=params.pop_size, 
        constraints=config['CONSTRAINTS'],
        time_info=config['TIME_INFO'],
        cycle_time=params.cycle_time,
        alpha=params.alpha,
        beta=params.beta,
        rho=params.rho
    )
    history_aco = []
    for _ in range(params.generations):
        aco.evolve()
        history_aco.append(int(aco.gbest_fitness))
    results.append({
        "algorithm": "ACO",
        "stations": int(aco.gbest_fitness),
        "history": history_aco,
        "time": round(time.time() - aco_start, 4)
    })

    # 4. Run SA
    sa_start = time.time()
    sa = SASolver(
        num_jobs=int(config['NUM_JOBS']),
        constraints=config['CONSTRAINTS'],
        time_info=config['TIME_INFO'],
        cycle_time=params.cycle_time,
        initial_temp=params.initial_temp,
        cooling_rate=params.cooling_rate
    )
    history_sa = []
    while sa.temp > sa.stopping_temp:
        sa.step()
        history_sa.append(int(sa.best_fitness))
    # Normalize SA history length to generations for comparison chart?? 
    # Or just return as is (chart.js handles different lengths ok)
    results.append({
        "algorithm": "SA",
        "stations": int(sa.best_fitness),
        "history": history_sa,
        "time": round(time.time() - sa_start, 4)
    })

    return {
        "algorithm": "ALL",
        "result": results
    }
