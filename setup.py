"""Setup script for CLI ToDo application."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cli-todo",
    version="1.0.0",
    author="CLI ToDo Team",
    description="A minimal command-line application for managing personal tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gianfranco-omnigpt/cli-todo-10",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "todo=todo.__main__:main",
        ],
    },
)
