# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="HTTP Echo Server",
    description="A Python HTTP echo server script",
    version="0.1",
    author=["Selena Flannery", "Kevin Gifford"],
    license="MIT",
    py_modules=["client", "server"],
    package_dir={"": "src"},
    install_requires=[],
    extras_require={"test": ["pytest", "pytest-xdist", "tox"]}
)
