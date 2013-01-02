import unittest
import invok

from testClasses import *

class TestAPI(unittest.TestCase):

    def setUp(self):
        invok.reset()

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
        self.assertIsInstance(instance.MyServiceC, MyServiceC)
        self.assertIsInstance(instance.MyServiceC.MyService, MyService)
        self.assertIsInstance(instance.MyServiceB, MyServiceB)
        self.assertIsInstance(instance.MyServiceB.MyServiceA, MyServiceA)
        self.assertIsInstance(instance.MyServiceB.MyServiceA.MyService, MyService)

    def test_service_uniqueness(self):
        invok.service(MyService)
        instance1 = invok.create("MyService")
        instance2 = invok.create("MyService")
        self.assertIs(instance1, instance2)

    def test_object_creation(self):
        invok.object(MyService)
        instance1 = invok.create("MyService")
        instance2 = invok.create("MyService")
        self.assertIsNot(instance1, instance2)

    def test_option_setting(self):
        invok.service(MyService)
        invok.service(MyServiceE)
        option = object()
        invok.config("MyServiceE", option=option)
        instance = invok.create("MyServiceE")
        self.assertEqual(instance.option, option)
