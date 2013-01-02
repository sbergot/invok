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


    def test_simple_dependency(self):
        self.provider.declare_service(MyService)
        self.provider.declare_service(MyServiceA)
        instance = self.provider.create("MyServiceA")
        self.assertIsInstance(instance, MyServiceA)
        self.assertIsInstance(instance.MyService, MyService)

    def test_invert_dependency(self):
        self.provider.declare_service(MyServiceA)
        self.provider.declare_service(MyService)
        instance = self.provider.create("MyServiceA")
        self.assertIsInstance(instance, MyServiceA)
        self.assertIsInstance(instance.MyService, MyService)

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
        self.assertIsInstance(instance.MyServiceA, MyServiceA)
        self.assertIsInstance(instance.MyServiceA.MyService, MyService)

    def test_multiple_nested_dependency(self):
        self.provider.declare_service(MyService)
        self.provider.declare_service(MyServiceA)
        self.provider.declare_service(MyServiceB)
        self.provider.declare_service(MyServiceC)
        self.provider.declare_service(MyServiceD)
        instance = self.provider.create("MyServiceD")
        self.assertIsInstance(instance, MyServiceD)
        self.assertIsInstance(instance.MyServiceC, MyServiceC)
        self.assertIsInstance(instance.MyServiceC.MyService, MyService)
        self.assertIsInstance(instance.MyServiceB, MyServiceB)
        self.assertIsInstance(instance.MyServiceB.MyServiceA, MyServiceA)
        self.assertIsInstance(instance.MyServiceB.MyServiceA.MyService, MyService)

    def test_service_uniqueness(self):
        self.provider.declare_service(MyService)
        instance1 = self.provider.create("MyService")
        instance2 = self.provider.create("MyService")
        self.assertIs(instance1, instance2)

    def test_object_creation(self):
        self.provider.declare_object(MyService)
        instance1 = self.provider.create("MyService")
        instance2 = self.provider.create("MyService")
        self.assertIsNot(instance1, instance2)
