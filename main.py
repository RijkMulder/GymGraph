import customtkinter
from api import *
from graph import *


MAX_RESULTS = 15

exercises = get_all_exercises()
exercise_names = [exercise["title"] for exercise in exercises]

class App(customtkinter.CTk):
    current_graph = None

    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.title("GymApp")
        self.geometry("800x400")

        self.last_search = ""

        # Make grid expandable
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Search bar (top left)
        self.entry = customtkinter.CTkEntry(
            self,
            width=200,
            placeholder_text="Search"
        )
        self.entry.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nw")
        self.entry.bind("<KeyRelease>", self.input_updated)

        # Scrollable results frame (under search bar)
        self.results_frame = customtkinter.CTkScrollableFrame(
            self,
            width=200,
            height=250
        )
        self.results_frame.grid_forget()

        # graph container
        self.graph_frame = customtkinter.CTkFrame(
            self,
            width=490,
            height=310
        )
        self.graph_frame.grid(row=1, column=1, padx=10, pady=10)
        self.graph_frame.grid_propagate(False)

        # pre-create buttons
        self.result_buttons = []
        for _ in range(MAX_RESULTS):
            btn = customtkinter.CTkButton(
                self.results_frame,
                text="",
                anchor="w"
            )
            btn.grid(row=len(self.result_buttons), column=0, sticky="ew", padx=5, pady=2)
            btn.grid_remove()  # hide initially
            self.result_buttons.append(btn)

        self.results_frame.grid_columnconfigure(0, weight=1)

    def input_updated(self, event):
        search_term = self.entry.get().lower().strip()
        self.results_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nw")

        if search_term == self.last_search:
            return

        self.last_search = search_term

        if search_term == "":
            self.hide_all_buttons()
            self.results_frame.grid_forget()
            return

        filtered = [
            name for name in exercise_names
            if search_term in name.lower()
        ][:MAX_RESULTS]

        self.update_results(filtered)

    def update_results(self, results):
        for i, button in enumerate(self.result_buttons):
            if i < len(results):
                name = results[i]
                button.configure(
                    text=self.truncate_text(name),
                    command=lambda n=name: self.exercise_clicked(n)
                )
                button.grid()
            else:
                button.grid_remove()

    def hide_all_buttons(self):
        for button in self.result_buttons:
            button.grid_remove()

    def exercise_clicked(self, name):
        exercise = next((ex for ex in exercises if ex["title"] == name), None)
        if self.current_graph is not None:

            self.current_graph.get_tk_widget().destroy()
        self.current_graph = create_graph(self.graph_frame, exercise)

    def truncate_text(self, text, max_chars=32):
        if len(text) > max_chars:
            return text[:max_chars - 3] + "..."
        return text

    def on_close(self):
        for widget in self.winfo_children():
            widget.destroy()

        plt.close("all")
        self.quit()
        self.destroy()


app = App()
app.mainloop()