import unittest
import invok

from testClasses import *

class TestProvider(unittest.TestCase):

    def setUp(self):
        self.provider = invok.Provider()

    def test_invok(self):
        self.provider.register_service(MyService = MyService)
        instance = self.provider.create("MyService")
        self.assertIsInstance(instance, MyService)

    def test_register(self):
        self.provider.declare_service(MyService)
        instance = self.provider.create("MyService")
        self.assertIsInstance(instance, MyService)

    def test_get_available_dependency(self):
        self.provider.declare_service(MyServiceA)
        self.assertEqual(self.provider.getDeps(MyServiceA), ["MyService"])

    def test_simple_dependency(self):
        self.provider.declare_service(MyService)
        self.provider.declare_service(MyServiceA)
        instance = self.provider.create("MyServiceA")
        self.assertIsInstance(instance, MyServiceA)
        self.assertIsInstance(instance.myService, MyService)

    def test_invert_dependency(self):
        self.provider.declare_service(MyServiceA)
        self.provider.declare_service(MyService)
        instance = self.provider.create("MyServiceA")
        self.assertIsInstance(instance, MyServiceA)
        self.assertIsInstance(instance.myService, MyService)

    def test_missing_dependency(self):
        self.provider.declare_service(MyServiceA)
        try:
            self.provider.create("MyServiceA")
        except invok.MissingDependencyError as e:
            return
        self.fail("no exception thrown")

    def test_nested_dependency(self):
        self.provider.declare_service(MyService)
        self.provider.declare_service(MyServiceA)
        self.provider.declare_service(MyServiceB)
        instance = self.provider.create("MyServiceB")
        self.assertIsInstance(instance, MyServiceB)
        self.assertIsInstance(instance.myServiceA, MyServiceA)
        self.assertIsInstance(instance.myServiceA.myService, MyService)

    def test_multiple_nested_dependency(self):
        self.provider.declare_service(MyService)
        self.provider.declare_service(MyServiceA)
        self.provider.declare_service(MyServiceB)
        self.provider.declare_service(MyServiceC)
        self.provider.declare_service(MyServiceD)
        instance = self.provider.create("MyServiceD")
        self.assertIsInstance(instance, MyServiceD)
        self.assertIsInstance(instance.myServiceC, MyServiceC)
        self.assertIsInstance(instance.myServiceC.myService, MyService)
        self.assertIsInstance(instance.myServiceB, MyServiceB)
        self.assertIsInstance(instance.myServiceB.myServiceA, MyServiceA)
        self.assertIsInstance(instance.myServiceB.myServiceA.myService, MyService)
