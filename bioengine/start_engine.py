import rpyc
import math
from rpyc.utils.server import ThreadedServer
from bioengine.engine import BioEngine

engine = BioEngine()


class APIService(rpyc.Service):
    def __init__(self):
        self._conn = None

    def on_connect(self, conn):
        print("connected", conn)
        self._conn = conn

    def on_disconnect(self, conn=None):
        print("disconnected", conn)

    def exposed_register_client(self):
        print("registering client:", self._conn)
        engine.on("register_service", self._conn.root.register)

    def exposed_load_package(self, path):
        print("loading package:", path)
        engine.load_package(path)


from rpyc.utils.server import ThreadedServer

t = ThreadedServer(APIService, port=18867)
print("starting server...")
t.start()
