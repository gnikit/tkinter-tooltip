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
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development",
        "Typing :: Typed",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
    keywords=["tkinter", "tktooltip", "tkinter-tooltip", "tooltip", "pop-up"],
    packages=["tktooltip"],
    include_package_data=True,
    install_requires=["tk"],
)