import numpy as np
import time
import csv
import os

def first_return_time(seed, max_time=60):
    np.random.seed(seed)
    
    x, y = 0, 0
    start_time = time.time()
    steps = 0

    while True:
        if time.time() - start_time > max_time:
            return None

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
            return steps

# ============================
# INPUT: how many new seeds
# ============================
n_new_seeds = 10
filename = "results.csv"

# ============================
# Find last seed (if file exists)
# ============================
last_seed = 0

if os.path.exists(filename):
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        seeds = [int(row["seed"]) for row in reader]
        if seeds:
            last_seed = max(seeds)

# ============================
# Generate new seeds
# ============================
new_seeds = range(last_seed + 1, last_seed + 1 + n_new_seeds)

# ============================
# Append results
# ============================
file_exists = os.path.exists(filename)

with open(filename, "a", newline="") as f:
    writer = csv.writer(f)

    # Write header only if file is new
    if not file_exists:
        writer.writerow(["seed", "steps", "returned"])

    for s in new_seeds:
        steps = first_return_time(s, max_time=60)
        returned = steps is not None

        writer.writerow([s, steps if steps is not None else -1, returned])

        print(f"seed={s} - steps={steps}")