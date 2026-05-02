import numpy as np
import time
import csv

def first_return_time(seed, max_time=60):
    np.random.seed(seed)
    
    position = np.array([0, 0])
    start_time = time.time()
    steps = 0

    while True:
        # Timeout check
        if time.time() - start_time > max_time:
            return None  # did not return in time

        # Random direction (grid walk)
        direction = np.random.choice([0, 1, 2, 3])
        
        if direction == 0:
            step = np.array([1, 0])
        elif direction == 1:
            step = np.array([-1, 0])
        elif direction == 2:
            step = np.array([0, 1])
        else:
            step = np.array([0, -1])

        position += step
        steps += 1

        # Check return to origin
        if np.array_equal(position, [0, 0]):
            return steps

# Run simulations
seeds = range(1, 6)

with open("results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    
    # Header
    writer.writerow(["seed", "steps", "returned"])
    
    for s in seeds:
        steps = first_return_time(s, max_time=60)
        returned = steps is not None
        
        # Save (-1 for timeout, optional choice)
        writer.writerow([s, steps if steps is not None else -1, returned])
        
        print(f"seed={s} - steps={steps}")