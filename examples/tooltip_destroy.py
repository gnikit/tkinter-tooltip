import tkinter as tk

from tktooltip import ToolTip  # Assuming tooltip.py is in the same directory


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.iter = 0

        # Create a label with a tooltip
        self.label = tk.Label(self, text="Hover over me!")
        self.label.pack(padx=10, pady=10)
        self.tooltip = ToolTip(self.label, msg=f"Hello {self.iter}")

        # Create a button that destroys the tooltip
        self.destroy_b = tk.Button(
            self, text="Destroy Tooltip", command=self.destroy_tooltip
        )
        self.destroy_b.pack(padx=10, pady=10)
        self.create_b = tk.Button(
            self, text="Create Tooltip", command=self.create_tooltip
        )
        self.create_b.pack(padx=10, pady=10)

    def destroy_tooltip(self):
        # Destroy the tooltip
        if self.tooltip is not None:
            self.tooltip.destroy()
            self.tooltip = None

    def create_tooltip(self):
        # Create the tooltip
        print(type(self.tooltip))
        print(self.tooltip)
        print("===========")
        for c in list(self.children.values()):
            print(c)
        print("***********")
        if self.tooltip is None:
            self.iter += 1
            self.tooltip = ToolTip(self.label, msg=f"Hello {self.iter}")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
