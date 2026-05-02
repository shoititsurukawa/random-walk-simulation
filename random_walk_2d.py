import numpy as np
import matplotlib.pyplot as plt
import time

# Parameters
seed = 1
max_time = 60  # seconds

np.random.seed(seed)

# Initialize
position = np.array([0, 0])
positions = [position.copy()]

start_time = time.time()
steps_count = 0

while True:
    # Check timeout
    if time.time() - start_time > max_time:
        print("Timeout reached (1 min). Did not return to origin.")
        break

    # Take one step (grid walk)
    direction = np.random.choice([0, 1, 2, 3])
    
    if direction == 0:
        step = np.array([1, 0])
    elif direction == 1:
        step = np.array([-1, 0])
    elif direction == 2:
        step = np.array([0, 1])
    else:
        step = np.array([0, -1])

    # Update position
    position = position + step
    positions.append(position.copy())
    steps_count += 1

    # Check return to origin (ignore step 0)
    if np.array_equal(position, [0, 0]):
        print(f"Returned to origin after {steps_count} steps")
        break

# Convert to array for plotting
positions = np.array(positions)

# Plot
plt.figure(figsize=(8, 8))
plt.plot(positions[:, 0], positions[:, 1], linewidth=1)

# Start
plt.scatter(0, 0, marker='o', s=150)

# End
plt.scatter(positions[-1, 0], positions[-1, 1], marker='x', s=150)

plt.title(f'2D Random Walk (seed = {seed})')
plt.xlabel('X')
plt.ylabel('Y')
plt.axis('equal')
plt.grid(True)

plt.show()