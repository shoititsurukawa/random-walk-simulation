# plot_histogram.py

import csv
import numpy as np
import matplotlib.pyplot as plt

filename = "results.csv"
steps = []

# Variables to track the maximum step and its corresponding seed
max_seed = None
max_step = -1

# Read CSV
with open(filename, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        value = int(row["steps"])
        seed = int(row["seed"])
        
        # ignore timeouts
        if value != -1:
            steps.append(value)
            
            # Check if this walk has the highest step count so far
            if value > max_step:
                max_step = value
                max_seed = seed

print(f"The seed with the max steps is {max_seed} with {max_step} steps.")

# Plot Histogram
plt.figure(figsize=(8, 6))
plt.hist(steps, bins=np.logspace(np.log10(min(steps)), np.log10(max(steps)), 50))
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Steps (log scale)")
plt.ylabel("Frequency (log scale)")
plt.title("Log-Log Histogram of Return Times")
plt.grid(True)
plt.show()
