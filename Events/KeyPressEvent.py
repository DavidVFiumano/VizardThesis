from .VizardEvent import VizardEvent

import viz

class KeyPressEvent(VizardEvent):
	
	def __init__(self, key : str):
		self.key = key
		