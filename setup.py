#!/usr/bin/env python3

from setuptools import setup

setup(
    name="lgsvl",
    description="LGSVL Simulator Api",
    author="LGSVL",
    author_email="contact@lgsvlsimulator.com",
    python_requires=">=3.5.0",
    url="https://github.com/lgsvl/simulator",
    packages=["lgsvl"],
    install_requires=[
        "websockets==7.0",
        "websocket-client==0.57.0",
        "websocket==0.2.1",
        "flake8==3.8.3",
        "absl-py==0.10.0",
        "pyyaml==5.3.1",
        "pymongo==3.11.0",
        "asyncio==3.4.3",
        "pynput==1.7.1",
    ],
    license="Other",
    classifiers=[
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
    ],
)
