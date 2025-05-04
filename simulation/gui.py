import tkinter as tk
from tkinter import ttk
from simulation.simulation import run_sim

def run_gui():
    def run_simulation():
        k = float(stiffness_slider.get())
        b = float(damping_slider.get())
        g = float(gravity_slider.get())
        body_size = float(body_size_slider.get())

        # Run the simulation
        run_sim(k, b, g, body_size, render=True)

    root = tk.Tk()
    root.title("Simulation GUI")

    # Sliders
    ttk.Label(root, text="Stiffness").pack()
    stiffness_slider = ttk.Scale(root, from_=0.05, to=3, orient="horizontal")
    stiffness_slider.pack()

    ttk.Label(root, text="Damping").pack()
    damping_slider = ttk.Scale(root, from_=0.05, to=3, orient="horizontal")
    damping_slider.pack()

    ttk.Label(root, text="Gravity").pack()
    gravity_slider = ttk.Scale(root, from_=0.01, to=100, orient="horizontal")
    gravity_slider.pack()

    ttk.Label(root, text="Body Size").pack()
    body_size_slider = ttk.Scale(root, from_=0.001, to=0.3, orient="horizontal")
    body_size_slider.pack()

    # Run button
    run_button = ttk.Button(root, text="Run Simulation", command=run_simulation)
    run_button.pack()

    root.mainloop()