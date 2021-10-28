"""
TkToolTip
=========

Provides a tooltip (pop-up) widget for tkinter

Features:
---------
    - Normal tooltips
    - Functions tooltips
    - Delayed tooltips
    - Tracking tooltips
    - Theme-aware tooltips and fully customisable
"""

from ._version import __version__
from .tooltip import ToolTip

__all__ = [
    "ToolTip",
    "__version__",
]
