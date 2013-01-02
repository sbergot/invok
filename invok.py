import inspect
import functools

class Provider:

    def __init__(self):
        self.nodes = {}
        self.instances = {}

    def create(self, name):
        if name not in self.nodes:
            raise MissingDependencyError(name)
        entry = self.nodes[name]
        if entry.cached and name in self.instances:
            return self.instances[name]
        instance = entry.cls(**self.resolve(entry.deps))
        if entry.cached:
            self.instances[name] = instance
        return instance

    def resolve(self, deps):
        return {dep : self.create(dep) for dep in deps}

    def register(self, cached, **kwargs):
        for name, cls in kwargs.items():
            self.nodes[name] = DependencyNode(
                cls = cls,
                cached = cached
                )

    def declare_service(self, cls):
        self.register(True, **{cls.__name__ : cls})

    def declare_object(self, cls):
        self.register(False, **{cls.__name__ : cls})

class DependencyNode:

    def __init__(self, cls, cached):
        self.cls = cls
        self.deps = self.get_deps(cls)
        self.cached = cached

    def get_deps(self, cls):
        try:
            return inspect.getargspec(cls.__init__).args[1:]
        except AttributeError:
            # no __init__ --> no dep
            return []

    def config(self, **kwargs):
        for name in kwargs:
            self.deps.remove(name)
        self.cls = functools.partial(self.cls, **kwargs)

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

def config(clsName, **kwargs):
    provider.nodes[clsName].config(**kwargs)
