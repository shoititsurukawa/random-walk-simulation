import numpy as np
import time
import csv
import os
from multiprocessing import Pool, cpu_count

def first_return_time(seed, max_time=180):
    np.random.seed(seed)
    
    x, y = 0, 0
    start_time = time.time()
    steps = 0

    while True:
        if time.time() - start_time > max_time:
            return (seed, None)

        direction = np.random.randint(4)

        if direction == 0:
            x += 1
        elif direction == 1:
            x -= 1
        elif direction == 2:
            y += 1
        else:
            y -= 1

        steps += 1

        if x == 0 and y == 0:
            return (seed, steps)

start_total = time.perf_counter()
# ============================
# INPUT
# ============================
n_new_seeds = 100
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

# Generate seeds
new_seeds = list(range(last_seed + 1, last_seed + 1 + n_new_seeds))

# ============================
# PARALLEL EXECUTION
# ============================
if __name__ == "__main__":
    n_workers = cpu_count()  # use all cores

    with Pool(n_workers) as pool:
        results = pool.map(first_return_time, new_seeds)

    # ============================
    # WRITE RESULTS
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

print(f"\nTotal execution time: {end_total - start_total:.4f} seconds")