import re
import tkinter as tk
from pathlib import Path
from tkinter import ttk

import sv_ttk
from PIL import Image, ImageTk

from tktooltip import ToolTip


class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        # Create widgets
        self.setup_widgets()

        # Bind the entries to the validator methods
        self.bind_them()

    def setup_widgets(self):
        self.color = "0,0,0"  # Default color to replace (it's black)
        img = Path(__file__).parent / "tooltip_logo.png"  # image name to loads
        self.img = Image.open(img).resize((100, 100))  # Load and scale image
        self.img_tk = ImageTk.PhotoImage(self.img)  # Store to stop garbage collection
        self.img_label = ttk.Label(self, image=self.img_tk)  # Create label with image
        ToolTip(self.img_label, msg=self.colorcode)  # Add toolip to label
        self.img_label.pack()

        # Create a mask with non-zero pixel coordinates
        self.mask = []
        for i in range(self.img_tk.width()):
            for j in range(self.img_tk.height()):
                if self.img.getpixel((i, j)) != (0, 0, 0, 0):
                    self.mask.append((i, j))

        self.color_entry = ttk.Entry(self)
        self.color_entry.pack(padx=50, pady=(25, 50))
        ToolTip(self.color_entry, msg="Input RGB values\nseparated by commas")

    def bind_them(self):
        self.color_entry.bind("<FocusOut>", self.validate_color)
        self.color_entry.bind("<FocusIn>", self.validate_color)
        self.color_entry.bind("<KeyRelease>", self.validate_color)

    def validate_color(self, *_):
        """Checks if color is valid RGB values"""
        if re.match(r"^\d{1,3},\d{1,3},\d{1,3}$", self.color_entry.get()):
            self.color_entry.state(["!invalid"])
        else:
            self.color_entry.state(["invalid"])

        if (
            "invalid" not in self.color_entry.state()
            and self.color != self.color_entry.get()
        ):
            self.color = self.color_entry.get()
            r, g, b = self.color_entry.get().split(",")
            # Using the cached mask replace the all the non-zero pixels
            for i, j in self.mask:
                self.img.putpixel((i, j), (int(r), int(g), int(b)))
            self.img_tk = ImageTk.PhotoImage(self.img)
            self.img_label.config(image=self.img_tk)

    def colorcode(self):
        """Returns the RGB and HEX color codes of a color"""
        msg = "RGB: ({},{},{})".format(*self.color.split(","))
        msg = msg + "\nHEX: #{:02x}{:02x}{:02x}".format(
            *list(map(int, self.color.split(",")))
        )
        return msg


def main():
    root = tk.Tk()
    root.title("")
    sv_ttk.set_theme("dark")

    app = App(root)
    app.pack(fill="both", expand=True)
    root.update_idletasks()  # Make sure every screen redrawing is done

    width, height = root.winfo_width(), root.winfo_height()
    x = int((root.winfo_screenwidth() / 2) - (width / 2))
    y = int((root.winfo_screenheight() / 2) - (height / 2))
    # Set a minsize for the window, and place it in the middle
    root.minsize(width, height)
    root.geometry(f"+{x}+{y}")
    root.mainloop()


if __name__ == "__main__":
    main()
