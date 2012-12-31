import inspect

class Provider:

    def __init__(self):
        self.services = {}

    def create(self, name):
        try:
            entry = self.services[name]
        except KeyError:
            raise MissingDependencyError(name)
        cls = entry["cls"]
        deps = entry["deps"]
        resolved_deps = {self.arg_name(dep) : self.create(dep) for dep in deps}
        return cls(**resolved_deps)

    def register(self, **kwargs):
        for name, cls in kwargs.items():
            self.services[name] = {
                "cls" : cls,
                "deps" : self.getDeps(cls)
                }

    def declareService(self, cls):
        self.register(**{cls.__name__ : cls})

    def class_name(self, name):
        return str.upper(name[0]) + name[1:]

    def arg_name(self, name):
        return str.lower(name[0]) + name[1:]

    def getDeps(self, cls):
        try:
            return map(self.class_name, inspect.getargspec(cls.__init__).args[1:])
        except AttributeError:
            # no __init__ --> no dep
            return []

class MissingDependencyError(Exception):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Unable to locate service: {}".format(self.name)
