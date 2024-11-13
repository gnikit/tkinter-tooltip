"""
Module defining the ToolTip widget
"""

from __future__ import annotations

import time
import tkinter as tk
from contextlib import suppress
from enum import Enum, auto
from typing import Any, Callable

import screeninfo

# This code is based on Tucker Beck's implementation licensed under an MIT License
# Original code: http://code.activestate.com/recipes/576688-tooltip-for-tkinter/


class ToolTipStatus(Enum):
    OUTSIDE = auto()
    INSIDE = auto()
    VISIBLE = auto()


class Binding:
    def __init__(self, widget: tk.Widget, binding_name: str, functor: Callable) -> None:
        self._widget = widget
        self._name: str = binding_name
        self._id: str = self._widget.bind(binding_name, functor, add="+")

    def unbind(self) -> None:
        self._widget.unbind(self._name, self._id)


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
        # Mkae ToolTip topmost to display over taskbar
        self.attributes("-topmost", True)

        # StringVar instance for msg string|function
        self.msg_var = tk.StringVar()
        self.msg = msg
        self._update_message()
        self.delay = delay
        self.follow = follow
        self.refresh = refresh
        # ensure a minimum offset of 2 to avoid flickering
        self.x_offset = x_offset if x_offset > 0 else 2
        self.y_offset = y_offset if y_offset > 0 else 2
        # visibility status of the ToolTip inside|outside|visible
        self.status = ToolTipStatus.OUTSIDE
        self.last_moved = 0
        # use Message widget to host ToolTip
        self.message_kwargs: dict = self.DEFAULT_MESSAGE_KWARGS.copy()
        self.message_kwargs.update(message_kwargs)
        self.message_widget = tk.Message(
            self,
            textvariable=self.msg_var,
            **self.message_kwargs,
        )
        self.message_widget.grid()
        self.monitors = screeninfo.get_monitors()
        self.bindigs = self._init_bindings()

    def _init_bindings(self) -> list[Binding]:
        """Initialize the bindings."""
        bindings = [
            Binding(self.widget, "<Enter>", self.on_enter),
            Binding(self.widget, "<Leave>", self.on_leave),
            Binding(self.widget, "<ButtonPress>", self.on_leave),
        ]
        if self.follow:
            bindings.append(
                Binding(self.widget, "<Motion>", self._update_tooltip_coords)
            )
        return bindings

    def destroy(self) -> None:
        """Destroy the ToolTip and unbind all the bindings."""
        with suppress(tk.TclError):
            for b in self.bindigs:
                b.unbind()
            self.bindigs.clear()
            super().destroy()

    def on_enter(self, event: tk.Event) -> None:
        """
        Processes motion within the widget including entering and moving.
        """
        self.last_moved = time.time()
        self.status = ToolTipStatus.INSIDE
        self._update_tooltip_coords(event)
        self.after(int(self.delay * self.S_TO_MS), self._show)

    def on_leave(self, event: tk.Event | None = None) -> None:
        """
        Hides the ToolTip.
        """
        self.status = ToolTipStatus.OUTSIDE
        self.withdraw()

    def _update_tooltip_coords(self, event: tk.Event) -> None:
        """
        Updates the ToolTip's position.
        """
        w_left = event.x_root + self.x_offset
        w_top = event.y_root + self.y_offset

        w_right = w_left + self.message_widget.winfo_width()
        w_bottom = w_top + self.message_widget.winfo_height()

        for monitor in self.monitors:
            # check if cursor is in monitor
            if (
                monitor.x <= event.x_root < monitor.x + monitor.width
                and monitor.y <= event.y_root < monitor.y + monitor.height
            ):
                # move tooltip left if it exceedes the monitor's right boundary
                if w_right >= monitor.x + monitor.width:
                    w_left = (
                        monitor.x
                        + monitor.width
                        - self.message_widget.winfo_width()
                        - 2
                    )

                # flip tooltip if it exceedes the monitor's bottom boundary
                if w_bottom >= monitor.y + monitor.height:
                    w_top = (
                        event.y_root
                        - self.y_offset
                        - self.message_widget.winfo_height()
                    )

                break

        self.geometry(f"+{w_left}+{w_top}")

    def _update_message(self) -> None:
        """Update the message displayed in the tooltip."""
        if callable(self.msg):
            msg = self.msg()
            if isinstance(msg, list):
                msg = "\n".join(msg)
        elif isinstance(self.msg, str):
            msg = self.msg
        elif isinstance(self.msg, list):
            msg = "\n".join(self.msg)
        else:
            raise TypeError(
                f"ToolTip `msg` must be a string, list of strings, or a "
                f"callable returning them, not {type(self.msg)}."
            )
        self.msg_var.set(msg)

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
