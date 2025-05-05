import numpy
from simulation.simulation import run_sim

def find_optimal_params(gravity, leg_size, stiffness):
    b_values = numpy.r_[0.05:3:.05] * 10**-3 / 100  # Range of damping values
    max_height = -float("inf")
    optimal_b = None
    heights = []
    optimal_t = None
    optimal_xy = None
    optimal_frames = None

    for b in b_values:
        t, xy, frames = run_sim(stiffness, b, gravity, leg_size, render=True)
        current_max_height = xy[:, 2].max()  # Get the maximum height

        # Track the maximum height
        heights.append(current_max_height)
        if current_max_height > max_height:
            max_height = current_max_height
            optimal_b = b
            optimal_t = t
            optimal_xy = xy
            optimal_frames = frames

    return optimal_b, max_height, b_values, heights, optimal_t, optimal_xy, optimal_frames