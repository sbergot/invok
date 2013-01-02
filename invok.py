import inspect

class Provider:

    def __init__(self):
        self.services = {}
        self.objects = {}
        self.service_instances = {}

    def create_service(self, name):
        if name in self.service_instances:
            return self.service_instances[name]
        entry = self.services[name]
        cls = entry["cls"]
        deps = entry["deps"]
        resolved_deps = {self.arg_name(dep) : self.create(dep) for dep in deps}
        instance = cls(**resolved_deps)
        self.service_instances[name] = instance
        return instance

    def create_object(self, name):
        entry = self.objects[name]
        cls = entry["cls"]
        deps = entry["deps"]
        resolved_deps = {self.arg_name(dep) : self.create(dep) for dep in deps}
        instance = cls(**resolved_deps)
        self.service_instances[name] = instance
        return instance

    def create(self, name):
        if name in self.services:
            return self.create_service(name)
        if name in self.objects:
            return self.create_object(name)
        raise MissingDependencyError(name)

    def register_service(self, **kwargs):
        for name, cls in kwargs.items():
            self.services[name] = {
                "cls" : cls,
                "deps" : self.getDeps(cls)
                }

    def register_object(self, **kwargs):
        for name, cls in kwargs.items():
            self.objects[name] = {
                "cls" : cls,
                "deps" : self.getDeps(cls)
                }

    def declare_service(self, cls):
        self.register_service(**{cls.__name__ : cls})

    def declare_object(self, cls):
        self.register_object(**{cls.__name__ : cls})

    def class_name(self, name):
        return str.upper(name[0]) + name[1:]

    def arg_name(self, name):
        return str.lower(name[0]) + name[1:]

    def getDeps(self, cls):
        try:
            return map(self.class_name,
                       inspect.getargspec(cls.__init__).args[1:])
        except AttributeError:
            # no __init__ --> no dep
            return []

class MissingDependencyError(Exception):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Unable to locate service: {}".format(self.name)

provider = Provider()

def reset():
    global provider
    provider = Provider()

def service(cls):
    provider.declare_service(cls)

def object(cls):
    provider.declare_object(cls)

def create(clsName):
    return provider.create(clsName)
