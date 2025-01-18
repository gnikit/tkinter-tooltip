"""
Module defining the ToolTip widget
"""

from __future__ import annotations

import threading
import time
import tkinter as tk
from contextlib import suppress
from enum import Enum, auto
from typing import Any, Callable

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
        animations: bool = True,
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
        animations : `bool`, optional
            ToolTip fades in when showing and fades out when hiding, by default True.
            This requires a compositing window manager on Linux to have any effect.
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
        self.msg = msg
        self._update_message()
        self.delay = delay
        self.follow = follow
        self.animations = animations
        self.refresh = refresh
        self.x_offset = x_offset
        self.y_offset = y_offset
        # visibility status of the ToolTip inside|outside|visible
        self.status = ToolTipStatus.OUTSIDE
        self.last_moved = 0.0
        # use Message widget to host ToolTip
        self.message_kwargs: dict = self.DEFAULT_MESSAGE_KWARGS.copy()
        self.message_kwargs.update(message_kwargs)
        self.message_widget = tk.Message(
            self,
            textvariable=self.msg_var,
            **self.message_kwargs,
        )
        self.message_widget.grid()
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
        self.last_moved = time.perf_counter()
        self.status = ToolTipStatus.INSIDE
        self._update_tooltip_coords(event)
        self.after(int(self.delay * self.S_TO_MS), self._show)

    def on_leave(self, event: tk.Event | None = None) -> None:
        """
        Hides the ToolTip.
        """
        self.status = ToolTipStatus.OUTSIDE

        def animation():
            self.wm_attributes("-alpha", 1)

            for i in range(11):
                self.wm_attributes("-alpha", 0.1 * (10 - i))
                time.sleep(0.01)

            self.withdraw()

        if self.animations:
            threading.Thread(target=animation, daemon=True).start()
        else:
            self.withdraw()

    def _update_tooltip_coords(self, event: tk.Event) -> None:
        """
        Updates the ToolTip's position.
        """
        self.geometry(f"+{event.x_root + self.x_offset}+{event.y_root + self.y_offset}")

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
            and time.perf_counter() - self.last_moved >= self.delay
        ):
            self.is_shown = False
            self.status = ToolTipStatus.VISIBLE

        if self.status == ToolTipStatus.VISIBLE:
            self._update_message()
            self.deiconify()

            if not self.is_shown:
                x_pos = self.x_offset + self.winfo_pointerx()
                y_pos = self.y_offset + self.winfo_pointery()

                self.geometry(f"+{x_pos}+{y_pos}")

            def animation():
                if not self.is_shown:
                    self.wm_attributes("-alpha", 0)

                    for i in range(11):
                        self.wm_attributes("-alpha", 0.1 * i)
                        time.sleep(0.01)

                    self.is_shown = True

            if self.animations:
                threading.Thread(target=animation, daemon=True).start()

            # Recursively call _show to update ToolTip with the newest value of msg
            # This is a race condition which only exits when upon a binding change
            # that in turn changes the `status` to outside
            self.after(int(self.refresh * self.S_TO_MS), self._show)
