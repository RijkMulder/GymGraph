import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def create_graph(parent, name):
    # Create a matplotlib figure
    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
    ax.plot([1, 2, 3, 4], [10, 5, 8, 12])
    ax.set_title(name)

    # Embed the figure in CustomTkinter
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True, padx=10, pady=10)
    return canvas



