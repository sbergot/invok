
class MyService:
    pass

class MyServiceA:
    def __init__(self, MyService):
        self.MyService = MyService

class MyServiceB:
    def __init__(self, MyServiceA):
        self.MyServiceA = MyServiceA

class MyServiceC:
    def __init__(self, MyService):
        self.MyService = MyService

class MyServiceD:
    def __init__(self, MyServiceC, MyServiceB):
        self.MyServiceC = MyServiceC
        self.MyServiceB = MyServiceB

class MyServiceE:
    def __init__(self, MyService, option):
        self.MyService = MyService
        self.option = option


class CycleA:
    def __init__(self, CycleC):
        pass
class CycleB:
    def __init__(self, CycleA):
        pass
class CycleC:
    def __init__(self, CycleB):
        pass
