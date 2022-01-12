[![Downloads](https://pepy.tech/badge/tkinter-tooltip)](https://pepy.tech/project/tkinter-tooltip)
[![PyPI Latest Release](https://img.shields.io/pypi/v/tkinter-tooltip.svg)](https://pypi.org/project/tkinter-tooltip/)
[![PyPi Release](https://github.com/gnikit/tkinter-tooltip/actions/workflows/python-publish.yml/badge.svg)](https://github.com/gnikit/tkinter-tooltip/actions/workflows/python-publish.yml)
[![Documentation](https://github.com/gnikit/tkinter-tooltip/actions/workflows/docs.yml/badge.svg)](https://github.com/gnikit/tkinter-tooltip/actions/workflows/docs.yml)
[![CodeFactor](https://www.codefactor.io/repository/github/gnikit/tkinter-tooltip/badge)](https://www.codefactor.io/repository/github/gnikit/tkinter-tooltip)
[![PyPI - License](https://img.shields.io/pypi/l/tkinter-tooltip)](https://github.com/gnikit/tkinter-tooltip/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<p align="center">
  <img src="https://raw.githubusercontent.com/gnikit/tkinter-tooltip/master/assets/images/tooltip_logo.svg" />
</p>

# tkinter-tooltip

## What this is

This is a simple yet fully customisable tooltip/pop-up implementation for
`tkinter` widgets. It is capable of fully integrating with custom `tkinter`
themes both light and dark ones.

![alt](https://raw.githubusercontent.com/gnikit/tkinter-tooltip/master/assets/images/header.png)

## Features

- normal tooltips
- show tooltip with `s` seconds `delay`
- tooltip tracks mouse cursor
- tooltip displays strings and string returning functions
- fully customisable, tooltip inherits underlying theme style

## Install

```shell
pip install tkinter-tooltip
```

## Examples

### Normal tooltips

By default the tooltip activates when entering and/or moving in the widget are
and deactivates when leaving and/or pressing any button.

![alt](https://raw.githubusercontent.com/gnikit/tkinter-tooltip/master/assets/images/tootil-simple.png)

```python
import tkinter as tk
import tkinter.ttk as ttk
from tktooltip import ToolTip

app = tk.Tk()
b = ttk.Button(app, text="Button")
b.pack()
ToolTip(b, msg="Hover info")
app.mainloop()
```

### Delayed tooltip

![alt](https://raw.githubusercontent.com/gnikit/tkinter-tooltip/master/assets/animations/tooltip-delayed.gif)

```python
import tkinter as tk
import tkinter.ttk as ttk
from tktooltip import ToolTip

app = tk.Tk()
b = ttk.Button(app, text="Button")
b.pack()
ToolTip(b, msg="Hover info", delay=2.0)   # True by default
app.mainloop()
```

### Tracking tooltip

Have the tooltip follow the mousse cursor around when moving.

![alt](https://raw.githubusercontent.com/gnikit/tkinter-tooltip/master/assets/animations/tooltip-tracking.gif)

```python
import tkinter as tk
import tkinter.ttk as ttk
from tktooltip import ToolTip

app = tk.Tk()
b = ttk.Button(app, text="Button")
b.pack()
ToolTip(b, msg="Hover info", follow=True)   # True by default
app.mainloop()
```

### Function as tooltip

Here the tooltip returns the value of `time.asctime()` which updates with every
movement. You can control the refresh rate of the `ToolTip` through the `refresh`
argument by default it is set to `1s`.

![alt](https://raw.githubusercontent.com/gnikit/tkinter-tooltip/master/assets/animations/tootip-function-refresh.gif)
![alt](https://raw.githubusercontent.com/gnikit/tkinter-tooltip/master/assets/animations/tootip-function.gif)

```python
import time
import tkinter as tk
import tkinter.ttk as ttk
from tktooltip import ToolTip

app = tk.Tk()
b = ttk.Button(app, text="Button")
b.pack()
# NOTE: pass the function itself not the return value
ToolTip(b, msg=time.asctime, delay=0)
app.mainloop()
```

### Themed tooltip

`tkinter-tooltip` is fully aware of the underlying theme (in this case a dark theme),
and can even be furher customised by passing `tk` styling arguments to the tooltip

![alt](https://raw.githubusercontent.com/gnikit/tkinter-tooltip/master/assets/animations/tootip-dark-theme.gif)

Style tooltip and underlying the button. If a full theme has been used then
the `ToolTip` will inherit the settings of the theme by default.

```python
import tkinter as tk
import tkinter.ttk as ttk
from tktooltip import ToolTip

app = tk.Tk()
s = ttk.Style()
s.configure("custom.TButton", foreground="#ffffff", background="#1c1c1c")
b = ttk.Button(app, text="Button", style="custom.TButton")
b.pack()
ToolTip(b, msg="Hover info", delay=0,
        parent_kwargs={"bg": "black", "padx": 5, "pady": 5},
        fg="#ffffff", bg="#1c1c1c", padx=10, pady=10)
app.mainloop()
```

## Support

If you want to support this project you can do it through

[![Alt](https://www.paypalobjects.com/webstatic/mktg/Logo/pp-logo-150px.png)](https://paypal.me/inikit)
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/gnikit)

## Acknowledgements

`tkinter-tooltip` is based on the original work performed by
[Tucker Beck](http://code.activestate.com/recipes/576688-tooltip-for-tkinter/)
licensed under an MIT License.

## License

MIT License
