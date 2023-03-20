from typing import Iterable, Tuple, Dict, Union, Callable
from math import sqrt

from viz import ActionData, FOREVER, VizNode, MainView
from vizact import moveTo, spinTo, sequence, parallel

from Events import FrameUpdateEvent
from .. import Bot

# TODO at some point make this it's own class so I can make paths a bit easier.
PATH_TYPE = Iterable[Dict[str, Union[Tuple[float, float, float], Tuple[float, float, float, float], float]]]

class PathfollowerBot(Bot):
	
	def __init__(self, avatar : VizNode, path : PATH_TYPE, seeingDistance : float, fieldOfView : float, hearingDistance : float, 
						chaseSpeed : float, chaseTurnDegPerSecond : float, 
						chasingSeeingDistance : float = None, chasingFieldOfView : float = None, chasingHearingDistance : float = None, 
						updateChasePathEveryNFrames : int = 15, endOfPathBehavior : str = "repeat",
						chaseVizNodeFunction : Callable[[VizNode], None] = lambda x : None, 
						resetVizNodeFunction : Callable[[VizNode], None] = lambda x : None):
		super().__init__(avatar, path[0]["Position"], MainView.getQuat())
		self.path = path
		self.currentAction : Union[None, ActionData] = None
		self.currentPositionInPathList = 0
		self.seeingDistance = seeingDistance
		self.fieldOfView = fieldOfView
		self.hearingDistance = hearingDistance
		self.chaseSpeed = chaseSpeed
		self.chaseTurnDegPerSecond = chaseTurnDegPerSecond
		self.chasingHearingDistance = chasingHearingDistance
		self.chasingSeeingDistance = chasingSeeingDistance
		self.chasingFieldOfView = chasingFieldOfView
		self.chasing = False
		self.updateChasePathEveryNFrames = updateChasePathEveryNFrames
		self.endOfPathBehavior = endOfPathBehavior
		self.setPath(self.path, self.endOfPathBehavior)
		self.chaseVizNodeFunction = chaseVizNodeFunction
		self.resetVizNodeFunction = resetVizNodeFunction
		self.resetVizNodeFunction(avatar)
	
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
	
	def canSeePlayer(self, playerPosition : Tuple[float, float, float]) -> bool:
		return False # For now
		
	def canHearPlayer(self, playerPosition : Tuple[float, float, float]) -> bool:
		if not self.chasing:
			return self.hearingDistance is not None and type(self)._distance(playerPosition, self.avatar.getPosition()) < self.hearingDistance
		else:
			hearingDistance = self.hearingDistance if self.chasingHearingDistance is None else self.chasingHearingDistance
			return hearingDistance is not None and type(self)._distance(playerPosition, self.avatar.getPosition()) < hearingDistance
			
	def chasePlayer(self, playerPosition : Tuple[float, float, float], playerVelocityVector : Tuple[float, float, float]):
		self.avatar.clearActions()
		chasePoint = playerPosition + playerVelocityVector
		lookAndFollow = parallel(moveTo(chasePoint, speed=self.chaseSpeed), spinTo(point=chasePoint, speed=self.chaseTurnDegPerSecond))
		self.avatar.addAction(lookAndFollow)
	
	def resetPath(self):
		print("Headed back to the track")
		self.setPath(self.path, self.endOfPathBehavior)
	
	def frameCallback(self, event : FrameUpdateEvent):
		playerPosition = FrameUpdateEvent.PlayerPosition
		if not self.chasing:
			if self.canHearPlayer(playerPosition) or self.canSeePlayer(playerPosition):
				self.chasing = True
				self.chaseVizNodeFunction(self.avatar)
				self.chasePlayer(playerPosition, FrameUpdateEvent.PlayerVelocity)
			else:
				self.chasing = False
		
		else:
			if not (self.canHearPlayer(playerPosition) or self.canSeePlayer(playerPosition)):
				self.chasing = False
				self.resetVizNodeFunction(self.avatar)
				self.resetPath()
			elif FrameUpdateEvent.FrameNumber % self.updateChasePathEveryNFrames == 0:
				self.chasePlayer(playerPosition, FrameUpdateEvent.PlayerVelocity)
				