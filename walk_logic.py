# walk_logic.py
import numpy as np
from numba import njit

@njit
def first_return_time_numba(seed, max_steps):
    """Core 2D Random Walk logic compiled with Numba."""
    np.random.seed(seed)
    x, y = 0, 0
    for steps in range(1, max_steps + 1):
        direction = np.random.randint(4)
        if direction == 0: x += 1
        elif direction == 1: x -= 1
        elif direction == 2: y += 1
        else: y -= 1
        
        if x == 0 and y == 0:
            return steps
    return -1

def worker(args):
    seed, max_steps = args
    steps = first_return_time_numba(seed, max_steps)
    return (seed, steps if steps != -1 else None)
