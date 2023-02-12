from typing import Union, List, Iterable, Callable, Optional, Dict
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
	
	CollectibleCounter : int = 0
	CollectibleLock : RLock = RLock()
	SpawnedCollectibles : List["Collectible"] = list()
	CollectedCollectibles : List["Collectible"] = list()
	
	def __init__(self, modelFilePath : str, *, 
						collectionDistance : float = 1.0,
						position : Union[Iterable[float], None] = None, 
						scale : float = 1, 
						spinAxis : Iterable[float] = tuple([0, 1, 0]), 
						spinDegPerSecond : Union[float, None] = None, 
						name : Union[str, None] = None):
		with type(self).CollectibleLock:
			name = name if name is not None else f"Collectible {type(self).CollectibleCounter}"
			super().__init__(modelFilePath, position=position, scale=scale, spinAxis=spinAxis, spinDegPerSecond=spinDegPerSecond, name=name)
			type(self).CollectibleCounter += 1
			self.collectionDistance = collectionDistance
			self.collectedBy : Union[None, str] = None
			type(self).SpawnedCollectibles[name] = self

	def collectItem(self, collector : str) -> bool:
		with type(self).CollectibleLock:
			if self.collectedBy is None:
				self.collectedBy = collector
				return self
			else:
				return None
				
	def getCollector(self) -> Union[None, str]:
		with type(self).CollectibleLock:
			return self.collectedBy

	@staticmethod
	def _getRole() -> Optional[str]:
		return Configuration.PLAYER_ROLE
				
	@staticmethod
	@njit
	def _distance(viewPosition : Iterable[float], collectiblePosition : Iterable[float]) -> float:
		sumOfSquaredResiduals = sum([v - c for v, c in zip(viewPosition, collectiblePosition)])
		return sqrt(sumOfSquaredResiduals)

	@classmethod
	def _handleFrameEvent(cls, event : FrameUpdateEvent) -> None:
		viewPosition = tuple(viz.MainView.getPosition())
		collectedCollectibles = list()
		for name, collectible in cls.SpawnedCollectibles.items():
			collectiblePosition = tuple(collectible.getModel().getPosition())
			collectionDistance = collectible.collectionDistance
			distance = cls._distance(viewPosition, collectiblePosition)
			if distance <= collectionDistance:
				collectible.collectItem(cls._getRole())
				collectible.remove()
				collectedCollectibles.append(name)					

		for name in collectedCollectibles:
			cls.CollectedCollectibles[name] = cls.SpawnedCollectibles.pop(name)
	
	@classmethod
	def _handleNetworkEvent(cls, event : NetworkEvent) -> None:
		pass
				
	@classmethod
	def getCallback(cls) -> EventHandler.CALLBACK_FUNCTION_TYPE:
		def callback(event : Union[FrameUpdateEvent, NetworkEvent]):
			if cls._getRole() is None:
				return # no need to run yet if the role isn't set yet
				
			with cls.CollectibleLock:
				if isinstance(event, FrameUpdateEvent):
					return cls._handleFrameEvent(event)
				elif isinstance(event, NetworkEvent):
					return cls._handleNetworkEvent(event)
				else:
					raise RuntimeError(f"Event type {type(event)} not supported, must be either a FrameUpdateEvent or NetworkEvent type")
					
		return callback