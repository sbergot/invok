import inspect
import functools

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
