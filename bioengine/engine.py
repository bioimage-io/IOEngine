"""The BioEngine class."""
import inspect
import sys
import threading
import uuid
from pathlib import Path
from types import ModuleType

import yaml

from bioengine.exceptions import PackageNotFound, UnsupportedAPI
from bioengine.utils import dotdict


class BioEngine:
    """The BioEngine class."""

    def __init__(self, vendor_api=None):
        """Set up engine."""
        self.services = []
        self.packages = {}
        self._service_lock = threading.Lock()
        self.vendor_api = vendor_api

    def generate_engine_api(self, package_info=None, make_api_module=True):
        """Return engine api."""
        engine_api = dotdict(
            showMessage=print, show_message=print, register=self.register_service
        )
        if self.vendor_api:
            engine_api.update(self.vendor_api)
        if package_info:
            engine_api.get_package_info = lambda: package_info
            engine_api.getPackageInfo = lambda: package_info
            engine_api.get_config = lambda: package_info.get("config")
            engine_api.getConfig = lambda: package_info.get("config")

        if make_api_module:
            # make a fake module with api
            mod = ModuleType("bioengine")
            sys.modules[mod.__name__] = mod  # pylint: disable=no-member
            mod.__file__ = mod.__name__ + ".py"  # pylint: disable=no-member
            mod.api = engine_api
        return engine_api

    def register_service(self, api):
        """Set interface."""
        if isinstance(api, dict):
            api = {a: value for a, value in api.items() if not a.startswith("_")}
        elif inspect.isclass(type(api)):
            api = {a: getattr(api, a) for a in dir(api) if not a.startswith("_")}
        else:
            raise UnsupportedAPI
        self.services.append(dotdict(**api))

    def register(self, **kwarg):
        """Register api resources."""
        if kwarg["type"] == "service":
            self.register_service(kwarg)
        else:
            raise NotImplementedError

    def execute(self, script):
        """Execute a script via the api."""
        self._execute_script(script)

    def load_package(self, package_dir):
        """Load a service package."""
        config_file = Path(package_dir) / "config.yaml"
        with open(config_file, "r") as fil:
            package_info = yaml.load(fil, Loader=yaml.FullLoader)
        package_info["package_dir"] = package_dir
        try:
            self._service_lock.acquire()

            entry_point = Path(package_dir) / package_info["entrypoint"]
            model_script = entry_point.read_text()
            sys.path.insert(0, package_dir)

            self._execute_script(model_script, package_info)
        except Exception as exc:
            if package_dir in sys.path:
                sys.path.remove(package_dir)
            raise exc
        finally:
            self._service_lock.release()

    def _execute_script(self, script, package_info=None):
        """Execute script."""
        if package_info is None:
            package_info = {}
        package_info["id"] = str(uuid.uuid4())
        package_info["_locals"] = {}
        self.generate_engine_api(package_info)
        exec(script, package_info["_locals"])  # pylint: disable=exec-used
        self.packages[package_info["id"]] = package_info

    def unload_package(self, package_id):
        """Unload package."""
        if package_id in self.packages:
            package_info = self.packages[package_id]
            package_dir = package_info["package_dir"]
            if package_dir in sys.path:
                sys.path.remove(package_dir)
            del self.packages[package_id]
        else:
            raise PackageNotFound(package_id)


def main():
    """Run main."""
    engine = BioEngine()
    # execute a model script directly
    engine.execute(
        """
from bioengine import api
def run():
    api.showMessage('hello')
api.register(dict(type='service', name='test', run=run))
"""
    )
    print(f"Service registered: {engine.services}")
    engine.services[0].run()

    engine = BioEngine()
    # load a service package
    engine.load_package("./example_packages/unet2d")
    print(f"Service registered: {engine.services}")
    # use the registered service
    engine.services[0].train()
    ret = engine.services[0].predict(1)
    print(ret)


if __name__ == "__main__":
    main()
