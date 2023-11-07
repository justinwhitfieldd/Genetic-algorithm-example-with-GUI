import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from geneticAlgo import mathFunction, binary_string_to_integer, mutations, roulette_wheel_creation, roulette_wheel_selection, crossover, initialize_chromosomes


def run_training(N, Pc, Pm, epochs, ax):
    chromosomes = initialize_chromosomes(N)
    max_values = []
    for epoch in range(epochs):
        roulette_selected_chromosomes = []
        fitnessValues = [0] * N
        fitness_to_binary_map = {}
        #print(chromosomes)
        for i in range(N):
            #print(i)
            #print("chromosome sizes: ", len(chromosomes[i]))
            x_binary = chromosomes[i][:10]
            y_binary = chromosomes[i][10:20]
            x_float = [0] * N
            y_float = [0] * N
            x_float[i] = binary_string_to_integer(x_binary)
            y_float[i] = binary_string_to_integer(y_binary)
            fitness = mathFunction(x_float[i], y_float[i])
            #print("X: ",x_float[i]," Y: ",y_float[i]," fitness: ", fitness)
            fitness_to_binary_map[fitness] = chromosomes[i]
            fitnessValues[i] = fitness

        # select pair of chromosomes N times by roulette
        for i in range(N):
            roulette_percent_to_fitness_map, roulette_percentages = roulette_wheel_creation(fitnessValues, N)
            selected = roulette_wheel_selection(roulette_percentages)   
            roulette_selected_chromosomes.append(fitness_to_binary_map[roulette_percent_to_fitness_map[selected]])

        chromosomes_after_crossover = crossover(roulette_selected_chromosomes, Pc)
        chromosomes = mutations(chromosomes_after_crossover, Pm)
        max_value = max(fitnessValues) 
        max_values.append(max_value)
        print("EPOCH: ", epoch, " MAX VAL: ", max_value)

    # Clear previous plot
    ax.clear()
    ax.plot(range(epochs), max_values, label="Max Value per Epoch")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Max Value")
    ax.legend()
    canvas.draw()

def start_training():
    N = N_slider.get()
    Pc = Pc_slider.get()
    Pm = Pm_slider.get()
    epochs = epochs_slider.get()
    run_training(N, Pc, Pm, epochs, ax)

# Main window
root = tk.Tk()
root.title("Genetic Algorithm GUI")

# Define frames for layout
control_frame = tk.Frame(root)
control_frame.pack(side=tk.TOP, pady=(10, 0), fill=tk.X)
plot_frame = tk.Frame(root)
plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Define sliders within the control frame
N_slider = tk.Scale(control_frame, from_=10, to=200, orient='horizontal', length=200, label="N (Population Size)")
N_slider.set(100)
N_slider.grid(row=0, column=0, padx=(0, 5), sticky="ew")

Pc_slider = tk.Scale(control_frame, from_=0.0, to=1.0, resolution=0.01, orient='horizontal', length=200, label="Pc (Crossover Probability)")
Pc_slider.set(0.7)
Pc_slider.grid(row=0, column=1, padx=(5, 5), sticky="ew")

Pm_slider = tk.Scale(control_frame, from_=0.0001, to=0.04, resolution=0.001, orient='horizontal', length=200, label="Pm (Mutation Probability)")
Pm_slider.set(0.02)
Pm_slider.grid(row=0, column=2, padx=(5, 5), sticky="ew")

epochs_slider = tk.Scale(control_frame, from_=1, to=1000, orient='horizontal', length=200, label="Epochs")
epochs_slider.set(500)
epochs_slider.grid(row=0, column=3, padx=(5, 0), sticky="ew")

# Run button
run_button = tk.Button(control_frame, text="Run Training", command=start_training)
run_button.grid(row=1, column=0, columnspan=4, pady=(5, 0))

# Ensure that the control frame adjusts with the window resizing
control_frame.columnconfigure(0, weight=1)
control_frame.columnconfigure(1, weight=1)
control_frame.columnconfigure(2, weight=1)
control_frame.columnconfigure(3, weight=1)

# Plotting area within the plot frame
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Start the GUI loop
root.mainloop()