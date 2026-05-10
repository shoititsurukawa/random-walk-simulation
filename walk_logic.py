# walk_logic.py
import numpy as np
from numba import njit

@njit
def first_return_time_numba(seed, max_steps):
    """Core 2D Random Walk logic compiled with Numba."""
    np.random.seed(seed)
    x, y = 0, 0
    steps = 0
    
    while steps < max_steps:
        # Generate one 32-bit integer for 16 steps
        random_batch = np.random.randint(0, 4294967295) # 2^32 - 1
        
        for _ in range(16):
            steps += 1
            if steps > max_steps:
                return -1
            
            # Extract the last 2 bits (values 0, 1, 2 or 3)
            direction = random_batch & 3
            
            # Shift the bits right by 2 to prep for the next step
            random_batch = random_batch >> 2
            
            if direction == 0: x += 1
            elif direction == 1: x -= 1
            elif direction == 2: y += 1
            else: y -= 1
        
            # Only check on even steps
            if steps % 2 == 0 and x == 0 and y == 0:
                return steps
            
    return -1

def worker(args):
    seed, max_steps = args
    steps = first_return_time_numba(seed, max_steps)
    return (seed, steps if steps != -1 else None)
