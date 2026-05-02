import numpy as np
from numba import njit
import csv

# ============================
# NUMBA FUNCTION
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

    return -1

# ============================
# INPUT
# ============================
seed_to_rerun = 17
max_steps = 500_000_000_000  # increase this
filename = "results.csv"

# ============================
# PRECOMPILE NUMBA
# ============================
print("Compiling Numba...")
first_return_time_numba(1, 10)

# ============================
# RE-RUN SEED
# ============================
print(f"Re-running seed {seed_to_rerun}...")
steps = first_return_time_numba(seed_to_rerun, max_steps)

returned = steps != -1
steps_out = steps if returned else -1

print(f"Result: steps={steps_out}, returned={returned}")

# ============================
# LOAD CSV
# ============================
rows = []

with open(filename, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

# ============================
# UPDATE TARGET SEED
# ============================
updated = False

for row in rows:
    if int(row["seed"]) == seed_to_rerun:
        row["steps"] = str(steps_out)
        row["returned"] = str(returned)
        updated = True
        break

if not updated:
    print("Seed not found in file. Adding it.")
    rows.append({
        "seed": str(seed_to_rerun),
        "steps": str(steps_out),
        "returned": str(returned)
    })

# ============================
# SAVE BACK TO CSV
# ============================
with open(filename, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["seed", "steps", "returned"])
    writer.writeheader()
    writer.writerows(rows)

print("CSV updated successfully.")