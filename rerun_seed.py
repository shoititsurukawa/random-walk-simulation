# rerun_seed.py

import csv
import os
import time
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
from walk_logic import first_return_time_numba, worker

if __name__ == "__main__":
    start_time = time.perf_counter()
    
    # Configuration
    N_RERUN_SEEDS = 1000
    MAX_STEPS = 10**8
    FILENAME = "results.csv"

    # Prepare Seeds
    all_rows = []
    seeds_to_rerun = []

    if not os.path.exists(FILENAME):
        print(f"Error: {FILENAME} not found.")
        exit()

    with open(FILENAME, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # We identify failed seeds where returned is 'False' or steps is -1
            if row["returned"] == "False" and len(seeds_to_rerun) < N_RERUN_SEEDS:
                seeds_to_rerun.append(int(row["seed"]))
            all_rows.append(row)

    if not seeds_to_rerun:
        print("No seeds with 'returned=False' found to rerun. Exiting.")
        exit()

    print(f"Found {len(seeds_to_rerun)} seeds to refine: {seeds_to_rerun}")

    # Warm up Numba
    print("Compiling Numba...")
    first_return_time_numba(1, 10)

    # Parallel Execution
    n_workers = cpu_count()
    print(f"Refining using {n_workers} workers...")
    
    args = [(s, MAX_STEPS) for s in seeds_to_rerun]
    refined_results = {} # Use a dict for easy lookup: {seed: steps}

    with Pool(n_workers) as pool:
        for seed, steps in tqdm(pool.imap_unordered(worker, args), total=len(args), desc="Refining"):
            refined_results[seed] = steps

    # Save
    # We update the 'all_rows' list with the new data
    for row in all_rows:
        s_id = int(row["seed"])
        if s_id in refined_results:
            new_steps = refined_results[s_id]
            if new_steps is not None:
                row["steps"] = str(new_steps)
                row["returned"] = "True"
                print(f"Seed {s_id} FIXED: {new_steps} steps.")
            else:
                print(f"Seed {s_id} TIMEOUT again at {MAX_STEPS} steps.")

    # Save back to CSV (Overwriting with updated rows)
    with open(FILENAME, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["seed", "steps", "returned"])
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\nTotal time: {time.perf_counter() - start_time:.2f}s")
    