import unittest
from invok import invok

from testClasses import *

class TestDependencyNode(unittest.TestCase):

    def test_get_available_dependency(self):
        node = invok.DependencyNode(cls = MyServiceA, cached =True)
        self.assertEqual(node.deps, ["MyService"])
