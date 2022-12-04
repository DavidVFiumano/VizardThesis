from .VizardEvent import VizardEvent

from viz import NetworkEvent as VizardNetworkEvent

class NetworkEvent(VizardEvent):
    
    def __init__(self, networkEvent : VizardNetworkEvent):
        self.sender = networkEvent.sender
        self.address = networkEvent.address
        self.data = networkEvent.data
        self.port = networkEvent.port
        self.kwargs = vars(networkEvent)['_NetworkEvent__props']