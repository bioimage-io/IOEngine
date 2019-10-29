import sys

sys.path.insert(0, '/Users/weiouyang/workspace/rpyc')

import time
import rpyc
import math
from ij.gui import GenericDialog

def create_selection_dialog(title='Run service'):
    choices = ['train', 'predict']
    gd = GenericDialog(title)
    gd.addChoice('Service', choices, 'predict')
    gd.showDialog()
    if gd.wasCanceled():
        return None
    # This function returns a list.
    # _ is used as a placeholder for values we don't use.
    # The for loop is used to call gd.getNextChoiceIndex() len(defaults) times.
    return gd.getNextChoiceIndex()


services = []
class APIService(rpyc.Service):

    def __init__(self):
        global services
        self.services = services
	
    def on_connect(self, conn=None):
        print('connected', conn)

    def on_disconnect(self, conn=None):
        print('disconnected', conn)

    def exposed_get_config(self):
        return {}

    def exposed_show_progress(self, progress):
        print('progress', progress)

    def exposed_show_status(self, status):
        print('status:', status)

    def exposed_register(self, service):
    	print('registering service', service)
    	self.services.append(service)
    	
#    	ret = service['train']()
#    	ret.set_expiry(100000)


service_port = 18867

# connect to the engine
engine = rpyc.connect("localhost", service_port, service=APIService)
api = engine.root

api.register_client()
api.load_package( '/Users/weiouyang/workspace/IOEngine/example_packages/unet2d')
#selected = create_selection_dialog()
print('done')

