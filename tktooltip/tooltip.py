"""
Module defining the ToolTip widget
"""

from __future__ import annotations

import time
import tkinter as tk
from enum import Enum, auto
from typing import Any, Callable

# This code is based on Tucker Beck's implementation licensed under an MIT License
# Original code: http://code.activestate.com/recipes/576688-tooltip-for-tkinter/


class ToolTipStatus(Enum):
    OUTSIDE = auto()
    INSIDE = auto()
    VISIBLE = auto()


class ToolTip(tk.Toplevel):
    """
    Creates a ToolTip (pop-up) widget for tkinter
    """

    DEFAULT_PARENT_KWARGS = {"bg": "black", "padx": 1, "pady": 1}
    DEFAULT_MESSAGE_KWARGS = {"aspect": 1000}
    S_TO_MS = 1000

    def __init__(
        self,
        widget: tk.Widget,
        msg: str | list[str] | Callable[[], str | list[str]],
        delay: float = 0.0,
        follow: bool = True,
        refresh: float = 1.0,
        x_offset: int = +10,
        y_offset: int = +10,
        parent_kwargs: dict | None = None,
        **message_kwargs: Any,
    ):
        """Create a ToolTip. Allows for `**kwargs` to be passed on both
            the parent frame and the ToolTip message

        Parameters
        ----------
        widget : tk.Widget
            The widget this ToolTip is assigned to
        msg : `Union[str, Callable]`, optional
            A string message (can be dynamic) assigned to the ToolTip.
            Alternatively, it can be set to a function thatreturns a string,
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
        tk.Toplevel.__init__(self, **(parent_kwargs or self.DEFAULT_PARENT_KWARGS))
        self.withdraw()  # Hide initially in case there is a delay
        # Disable ToolTip's title bar
        self.overrideredirect(True)

        # StringVar instance for msg string|function
        self.msg_var = tk.StringVar()
        # This can be a string or a function
        if not (
            callable(msg)
            or (isinstance(msg, str))
            or (isinstance(msg, list) and all(isinstance(m, str) for m in msg))
        ):
            raise TypeError(
                "Error: ToolTip `msg` must be a string, list of strings or string "
                + f"returning function instead `msg` of type {type(msg)} was input"
            )
        self.msg = msg
        self.delay = delay
        self.follow = follow
        self.refresh = refresh
        self.x_offset = x_offset
        self.y_offset = y_offset
        # visibility status of the ToolTip inside|outside|visible
        self.status = ToolTipStatus.OUTSIDE
        self.last_moved = 0
        # use Message widget to host ToolTip
        self.message_kwargs: dict = message_kwargs or self.DEFAULT_MESSAGE_KWARGS
        self.message_widget = tk.Message(
            self,
            textvariable=self.msg_var,
            **self.message_kwargs,
        )
        self.message_widget.grid()

        self._init_bindings()

    def _init_bindings(self) -> None:
        """
        Initialise the bindings for the ToolTip without overriding the existing ones.
        """
        self.widget.bind("<Enter>", self.on_enter, add="+")
        self.widget.bind("<Leave>", self.on_leave, add="+")
        if self.follow:
            self.widget.bind("<Motion>", self.on_enter, add="+")

    def on_enter(self, event: tk.Event) -> None:
        """
        Processes motion within the widget including entering and moving.
        """
        self.last_moved = time.time()
        self.status = ToolTipStatus.INSIDE

        # Offsets the ToolTip using the coordinates od an event as an origin
        self.geometry(f"+{event.x_root + self.x_offset}+{event.y_root + self.y_offset}")

        self.after(int(self.delay * self.S_TO_MS), self._show)

    def on_leave(self, event: tk.Event | None = None) -> None:
        """
        Hides the ToolTip.
        """
        self.status = ToolTipStatus.OUTSIDE
        self.withdraw()

    def _update_message(self) -> None:
        """Update the message displayed in the tooltip."""
        if callable(self.msg):
            self.msg_var.set(self.msg())
        elif isinstance(self.msg, str):
            self.msg_var.set(self.msg)
        elif isinstance(self.msg, list):
            self.msg_var.set("\n".join(self.msg))
        # TODO: throw exception if none of the above

    def _show(self) -> None:
        """
        Displays the ToolTip.

        Recursively queues `_show` in the scheduler every `self.refresh` seconds
        """
        if (
            self.status == ToolTipStatus.INSIDE
            and time.time() - self.last_moved > self.delay
        ):
            self.status = ToolTipStatus.VISIBLE

        if self.status == ToolTipStatus.VISIBLE:
            self._update_message()
            self.deiconify()

            # Recursively call _show to update ToolTip with the newest value of msg
            # This is a race condition which only exits when upon a binding change
            # that in turn changes the `status` to outside
            self.after(int(self.refresh * self.S_TO_MS), self._show)
