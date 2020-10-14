# Python CLient for Simulator

This folder contains Python API for LGSVL Simulator.


# Requirements

* Python 3.5 or higher

# Installing

    pip3 install --user .
    
    # install in development mode
    pip3 install --user -e .

# Running unit tests

    # run all unittests
    python3 -m unittest discover -v -c
    
    # run single test module
    python3 -m unittest -v -c tests/test_XXXX.py
    
    # run individual test case
    python3 -m unittest -v tests.test_XXX.TestCaseXXX.test_XXX
    python3 -m unittest -v tests.test_Simulator.TestSimulator.test_unload_scene

# Creating test coverage report

    # (one time only) install coverage.py
    pip3 install --user coverage
    
    # run all tests with coverage
    ~/.local/bin/coverage run -m unittest discover
    
    # generate html report
    ~/.local/bin/coverage html --omit "~/.local/*","tests/*"
    
    # output is in htmlcov/index.html

# Copyright and License

