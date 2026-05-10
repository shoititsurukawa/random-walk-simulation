# README.md

## Description
This project is a computational study of random walks on a 2D lattice. The primary goal is to simulate and visualize the distribution of the first return time to the origin.

## 1. Initial Collection (`collect_walks.py`)
This script performs the initial broad sampling. It identifies the "easy" returns and marks "lost" walkers as timeouts. It will take ~150 seconds using the following parameters:  
`n_new_seeds` = 10_000  
`max_steps` = 10**8 

## 2. Targeted Refinement (`rerun_seed.py`)
This script automatically scans the results for seeds that hit the initial timeout (`returned=False`) and re-simulates them with a significantly higher `max_steps`. `N_RERUN_SEEDS` is fixed at 16 for all measurements.

| MAX_STEPS | Approx. Runtime |
| --------- | --------------- |
| 10**9     | ~15 seconds     |
| 10**10    | ~135 seconds    |
| 10**11    | ~1400 seconds   |
| 10**12    | ~14700 seconds  |

## Conclusion
???
