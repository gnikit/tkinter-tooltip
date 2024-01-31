import tkinter as tk
from typing import Callable

import pytest

from tktooltip import ToolTip, ToolTipStatus


@pytest.fixture()
def widget():
    widget = tk.Entry()
    widget.pack()
    widget.update()
    yield widget
    widget.destroy()


def test_tooltip(widget: tk.Widget):
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


@pytest.mark.parametrize(
    "msg",
    [
        1,
        (["text 1", 2]),
    ],
)
def test_tooltip_exceptions(
    widget: tk.Widget,
    msg: str | list[str] | Callable[[], str | list[str]],
):
    with pytest.raises(TypeError):
        ToolTip(widget, msg=msg)  # type: ignore


def test_tooltip_follow(widget: tk.Widget):
    tooltip = ToolTip(widget, msg="Test", follow=False)
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
    msg: str | list[str] | Callable[[], str | list[str]],
):
    tooltip = ToolTip(widget, msg=msg)
    assert tooltip.status == ToolTipStatus.OUTSIDE
    widget.event_generate("<Enter>")
    assert tooltip.status == ToolTipStatus.INSIDE
    tooltip._show()
    assert tooltip.status == ToolTipStatus.VISIBLE
    widget.event_generate("<Leave>")
    assert tooltip.status == ToolTipStatus.OUTSIDE
