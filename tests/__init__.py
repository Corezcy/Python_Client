#
# Copyright (c) 2019 LG Electronics, Inc.
#
# This software contains code licensed as described in LICENSE.
#

import unittest
from .common import SimConnection,spawnState

def load_tests(loader, standard_tests, pattern):
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestNPC)) # must be first
    suite.addTests(loader.loadTestsFromTestCase(TestCollisions))
    suite.addTests(loader.loadTestsFromTestCase(TestEGO))
    suite.addTests(loader.loadTestsFromTestCase(TestSensors))
    suite.addTests(loader.loadTestsFromTestCase(TestPeds))
    suite.addTests(loader.loadTestsFromTestCase(TestUtils))
    suite.addTests(loader.loadTestsFromTestCase(TestSimulator)) #must be last
    return suite
