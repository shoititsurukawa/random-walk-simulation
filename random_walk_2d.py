import numpy as np
import matplotlib.pyplot as plt

# Parameters
seed = 1
n_steps = 100

# Set seed for reproducibility
np.random.seed(seed)

# Generate random steps
steps = np.zeros((n_steps, 2))
directions = np.random.choice([0, 1, 2, 3], size=n_steps)

steps[directions == 0] = [1, 0]   # right
steps[directions == 1] = [-1, 0]  # left
steps[directions == 2] = [0, 1]   # up
steps[directions == 3] = [0, -1]  # down
#steps = np.random.randn(n_steps, 2)

# Compute cumulative sum to get positions
positions = np.cumsum(steps, axis=0)

# Add origin (0,0) at the start
positions = np.vstack(([0, 0], positions))

# Plot
plt.figure(figsize=(8, 8))
plt.plot(positions[:, 0], positions[:, 1], linewidth=1)
plt.scatter(0, 0, marker='o')  # starting point
plt.scatter(positions[-1, 0], positions[-1, 1], marker='x')  # ending point

plt.title('2D Random Walk (seed = 1)')
plt.xlabel('X')
plt.ylabel('Y')
plt.axis('equal')

plt.show()