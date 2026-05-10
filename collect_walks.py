# collect_walks.py
import csv
import os
import time
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
from walk_logic import first_return_time_numba, worker

def get_last_seed(filename):
    if not os.path.exists(filename):
        return 0
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        seeds = [int(row["seed"]) for row in reader]
        return max(seeds) if seeds else 0

if __name__ == "__main__":
    start_time = time.perf_counter()
    
    # Configuration
    N_NEW_SEEDS = 10_000 
    MAX_STEPS = 10**8
    FILENAME = "results.csv"
    
    # Prepare Seeds
    last_seed = get_last_seed(FILENAME)
    new_seeds = list(range(last_seed + 1, last_seed + 1 + N_NEW_SEEDS))
    
    # Warm up Numba
    print("Compiling Numba core...")
    first_return_time_numba(1, 10)
    
    # Parallel Execution
    print(f"Starting simulation with {cpu_count()} workers...")
    results = []
    args = [(s, MAX_STEPS) for s in new_seeds]
    
    with Pool(cpu_count()) as pool:
        for result in tqdm(pool.imap_unordered(worker, args), total=len(args), desc="Progress"):
            results.append(result)
            
    # Sort and Save
    results.sort(key=lambda x: x[0])
    
    file_exists = os.path.exists(FILENAME)
    with open(FILENAME, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["seed", "steps", "returned"])
        
        for seed, steps in results:
            writer.writerow([seed, steps if steps is not None else -1, steps is not None])

    print(f"\nTotal time: {time.perf_counter() - start_time:.2f}s")
    