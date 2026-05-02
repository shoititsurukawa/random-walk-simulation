import numpy as np
from numba import njit
import csv
import os
from multiprocessing import Pool, cpu_count
import time

# ============================
# NUMBA CORE
# ============================
@njit
def first_return_time_numba(seed, max_steps):
    np.random.seed(seed)
    
    x = 0
    y = 0

    for steps in range(1, max_steps + 1):
        direction = np.random.randint(4)

        if direction == 0:
            x += 1
        elif direction == 1:
            x -= 1
        elif direction == 2:
            y += 1
        else:
            y -= 1

        if x == 0 and y == 0:
            return steps

    return -1  # timeout

# ============================
# WORKER (multiprocessing)
# ============================
def worker(args):
    seed, max_steps = args
    steps = first_return_time_numba(seed, max_steps)

    if steps == -1:
        return (seed, None)
    return (seed, steps)

# ============================
# MAIN
# ============================
if __name__ == "__main__":

    start_total = time.perf_counter()

    n_new_seeds = 100
    max_steps = 10_000_000
    filename = "results.csv"

    # ============================
    # Find last seed
    # ============================
    last_seed = 0

    if os.path.exists(filename):
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            seeds = [int(row["seed"]) for row in reader]
            if seeds:
                last_seed = max(seeds)

    new_seeds = list(range(last_seed + 1, last_seed + 1 + n_new_seeds))

    # ============================
    # PRE-COMPILE NUMBA (VERY IMPORTANT)
    # ============================
    print("Compiling Numba function...")
    first_return_time_numba(1, 10)  # warm-up

    # ============================
    # PARALLEL EXECUTION
    # ============================
    n_workers = cpu_count()
    print(f"Using {n_workers} workers")

    with Pool(n_workers) as pool:
        args = [(s, max_steps) for s in new_seeds]
        results = pool.map(worker, args, chunksize=10)

    # ============================
    # SAVE RESULTS
    # ============================
    file_exists = os.path.exists(filename)

    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["seed", "steps", "returned"])

        for seed, steps in results:
            returned = steps is not None
            writer.writerow([seed, steps if steps is not None else -1, returned])
            print(f"seed={seed} - steps={steps}")

    end_total = time.perf_counter()
    print(f"\nTotal execution time: {end_total - start_total:.2f} seconds")