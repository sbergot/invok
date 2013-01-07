import DependencyNode

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
            self.nodes[name] = DependencyNode.DependencyNode(
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
