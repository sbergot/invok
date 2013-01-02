import unittest
import invok

from testClasses import *

class TestAPI(unittest.TestCase):

    def test_service(self):
        invok.service(MyService)
        instance = invok.create("MyService")
        self.assertIsInstance(instance, MyService)


    def test_multiple_nested_dependency(self):
        invok.service(MyService)
        invok.service(MyServiceA)
        invok.service(MyServiceB)
        invok.service(MyServiceC)
        invok.service(MyServiceD)
        instance = invok.create("MyServiceD")
        self.assertIsInstance(instance, MyServiceD)
        self.assertIsInstance(instance.myServiceC, MyServiceC)
        self.assertIsInstance(instance.myServiceC.myService, MyService)
        self.assertIsInstance(instance.myServiceB, MyServiceB)
        self.assertIsInstance(instance.myServiceB.myServiceA, MyServiceA)
        self.assertIsInstance(instance.myServiceB.myServiceA.myService, MyService)

    def test_service_uniqueness(self):
        invok.service(MyService)
        instance1 = invok.create("MyService")
        instance2 = invok.create("MyService")
        self.assertIs(instance1, instance2)
