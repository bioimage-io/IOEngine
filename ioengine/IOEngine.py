"""The IOEngine class."""
import inspect
from types import ModuleType
import sys
from .utils import dotdict


class IOEngine:
    """The IOEngine class"""

    def __init__(self):
        self.services = []
        self.engine_api = dotdict(showMessage=print, register=self.register_service)

        # make a fake module with api
        mod = ModuleType("bioimage")
        sys.modules[mod.__name__] = mod  # pylint: disable=no-member
        mod.__file__ = mod.__name__ + ".py"  # pylint: disable=no-member
        mod.api = self.engine_api

    def register_service(self, **api):
        """Set interface."""
        if isinstance(api, dict):
            api = {a: api[a] for a in api if not a.startswith("_")}
        elif inspect.isclass(type(api)):
            api = {a: getattr(api, a) for a in dir(api) if not a.startswith("_")}
        else:
            raise Exception("unsupported api export")
        self.services.append(dotdict(**api))

    def register(self, **kwarg):
        if kwarg["type"] == "service":
            self.register_service(kwarg)
        else:
            raise NotImplementedError

    def execute(self, script):
        exec(script, self.engine_api)  # pylint: disable=exec-used


if __name__ == "__main__":
    test_script = """
from bioimage import api
def run():
    api.showMessage('hello')
api.register(type='service', name='test', run=run)
"""
    ioe = IOEngine()
    ioe.execute(test_script)
    print(f"Service registered: {ioe.services}")

    # use the registered service
    ioe.services[0].run()
