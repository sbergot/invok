import unittest
import invok

class MyService:
    pass

class MyServiceA:
    def __init__(self, myService):
        self.myService = myService

class MyServiceB:
    def __init__(self, myServiceA):
        self.myServiceA = myServiceA

class MyServiceC:
    def __init__(self, myService):
        self.myService = myService

class MyServiceD:
    def __init__(self, myServiceC, myServiceB):
        self.myServiceC = myServiceC
        self.myServiceB = myServiceB

class TestInvok(unittest.TestCase):

    def setUp(self):
        self.provider = invok.Provider()

    def test_invok(self):
        self.provider.register(MyService = MyService)
        instance = self.provider.create("MyService")
        self.assertIsInstance(instance, MyService)

    def test_register(self):
        self.provider.declareService(MyService)
        instance = self.provider.create("MyService")
        self.assertIsInstance(instance, MyService)

    def test_get_available_dependency(self):
        self.provider.declareService(MyServiceA)
        self.assertEqual(self.provider.getDeps(MyServiceA), ["MyService"])

    def test_simple_dependency(self):
        self.provider.declareService(MyService)
        self.provider.declareService(MyServiceA)
        instance = self.provider.create("MyServiceA")
        self.assertIsInstance(instance, MyServiceA)
        self.assertIsInstance(instance.myService, MyService)

    def test_invert_dependency(self):
        self.provider.declareService(MyServiceA)
        self.provider.declareService(MyService)
        instance = self.provider.create("MyServiceA")
        self.assertIsInstance(instance, MyServiceA)
        self.assertIsInstance(instance.myService, MyService)

    def test_missing_dependency(self):
        self.provider.declareService(MyServiceA)
        try:
            self.provider.create("MyServiceA")
        except invok.MissingDependencyError as e:
            return
        self.fail("no exception thrown")

    def test_nested_dependency(self):
        self.provider.declareService(MyService)
        self.provider.declareService(MyServiceA)
        self.provider.declareService(MyServiceB)
        instance = self.provider.create("MyServiceB")
        self.assertIsInstance(instance, MyServiceB)
        self.assertIsInstance(instance.myServiceA, MyServiceA)
        self.assertIsInstance(instance.myServiceA.myService, MyService)

    def test_multiple_nested_dependency(self):
        self.provider.declareService(MyService)
        self.provider.declareService(MyServiceA)
        self.provider.declareService(MyServiceB)
        self.provider.declareService(MyServiceC)
        self.provider.declareService(MyServiceD)
        instance = self.provider.create("MyServiceD")
        self.assertIsInstance(instance, MyServiceD)
        self.assertIsInstance(instance.myServiceC, MyServiceC)
        self.assertIsInstance(instance.myServiceC.myService, MyService)
        self.assertIsInstance(instance.myServiceB, MyServiceB)
        self.assertIsInstance(instance.myServiceB.myServiceA, MyServiceA)
        self.assertIsInstance(instance.myServiceB.myServiceA.myService, MyService)
