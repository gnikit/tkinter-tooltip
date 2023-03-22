import threading
import time
import tkinter as tk
from typing import Callable

from tktooltip.tooltip import ToolTip


def loading_tooltip(
    widget: tk.Widget | tk.Tk | tk.Toplevel | list[tk.Widget | tk.Tk | tk.Toplevel],
    func: Callable,
    msg: str = "Loading..",
    delay: int | float = 0.001,
):
    """
    Loads a tooltip which follows the cursor, calls
    the function and then unbinds & destroys the tooltip.

    Parameters
    ----------
    widget : `tk.Widget | tk.Tk | tk.Toplevel | list[tk.Widget | tk.Tk | tk.Toplevel]`
        The widget to be followed by the Tooltip
    func : `Callable`
        The function to be called
    msg : `str`
        The message to be displayed in the tooltip
    delay : The time to delay the appearance of the tooltip
    """
    if not isinstance(widget, list):
        tooltip = ToolTip(widget, msg=msg, delay=delay)
        func()
        tooltip.self_destroy_handler()
    else:
        tooltip = ToolTip(widget, msg=msg, delay=delay)
        for number, item in enumerate(widget):
            if number == 0:
                # Run the function only in the first time.
                func()
        tooltip.self_destroy_handler()


def fibonacci(numbers):
    """Calculates the fibonacci numbers up to `numbers`"""
    number0 = 0
    number1 = 1
    count = 0
    while count < numbers:
        time.sleep(0.001)
        # print(number1)
        new_number = number0 + number1
        number0, number1 = number1, new_number
        count += 1
    else:
        print("Ended")


def center_toplevel(window: tk.Tk | tk.Toplevel, side: str | None = "Right") -> None:
    """
    Places the `window` at the center, center-right or center-left of the screen.
    """
    window.update_idletasks()
    width = window.winfo_width()
    frm_width = window.winfo_rootx() - window.winfo_x()
    win_width = width + 2 * frm_width
    height = window.winfo_height()
    titlebar_height = window.winfo_rooty() - window.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = None
    if isinstance(window, tk.Tk):
        x = window.winfo_screenwidth() // 2 - win_width // 2
    if side == "Left":
        x = window.winfo_screenwidth() // 3 - win_width // 2
    elif side == "Right":
        x = window.winfo_screenwidth() // 1.5 - win_width // 2
        x = int(x)
    y = window.winfo_screenheight() // 2 - win_height // 2
    window.geometry("+{}+{}".format(x, y))
    window.deiconify()
    print(
        f"Window: {window} centered according to the width and the height of the screen"
    )


if __name__ == "__main__":
    # An example for the tooltip assigned to two windows
    root = tk.Tk()
    root.title("Parent window")
    center_toplevel(root, side=None)
    toplevel = tk.Toplevel(root)
    toplevel.title("Second window")
    center_toplevel(toplevel, side="Right")
    toplevel2 = tk.Toplevel(toplevel)
    toplevel2.title("Third window")
    center_toplevel(toplevel2, side="Left")
    # Start a thread for the tooltip so as the mainloop not to be blocked
    thread = threading.Thread(
        target=lambda: loading_tooltip(
            widget=[root, toplevel, toplevel2], func=lambda: fibonacci(500)
        )
    )
    thread.start()
    root.mainloop()
