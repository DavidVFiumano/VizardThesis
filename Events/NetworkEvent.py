from .VizardEvent import VizardEvent

from viz import NetworkEvent as VizardNetworkEvent

class NetworkEvent(VizardEvent):
    
    def __init__(self, networkEvent : VizardNetworkEvent):
        self.sender = networkEvent.sender
        self.address = networkEvent.address
        self.data = networkEvent.data
        self.kwargs = {key : value for key, value in vars(networkEvent).items() if key not in ["sender", "address", "data"]}