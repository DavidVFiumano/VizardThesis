from typing import Tuple, List

import viz

from Events import FrameUpdateEvent

class Bot:

	Bots : List["Bot"] = list()
	
	def __init__(self, avatar : viz.VizNode, position : Tuple[float, float, float], facing : Tuple[float, float, float, float]):
		self.avatar = avatar
		self.avatar.setPosition(*position)
		self.avatar.setQuat(*facing)
		type(self).Bots.append(self)
		
	def frameCallback(self, event : FrameUpdateEvent):
		return event
	
	@classmethod
	def getCallback(cls):
		def callback(event : FrameUpdateEvent):
			for bot in cls.Bots:
				bot.frameCallback(event)
		return callback
			