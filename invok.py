import inspect
import functools

class Provider:

    def __init__(self):
        self.nodes = {}
        self.instances = {}

    def create(self, name, chain=None):
        if chain is None:
            chain = []
        if name in chain:
            chain.append(name)
            raise ResolutionError(
                "Cycle detected",
                chain)
        chain.append(name)
        if name not in self.nodes:
            raise ResolutionError(
                "Unable to locate service: {}".format(name),
                chain)
        entry = self.nodes[name]
        if entry.cached and name in self.instances:
            return self.instances[name]
        instance = entry.cls(**self.resolve(entry.deps, chain))
        if entry.cached:
            self.instances[name] = instance
        return instance

    def resolve(self, deps, chain):
        return {dep : self.create(dep, list(chain)) for dep in deps}

    def register(self, cached, **kwargs):
        for name, cls in kwargs.items():
            if name in self.nodes:
                raise DuplicateDependencyError(name)
            self.nodes[name] = DependencyNode(
                cls = cls,
                cached = cached
                )

    def declare_service(self, cls, alias=None):
        if alias is None:
            alias = cls.__name__
        self.register(True, **{alias : cls})

    def declare_object(self, cls, alias=None):
        if alias is None:
            alias = cls.__name__
        self.register(False, **{alias : cls})

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

class ResolutionError(Exception):

    def __init__(self, msg, chain):
        self.msg = msg
        self.chain = chain

    def chainDescr(self):
        return " -> ".join(self.chain)

    def __str__(self):
        return "{}. Chain: {}".format(self.msg, self.chainDescr())

class DuplicateDependencyError(Exception):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Duplicate dependency: {}".format(self.name)

provider = Provider()

def reset():
    global provider
    provider = Provider()

def service(cls):
    def service_decorator(**kwargs):
        return provider.declare_service(cls, **kwargs)
    return service_decorator

def object(cls):
    def object_decorator(**kwargs):
        return provider.declare_object(cls, **kwargs)
    return object_decorator

def create(clsName):
    return provider.create(clsName)

def config(clsName, **kwargs):
    provider.nodes[clsName].config(**kwargs)
