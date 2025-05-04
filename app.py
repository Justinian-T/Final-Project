import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from simulation.simulation import run_sim
from simulation.optimization import find_optimal_params
import pandas as pd
import matplotlib.pyplot as plt
import mediapy as media
import mujoco

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")  # Main page with sliders

@app.route("/run_simulation", methods=["POST"])
def run_simulation():
    # Get slider values from the request
    data = request.json
    k = float(data["stiffness"])*10**-2  # Convert to float
    b = float(data["damping"])*10**-2/100    # Convert to float
    g = float(data["gravity"])    # Convert to float
    body_size = float(data["body_size"])  # Convert to float

    # Run the simulation
    t, xy, frames = run_sim(k, b, g, body_size, render=True)

    # Save results to CSV
    with open("simulation_params.csv", "w") as f:
        f.write("Stiffness,Damping,Gravity,Body Size\n")
        f.write(f"{k},{b},{g},{body_size}\n")

    # Generate and save the plot
    plot_path = os.path.join("static", "simulation_plot.png")
    plt.figure(figsize=(8, 6))
    plt.plot(t, [pos[2] for pos in xy], label="Height vs Time", color="purple")
    plt.title("Simulation Results")
    plt.xlabel("Time (s)")
    plt.ylabel("Height (m)")
    plt.legend()
    plt.grid()
    plt.savefig(plot_path)
    plt.close()

    # Save the video
    video_path = os.path.join("static", "simulation_video.mp4")
    media.write_video(video_path, frames, fps=30)

    return jsonify({
        "message": "Simulation completed!",
        "plot_path": plot_path,
        "video_path": video_path
    })

@app.route("/find_optimal", methods=["GET"])
def find_optimal():
    # Read the CSV file to get gravity and body size
    df = pd.read_csv("simulation_params.csv")
    g = df["Gravity"].iloc[0]
    body_size = df["Body Size"].iloc[0]
    damp = df["Damping"].iloc[0]

    # Find optimal parameters and collect data for the plot
    optimal_k, max_height, k_values, heights, optimal_t, optimal_xy, optimal_frames = find_optimal_params(g, body_size, damp)

    # Ensure the static directory exists
    static_dir = os.path.join(os.getcwd(), "static")
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    # Generate and save the k vs. height plot
    comparison_plot_path = os.path.join(static_dir, "k_vs_height_plot.png")
    plt.figure(figsize=(8, 6))
    plt.plot(k_values, heights, marker="o", label="Max Height vs Stiffness (k)")
    plt.axvline(optimal_k, color="red", linestyle="--", label=f"Optimal k = {optimal_k:.2f}")
    plt.title("Max Height vs Stiffness (k)")
    plt.xlabel("Stiffness (k)")
    plt.ylabel("Max Height (m)")
    plt.ylim(0, max_height * 1.1)  # Adjust y-axis limit
    plt.legend()
    plt.grid()
    plt.savefig(comparison_plot_path)
    plt.close()

    # Generate the optimal simulation video
    video_path = os.path.join("static", "optimal_simulation_video.mp4")
    media.write_video(video_path, optimal_frames, fps=30)

    # Generate the optimal vs. user-defined jump plot
    user_t, user_xy, _ = run_sim(df["Stiffness"].iloc[0], damp, g, body_size, render=False)

    comparison_jump_plot_path = os.path.join(static_dir, "optimal_vs_user_jump_plot.png")
    plt.figure(figsize=(8, 6))
    plt.plot(user_t, user_xy[:, 2], label="User-Defined Jump", color="purple")
    plt.plot(optimal_t, optimal_xy[:, 2], label="Optimal Jump", color="gold")
    plt.title("Optimal vs User-Defined Jump")
    plt.xlabel("Time (s)")
    plt.ylabel("Height (m)")
    plt.legend()
    plt.grid()
    plt.savefig(comparison_jump_plot_path)
    plt.close()

    return jsonify({
        "message": "Optimization completed!",
        "optimal_stiffness": optimal_k,
        "max_height": max_height,
        "comparison_plot_path": "/static/k_vs_height_plot.png",
        "video_path": "/static/optimal_simulation_video.mp4",
        "comparison_jump_plot_path": "/static/optimal_vs_user_jump_plot.png"
    })

@app.route("/reset_simulation", methods=["POST"])
def reset_simulation():
    # Paths to files to delete
    files_to_delete = [
        os.path.join("static", "simulation_plot.png"),
        os.path.join("static", "simulation_video.mp4"),
        os.path.join("static", "k_vs_height_plot.png"),
        os.path.join("static", "optimal_simulation_plot.png"),
        os.path.join("static", "optimal_simulation_video.mp4"),
        "simulation_params.csv"
    ]

    # Delete the files if they exist
    for file_path in files_to_delete:
        if os.path.exists(file_path):
            os.remove(file_path)

    return jsonify({"message": "Simulation and optimization reset successfully!"})

if __name__ == "__main__":
    app.run(debug=True)