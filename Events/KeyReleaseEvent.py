from .VizardEvent import VizardEvent

import viz

class KeyReleaseEvent(VizardEvent):
	
	def __init__(self, key : str):
		self.key = key
		