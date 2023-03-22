"""
Module defining the ToolTip widget
"""
from __future__ import annotations

import time
import tkinter as tk
from typing import Callable


# This code is based on Tucker Beck's implementation licensed under an MIT License
# Original code: http://code.activestate.com/recipes/576688-tooltip-for-tkinter/


class ToolTip(tk.Toplevel):
    """
    Creates a ToolTip (pop-up) widget for tkinter
    """

    def __init__(
        self,
        widget: (
            tk.Widget | tk.Tk | tk.Toplevel | list[tk.Widget | tk.Tk | tk.Toplevel]
        ),
        msg: str | Callable = None,
        delay: float = 0.0,
        follow: bool = True,
        refresh: float = 1.0,
        x_offset: int = +10,
        y_offset: int = +10,
        parent_kwargs: dict = {"bg": "black", "padx": 1, "pady": 1},
        **message_kwargs,
    ):
        """Create a ToolTip. Allows for `**kwargs` to be passed on both
            the parent frame and the ToolTip message

        Parameters
        ----------
        widget : `tk.Widget, tk.Tk, tk.Toplevel, list[tk.Widget, tk.Tk, tk.Toplevel]`
            The widget this ToolTip is assigned to
        msg : `Union[str, Callable]`, optional
            A string message (can be dynamic) assigned to the ToolTip.
            Alternatively, it can be set to a function that returns a string,
            by default None
        delay : `float`, optional
            Delay in seconds before the ToolTip appears, by default 0.0
        follow : `bool`, optional
            ToolTip follows motion, otherwise hides, by default True
        refresh : `float`, optional
            Refresh rate in seconds for strings and functions when mouse is
            stationary and inside the widget, by default 1.0
        x_offset : `int`, optional
            x-coordinate offset for the ToolTip, by default +10
        y_offset : `int`, optional
            y-coordinate offset for the ToolTip, by default +10
        parent_kwargs : `dict`, optional
            Optional kwargs to be passed into the parent frame,
            by default `{"bg": "black", "padx": 1, "pady": 1}`
        **message_kwargs : tkinter `**kwargs` passed directly into the ToolTip
        """
        self.widget = widget
        # ToolTip should have the same parent as the widget unless stated
        # otherwise in the `parent_kwargs`
        tk.Toplevel.__init__(self, **parent_kwargs)
        # Hide initially in case there is a delay
        self.iconify()
        self.withdraw()
        # Disable ToolTip's title bar
        self.overrideredirect(True)

        # StringVar instance for msg string|function
        self.msgVar = tk.StringVar()
        # This can be a string or a function
        # Do not bother doing any sort of checks here since it sometimes results
        # into multiple spawn-hide calls being made when swapping between tooltips
        self.msg = msg
        self.delay = delay
        self.follow = follow
        self.refresh = refresh
        self.x_offset = x_offset
        self.y_offset = y_offset
        # visibility status of the ToolTip inside|outside|visible
        self.status = "outside"
        self.last_moved = 0
        # use Message widget to host ToolTip
        tk.Message(self, textvariable=self.msgVar, aspect=1000, **message_kwargs).grid()
        # Add bindings to the widget without overriding the existing ones
        if not isinstance(self.widget, list):
            self.create_binds(widget=self.widget)
        # Add bindings to each item in the widget list
        else:
            for item in self.widget:
                self.create_binds(widget=item)

    def on_enter(self, event) -> None:
        """
        Processes motion within the widget including entering and moving.
        """
        self.last_moved = time.time()

        # Set the status as inside for the very first time
        if self.status == "outside":
            self.status = "inside"

        # If the follow flag is not set, motion within the widget will
        # make the ToolTip disappear
        if not self.follow:
            self.status = "inside"
            self.withdraw()

        # Offsets the ToolTip using the coordinates od an event as an origin
        self.geometry(f"+{event.x_root + self.x_offset}+{event.y_root + self.y_offset}")

        # Time is integer and in milliseconds
        self.after(int(self.delay * 1000), self._show)

    def on_leave(self, event=None) -> None:
        """
        Hides the ToolTip.
        """
        self.status = "outside"
        self.withdraw()

    def _show(self) -> None:
        """
        Displays the ToolTip.

        Recursively queues `_show` in the scheduler every `self.refresh` seconds
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

            # Recursively call _show to update ToolTip with the newest value of msg
            # This is a race condition which only exits when upon a binding change
            # that in turn changes the `status` to outside
            self.after(int(self.refresh * 1000), self._show)

    def create_binds(self, widget: tk.Tk | tk.Widget | tk.Toplevel) -> None:
        """Creates the binds without overriding the existing ones"""
        widget.bind("<Enter>", self.on_enter, add="+")
        widget.bind("<Leave>", self.on_leave, add="+")
        widget.bind("<Motion>", self.on_enter, add="+")
        widget.bind("<ButtonPress>", self.on_leave, add="+")

    def unbind_itself(self) -> None:
        """
        Unbinds every event sequence.
        """
        if not isinstance(self.widget, list):
            self.widget.bind("<Enter>", "")
            self.widget.bind("<Leave>", "")
            self.widget.bind("<Motion>", "")
            self.widget.bind("<ButtonPress>", "")
        else:
            for item in self.widget:
                item.bind("<Enter>", "")
                item.bind("<Leave>", "")
                item.bind("<Motion>", "")
                item.bind("<ButtonPress>", "")

    def self_destroy_handler(self) -> None:
        """A handler for destroying itself after a given time"""
        self.after(1000, self.self_destroy())

    def self_destroy(self) -> None:
        """Unbinds and destroys itself after a given time
        after checking if the tooltip still exists"""
        self.unbind_itself()
        if self.winfo_exists() == 1:
            self.destroy()
