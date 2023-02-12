from typing import Tuple

import viz

from Events import FrameUpdateEvent

class Bot:
	
	def __init__(self, avatar : viz.VizNode, position : Tuple[float, float, float], facing : Tuple[float, float, float, float]):
		self.avatar = avatar
		self.avatar.setPosition(*position)
		self.avatar.setQuat(*facing)
		
	def frameCallback(self, event : FrameUpdateEvent):
		pass
	
	def getFrameEventHandler(self):
		def callback(event : FrameUpdateEvent):
			return self.frameCallback(event)
		return callback
			