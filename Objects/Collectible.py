from typing import Tuple, Union, Iterable, List
from threading import RLock
from math import sqrt

from numba import njit

import viz

from AlexaEngine import StateMachine, State, EventHandler

from .AnimatedSprite import AnimatedSprite
from Events import FrameUpdateEvent, NetworkEvent
from Globals import globalGameState
import Configuration

# this system for collecting collectibles is not as performant as it could be
# there is almost definitely a way to do this without so many python loops
# still, it works well enough for now
class Collectible(AnimatedSprite):
	
	TotalValue : int = 0
	TotalCollected : int = 0
	CollectedValue : int = 0
	CollectibleProgressBar : viz.VizProgressBar = None
	CollectibleProgressBarColor : Tuple[int, int, int, int] = (0, 0.5, 0, 1)
	Collectibles : List["Collectible"] = list()
	
	@classmethod
	def initProgressBar(cls):
		if cls.CollectibleProgressBar is None:
			cls.theme = viz.Theme()
			cls.theme.highBackColor = cls.CollectibleProgressBarColor
			cls.theme.borderColor = (0, 0, 0, 1)
			cls.theme.backColor = (0.1, 0.1, 0.1, 0.5)
			cls.CollectibleProgressBar = viz.addProgressBar(f"0/? Points")
			cls.CollectibleProgressBar.set(0)
			cls.CollectibleProgressBar.setPosition(0.93, 0.95)
			cls.CollectibleProgressBar.setScale(0.5, 0.75)
			cls.CollectibleProgressBar.setTheme(cls.theme)
			cls.CollectibleProgressBar.disable()
	
	@classmethod
	def addCollectible(cls, collectible : "Collectible"):
		cls.TotalValue += collectible.value
		percent = cls.CollectedValue/cls.TotalValue
		cls.CollectibleProgressBar.message(f"{cls.CollectedValue}/{cls.TotalValue}")
		cls.CollectibleProgressBar.set(percent)
		cls.Collectibles.append(collectible)
		
	@classmethod
	def collectCollectible(cls, collectible : "Collectible"):
		cls.CollectedValue += collectible.value
		cls.TotalCollected += 1
		cls.CollectibleProgressBar.set(cls.CollectedValue/cls.TotalValue)
		cls.CollectibleProgressBar.message(f"{cls.CollectedValue}/{cls.TotalValue} Points")
	
	def __init__(self, modelFilePath : str, *, 
						collectionDistance : float = 1.0,
						position : Union[Iterable[float], None] = None, 
						scale : float = 1, 
						spinAxis : Iterable[float] = tuple([0, 1, 0]), 
						spinDegPerSecond : Union[float, None] = None, 
						name : Union[str, None] = None,
						value : int = 1):
		super().__init__(modelFilePath, position=position, scale=scale, spinAxis=spinAxis, spinDegPerSecond=spinDegPerSecond, name=name)
		type(self).initProgressBar()
		
		self.collectionDistance = collectionDistance
		self.value = value
		self.collected = False
		type(self).addCollectible(self) 
		#type(self).CollectibleCounter += 1
		

	def collectItem(self) -> bool:
		type(self).collectCollectible(self)
		self.remove()
		self.collected = True
		
	def isCollected(self) -> bool:
		return self.collected

	@staticmethod
	def _distance(viewPosition : Iterable[float], collectiblePosition : Iterable[float]) -> float:
		sumOfSquaredResiduals = sum([(v - c)**2 for v, c in zip(viewPosition, collectiblePosition)])
		return sqrt(sumOfSquaredResiduals)

	@classmethod
	def _handleFrameEvent(cls, event : FrameUpdateEvent) -> None:
		playerPos = viz.MainView.getPosition()
		collectibles = [c for c in cls.Collectibles if not c.isCollected()]
		for c in collectibles:
			distance = cls._distance(playerPos, c.getModel().getPosition())
			if distance < c.collectionDistance:
				c.collectItem()
			
	@classmethod
	def getCallback(cls) -> EventHandler.CALLBACK_FUNCTION_TYPE:
		def callback(event : FrameUpdateEvent):
			if isinstance(event, FrameUpdateEvent):
				return cls._handleFrameEvent(event)
			else:
				raise RuntimeError(f"Event type {type(event)} not supported, must be either a FrameUpdateEvent or NetworkEvent type")
				
		return callback