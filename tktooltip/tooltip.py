"""
Module defining the ToolTip widget
"""

import time
import tkinter as tk
from typing import Callable, Union

# This code is based on Tucker Beck's implementation licensed under an MIT License
# Original code: http://code.activestate.com/recipes/576688-tooltip-for-tkinter/


class ToolTip(tk.Toplevel):
    """
    Creates a ToolTip (pop-up) widget for tkinter
    """

    def __init__(
        self,
        widget: tk.Widget,
        msg: Union[str, Callable] = None,
        delay: float = 0.0,
        follow: bool = True,
        x_offset: int = +10,
        y_offset: int = +10,
        parent_kwargs: dict = {"bg": "black", "padx": 1, "pady": 1},
        **message_kwargs,
    ):
        """Initialise the ToolTip allows for **kwargs to be passed on both
            the parent frame and the ToolTip message

        Args:
            widget (tk.Widget): The widget this ToolTip is assigned to
            msg (str, optional): A string message (can be dynamic) assigned to the ToolTip.
                                 Alternatively, it can be set to a function that
                                 returns a string.
                                 Defaults to None.
            delay (float, optional): delay in seconds before the ToolTip appears.
                                     Defaults to 0.0
            follow (bool, optional): ToolTip follows motion, otherwise hides.
                                     Defaults to True.
            x_offset (int, optional): x-coordinate offset for the ToolTip.
                                      Defaults to +10.
            y_offset (int, optional): x-coordinate offset for the ToolTip.
                                      Defaults to +10.
            parent_kwargs (dict, optional): Optional kwargs to be passed into
                                            the parent frame.
                                            Defaults to {"bg": "black", "padx": 1, "pady": 1}.
        """

        self.widget = widget
        # ToolTip shares parent the same parent as the widget
        tk.Toplevel.__init__(self, self.widget.master, **parent_kwargs)

        self.withdraw()  # Hide initially in case there is a delay
        # The ToolTip Toplevel should have no frame or title bar
        self.overrideredirect(True)

        # StringVar instance for msg string|function
        self.msgVar = tk.StringVar()
        # This can be a string or a function
        # Do not bother doing any sort of checks here since it sometimes results
        # into multiple spawn-hide calls being made when swapping between tooltips
        self.msg = msg
        self.delay = delay
        self.follow = follow
        self.x_offset = x_offset
        self.y_offset = y_offset
        # visibility status of the ToolTip inside|outside|visible
        self.status = "outside"
        self.last_moved = 0
        # use Message widget to host ToolTip
        tk.Message(self, textvariable=self.msgVar, aspect=1000, **message_kwargs).grid()
        # Add bindings to the widget.
        # This will NOT override bindings that the widget already has
        self.widget.bind("<Enter>", lambda event: self.on_enter(event))
        self.widget.bind("<Leave>", lambda event: self.on_leave(event))
        self.widget.bind("<Motion>", lambda event: self.on_enter(event))
        self.widget.bind("<ButtonPress>", lambda event: self.on_leave(event))

    def on_enter(self, event) -> None:
        """
        Processes motion within the widget including entering and moving.
        """
        self.last_moved = time.time()

        # Set the status as inside for the very first time
        if self.status == "outside":
            self.status = "inside"

        # If the follow flag is not set, motion within the widget will
        # make the ToolTip dissapear
        if not self.follow:
            self.status = "inside"
            self.withdraw()

        # Offsets the ToolTip using the coordinates od an event as an origin
        self.geometry(f"+{event.x_root + self.x_offset}+{event.y_root + self.y_offset}")

        # The after function takes a time argument in milliseconds
        self.after(int(self.delay * 1000), self._show)

    def on_leave(self, event=None) -> None:
        """
        Hides the ToolTip.
        """
        self.status = "outside"
        self.withdraw()

    def _show(self) -> None:
        """
        Displays the ToolTip if the time delay has been long enough
        """
        if self.status == "inside" and time.time() - self.last_moved > self.delay:
            self.status = "visible"

        if self.status == "visible":
            # Update the string with the latest function call
            # Try and call self.msg as a function, if msg is not callable try and
            # set it as a normal string if that fails throw an error
            try:
                self.msgVar.set(self.msg())
            except TypeError:
                # Intentionally do not check if msg is str, can be a list of str
                self.msgVar.set(self.msg)
            except:
                raise (
                    "Error: ToolTip `msg` must be a string or string returning "
                    + f"function instead `msg` of type {type(self.msg)} was input"
                )
            self.deiconify()
