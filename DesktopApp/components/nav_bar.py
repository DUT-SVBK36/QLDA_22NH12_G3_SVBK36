import tkinter as tk

class NavBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="gray")
        
        self.label = tk.Label(self, text="Posture App", font=("Arial", 16), bg="gray", fg="white")
        self.label.pack(pady=10)

        self.btn_dashboard = tk.Button(self, text="Dashboard", command=self.show_dashboard)
        self.btn_dashboard.pack(side="left", padx=10)

        self.btn_charts = tk.Button(self, text="Charts", command=self.show_charts)
        self.btn_charts.pack(side="left", padx=10)

    def show_dashboard(self):
        print("Switching to Dashboard")

    def show_charts(self):
        print("Switching to Charts")
