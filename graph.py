from api import get_exercise_history
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator

def create_graph(parent, exercise):
    history = get_exercise_history(exercise["id"])

    # collect highest weight per date
    max_weights_per_day = {}

    for entry in history:
        dt = datetime.fromisoformat(entry["workout_start_time"])
        date = dt.date()  # remove time
        weight = entry["weight_kg"]

        if date not in max_weights_per_day or weight > max_weights_per_day[date]:
            max_weights_per_day[date] = weight

    # convert back to sorted lists
    dates = sorted(max_weights_per_day.keys())
    weights = [max_weights_per_day[d] for d in dates]

    # Create a matplotlib figure
    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)

    ax.plot(dates, weights, marker="o", markersize=3, label="Max Weight")
    ax.set_title(f"Weight Progression for {exercise['title']}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Weight (kg)")
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    fig.autofmt_xdate()

    # Embed the figure in CustomTkinter
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()

    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True, padx=10, pady=10)

    return canvas




