import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from simulation.simulation import run_sim
from simulation.optimization import find_optimal_params
import pandas as pd
import matplotlib.pyplot as plt
import mediapy as media

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")  # Main page with sliders

@app.route("/run_simulation", methods=["POST"])
def run_simulation():
    # Get slider values from the request
    data = request.json
    k = float(data["stiffness"])  # Convert to float
    b = float(data["damping"])    # Convert to float
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
    plt.plot(t, [pos[2] for pos in xy], label="Height vs Time")
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
    # Read the CSV file
    df = pd.read_csv("simulation_params.csv")
    g = df["Gravity"].iloc[0]
    body_size = df["Body Size"].iloc[0]

    # Find optimal parameters
    optimal_k, optimal_b, max_height = find_optimal_params(g, body_size)

    return jsonify({
        "optimal_stiffness": optimal_k,
        "optimal_damping": optimal_b,
        "max_height": max_height
    })

if __name__ == "__main__":
    app.run(debug=True)