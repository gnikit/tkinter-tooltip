import pathlib
from setuptools import setup
from tktooltip import __version__

# The directory containing this file
HERE = pathlib.Path(__file__).resolve().parent

# The text of the README file is used as a description
README = (HERE / "README.md").read_text()

NAME = "tkinter-tooltip"

setup(
    name=NAME,
    version=__version__,
    url="https://github.com/gnikit/tkinter-tooltip",
    author="Giannis Nikiteas",
    author_email="giannis.nikiteas@gmail.com",
    description="An easy and customisable ToolTip implementation for Tkinter",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    keywords=["tktooltip", "tkinter-tooltip", "tkinter", "tooltip", "pop-up"],
    packages=["tktooltip"],
    include_package_data=True,
    install_requires=["tkinter"],
)