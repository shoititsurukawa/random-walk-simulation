# plot_histogram.py

import csv
import numpy as np
import matplotlib.pyplot as plt

filename = "results.csv"
steps = []

# Read CSV
with open(filename, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        value = int(row["steps"])
        if value != -1:  # ignore timeouts
            steps.append(value)

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
