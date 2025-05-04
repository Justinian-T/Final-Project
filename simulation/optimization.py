import numpy as np
from scipy.optimize import minimize_scalar

def find_optimal_params(gravity, body_size):
    def objective_function(k):
        b = k / 100  # Example relationship between stiffness and damping
        # Simulate and calculate max height (replace with actual simulation logic)
        _, xy, _ = run_sim(k, b, gravity, body_size, render=False)
        max_height = xy[:, 2, 2].max()
        return -max_height  # Minimize negative height to maximize height

    result = minimize_scalar(objective_function, bounds=(0.05, 3), method="bounded")
    optimal_k = result.x
    optimal_b = optimal_k / 100
    max_height = -result.fun

    return optimal_k, optimal_b, max_height