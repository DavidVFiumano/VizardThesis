from typing import Tuple, Union, Iterable, List
from threading import RLock
from math import sqrt
from logging import Logger

from numba import njit

import viz

from AlexaEngine import StateMachine, State, EventHandler

from .AnimatedSprite import AnimatedSprite
from Events import FrameUpdateEvent
from LoggerFactory import CSVFormatter, LoggerFactory, LoggerNotInitializedError
import Configuration

# GPT-4 wrote this code (mostly). Editted by David Fiumano
loggerName = "CollectibleLogger"
csvFormatter = CSVFormatter(fieldnames=["FrameNumber", "ItemName", "Value"])

def logCollection(logger : Logger, frameNumber : int, itemName : str, value : float):
    
    fieldValues = {
        "FrameNumber" : frameNumber,
        "ItemName" : itemName,
        "Value" : value
    }
    logger.info("", extra=fieldValues)

# this system isn't perfect but works
class Collectible(AnimatedSprite):
	
	TotalValue : int = 0
	TotalCollected : int = 0
	CollectedValue : int = 0
	CollectibleProgressBar : viz.VizProgressBar = None
	CollectibleProgressBarColor : Tuple[int, int, int, int] = (0, 0.5, 0, 1)
	Collectibles : List["Collectible"] = list()
	
	@classmethod
	def collectedAllCoins(cls):
		return cls.CollectedValue == cls.TotalValue
	
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
		

	def collectItem(self, logger : Logger, event : FrameUpdateEvent):
		logCollection(logger, event.FrameNumber, self.name, self.value)
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
		try:
			collectibleLogger = LoggerFactory.getLogger(loggerName, formatter=csvFormatter, file="CollectiblesLog.csv")
		except LoggerNotInitializedError:
			return None
		playerPos = viz.MainView.getPosition()
		collectibles = [c for c in cls.Collectibles if not c.isCollected()]
		for c in collectibles:
			distance = cls._distance(playerPos, c.getModel().getPosition())
			if distance < c.collectionDistance:
				c.collectItem(collectibleLogger, event)
			
	@classmethod
	def getCallback(cls) -> EventHandler.CALLBACK_FUNCTION_TYPE:
		def callback(event : FrameUpdateEvent):
			if isinstance(event, FrameUpdateEvent):
				return cls._handleFrameEvent(event)
			else:
				raise RuntimeError(f"Event type {type(event)} not supported, must be either a FrameUpdateEvent or NetworkEvent type")
				
		return callback