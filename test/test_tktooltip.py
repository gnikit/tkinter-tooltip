import tkinter as tk
from typing import Callable

import pytest

from tktooltip import ToolTip


@pytest.fixture()
def widget():
    widget = tk.Entry()
    widget.pack()
    widget.update()
    yield widget
    widget.destroy()


def test_tooltip_default(widget: tk.Widget):
    tooltip = ToolTip(widget)
    assert tooltip.msg is None
    assert tooltip.delay == 0.0
    assert tooltip.follow
    assert tooltip.refresh == 1.0
    assert tooltip.x_offset == 10
    assert tooltip.y_offset == 10
    # assert tooltip.parent_kwargs == {"bg": "black", "padx": 1, "pady": 1}


def test_tooltip_custom(widget: tk.Widget):
    tooltip = ToolTip(
        widget,
        msg="Test Tooltip",
        delay=0.5,
        follow=False,
        refresh=0.5,
        x_offset=20,
        y_offset=20,
        parent_kwargs={"bg": "red", "padx": 2, "pady": 2},
        fg="white",
        bg="red",
        font=("Helvetica", 12),
    )

    assert tooltip.msg == "Test Tooltip"
    assert tooltip.delay == 0.5
    assert not tooltip.follow
    assert tooltip.refresh == 0.5
    assert tooltip.x_offset == 20
    assert tooltip.y_offset == 20


def test_tooltip_follow(widget: tk.Widget):
    tooltip = ToolTip(widget, follow=False)
    widget.event_generate("<Enter>")
    assert not tooltip.follow


@pytest.mark.parametrize(
    "msg",
    [
        (lambda: "Callable Tooltip"),
        "text",
        (["text 1", "text 2"]),
    ],
)
def test_tooltip_show(
    widget: tk.Widget,
    msg: str | list[str] | Callable[[], str],
):
    tooltip = ToolTip(widget, msg=msg)
    assert tooltip.status == "outside"
    widget.event_generate("<Enter>")
    assert tooltip.status == "inside"
    tooltip._show()
    assert tooltip.status == "visible"
    widget.event_generate("<Leave>")
    assert tooltip.status == "outside"
