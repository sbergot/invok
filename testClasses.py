
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
