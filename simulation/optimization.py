import numpy
from simulation.simulation import run_sim

def find_optimal_params(gravity, body_size, damp):
    k_values = numpy.r_[0.05:3:.05] * 10**-2  # Range of stiffness values
    max_height = -float("inf")
    optimal_k = None
    optimal_b = damp
    heights = []
    optimal_t = None
    optimal_xy = None
    optimal_frames = None

    for k in k_values:
        t, xy, frames = run_sim(k, damp, gravity, body_size, render=True)
        current_max_height = xy[:, 2].max()  # Get the maximum height

        # Track the maximum height
        heights.append(current_max_height)
        if current_max_height > max_height:
            max_height = current_max_height
            optimal_k = k
            optimal_t = t
            optimal_xy = xy
            optimal_frames = frames

    return optimal_k, max_height, k_values, heights, optimal_t, optimal_xy, optimal_frames