import time
import tkinter as tk
import tkinter.ttk as ttk
from itertools import product
from tkinter import font as tkFont

from tooltip import ToolTip


def custom_font(frame, **kwargs):
    return tkFont.Font(frame, **kwargs)


def main():
    root = tk.Tk()
    s = ttk.Style()
    s.configure("custom.TButton", foreground="#208020", background="#fafafa")
    # root.tk.call("source", "themes/sun-valley/sun-valley.tcl")
    # root.tk.call("set_theme", "dark")
    btnList = []
    for (i, j) in list(product(range(2), range(4))):
        text = f"delay={i}s\n"
        delay = i
        if j >= 2:
            follow = True
            text += "follow tooltip: \u2714\n"  # yes
        else:
            follow = False
            text += "follow tooltip: \u274C\n"  # no
        if j % 2 == 0:
            msg = time.asctime
            text += "tooltip: Function"
        else:
            msg = f"Button at {str((i, j))}"
            text += "tooltip: String"
        btnList.append(ttk.Button(root, text=text, style="custom.TButton"))
        ToolTip(
            btnList[-1],
            msg=msg,
            follow=follow,
            delay=delay,
            # Parent frame arguments
            parent_kwargs={"bg": "black", "padx": 5, "pady": 5},
            # These are arguments to the tk.Message
            fg="#202020",
            bg="#fafafa",
            padx=10,
            pady=10,
            font=custom_font(root, size=8, weight=tkFont.BOLD),
        )
        btnList[-1].grid(row=i, column=j, sticky="nsew", ipadx=20, ipady=20)
    root.mainloop()


if __name__ == "__main__":
    main()
