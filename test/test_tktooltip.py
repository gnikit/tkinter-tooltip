import tkinter as tk
from typing import Callable
from unittest.mock import patch

import pytest
from screeninfo.common import Monitor

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
        (lambda: ["Callable Tooltip 1", "Callable Tooltip 2"]),
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


def test_tooltip_destroy(widget: tk.Widget):
    tooltip = ToolTip(widget, msg="Test")
    widget.event_generate("<Enter>")
    assert tooltip.status == ToolTipStatus.INSIDE
    tooltip._show()
    assert tooltip.status == ToolTipStatus.VISIBLE
    tooltip.destroy()
    print(tooltip.bindigs)
    assert tooltip.bindigs == []


@pytest.fixture
def get_monitors():
    return [
        Monitor(x=0, y=0, width=1920, height=1080, name="DISPLAY1", is_primary=True),
        Monitor(x=1920, y=0, width=1366, height=768, name="DISPLAY2", is_primary=False),
        Monitor(
            x=3286, y=0, width=1920, height=1080, name="DISPLAY3", is_primary=False
        ),
    ]


def test_tooltip_overflow(widget: tk.Widget, get_monitors: list[Monitor]):
    with patch("screeninfo.get_monitors", return_value=get_monitors):
        tooltip = ToolTip(widget, msg="Test\nTest")
        widget.event_generate("<Enter>", rootx=3280, rooty=760)
        tooltip._show()
        assert (
            tooltip.message_widget.winfo_rootx() + tooltip.message_widget.winfo_width()
            < 3286
        )
        assert (
            tooltip.message_widget.winfo_rooty() + tooltip.message_widget.winfo_height()
            < 768
        )
