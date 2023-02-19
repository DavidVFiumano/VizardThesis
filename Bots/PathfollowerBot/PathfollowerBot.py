from typing import Iterable, Tuple, Dict, Union

from viz import ActionData, FOREVER, VizNode, MainView
from vizact import moveTo, spinTo, sequence

from Events import FrameUpdateEvent
from .. import Bot

# TODO at some point make this it's own class so I can make paths a bit easier.
PATH_TYPE = Iterable[Dict[str, Union[Tuple[float, float, float], Tuple[float, float, float, float], float]]]

class PathfollowerBot(Bot):
	
	def __init__(self, avatar : VizNode, path : PATH_TYPE, seeingDistance : float, fieldOfView : float, hearingDistance : float, chaseSpeed : float, endOfPathBehavior : str = "repeat"):
		super().__init__(avatar, path[0]["Position"], MainView.getQuat())
		self.path = path
		self.currentAction : Union[None, ActionData] = None
		self.currentPositionInPathList = 0
		self.seeingDistance = seeingDistance
		self.fieldOfView = fieldOfView
		self.hearingDistance = hearingDistance
		self.chaseSpeed = chaseSpeed
		self.setPath(self.path, endOfPathBehavior)
	
	def setPath(self, path, endOfPathBehavior):
		self.actionList = list()
		for i, point in enumerate(path):
			moveAction = moveTo(point["Position"], speed=point["Speed"])
			turnAction = spinTo(point=path[(i+1)%len(path)]["Position"], speed=point["DegreesPerSecond"])
			self.actionList.append(moveAction)
			self.actionList.append(turnAction)
		
		if endOfPathBehavior == "reverse":
			raise NotImplementedError("Reverse not implemented yet")
		elif endOfPathBehavior == "repeat":
			self.action = sequence(*self.actionList, FOREVER)
			
		self.avatar.addAction(self.action)
		
	@staticmethod
	def _distance(viewPosition : Iterable[float], collectiblePosition : Iterable[float]) -> float:
		sumOfSquaredResiduals = sum([(v - c)**2 for v, c in zip(viewPosition, collectiblePosition)])
		return sqrt(sumOfSquaredResiduals)
		
	def frameCallback(self, event : FrameUpdateEvent):
		playerPosition = event.playerPosition
		if type(self)._distance(self.avatar.getPosition(), playerPosition) < 