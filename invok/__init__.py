import Provider

provider = Provider.Provider()

def reset():
    global provider
    provider = Provider.Provider()

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
